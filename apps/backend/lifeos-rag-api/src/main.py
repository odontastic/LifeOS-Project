import uuid
import json
import logging
import time # Import the time module
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from uuid import UUID

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm # Import OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlalchemy.orm import Session # Import Session for database dependency

from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from fastapi_limiter import FastAPILimiter # Import FastAPILimiter

from config import (
    NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD,
    QDRANT_URL, ARANGODB_HOST, ARANGODB_DB, ARANGODB_USER, ARANGODB_PASSWORD, QDRANT_API_KEY, QDRANT_GRPC_PORT,
    REDIS_HOST, REDIS_PORT, REDIS_DB,
    ALLOWED_ORIGINS, LOG_LEVEL, ACCESS_TOKEN_EXPIRE_MINUTES
)

from extractor import get_schema_extractor
from safety import detect_crisis_language, DEFAULT_DISCLAIMER
from temporal import parse_time_references
from reconciliation import DataReconciler # Import DataReconciler
from auth import ( # Import auth functions and models
    create_user, get_user_by_username, verify_password,
    create_access_token, get_current_user
)
from database import (
    get_db, Base, engine, User, StoredEvent,
    ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
    TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
    EmotionReadModel, BeliefReadModel, TriggerReadModel,
    EmotionEntryModel, ContactProfileModel, TaskItemModel, KnowledgeNodeModel, SystemInsightModel
)
from schemas import (
    EmotionEntry, ContactProfile, TaskItem, KnowledgeNode, SystemInsight,
    CalmFeedbackRequest, SystemInsightFeedbackEvent, ContactCreatedEvent, ContactDeletedEvent, NodeCreatedEvent,
    EdgeCreatedEvent, KnowledgeNodeEvent, RelationLoggedEvent
) # Import Pydantic schemas for entities
from crud import create_item, get_item_by_id, get_items, update_item, delete_item, get_db_core_session
from calm_compass import process_emotion_entry_for_calm_compass, update_calm_compass_model_with_feedback # Import Calm Compass processing

# Imports for event sourcing
from event_sourcing.event_store import EventStore # Import the EventStore class
from event_sourcing.models import Event as EventPydantic # Import the Event Pydantic model and alias it
from event_sourcing.event_processor import EventProcessor # Import the EventProcessor class
from dependencies import (
    initialize_dependencies, get_event_store, get_event_processor, 
    get_qdrant_client, get_arangodb_db, 
    event_store_instance, event_processor_instance # Explicitly import instances
)





# --- Logging Setup ---
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Explicitly set log levels for event_sourcing modules to DEBUG
logging.getLogger("event_sourcing.event_processor").setLevel(logging.DEBUG)
logging.getLogger("event_sourcing.event_store").setLevel(logging.DEBUG)

# --- Redis Client ---
redis_client = None # Declare globally, initialized asynchronously
async def setup_redis():
    global redis_client
    try:
        redis_client = await redis.from_url(
            f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2
        )
        logger.info("redis-py async client initialized successfully.")
    except Exception as e:
        logger.warning(f"Failed to initialize redis-py async client: {e}")
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



# --- FastAPI App ---
app = FastAPI(title="LifeOS RAG API", version="20.0.0")



