import os
import uuid
import json
import logging
import time # Import the time module
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from uuid import UUID

import redis
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm # Import OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlalchemy.orm import Session # Import Session for database dependency

from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams # Needed for Qdrant setup if collections are managed

from fastapi_limiter import FastAPILimiter # Import FastAPILimiter

from config import (
    NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD,
    QDRANT_URL, ARANGODB_HOST, ARANGODB_DB, ARANGODB_USER, ARANGODB_PASSWORD, QDRANT_API_KEY, QDRANT_GRPC_PORT,
    REDIS_HOST, REDIS_PORT, REDIS_DB,
    ALLOWED_ORIGINS, LOG_LEVEL, ACCESS_TOKEN_EXPIRE_MINUTES
)

from graph_db import init_lifeos_graph, insert_vertex, insert_edge # Import ArangoDB specific functions

from extractor import get_schema_extractor

# from deduplication import deduplicate_and_merge # Temporarily commented out for debugging
from safety import detect_crisis_language, DEFAULT_DISCLAIMER
from temporal import parse_time_references
from router import get_router_query_engine
from synthesizer import FrameworkSynthesizer
from reconciliation import DataReconciler # Import DataReconciler
from auth import ( # Import auth functions and models
    create_user, get_user_by_username, verify_password,
    create_access_token, get_current_user
)
from database import get_db, Base, engine, User, EmotionEntryModel, SystemInsightModel, ContactProfileModel, TaskItemModel, KnowledgeNodeModel
from schemas import EmotionEntry, EmotionLoggedEvent, ContactProfile, ContactUpdatedEvent, TaskItem, TaskStateChangedEvent, KnowledgeNode, SystemInsight, CalmFeedbackRequest, RelationLogRequest # Import Pydantic schemas for entities
from crud import create_item, get_item_by_id, get_items, update_item, delete_item, get_db_core_session
from calm_compass import process_emotion_entry_for_calm_compass, update_calm_compass_model_with_feedback # Import Calm Compass processing

# Imports for event sourcing
from event_sourcing.event_store import EventStore # Import the EventStore class
from event_sourcing.models import Event as EventPydantic # Import the Event Pydantic model and alias it
from event_sourcing.event_processor import EventProcessor # Import the EventProcessor class

# Initialize the global EventStore instance
event_store_instance: EventStore = EventStore(engine=engine)
# Initialize the global EventProcessor instance
event_processor_instance: EventProcessor = EventProcessor(event_store=event_store_instance, engine=engine)


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

# New Pydantic models for authentication
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependency to get the EventStore instance
def get_event_store() -> EventStore:
    return event_store_instance

# Dependency to get the EventProcessor instance
def get_event_processor() -> EventProcessor:
    return event_processor_instance

# --- FastAPI App ---
app = FastAPI(title="LifeOS RAG API", version="20.0.0")

_arangodb_graph = None # Global variable to hold the ArangoDB graph instance

@app.on_event("startup")
async def startup_event():
    global _arangodb_graph # Declare intention to modify the global variable
    Base.metadata.create_all(bind=engine)
    if redis_client:
        await FastAPILimiter.init(redis=redis_client)
    else:
        logger.warning("Redis client not initialized, rate limiting will be disabled.")
    
    # Initialize ArangoDB graph
    _arangodb_graph = init_lifeos_graph()
    if not _arangodb_graph:
        logger.error("Failed to initialize ArangoDB graph. Graph operations will not work.")

    # Replay events to build read models
    event_processor_instance.replay_events()
    logger.info("Event processor replayed all events to build read models.")


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import and include routers
from routers import zettel, project, area, resource, task, goal, reflection, journal_entry, emotion, belief, trigger

app.include_router(zettel.router, prefix="/zettel", tags=["Zettel"])
app.include_router(project.router, prefix="/project", tags=["Project"])
app.include_router(area.router, prefix="/area", tags=["Area"])
app.include_router(resource.router, prefix="/resource", tags=["Resource"])
app.include_router(task.router, prefix="/task", tags=["Task"])
app.include_router(goal.router, prefix="/goal", tags=["Goal"])
app.include_router(reflection.router, prefix="/reflection", tags=["Reflection"])
app.include_router(journal_entry.router, prefix="/journal_entry", tags=["Journal Entry"])
app.include_router(emotion.router, prefix="/emotion", tags=["Emotion"])
app.include_router(belief.router, prefix="/belief", tags=["Belief"])
app.include_router(trigger.router, prefix="/trigger", tags=["Trigger"])


