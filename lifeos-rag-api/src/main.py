import os
import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from .graph import get_property_graph_index
from .extractor import get_schema_extractor
from .deduplication import deduplicate_and_merge
from .safety import detect_crisis_language, DEFAULT_DISCLAIMER
from .temporal import parse_time_references
from .router import get_router_query_engine
from .synthesizer import FrameworkSynthesizer

# Pydantic models for the request bodies
class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    interaction_id: str
    rating: float  # e.g., 1.0 for positive, -1.0 for negative
    comment: str = ""

class StartFlowRequest(BaseModel):
    flow_type: str

class AdvanceFlowRequest(BaseModel):
    flow_id: str
    current_step: str
    response: str

app = FastAPI()

# In-memory store for flow states. In a production environment, this would be
# replaced with a more robust solution like Redis or a database.
flow_states = {}

@app.post("/api/ingest")
async def ingest_data(request: IngestRequest):
    """
    Receives text, creates a LlamaIndex Document, extracts entities and
    relationships, deduplicates them against the existing graph, and upserts
    the new data.
    """
    try:
        # 1. Perform safety check on the input text
        if detect_crisis_language(request.text):
            return {
                "warning": "Crisis language detected.",
                "disclaimer": DEFAULT_DISCLAIMER,
            }

        # 2. Initialize the schema-aware extractor
        extractor = get_schema_extractor()

        # 3. Get the property graph index
        index = get_property_graph_index()

        # 4. Create a LlamaIndex Document from the raw text
        document = Document(text=request.text)

        # 5. Extract nodes and relationships from the document
        nodes, relationships = await extractor.aextract([document])

        # 6. Deduplicate nodes and re-wire relationships
        deduped_nodes, deduped_rels = await deduplicate_and_merge(
            nodes,
            relationships,
            index.property_graph_store,
        )

        # 7. Upsert the deduplicated data into the graph
        if deduped_nodes:
            index.insert_nodes(deduped_nodes)
        if deduped_rels:
            index.insert_relationships(deduped_rels)

        num_new_nodes = len(deduped_nodes)
        total_rels = len(deduped_rels)

        return {
            "message": (
                "Successfully ingested data. "
                f"Added {num_new_nodes} new nodes and processed {total_rels} relationships."
            )
        }

    except Exception as e:
        return {"error": f"Failed to ingest data: {str(e)}"}

@app.post("/api/query")
async def query(request: QueryRequest):
    """
    Receives a query, routes it to the appropriate query engine, and returns
    a synthesized response.
    """
    try:
        # 1. Perform safety check on the input query
        if detect_crisis_language(request.query):
            return {
                "warning": "Crisis language detected.",
                "disclaimer": DEFAULT_DISCLAIMER,
            }

        # 2. Parse time references from the query
        time_filters = parse_time_references(request.query)

        # 3. Get the property graph index and query engine
        graph_index = get_property_graph_index()
        graph_query_engine = graph_index.as_query_engine(include_text=True)

        # 4. Get the resource index and query engine
        qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))
        resource_vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name="lifeos_resources"
        )
        resource_index = VectorStoreIndex.from_vector_store(resource_vector_store)
        resource_query_engine = resource_index.as_query_engine()

        # 5. Get the router query engine
        router_query_engine = get_router_query_engine(
            graph_query_engine,
            resource_query_engine,
        )

        # 6. Perform the query
        response = await router_query_engine.aquery(request.query)

        # 7. Synthesize the response into a structured mental model
        synthesizer = FrameworkSynthesizer()
        mental_model = synthesizer.synthesize(response.response)

        return {
            "response": mental_model,
            "time_filters": time_filters,
            "source_nodes": [
                {
                    "text": node.node.get_content(),
                    "score": node.score,
                    "metadata": node.node.metadata,
                }
                for node in response.source_nodes
            ],
        }

    except Exception as e:
        return {"error": f"Failed to query: {str(e)}"}

@app.post("/api/flows/start")
async def start_flow(request: StartFlowRequest):
    """
    Initializes a new coaching flow for a user.
    """
    flow_id = str(uuid.uuid4())
    flow_states[flow_id] = {
        "flow_type": request.flow_type,
        "current_step": "step_1_greeting",
        "context": {},
    }
    return {
        "flow_id": flow_id,
        "current_step": "step_1_greeting",
        "message": "Welcome to your daily check-in. How are you feeling right now?",
    }

@app.post("/api/flows/advance")
async def advance_flow(request: AdvanceFlowRequest):
    """
    Submits a user's response and advances the flow to the next step.
    """
    flow_state = flow_states.get(request.flow_id)
    if not flow_state:
        return {"error": "Flow not found."}

    # This is a placeholder for the actual flow logic.
    # In a real implementation, this would be a state machine or a more
    # sophisticated flow engine.
    if request.current_step == "step_1_greeting":
        flow_state["current_step"] = "step_2_explore_emotion"
        flow_state["context"]["emotion"] = request.response
        return {
            "flow_id": request.flow_id,
            "current_step": "step_2_explore_emotion",
            "message": f"I understand you're feeling {request.response}. Can you tell me more about what's on your mind?",
        }
    elif request.current_step == "step_2_explore_emotion":
        flow_state["current_step"] = "step_final_summary"
        return {
            "flow_id": request.flow_id,
            "current_step": "step_final_summary",
            "message": "Thank you for sharing. It's important to acknowledge these feelings. Remember to be kind to yourself today.",
            "is_complete": True,
        }
    else:
        return {"error": "Invalid step."}

@app.post("/api/feedback")
async def log_feedback(request: FeedbackRequest):
    """
    Receives and logs user feedback for a specific interaction.
    """
    try:
        feedback_file = "feedback.csv"
        file_exists = os.path.exists(feedback_file)

        with open(feedback_file, "a") as f:
            if not file_exists:
                f.write("interaction_id,rating,comment,timestamp\n")

            timestamp = datetime.now().isoformat()
            f.write(f'"{request.interaction_id}",{request.rating},"{request.comment}",{timestamp}\n')

        return {"message": "Feedback logged successfully."}

    except Exception as e:
        return {"error": f"Failed to log feedback: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "LifeOS RAG API is running."}
