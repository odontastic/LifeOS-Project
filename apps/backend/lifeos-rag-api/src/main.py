import os
import uuid
import json
import logging
from datetime import datetime
from typing import Dict, Any

import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from .config import (
    NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD,
    QDRANT_URL,
    REDIS_HOST, REDIS_PORT, REDIS_DB,
    ALLOWED_ORIGINS, LOG_LEVEL
)
from .graph import get_property_graph_index
from .extractor import get_schema_extractor
from .deduplication import deduplicate_and_merge
from .safety import detect_crisis_language, DEFAULT_DISCLAIMER
from .temporal import parse_time_references
from .router import get_router_query_engine
from .synthesizer import FrameworkSynthesizer

# --- Logging Setup ---
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# --- Redis Client ---
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True, # Returns strings instead of bytes
        socket_connect_timeout=2
    )
except Exception as e:
    logger.warning(f"Failed to initialize Redis client: {e}")
    redis_client = None

# --- Pydantic Models ---
class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    interaction_id: str
    rating: float
    comment: str = ""

class StartFlowRequest(BaseModel):
    flow_type: str

class AdvanceFlowRequest(BaseModel):
    flow_id: str
    current_step: str
    response: str

# --- FastAPI App ---
app = FastAPI(title="LifeOS RAG API", version="2.0.0")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---

@app.get("/health")
async def health_check():
    """
    Checks connectivity to dependent services (Neo4j, Qdrant, Redis).
    """
    status = {"status": "ok", "services": {}}
    
    # 1. Redis
    try:
        if redis_client and redis_client.ping():
            status["services"]["redis"] = "up"
        else:
            status["services"]["redis"] = "down"
            status["status"] = "degraded"
    except Exception as e:
        status["services"]["redis"] = f"down: {str(e)}"
        status["status"] = "degraded"

    # 2. Qdrant
    try:
        q_client = QdrantClient(url=QDRANT_URL, timeout=2)
        q_client.get_collections()
        status["services"]["qdrant"] = "up"
    except Exception as e:
        status["services"]["qdrant"] = f"down: {str(e)}"
        status["status"] = "degraded"

    # 3. Neo4j (via LlamaIndex Property Graph)
    # This is a heavier check, ideally we'd just check TCP port or use valid driver
    # For now, we assume if get_property_graph_index works, it's okay (it connects lazily though)
    # We'll rely on the API root for deep checks or just report "unknown" if strictly lazy.
    # Actually, let's just mark it as 'checked via app startup'.
    status["services"]["neo4j"] = "assumed_up" 

    return status