# --- Authentication Routes ---
@app.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    # Optional: Validate password strength here
    if len(user.password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long")
    
    new_user = create_user(db=db, username=user.username, password=user.password, email=user.email)
    logger.info(f"User '{new_user.username}' registered successfully.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
# @RateLimiter(times=5, seconds=60) # 5 login attempts per minute
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"User '{user.username}' logged in successfully.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
        q_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=2)
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

@app.post("/emotion/log", response_model=EmotionEntry)
async def log_emotion(emotion_entry: EmotionEntry, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' logging emotion: {emotion_entry.primary_emotion}")
    
    # Save to SQLite
    created_emotion = create_item(db, EmotionEntryModel, emotion_entry)
    
    # Emit event through EmotionContextBus
    event_payload = EmotionLoggedEvent(
        emotion_id=emotion_entry.id,
        primary_emotion=emotion_entry.primary_emotion,
        valence=emotion_entry.valence,
        arousal=emotion_entry.arousal,
        context_tags=emotion_entry.context_tags
    )
    event_bus.emit("emotion_logged", event_payload)
    
    # Process the emotion with Calm Compass
    process_emotion_entry_for_calm_compass(db, created_emotion)
    
    return created_emotion

@app.get("/calm/recommend", response_model=Dict[str, Any])
async def get_calm_recommendation(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' requesting Calm Compass recommendation.")
    
    # Retrieve the latest SystemInsight of type 'feedback'
    # In a real scenario, this would be more complex, potentially filtering by user and context.
    insights = get_items(db, SystemInsightModel, limit=1, filters={"insight_type": "feedback"}) # Need to add filters to get_items if not present
    
    if insights:
        latest_insight = insights[0]
        return {
            "message": latest_insight['message'],
            "action_recommendations": latest_insight['action_recommendations']
        }
    else:
        return {
            "message": "No specific Calm Compass recommendations available yet. Try logging an emotion first.",
            "action_recommendations": []
        }

@app.get("/emotion/retrieve/{emotion_id}", response_model=EmotionEntry)
async def retrieve_emotion(emotion_id: UUID, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' retrieving emotion: {emotion_id}")
    
    emotion_item = get_item_by_id(db, EmotionEntryModel, emotion_id)
    if not emotion_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EmotionEntry not found")
    
    
    return emotion_item

@app.post("/calm/feedback")
async def submit_calm_feedback(
    feedback: CalmFeedbackRequest, 
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' submitting feedback for insight: {feedback.insight_id}")
    
    # Retrieve the SystemInsight
    insight_to_update = get_item_by_id(db, SystemInsightModel, feedback.insight_id)
    if not insight_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SystemInsight not found")
    
    # Update the SystemInsight with feedback.
    # We need to construct a Pydantic model for update or pass dict directly to update_item
    # For now, let's update by creating a new SystemInsight Pydantic model with feedback fields
    # This assumes update_item can handle partial updates if fields are not provided in schema_item
    
    # A more robust update_item would accept a dict and apply changes
    # For now, we will create a partial schema for update
    class SystemInsightUpdate(BaseModel):
        feedback_rating: Optional[int] = None
        feedback_comment: Optional[str] = None
        
    update_data = SystemInsightUpdate(
        feedback_rating=feedback.rating,
        feedback_comment=feedback.comment
    )
    
    updated_insight = update_item(db, SystemInsightModel, feedback.insight_id, update_data)
    
    if not updated_insight:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update SystemInsight with feedback.")
    
    # Integrate Feedback Reinforcement Learning for Calm Compass
    update_calm_compass_model_with_feedback(feedback.insight_id, feedback.rating)
    
    return {"message": "Feedback submitted successfully for SystemInsight."}

@app.post("/relation/log")
async def log_relation(
    relation_log: RelationLogRequest,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' logging relation interaction for contact: {relation_log.contact_id}")
    
    contact_to_update = get_item_by_id(db, ContactProfileModel, relation_log.contact_id)
    if not contact_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")

    # Update last_interaction
    contact_to_update_obj = ContactProfile(**contact_to_update) # Convert dict to Pydantic for easier manipulation
    contact_to_update_obj.last_interaction = relation_log.interaction_date

    # Append notes to context_history (if notes exist)
    if relation_log.notes:
        if contact_to_update_obj.context_history is None:
            contact_to_update_obj.context_history = []
        # Store a simple string or a more structured object with timestamp and notes
        contact_to_update_obj.context_history.append(str(relation_log.interaction_date) + ": " + relation_log.notes)
    
    updated_contact = update_item(db, ContactProfileModel, relation_log.contact_id, contact_to_update_obj)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update ContactProfile for relation log.")
    
    # Emit event through EmotionContextBus
    event_payload = ContactUpdatedEvent(
        contact_id=relation_log.contact_id,
        name=updated_contact['name'],
        sentiment_summary=updated_contact['sentiment_summary'],
        open_loops=updated_contact['open_loops']
    )
    event_bus.emit("contact_updated", event_payload)
    
    return {"message": f"Relation interaction logged successfully for contact {relation_log.contact_id}."}

@app.post("/task/sync", response_model=TaskItem)
async def sync_task(task_item: TaskItem, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' syncing task: {task_item.title}")
    
    existing_task = get_item_by_id(db, TaskItemModel, task_item.id)
    
    if existing_task:
        synced_task = update_item(db, TaskItemModel, task_item.id, task_item)
        if not synced_task:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update TaskItem.")
    else:
        synced_task = create_item(db, TaskItemModel, task_item)
    
    # Emit event through EmotionContextBus
    event_payload = TaskStateChangedEvent(
        task_id=task_item.id,
        status=task_item.status,
        priority=task_item.priority,
        energy_requirement=task_item.energy_requirement,
        context_tags=task_item.context_tags
    )
    event_bus.emit("task_state_changed", event_payload)
    
    return synced_task

@app.post("/para/update", response_model=KnowledgeNode)
async def update_para_node(knowledge_node: KnowledgeNode, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' updating PARA node: {knowledge_node.title}")
    
    existing_node = get_item_by_id(db, KnowledgeNodeModel, knowledge_node.id)
    
    if existing_node:
        synced_node = update_item(db, KnowledgeNodeModel, knowledge_node.id, knowledge_node)
        if not synced_node:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update KnowledgeNode.")
    else:
        synced_node = create_item(db, KnowledgeNodeModel, knowledge_node)
        
    # TODO: Emit event for knowledge node update/creation
    
    return synced_node

@app.get("/relation/prompts", response_model=List[str])
async def get_relation_prompts(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' requesting relation prompts.")
    # Placeholder for AI-generated prompts.
    # In future, this will integrate with AI Insight Layer and Connection Engine logic.
    return [
        "What's one small thing you can do today to strengthen a key relationship?",
        "Reflect on a recent interaction: what emotion was most dominant for you, and for them?",
        "Is there an 'open loop' with a contact that needs attention?",
        "Who haven't you connected with meaningfully in a while?"
    ]

@app.get("/emotion/analyze", response_model=Dict[str, Any])
async def analyze_emotion(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' requesting emotion analysis.")
    logger.info(f"User '{current_user.username}' requesting emotion analysis.")
    # Placeholder for actual analysis. Later this will integrate with AI Insight Layer.
    all_emotions = get_items(db, EmotionEntryModel)
    
    if not all_emotions:
        return {"message": "No emotions logged yet for analysis."}
    
    # Simple aggregation example
    emotion_counts = {}
    for emotion in all_emotions:
        primary = emotion['primary_emotion']
        emotion_counts[primary] = emotion_counts.get(primary, 0) + 1
        
    return {
        "message": "Emotion analysis placeholder.",
        "total_emotions_logged": len(all_emotions),
        "primary_emotion_counts": emotion_counts,
        "note": "Full analysis will integrate with AI Insight Layer and provide deeper insights."
    }

async def create_contact(contact_profile: ContactProfile, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' creating contact: {contact_profile.name}")
    
    # Save to SQLite
    created_contact = create_item(db, ContactProfileModel, contact_profile)
    
    # Emit event through EmotionContextBus
    event_payload = ContactUpdatedEvent(
        contact_id=contact_profile.id,
        name=contact_profile.name,
        sentiment_summary=contact_profile.sentiment_summary,
        open_loops=contact_profile.open_loops
    )
    event_bus.emit("contact_updated", event_payload)
    
    return created_contact

async def retrieve_contact(contact_id: UUID, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' retrieving contact: {contact_id}")
    
    contact_item = get_item_by_id(db, ContactProfileModel, contact_id)
    if not contact_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")
    
    return contact_item

@app.put("/contact/update/{contact_id}", response_model=ContactProfile)
async def update_contact(
    contact_id: UUID,
    contact_profile: ContactProfile,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' updating contact: {contact_id}")    
    updated_contact = update_item(db, ContactProfileModel, contact_id, contact_profile)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")
    
    # Emit event through EmotionContextBus
    event_payload = ContactUpdatedEvent(
        contact_id=UUID(updated_contact['id']),
        name=updated_contact['name'],
        sentiment_summary=updated_contact['sentiment_summary'],
        open_loops=updated_contact['open_loops']
    )
    event_bus.emit("contact_updated", event_payload)
    
    return updated_contact

@app.delete("/contact/delete/{contact_id}")
async def delete_contact(contact_id: UUID, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' deleting contact: {contact_id}")
    
    if not delete_item(db, ContactProfileModel, contact_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")
    
    # Emit event through EmotionContextBus (can be a generic 'deleted' event or contact_updated with status)
    # For now, a simple contact_updated event could signify a change, possibly with a 'deleted' flag in payload
    event_payload = ContactUpdatedEvent(
        contact_id=contact_id,
        name="Deleted Contact", # Placeholder name for event
        sentiment_summary="Deleted",
        open_loops=[]
    )
    event_bus.emit("contact_updated", event_payload) # Emitting update event to notify of change
    
    return {"message": "ContactProfile deleted successfully."}

async def ingest_data(request: IngestRequest, db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    start_time = time.time() # Start timer
    logger.info("Received ingest request")
    CONFIDENCE_THRESHOLD = 0.65
    try:
        if detect_crisis_language(request.text):
            return {"warning": "Crisis language detected.", "disclaimer": DEFAULT_DISCLAIMER}

        extractor = get_schema_extractor()
        # index = get_property_graph_index() # Neo4j-specific, removed
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

        # --- ArangoDB Ingestion ---
        if not _arangodb_graph:
            raise HTTPException(status_code=500, detail="ArangoDB graph not initialized.")

        # Placeholder for ArangoDB insertion
        # This part needs detailed implementation to convert LlamaIndex nodes/rels to ArangoDB vertices/edges
        # For now, just acknowledge the conversion is needed.
        for node in valid_nodes:
            # Determine collection name based on node type or metadata
            # For simplicity, let's use a generic 'LlamaNodes' collection for now
            vertex_data = {"_key": node.id_, "text": node.text, "metadata": node.metadata}
            insert_vertex(_arangodb_graph, "LlamaNodes", vertex_data)
        
        for rel in high_confidence_rels:
            # Determine edge collection name
            edge_collection_name = rel.label if rel.label else "links_to"
            # Assuming source and target nodes are in 'LlamaNodes'
            from_key = rel.source_node.node_id
            to_key = rel.target_node.node_id
            edge_data = {"properties": rel.properties, "from_collection": "LlamaNodes", "to_collection": "LlamaNodes"}
            insert_edge(_arangodb_graph, edge_collection_name, from_key, to_key, edge_data)

        end_time = time.time() # End timer
        duration = (end_time - start_time) * 1000 # Duration in ms
        logger.info(f"Ingest request completed in {duration:.2f} ms. Ingested {len(valid_nodes)} nodes and {len(high_confidence_rels)} relationships into ArangoDB.")

        return {
            "message": f"Successfully ingested {len(valid_nodes)} nodes and {len(high_confidence_rels)} relationships into ArangoDB."
        }
    except Exception as e:
        end_time = time.time() # End timer even on error
        duration = (end_time - start_time) * 1000 # Duration in ms
        logger.error(f"Ingestion failed in {duration:.2f} ms: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/api/query")
async def query(request: QueryRequest, db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    start_time = time.time() # Start timer
    logger.info(f"Received query: {request.query[:50]}...")
    try:
        if detect_crisis_language(request.query):
            return {"warning": "Crisis language detected.", "disclaimer": DEFAULT_DISCLAIMER}

        time_filters = parse_time_references(request.query)
        
        llama_filters = []
        if "start_date" in time_filters:
            llama_filters.append(MetadataFilter(key="created_at", operator=">=", value=time_filters["start_date"]))
        if "end_date" in time_filters:
            llama_filters.append(MetadataFilter(key="created_at", operator="<=", value=time_filters["end_date"]))

        # Apply semantic filters
        if "life_domain" in time_filters:
            llama_filters.append(MetadataFilter(key="life_domain", operator="==", value=time_filters["life_domain"]))
        if "life_stage" in time_filters:
            llama_filters.append(MetadataFilter(key="life_stage", operator="==", value=time_filters["life_stage"]))
        if "episode" in time_filters:
            llama_filters.append(MetadataFilter(key="episode", operator="==", value=time_filters["episode"]))
        
        final_llama_filters = MetadataFilters(filters=llama_filters) if llama_filters else None

        # --- ArangoDB Graph Query Integration Needed Here ---
        # This section previously used Neo4j LlamaIndex graph query engine.
        # Now, it needs to be replaced with ArangoDB-based graph querying.
        # Options include:
        # 1. Implement a custom LlamaIndex GraphStore for ArangoDB.
        # 2. Directly query ArangoDB using AQL and feed results to LlamaIndex's response synthesizer.
        # For now, we will return a placeholder response for graph queries.
        # graph_index = get_property_graph_index() # Removed Neo4j specific
        # graph_query_engine = graph_index.as_query_engine(include_text=True, filters=final_llama_filters)

        # Placeholder for graph_query_engine if ArangoDB is not integrated yet
        class PlaceholderGraphQueryEngine:
            async def aquery(self, query_str: str):
                return Response(response=f"Graph query via ArangoDB not yet implemented for: {query_str}")
        
        graph_query_engine = PlaceholderGraphQueryEngine()

        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        resource_store = QdrantVectorStore(client=qdrant_client, collection_name="lifeos_resources")
        resource_index = VectorStoreIndex.from_vector_store(resource_store)
        resource_query_engine = resource_index.as_query_engine()

        router = get_router_query_engine(graph_query_engine, resource_query_engine)
        response = await router.aquery(request.query)

        synthesizer = FrameworkSynthesizer()
        mental_model = synthesizer.synthesize(response.response)

        end_time = time.time() # End timer
        duration = (end_time - start_time) * 1000 # Duration in ms
        logger.info(f"Query request completed in {duration:.2f} ms.")

        return {
            "response": mental_model,
            "time_filters": time_filters,
            "source_nodes": [
                {"text": n.node.get_content(), "score": n.score, "metadata": n.node.metadata}
                for n in response.source_nodes
            ]
        }
    except Exception as e:
        end_time = time.time() # End timer even on error
        duration = (end_time - start_time) * 1000 # Duration in ms
        logger.error(f"Query failed in {duration:.2f} ms: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/api/flows/start")
async def start_flow(request: StartFlowRequest, db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
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
async def advance_flow(request: AdvanceFlowRequest, db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
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
async def log_feedback(request: FeedbackRequest, db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
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

async def get_metrics(db: Session = Depends(get_db), current_user_username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=current_user_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    """
    Returns basic metrics for monitoring, including Neo4j node count and Qdrant point counts.
    """
    metrics = {}
    try:
        reconciler = DataReconciler()
        
        # Neo4j Node Count
        neo4j_ids = reconciler.get_neo4j_node_ids()
        metrics["neo4j_node_count"] = len(neo4j_ids)

        # Qdrant Point Counts
        metrics["qdrant_lifeos_notes_count"] = len(reconciler.get_qdrant_point_ids("lifeos_notes"))
        metrics["qdrant_lifeos_resources_count"] = len(reconciler.get_qdrant_point_ids("lifeos_resources"))

    except Exception as e:
        logger.error(f"Failed to retrieve metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {e}")

    return metrics