@app.on_event("startup")
async def startup_event():
    await setup_redis()
    
    logger.info(f"Attempting to create database tables. Tables known to Base.metadata: {list(Base.metadata.tables.keys())}")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/checked successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)

    if redis_client:
        await FastAPILimiter.init(redis=redis_client)
    else:
        logger.warning("Redis client not initialized, rate limiting will be disabled.")
    
    # Initialize all application-wide dependencies
    await initialize_dependencies(
        engine=engine, 
        qdrant_url=QDRANT_URL, 
        qdrant_api_key=QDRANT_API_KEY, 
        arangodb_host=ARANGODB_HOST, 
        arangodb_db=ARANGODB_DB, 
        arangodb_user=ARANGODB_USER, 
        arangodb_password=ARANGODB_PASSWORD
    )


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
# # @RateLimiter(times=5, seconds=60) # 5 login attempts per minute
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
    
    # Emit EmotionCreated event
    # created_emotion = create_item(db, EmotionEntryModel, emotion_entry) # Removed direct CRUD
    event_payload_dict = emotion_entry.model_dump(mode='json') # Get dict representation for payload

    emotion_created_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="EmotionCreated",
        timestamp=datetime.now(timezone.utc), # Ensure timezone aware datetime
        payload=event_payload_dict,
        schema_version="1.0"
    )
    # Append event to the store
    stored_event = event_store_instance.append_event(
        event_id=emotion_created_event.event_id,
        event_type=emotion_created_event.event_type,
        timestamp=emotion_created_event.timestamp,
        payload=emotion_created_event.payload,
        schema_version=emotion_created_event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied EmotionCreated event for emotion_id: {emotion_entry.id}")
    
    # Process the emotion with Calm Compass (now using the original emotion_entry)
    process_emotion_entry_for_calm_compass(db, emotion_entry) # Pass the original Pydantic model
    
    return emotion_entry

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
    
    # Emit SystemInsightFeedbackEvent
    # Align payload: CalmFeedbackRequest(insight_id, rating, comment) -> SystemInsightFeedbackEvent(insight_id, feedback_rating, feedback_comment)
    feedback_event_payload = SystemInsightFeedbackEvent(
        insight_id=feedback.insight_id,
        feedback_rating=feedback.rating,
        feedback_comment=feedback.comment
    )
    event_payload_dict = feedback_event_payload.model_dump(mode='json') # Get dict representation for payload

    system_insight_feedback_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="SystemInsightFeedbackCreated", # Consistent with EventProcessor
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    stored_event = event_store_instance.append_event(
        event_id=system_insight_feedback_event.event_id,
        event_type=system_insight_feedback_event.event_type,
        timestamp=system_insight_feedback_event.timestamp,
        payload=system_insight_feedback_event.payload,
        schema_version=system_insight_feedback_event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied SystemInsightFeedback event for insight_id: {feedback.insight_id}")
    
    # The actual update of SystemInsight will be handled by the EventProcessor.
    # We still need to integrate Feedback Reinforcement Learning for Calm Compass.
    # Ideally, this would also be event-driven or triggered by the EventProcessor.
    update_calm_compass_model_with_feedback(feedback.insight_id, feedback.rating)
    
    return {"message": "Feedback submitted successfully for SystemInsight."}

@app.post("/relation/log")
async def log_relation(
    relation_log: RelationLoggedEvent,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' logging relation interaction for contact: {relation_log.contact_id}")

    # Check if contact exists in the read model before emitting an event
    existing_contact = event_processor_instance.get_read_model(ContactProfileReadModel, str(relation_log.contact_id))
    if not existing_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")

    event_payload_dict = relation_log.model_dump(mode='json')

    relation_logged_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="RelationLogged",
        timestamp=datetime.now(timezone.utc), # The event captures when it was processed, not when the interaction happened
        payload=event_payload_dict,
        schema_version="1.0"
    )
    stored_event = event_store_instance.append_event(
        event_id=relation_logged_event.event_id,
        event_type=relation_logged_event.event_type,
        timestamp=relation_logged_event.timestamp,
        payload=relation_logged_event.payload,
        schema_version=relation_logged_event.schema_version
    )
    # Immediately apply event to rebuild/update read model (STUBbed in Phase 3)
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied RelationLogged event for contact id: {relation_log.contact_id}")

    return {"message": f"Relation interaction log event emitted successfully for contact {relation_log.contact_id}."}

@app.post("/task/sync", response_model=TaskItem)
async def sync_task(task_item: TaskItem, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' syncing task: {task_item.title}")
    
    # Determine if it's a create or update by checking the read model
    existing_task = event_processor_instance.get_read_model(TaskReadModel, str(task_item.id))
    
    event_type = "TaskUpdated" if existing_task else "TaskCreated"

    # Emit event
    event_payload_dict = task_item.model_dump(mode='json')

    task_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    stored_event = event_store_instance.append_event(
        event_id=task_event.event_id,
        event_type=task_event.event_type,
        timestamp=task_event.timestamp,
        payload=task_event.payload,
        schema_version=task_event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied {event_type} event for Task id: {task_item.id}")
    
    # The response should be the original task_item, as the state is now managed by the event processor
    return task_item

@app.post("/para/update", response_model=KnowledgeNode)
async def update_para_node(knowledge_node: KnowledgeNode, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' updating PARA node: {knowledge_node.title}")
    
    # Determine if it's a create or update by checking the read model
    existing_node = event_processor_instance.get_read_model(KnowledgeNodeReadModel, str(knowledge_node.id))
    
    event_type = "KnowledgeNodeUpdated" if existing_node else "KnowledgeNodeCreated"

    # Emit event
    event_payload = KnowledgeNodeEvent(
        id=knowledge_node.id,
        title=knowledge_node.title,
        content=knowledge_node.content,
        node_type=knowledge_node.node_type,
        tags=knowledge_node.tags,
        related_nodes=knowledge_node.related_nodes,
        timestamp=datetime.now(timezone.utc)
    )
    event_payload_dict = event_payload.model_dump(mode='json')

    knowledge_node_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    # PHASE4: KnowledgeNodeReadModel will be introduced in Phase 4.
    # Until then, events are validated but not materialized into a dedicated read model.
    stored_event = event_store_instance.append_event(
        event_id=knowledge_node_event.event_id,
        event_type=knowledge_node_event.event_type,
        timestamp=knowledge_node_event.timestamp,
        payload=knowledge_node_event.payload,
        schema_version=knowledge_node_event.schema_version
    )
    # Immediately apply event to rebuild/update read model (STUBbed in Phase 3)
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied {event_type} event for KnowledgeNode id: {knowledge_node.id}")
    
    return knowledge_node
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
    
    # Emit ContactCreated event
    event_payload_dict = contact_profile.model_dump(mode='json') # Get dict representation for payload

    contact_created_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="ContactCreated", # New event type for contact creation
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    # Append event to the store
    stored_event = event_store_instance.append_event(
        event_id=contact_created_event.event_id,
        event_type=contact_created_event.event_type,
        timestamp=contact_created_event.timestamp,
        payload=contact_created_event.payload,
        schema_version=contact_created_event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied ContactCreated event for contact_id: {contact_profile.id}")
    
    return contact_profile

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

    # Check if contact exists in the read model
    existing_contact = event_processor_instance.get_read_model(ContactProfileReadModel, str(contact_id))
    if not existing_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")

    # The payload for the event should be the full ContactProfile
    # The client is expected to send the full updated profile
    event_payload_dict = contact_profile.model_dump(mode='json')

    contact_updated_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="ContactUpdated",
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    stored_event = event_store_instance.append_event(
        event_id=contact_updated_event.event_id,
        event_type=contact_updated_event.event_type,
        timestamp=contact_updated_event.timestamp,
        payload=contact_updated_event.payload,
        schema_version=contact_updated_event.schema_version
    )
    # Immediately apply event to rebuild/update read model (STUBbed in Phase 3)
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied ContactUpdated event for contact id: {contact_id}")
    
    return contact_profile

@app.delete("/contact/delete/{contact_id}")
async def delete_contact(contact_id: UUID, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    logger.info(f"User '{user.username}' deleting contact: {contact_id}")
    
    # Check if contact exists in the read model
    existing_contact = event_processor_instance.get_read_model(ContactProfileReadModel, str(contact_id))
    if not existing_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ContactProfile not found")

    event_payload = ContactDeletedEvent(
        contact_id=contact_id
    )
    event_payload_dict = event_payload.model_dump(mode='json')

    contact_deleted_event = EventPydantic(
        event_id=str(uuid.uuid4()),
        event_type="ContactDeleted",
        timestamp=datetime.now(timezone.utc),
        payload=event_payload_dict,
        schema_version="1.0"
    )
    stored_event = event_store_instance.append_event(
        event_id=contact_deleted_event.event_id,
        event_type=contact_deleted_event.event_type,
        timestamp=contact_deleted_event.timestamp,
        payload=contact_deleted_event.payload,
        schema_version=contact_deleted_event.schema_version
    )
    # Immediately apply event to rebuild/update read model (STUBbed in Phase 3)
    event_processor_instance._apply_event(stored_event)
    logger.info(f"Emitted and applied ContactDeleted event for contact_id: {contact_id}")
    
    return {"message": "ContactProfile deletion event emitted successfully."}

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

        for node in valid_nodes:
            # Determine collection name based on node type or metadata
            collection_name = "LlamaNodes" # For simplicity, using a generic collection name
            
            node_created_event_payload = NodeCreatedEvent(
                node_id=node.id_,
                text=node.text,
                metadata=node.metadata,
                collection_name=collection_name
            )
            stored_event = event_store_instance.append_event(
                event_id=str(uuid.uuid4()),
                event_type="NodeCreated",
                timestamp=datetime.now(timezone.utc),
                payload=node_created_event_payload.model_dump(mode='json'),
                schema_version="1.0"
            )
            event_processor_instance._apply_event(stored_event)
        
        for rel in high_confidence_rels:
            # Determine edge collection name
            edge_collection_name = rel.label if rel.label else "links_to"
            # Assuming source and target nodes are in 'LlamaNodes'
            from_node_id = rel.source_node.node_id
            to_node_id = rel.target_node.node_id
            
            edge_created_event_payload = EdgeCreatedEvent(
                from_node_id=from_node_id,
                to_node_id=to_node_id,
                label=rel.label,
                properties=rel.properties,
                from_collection="LlamaNodes", # Assuming this for now
                to_collection="LlamaNodes",   # Assuming this for now
                edge_collection_name=edge_collection_name
            )
            stored_event = event_store_instance.append_event(
                event_id=str(uuid.uuid4()),
                event_type="EdgeCreated",
                timestamp=datetime.now(timezone.utc),
                payload=edge_created_event_payload.model_dump(mode='json'),
                schema_version="1.0"
            )
            event_processor_instance._apply_event(stored_event)
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
    Returns basic metrics for monitoring, including ArangoDB node count and Qdrant point counts.
    """
    metrics = {}
    try:
        # Pass the global ArangoDB graph instance to the DataReconciler
        if not _arangodb_graph:
            raise HTTPException(status_code=500, detail="ArangoDB graph not initialized for metrics.")
        reconciler = DataReconciler(_arangodb_graph)
        
        # ArangoDB Node Count
        arangodb_ids = reconciler.get_arangodb_node_ids()
        metrics["arangodb_node_count"] = len(arangodb_ids)

        # Qdrant Point Counts
        metrics["qdrant_lifeos_notes_count"] = len(reconciler.get_qdrant_point_ids("lifeos_notes"))
        metrics["qdrant_lifeos_resources_count"] = len(reconciler.get_qdrant_point_ids("lifeos_resources"))

    except Exception as e:
        logger.error(f"Failed to retrieve metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {e}")

    return metrics