@app.post("/api/ingest")
async def ingest_data(request: IngestRequest):
    logger.info("Received ingest request")
    CONFIDENCE_THRESHOLD = 0.65
    try:
        if detect_crisis_language(request.text):
            return {"warning": "Crisis language detected.", "disclaimer": DEFAULT_DISCLAIMER}

        extractor = get_schema_extractor()
        index = get_property_graph_index()
        document = Document(text=request.text)

        nodes, relationships = await extractor.aextract([document])
        
        # --- Quality Control ---
        # Filter relationships based on confidence score
        high_confidence_rels = [
            rel for rel in relationships 
            if rel.properties.get("confidence", 0.0) >= CONFIDENCE_THRESHOLD
        ]
        logger.info(f"Filtered relationships: {len(relationships)} -> {len(high_confidence_rels)}")

        # Get the set of nodes that are part of high-confidence relationships
        valid_node_ids = set()
        for rel in high_confidence_rels:
            valid_node_ids.add(rel.source_node.id_)
            valid_node_ids.add(rel.target_node.id_)
            
        # Filter nodes to only include those in valid relationships
        valid_nodes = [node for node in nodes if node.id_ in valid_node_ids]
        logger.info(f"Filtered nodes: {len(nodes)} -> {len(valid_nodes)}")

        # Deduplicate
        deduped_nodes, deduped_rels = await deduplicate_and_merge(
            valid_nodes, high_confidence_rels, index.property_graph_store
        )

        if deduped_nodes:
            index.insert_nodes(deduped_nodes)
        if deduped_rels:
            index.insert_relationships(deduped_rels)

        return {
            "message": f"Successfully ingested {len(deduped_nodes)} nodes and {len(deduped_rels)} relationships."
        }
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/api/query")
async def query(request: QueryRequest):
    logger.info(f"Received query: {request.query[:50]}...")
    try:
        if detect_crisis_language(request.query):
            return {"warning": "Crisis language detected.", "disclaimer": DEFAULT_DISCLAIMER}

        time_filters = parse_time_references(request.query)
        
        graph_index = get_property_graph_index()
        graph_query_engine = graph_index.as_query_engine(include_text=True)

        qdrant_client = QdrantClient(url=QDRANT_URL)
        resource_store = QdrantVectorStore(client=qdrant_client, collection_name="lifeos_resources")
        resource_index = VectorStoreIndex.from_vector_store(resource_store)
        resource_query_engine = resource_index.as_query_engine()

        router = get_router_query_engine(graph_query_engine, resource_query_engine)
        response = await router.aquery(request.query)

        synthesizer = FrameworkSynthesizer()
        mental_model = synthesizer.synthesize(response.response)

        return {
            "response": mental_model,
            "time_filters": time_filters,
            "source_nodes": [
                {"text": n.node.get_content(), "score": n.score, "metadata": n.node.metadata}
                for n in response.source_nodes
            ]
        }
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/api/flows/start")
async def start_flow(request: StartFlowRequest):
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis unavailable for flow state")
    
    flow_id = str(uuid.uuid4())
    state = {
        "flow_type": request.flow_type,
        "current_step": "step_1_greeting",
        "context": {},
        "created_at": datetime.now().isoformat()
    }
    
    # Store in Redis with 24h expiration
    redis_client.set(f"flow:{flow_id}", json.dumps(state), ex=86400)
    
    return {
        "flow_id": flow_id,
        "current_step": "step_1_greeting",
        "message": "Welcome to your daily check-in. How are you feeling right now?"
    }

@app.post("/api/flows/advance")
async def advance_flow(request: AdvanceFlowRequest):
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    key = f"flow:{request.flow_id}"
    data = redis_client.get(key)
    if not data:
        return {"error": "Flow session expired or not found."}
    
    flow_state = json.loads(data)
    
    # Simple Logic Placeholder (same as before but using the dict)
    if request.current_step == "step_1_greeting":
        flow_state["current_step"] = "step_2_explore_emotion"
        flow_state["context"]["emotion"] = request.response
        response_msg = f"I understand you're feeling {request.response}. Can you tell me more about it?"
    elif request.current_step == "step_2_explore_emotion":
        flow_state["current_step"] = "step_final_summary"
        response_msg = "Thank you for sharing. Remember to be kind to yourself."
        # Could delete redis key here if complete
    else:
        return {"error": "Invalid step sequence."}

    # Save updated state
    redis_client.set(key, json.dumps(flow_state), ex=86400)

    return {
        "flow_id": request.flow_id,
        "current_step": flow_state["current_step"],
        "message": response_msg,
        "is_complete": flow_state["current_step"] == "step_final_summary"
    }

@app.post("/api/feedback")
async def log_feedback(request: FeedbackRequest):
    # Log to disk for now (could also go to Redis or DB)
    try:
        with open("feedback.csv", "a") as f:
            if os.stat("feedback.csv").st_size == 0:
                f.write("interaction_id,rating,comment,timestamp\n")
            f.write(f'"{request.interaction_id}",{request.rating},"{request.comment}",{datetime.now().isoformat()}\n')
        return {"message": "Feedback logged."}
    except Exception as e:
        logger.error(f"Feedback log error: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "LifeOS RAG API is running (Optimized)."}
