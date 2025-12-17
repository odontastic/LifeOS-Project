    import os
    import json
    from datetime import datetime
    from typing import Dict, Any, Type, List, Optional, AsyncGenerator

    from arango.database import StandardDatabase
    from qdrant_client import QdrantClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from dotenv import load_dotenv
    import logging

    from event_sourcing.event_store import EventStore
    from database import (
        Base, StoredEvent,
        ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
        TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
        EmotionReadModel, BeliefReadModel, TriggerReadModel, SystemInsightReadModel, ContactProfileReadModel
    )
    from models.zettel import Zettel
    from models.project import Project
    from models.area import Area
    from models.resource import Resource
    from models.task import Task
    from models.goal import Goal
    from models.reflection import Reflection
    from models.journal_entry import JournalEntry
    from models.emotion import Emotion
    from models.belief import Belief
    from models.trigger import Trigger
    from schemas import SystemInsightFeedbackEvent, ContactCreatedEvent, ContactProfile


# Load environment variables
load_dotenv()
# SQLITE_READ_MODELS_DB_PATH is now managed by the injected engine for tests
# os.makedirs(os.path.dirname(SQLITE_READ_MODELS_DB_PATH), exist_ok=True)

logger = logging.getLogger(__name__) # Initialize logger

class EventProcessor:
    def __init__(self, event_store: EventStore, engine, qdrant_client: QdrantClient, arangodb_db: StandardDatabase):
        self.event_store = event_store
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.qdrant_client = qdrant_client
        self.arangodb_db = arangodb_db
        self.qdrant_service = QdrantService(qdrant_client)
        self.arangodb_service = ArangoDBService(arangodb_db)

        # Mapping of event types to their Pydantic schemas for payload validation
        self.event_payload_schemas: Dict[str, Type[BaseModel]] = {
            "ZettelCreated": Zettel,
            "ZettelUpdated": Zettel,
            "ZettelDeleted": Zettel,
            "ProjectCreated": Project,
            "ProjectUpdated": Project,
            "ProjectDeleted": Project,
            "AreaCreated": Area,
            "AreaUpdated": Area,
            "AreaDeleted": Area,
            "ResourceCreated": Resource,
            "ResourceUpdated": Resource,
            "ResourceDeleted": Resource,
            "TaskCreated": Task,
            "TaskUpdated": Task,
            "TaskDeleted": Task,
            "GoalCreated": Goal,
            "GoalUpdated": Goal,
            "GoalDeleted": Goal,
            "ReflectionCreated": Reflection,
            "ReflectionUpdated": Reflection,
            "ReflectionDeleted": Reflection,
            "JournalEntryCreated": JournalEntry,
            "JournalEntryUpdated": JournalEntry,
            "JournalEntryDeleted": JournalEntry,
            "EmotionCreated": Emotion,
            "EmotionUpdated": Emotion,
            "EmotionDeleted": Emotion,
            "BeliefCreated": Belief,
            "BeliefUpdated": Belief,
            "BeliefDeleted": Belief,
            "TriggerCreated": Trigger,
            "TriggerUpdated": Trigger,
            "TriggerDeleted": Trigger,
            "SystemInsightFeedbackCreated": SystemInsightFeedbackEvent,
            "ContactCreated": ContactProfile, # Map to ContactProfile Pydantic model
            "ContactUpdated": ContactProfile,
            "ContactDeleted": ContactProfile,
        }


        # Mapping of event types to handler methods
        self.event_handlers: Dict[str, callable] = {
            "ZettelCreated": self._handle_zettel_created,
            "ZettelUpdated": self._handle_zettel_updated,
            "ZettelDeleted": self._handle_zettel_deleted,
            "ProjectCreated": self._handle_project_created,
            "ProjectUpdated": self._handle_project_updated,
            "ProjectDeleted": self._handle_project_deleted,
            "AreaCreated": self._handle_area_created,
            "AreaUpdated": self._handle_area_updated,
            "AreaDeleted": self._handle_area_deleted,
            "ResourceCreated": self._handle_resource_created,
            "ResourceUpdated": self._handle_resource_updated,
            "ResourceDeleted": self._handle_resource_deleted,
            "TaskCreated": self._handle_task_created,
            "TaskUpdated": self._handle_task_updated,
            "TaskDeleted": self._handle_task_deleted,
            "GoalCreated": self._handle_goal_created,
            "GoalUpdated": self._handle_goal_updated,
            "GoalDeleted": self._handle_goal_deleted,
            "ReflectionCreated": self._handle_reflection_created,
            "ReflectionUpdated": self._handle_reflection_updated,
            "ReflectionDeleted": self._handle_reflection_deleted,
            "JournalEntryCreated": self._handle_journal_entry_created,
            "JournalEntryUpdated": self._handle_journal_entry_updated,
            "JournalEntryDeleted": self._handle_journal_entry_deleted,
            "EmotionCreated": self._handle_emotion_created,
            "EmotionUpdated": self._handle_emotion_updated,
            "EmotionDeleted": self._handle_emotion_deleted,
            "BeliefCreated": self._handle_belief_created,
            "BeliefUpdated": self._handle_belief_updated,
            "BeliefDeleted": self._handle_belief_deleted,
            "TriggerCreated": self._handle_trigger_created,
            "TriggerUpdated": self._handle_trigger_updated,
            "TriggerDeleted": self._handle_trigger_deleted,
    import os
    import json
    from datetime import datetime
    from typing import Dict, Any, Type, List, Optional, AsyncGenerator

    from arango.database import StandardDatabase
    from qdrant_client import QdrantClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from dotenv import load_dotenv
    import logging

    from event_sourcing.event_store import EventStore
    from database import (
        Base, StoredEvent,
        ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
        TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
        EmotionReadModel, BeliefReadModel, TriggerReadModel, SystemInsightReadModel, ContactProfileReadModel
    )
    from models.zettel import Zettel
    from models.project import Project
    from models.area import Area
    from models.resource import Resource
    from models.task import Task
    from models.goal import Goal
    from models.reflection import Reflection
    from models.journal_entry import JournalEntry
    from models.emotion import Emotion
    from models.belief import Belief
    from models.trigger import Trigger
    from schemas import SystemInsightFeedbackEvent, ContactCreatedEvent, ContactProfile


# Load environment variables
load_dotenv()
# SQLITE_READ_MODELS_DB_PATH is now managed by the injected engine for tests
# os.makedirs(os.path.dirname(SQLITE_READ_MODELS_DB_PATH), exist_ok=True)

logger = logging.getLogger(__name__) # Initialize logger

class EventProcessor:
    def __init__(self, event_store: EventStore, engine, qdrant_client: QdrantClient, arangodb_db: StandardDatabase):
        self.event_store = event_store
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.qdrant_client = qdrant_client
        self.arangodb_db = arangodb_db
        self.qdrant_service = QdrantService(qdrant_client)
        self.arangodb_service = ArangoDBService(arangodb_db)

        # Mapping of event types to their Pydantic schemas for payload validation
        self.event_payload_schemas: Dict[str, Type[BaseModel]] = {
            "ZettelCreated": Zettel,
            "ZettelUpdated": Zettel,
            "ZettelDeleted": Zettel,
            "ProjectCreated": Project,
            "ProjectUpdated": Project,
            "ProjectDeleted": Project,
            "AreaCreated": Area,
            "AreaUpdated": Area,
            "AreaDeleted": Area,
            "ResourceCreated": Resource,
            "ResourceUpdated": Resource,
            "ResourceDeleted": Resource,
            "TaskCreated": Task,
            "TaskUpdated": Task,
            "TaskDeleted": Task,
            "GoalCreated": Goal,
            "GoalUpdated": Goal,
            "GoalDeleted": Goal,
            "ReflectionCreated": Reflection,
            "ReflectionUpdated": Reflection,
            "ReflectionDeleted": Reflection,
            "JournalEntryCreated": JournalEntry,
            "JournalEntryUpdated": JournalEntry,
            "JournalEntryDeleted": JournalEntry,
            "EmotionCreated": Emotion,
            "EmotionUpdated": Emotion,
            "EmotionDeleted": Emotion,
            "BeliefCreated": Belief,
            "BeliefUpdated": Belief,
            "BeliefDeleted": Belief,
            "TriggerCreated": Trigger,
            "TriggerUpdated": Trigger,
            "TriggerDeleted": Trigger,
            "SystemInsightFeedbackCreated": SystemInsightFeedbackEvent,
            "ContactCreated": ContactProfile, # Map to ContactProfile Pydantic model
            "ContactUpdated": ContactProfile,
            "ContactDeleted": ContactProfile,
        }


        # Mapping of event types to handler methods
        self.event_handlers: Dict[str, callable] = {
            "ZettelCreated": self._handle_zettel_created,
            "ZettelUpdated": self._handle_zettel_updated,
            "ZettelDeleted": self._handle_zettel_deleted,
            "ProjectCreated": self._handle_project_created,
            "ProjectUpdated": self._handle_project_updated,
            "ProjectDeleted": self._handle_project_deleted,
            "AreaCreated": self._handle_area_created,
            "AreaUpdated": self._handle_area_updated,
            "AreaDeleted": self._handle_area_deleted,
            "ResourceCreated": self._handle_resource_created,
            "ResourceUpdated": self._handle_resource_updated,
            "ResourceDeleted": self._handle_resource_deleted,
            "TaskCreated": self._handle_task_created,
            "TaskUpdated": self._handle_task_updated,
            "TaskDeleted": self._handle_task_deleted,
            "GoalCreated": self._handle_goal_created,
            "GoalUpdated": self._handle_goal_updated,
            "GoalDeleted": self._handle_goal_deleted,
            "ReflectionCreated": self._handle_reflection_created,
            "ReflectionUpdated": self._handle_reflection_updated,
            "ReflectionDeleted": self._handle_reflection_deleted,
            "JournalEntryCreated": self._handle_journal_entry_created,
            "JournalEntryUpdated": self._handle_journal_entry_updated,
            "JournalEntryDeleted": self._handle_journal_entry_deleted,
            "EmotionCreated": self._handle_emotion_created,
            "EmotionUpdated": self._handle_emotion_updated,
            "EmotionDeleted": self._handle_emotion_deleted,
            "BeliefCreated": self._handle_belief_created,
            "BeliefUpdated": self._handle_belief_updated,
            "BeliefDeleted": self._handle_belief_deleted,
            "TriggerCreated": self._handle_trigger_created,
            "TriggerUpdated": self._handle_trigger_updated,
            "TriggerDeleted": self._handle_trigger_deleted,
            "SystemInsightFeedbackCreated": self._handle_system_insight_feedback_created,
            "ContactCreated": self._handle_contact_created,
    import os
    import json
    from datetime import datetime
    from typing import Dict, Any, Type, List, Optional, AsyncGenerator

    from arango.database import StandardDatabase
    from qdrant_client import QdrantClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    from dotenv import load_dotenv
    import logging

    from event_sourcing.event_store import EventStore
    from database import (
        Base, StoredEvent,
        ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
        TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
        EmotionReadModel, BeliefReadModel, TriggerReadModel, SystemInsightReadModel, ContactProfileReadModel
    )
    from models.zettel import Zettel
    from models.project import Project
    from models.area import Area
    from models.resource import Resource
    from models.task import Task
    from models.goal import Goal
    from models.reflection import Reflection
    from models.journal_entry import JournalEntry
    from models.emotion import Emotion
    from models.belief import Belief
    from models.trigger import Trigger
    from schemas import SystemInsightFeedbackEvent, ContactCreatedEvent, ContactProfile


# Load environment variables
load_dotenv()
# SQLITE_READ_MODELS_DB_PATH is now managed by the injected engine for tests
# os.makedirs(os.path.dirname(SQLITE_READ_MODELS_DB_PATH), exist_ok=True)

logger = logging.getLogger(__name__) # Initialize logger

class EventProcessor:
    def __init__(self, event_store: EventStore, engine, qdrant_client: QdrantClient, arangodb_db: StandardDatabase):
        self.event_store = event_store
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.qdrant_client = qdrant_client
        self.arangodb_db = arangodb_db
        self.qdrant_service = QdrantService(qdrant_client)
        self.arangodb_service = ArangoDBService(arangodb_db)

        # Mapping of event types to their Pydantic schemas for payload validation
        self.event_payload_schemas: Dict[str, Type[BaseModel]] = {
            "ZettelCreated": Zettel,
            "ZettelUpdated": Zettel,
            "ZettelDeleted": Zettel,
            "ProjectCreated": Project,
            "ProjectUpdated": Project,
            "ProjectDeleted": Project,
            "AreaCreated": Area,
            "AreaUpdated": Area,
            "AreaDeleted": Area,
            "ResourceCreated": Resource,
            "ResourceUpdated": Resource,
            "ResourceDeleted": Resource,
            "TaskCreated": Task,
            "TaskUpdated": Task,
            "TaskDeleted": Task,
            "GoalCreated": Goal,
            "GoalUpdated": Goal,
            "GoalDeleted": Goal,
            "ReflectionCreated": Reflection,
            "ReflectionUpdated": Reflection,
            "ReflectionDeleted": Reflection,
            "JournalEntryCreated": JournalEntry,
            "JournalEntryUpdated": JournalEntry,
            "JournalEntryDeleted": JournalEntry,
            "EmotionCreated": Emotion,
            "EmotionUpdated": Emotion,
            "EmotionDeleted": Emotion,
            "BeliefCreated": Belief,
            "BeliefUpdated": Belief,
            "BeliefDeleted": Belief,
            "TriggerCreated": Trigger,
            "TriggerUpdated": Trigger,
            "TriggerDeleted": Trigger,
            "SystemInsightFeedbackCreated": SystemInsightFeedbackEvent,
            "ContactCreated": ContactProfile, # Map to ContactProfile Pydantic model
            "ContactUpdated": ContactProfile,
            "ContactDeleted": ContactProfile,
        }


        # Mapping of event types to handler methods
        self.event_handlers: Dict[str, callable] = {
            "ZettelCreated": self._handle_zettel_created,
            "ZettelUpdated": self._handle_zettel_updated,
            "ZettelDeleted": self._handle_zettel_deleted,
            "ProjectCreated": self._handle_project_created,
            "ProjectUpdated": self._handle_project_updated,
            "ProjectDeleted": self._handle_project_deleted,
            "AreaCreated": self._handle_area_created,
            "AreaUpdated": self._handle_area_updated,
            "AreaDeleted": self._handle_area_deleted,
            "ResourceCreated": self._handle_resource_created,
            "ResourceUpdated": self._handle_resource_updated,
            "ResourceDeleted": self._handle_resource_deleted,
            "TaskCreated": self._handle_task_created,
            "TaskUpdated": self._handle_task_updated,
            "TaskDeleted": self._handle_task_deleted,
            "GoalCreated": self._handle_goal_created,
            "GoalUpdated": self._handle_goal_updated,
            "GoalDeleted": self._handle_goal_deleted,
            "ReflectionCreated": self._handle_reflection_created,
            "ReflectionUpdated": self._handle_reflection_updated,
            "ReflectionDeleted": self._handle_reflection_deleted,
            "JournalEntryCreated": self._handle_journal_entry_created,
            "JournalEntryUpdated": self._handle_journal_entry_updated,
            "JournalEntryDeleted": self._handle_journal_entry_deleted,
            "EmotionCreated": self._handle_emotion_created,
            "EmotionUpdated": self._handle_emotion_updated,
            "EmotionDeleted": self._handle_emotion_deleted,
            "BeliefCreated": self._handle_belief_created,
            "BeliefUpdated": self._handle_belief_updated,
            "BeliefDeleted": self._handle_belief_deleted,
            "TriggerCreated": self._handle_trigger_created,
            "TriggerUpdated": self._handle_trigger_updated,
            "TriggerDeleted": self._handle_trigger_deleted,
            "SystemInsightFeedbackCreated": self._handle_system_insight_feedback_created,
            "ContactCreated": self._handle_contact_created,
        }

    def _get_db(self) -> Session:
        return self.SessionLocal()

    def _apply_event(self, event: StoredEvent):
        handler = self.event_handlers.get(event.event_type)
        if handler:
            payload = json.loads(event.payload) # Deserialize JSON payload
            with self._get_db() as db:
                handler(db, payload)
                db.commit() # Commit after each event application for simplicity, can be batched

    def replay_events(self):
        """Fetches all events from the event store and applies them to rebuild the read models."""
        with self._get_db() as db: # Creates a new session for the EventProcessor's engine
            # Clear existing read models before replaying
            for table in reversed(Base.metadata.sorted_tables): # Delete in reverse order for foreign key constraints
                db.execute(table.delete())
            db.commit()

        events = self.event_store.get_all_events()
        for event in events:
            self._apply_event(event)

    @staticmethod # Mark as static method
    def _convert_str_to_datetime(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Converts string representations of datetime fields back to datetime objects."""
        for key, value in payload.items():
            if isinstance(value, str):
                try:
                    # Attempt to parse common ISO format (Pydantic's default for datetime)
                    dt = datetime.fromisoformat(value)
                    payload[key] = dt
                except ValueError:
                    pass # Not a datetime string, ignore
        return payload

    # --- Zettel Handlers ---
    def _handle_zettel_created(self, db: Session, payload: Dict[str, Any]):
        print(f"DEBUG(EventProcessor): _handle_zettel_created received payload: {payload}")
        try:
            zettel = ZettelReadModel(**payload) # Pass payload to model constructor
            db.add(zettel)
            print(f"DEBUG(EventProcessor): Added zettel to session: {zettel.id}")
            db.commit()
            print(f"DEBUG(EventProcessor): Committed zettel to database: {zettel.id}")
        except Exception as e:
            logger.error(f"Error creating ZettelReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise # Re-raise to prevent silent failures

    def _handle_zettel_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).update(payload)

    def _handle_zettel_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).delete()

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
        except Exception as e:
            logger.error(f"Error creating ProjectReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_project_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).update(payload)

    def _handle_project_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()
    
    # --- Area Handlers ---
    def _handle_area_created(self, db: Session, payload: Dict[str, Any]):
        try:
            area = AreaReadModel(**payload)
            db.add(area)
        except Exception as e:
            logger.error(f"Error creating AreaReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_area_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).update(payload)

    def _handle_area_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()
    
    # --- Resource Handlers ---
    def _handle_resource_created(self, db: Session, payload: Dict[str, Any]):
        try:
            resource = ResourceReadModel(**payload)
            db.add(resource)
        except Exception as e:
            logger.error(f"Error creating ResourceReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_resource_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).update(payload)

    def _handle_resource_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).delete()

    # --- Task Handlers ---
    def _handle_task_created(self, db: Session, payload: Dict[str, Any]):
        try:
            task = TaskReadModel(**payload)
            db.add(task)
        except Exception as e:
            logger.error(f"Error creating TaskReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_task_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).update(payload)

    def _handle_task_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()
    
    # --- Goal Handlers ---
    def _handle_goal_created(self, db: Session, payload: Dict[str, Any]):
        try:
            goal = GoalReadModel(**payload)
            db.add(goal)
        except Exception as e:
            logger.error(f"Error creating GoalReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_goal_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).update(payload)

    def _handle_goal_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()
    
    # --- Reflection Handlers ---
    def _handle_reflection_created(self, db: Session, payload: Dict[str, Any]):
        try:
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)
        except Exception as e:
            logger.error(f"Error creating ReflectionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_reflection_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).update(payload)

    def _handle_reflection_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()
    
    # --- Journal Entry Handlers ---
    def _handle_journal_entry_created(self, db: Session, payload: Dict[str, Any]):
        try:
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)
        except Exception as e:
            logger.error(f"Error creating JournalEntryReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_journal_entry_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).update(payload)

    def _handle_journal_entry_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
        except Exception as e:
            logger.error(f"Error creating EmotionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_emotion_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).update(payload)

    def _handle_emotion_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()
    
    # --- Belief Handlers ---
    def _handle_belief_created(self, db: Session, payload: Dict[str, Any]):
        try:
            belief = BeliefReadModel(**payload)
            db.add(belief)
        except Exception as e:
            logger.error(f"Error creating BeliefReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_belief_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).update(payload)

    def _handle_belief_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()
    
    # --- Trigger Handlers ---
    def _handle_trigger_created(self, db: Session, payload: Dict[str, Any]):
        try:
            trigger = TriggerReadModel(**payload)
            db.add(trigger)
        except Exception as e:
            logger.error(f"Error creating TriggerReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_trigger_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).update(payload)

    def _handle_trigger_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()

    # --- New Event Handlers ---
    def _handle_system_insight_feedback_created(self, db: Session, payload: Dict[str, Any]):
        """Handles the SystemInsightFeedbackCreated event by updating ArangoDB and SQLite read model."""
        insight_feedback_event = SystemInsightFeedbackEvent(**payload)
        
        # Update ArangoDB
        try:
            self.arangodb_service.update_system_insight(
                insight_feedback_event.id,
                insight_feedback_event.user_id,
                insight_feedback_event.feedback_type,
                insight_feedback_event.comment,
                insight_feedback_event.timestamp
            )
            logger.info(f"ArangoDB: Updated system insight {insight_feedback_event.id}")
        except Exception as e:
            logger.error(f"ArangoDB: Failed to update system insight {insight_feedback_event.id}: {e}", exc_info=True)
            # Depending on requirements, could raise or log and continue

        # Update SQLite Read Model
        try:
            # Find or create the record in the read model
            existing_record = db.query(SystemInsightReadModel).filter(SystemInsightReadModel.id == insight_feedback_event.id).first()
            if existing_record:
                existing_record.user_id = insight_feedback_event.user_id
                existing_record.feedback_type = insight_feedback_event.feedback_type
                existing_record.comment = insight_feedback_event.comment
                existing_record.timestamp = insight_feedback_event.timestamp
                db.add(existing_record)
            else:
                new_record = SystemInsightReadModel(
                    id=insight_feedback_event.id,
                    user_id=insight_feedback_event.user_id,
                    feedback_type=insight_feedback_event.feedback_type,
                    comment=insight_feedback_event.comment,
                    timestamp=insight_feedback_event.timestamp
                )
                db.add(new_record)
            db.commit() # Commit changes to SQLite
            logger.info(f"SQLite: Updated system insight {insight_feedback_event.id}")
        except Exception as e:
            logger.error(f"SQLite: Failed to update system insight {insight_feedback_event.id}: {e}", exc_info=True)
            db.rollback() # Rollback transaction if SQLite update fails
            raise


    def _handle_contact_created(self, db: Session, payload: Dict[str, Any]):
        """Handles the ContactCreated event by updating ArangoDB and SQLite read model."""
        # The payload for ContactCreated is expected to be a ContactProfile object directly
        contact_profile = ContactProfile(**payload) 

        # Update ArangoDB
        try:
            # Assuming ArangoDBService has a method to create/update contacts
            self.arangodb_service.create_or_update_contact(
                contact_profile.id,
                contact_profile.user_id,
                contact_profile.name,
                contact_profile.email,
                contact_profile.phone,
                contact_profile.created_at,
                contact_profile.updated_at
            )
            logger.info(f"ArangoDB: Created/Updated contact {contact_profile.id}")
        except Exception as e:
            logger.error(f"ArangoDB: Failed to create/update contact {contact_profile.id}: {e}", exc_info=True)
            # Depending on requirements, could raise or log and continue

        # Update SQLite Read Model
        try:
            # Find or create the record in the read model
            existing_record = db.query(ContactProfileReadModel).filter(ContactProfileReadModel.id == contact_profile.id).first()
            if existing_record:
                existing_record.user_id = contact_profile.user_id
                existing_record.name = contact_profile.name
                existing_record.email = contact_profile.email
                existing_record.phone = contact_profile.phone
                existing_record.created_at = contact_profile.created_at
                existing_record.updated_at = contact_profile.updated_at
                db.add(existing_record)
            else:
                new_record = ContactProfileReadModel(
                    id=contact_profile.id,
                    user_id=contact_profile.user_id,
                    name=contact_profile.name,
                    email=contact_profile.email,
                    phone=contact_profile.phone,
                    created_at=contact_profile.created_at,
                    updated_at=contact_profile.updated_at
                )
                db.add(new_record)
            db.commit() # Commit changes to SQLite
            logger.info(f"SQLite: Created/Updated contact {contact_profile.id}")
        except Exception as e:
            logger.error(f"SQLite: Failed to create/update contact {contact_profile.id}: {e}", exc_info=True)
            db.rollback() # Rollback transaction if SQLite update fails
            raise


    # --- Query Methods ---
    def get_read_model(self, model_type: Type[Base], item_id: str) -> Optional[Dict[str, Any]]:
        with self._get_db() as db:
            item = db.query(model_type).filter(model_type.id == item_id).first()
            if item:
                return item.__dict__
            return None

    def get_all_read_models(self, model_type: Type[Base]) -> List[Dict[str, Any]]:
        with self._get_db() as db:
            items = db.query(model_type).all()
            return [item.__dict__ for item in items]

    def _apply_event(self, event: StoredEvent):
        handler = self.event_handlers.get(event.event_type)
        if handler:
            payload = json.loads(event.payload) # Deserialize JSON payload
            with self._get_db() as db:
                handler(db, payload)
                db.commit() # Commit after each event application for simplicity, can be batched

    def replay_events(self):
        """Fetches all events from the event store and applies them to rebuild the read models."""
        with self._get_db() as db: # Creates a new session for the EventProcessor's engine
            # Clear existing read models before replaying
            for table in reversed(Base.metadata.sorted_tables): # Delete in reverse order for foreign key constraints
                db.execute(table.delete())
            db.commit()

        events = self.event_store.get_all_events()
        for event in events:
            self._apply_event(event)

    @staticmethod # Mark as static method
    def _convert_str_to_datetime(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Converts string representations of datetime fields back to datetime objects."""
        for key, value in payload.items():
            if isinstance(value, str):
                try:
                    # Attempt to parse common ISO format (Pydantic's default for datetime)
                    dt = datetime.fromisoformat(value)
                    payload[key] = dt
                except ValueError:
                    pass # Not a datetime string, ignore
        return payload

    # --- Zettel Handlers ---
    def _handle_zettel_created(self, db: Session, payload: Dict[str, Any]):
        print(f"DEBUG(EventProcessor): _handle_zettel_created received payload: {payload}")
        try:
            zettel = ZettelReadModel(**payload) # Pass payload to model constructor
            db.add(zettel)
            print(f"DEBUG(EventProcessor): Added zettel to session: {zettel.id}")
            db.commit()
            print(f"DEBUG(EventProcessor): Committed zettel to database: {zettel.id}")
        except Exception as e:
            logger.error(f"Error creating ZettelReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise # Re-raise to prevent silent failures

    def _handle_zettel_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).update(payload)

    def _handle_zettel_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).delete()

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
        except Exception as e:
            logger.error(f"Error creating ProjectReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_project_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).update(payload)

    def _handle_project_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()
    
    # --- Area Handlers ---
    def _handle_area_created(self, db: Session, payload: Dict[str, Any]):
        try:
            area = AreaReadModel(**payload)
            db.add(area)
        except Exception as e:
            logger.error(f"Error creating AreaReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_area_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).update(payload)

    def _handle_area_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()
    
    # --- Resource Handlers ---
    def _handle_resource_created(self, db: Session, payload: Dict[str, Any]):
        try:
            resource = ResourceReadModel(**payload)
            db.add(resource)
        except Exception as e:
            logger.error(f"Error creating ResourceReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_resource_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).update(payload)

    def _handle_resource_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).delete()

    # --- Task Handlers ---
    def _handle_task_created(self, db: Session, payload: Dict[str, Any]):
        try:
            task = TaskReadModel(**payload)
            db.add(task)
        except Exception as e:
            logger.error(f"Error creating TaskReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_task_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).update(payload)

    def _handle_task_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()
    
    # --- Goal Handlers ---
    def _handle_goal_created(self, db: Session, payload: Dict[str, Any]):
        try:
            goal = GoalReadModel(**payload)
            db.add(goal)
        except Exception as e:
            logger.error(f"Error creating GoalReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_goal_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).update(payload)

    def _handle_goal_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()
    
    # --- Reflection Handlers ---
    def _handle_reflection_created(self, db: Session, payload: Dict[str, Any]):
        try:
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)
        except Exception as e:
            logger.error(f"Error creating ReflectionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_reflection_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).update(payload)

    def _handle_reflection_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()
    
    # --- Journal Entry Handlers ---
    def _handle_journal_entry_created(self, db: Session, payload: Dict[str, Any]):
        try:
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)
        except Exception as e:
            logger.error(f"Error creating JournalEntryReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_journal_entry_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).update(payload)

    def _handle_journal_entry_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
        except Exception as e:
            logger.error(f"Error creating EmotionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_emotion_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).update(payload)

    def _handle_emotion_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()
    
    # --- Belief Handlers ---
    def _handle_belief_created(self, db: Session, payload: Dict[str, Any]):
        try:
            belief = BeliefReadModel(**payload)
            db.add(belief)
        except Exception as e:
            logger.error(f"Error creating BeliefReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_belief_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).update(payload)

    def _handle_belief_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()
    
    # --- Trigger Handlers ---
    def _handle_trigger_created(self, db: Session, payload: Dict[str, Any]):
        try:
            trigger = TriggerReadModel(**payload)
            db.add(trigger)
        except Exception as e:
            logger.error(f"Error creating TriggerReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_trigger_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).update(payload)

    def _handle_trigger_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()

    # --- New Event Handlers ---
    def _handle_system_insight_feedback_created(self, db: Session, payload: Dict[str, Any]):
        """Handles the SystemInsightFeedbackCreated event by updating ArangoDB and SQLite read model."""
        insight_feedback_event = SystemInsightFeedbackEvent(**payload)
        
        # Update ArangoDB
        try:
            self.arangodb_service.update_system_insight(
                insight_feedback_event.id,
                insight_feedback_event.user_id,
                insight_feedback_event.feedback_type,
                insight_feedback_event.comment,
                insight_feedback_event.timestamp
            )
            logger.info(f"ArangoDB: Updated system insight {insight_feedback_event.id}")
        except Exception as e:
            logger.error(f"ArangoDB: Failed to update system insight {insight_feedback_event.id}: {e}", exc_info=True)
            # Depending on requirements, could raise or log and continue

        # Update SQLite Read Model
        try:
            # Find or create the record in the read model
            existing_record = db.query(SystemInsightReadModel).filter(SystemInsightReadModel.id == insight_feedback_event.id).first()
            if existing_record:
                existing_record.user_id = insight_feedback_event.user_id
                existing_record.feedback_type = insight_feedback_event.feedback_type
                existing_record.comment = insight_feedback_event.comment
                existing_record.timestamp = insight_feedback_event.timestamp
                db.add(existing_record)
            else:
                new_record = SystemInsightReadModel(
                    id=insight_feedback_event.id,
                    user_id=insight_feedback_event.user_id,
                    feedback_type=insight_feedback_event.feedback_type,
                    comment=insight_feedback_event.comment,
                    timestamp=insight_feedback_event.timestamp
                )
                db.add(new_record)
            db.commit() # Commit changes to SQLite
            logger.info(f"SQLite: Updated system insight {insight_feedback_event.id}")
        except Exception as e:
            logger.error(f"SQLite: Failed to update system insight {insight_feedback_event.id}: {e}", exc_info=True)
            db.rollback() # Rollback transaction if SQLite update fails
            raise


    def _handle_contact_created(self, db: Session, payload: Dict[str, Any]):
        """Handles the ContactCreated event by updating ArangoDB and SQLite read model."""
        # The payload for ContactCreated is expected to be a ContactProfile object directly
        contact_profile = ContactProfile(**payload) 

        # Update ArangoDB
        try:
            # Assuming ArangoDBService has a method to create/update contacts
            self.arangodb_service.create_or_update_contact(
                contact_profile.id,
                contact_profile.user_id,
                contact_profile.name,
                contact_profile.email,
                contact_profile.phone,
                contact_profile.created_at,
                contact_profile.updated_at
            )
            logger.info(f"ArangoDB: Created/Updated contact {contact_profile.id}")
        except Exception as e:
            logger.error(f"ArangoDB: Failed to create/update contact {contact_profile.id}: {e}", exc_info=True)
            # Depending on requirements, could raise or log and continue

        # Update SQLite Read Model
        try:
            # Find or create the record in the read model
            existing_record = db.query(ContactProfileReadModel).filter(ContactProfileReadModel.id == contact_profile.id).first()
            if existing_record:
                existing_record.user_id = contact_profile.user_id
                existing_record.name = contact_profile.name
                existing_record.email = contact_profile.email
                existing_record.phone = contact_profile.phone
                existing_record.created_at = contact_profile.created_at
                existing_record.updated_at = contact_profile.updated_at
                db.add(existing_record)
            else:
                new_record = ContactProfileReadModel(
                    id=contact_profile.id,
                    user_id=contact_profile.user_id,
                    name=contact_profile.name,
                    email=contact_profile.email,
                    phone=contact_profile.phone,
                    created_at=contact_profile.created_at,
                    updated_at=contact_profile.updated_at
                )
                db.add(new_record)
            db.commit() # Commit changes to SQLite
            logger.info(f"SQLite: Created/Updated contact {contact_profile.id}")
        except Exception as e:
            logger.error(f"SQLite: Failed to create/update contact {contact_profile.id}: {e}", exc_info=True)
            db.rollback() # Rollback transaction if SQLite update fails
            raise


    # --- Query Methods ---
    def get_read_model(self, model_type: Type[Base], item_id: str) -> Optional[Dict[str, Any]]:
        with self._get_db() as db:
            item = db.query(model_type).filter(model_type.id == item_id).first()
            if item:
                return item.__dict__
            return None

    def get_all_read_models(self, model_type: Type[Base]) -> List[Dict[str, Any]]:
        with self._get_db() as db:
            items = db.query(model_type).all()
            return [item.__dict__ for item in items]

    def _apply_event(self, event: StoredEvent):
        handler = self.event_handlers.get(event.event_type)
        if handler:
            payload = json.loads(event.payload) # Deserialize JSON payload
            with self._get_db() as db:
                handler(db, payload)
                db.commit() # Commit after each event application for simplicity, can be batched

    def replay_events(self):
        """Fetches all events from the event store and applies them to rebuild the read models."""
        with self._get_db() as db: # Creates a new session for the EventProcessor's engine
            # Clear existing read models before replaying
            for table in reversed(Base.metadata.sorted_tables): # Delete in reverse order for foreign key constraints
                db.execute(table.delete())
            db.commit()

        events = self.event_store.get_all_events()
        for event in events:
            self._apply_event(event)

    @staticmethod # Mark as static method
    def _convert_str_to_datetime(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Converts string representations of datetime fields back to datetime objects."""
        for key, value in payload.items():
            if isinstance(value, str):
                try:
                    # Attempt to parse common ISO format (Pydantic's default for datetime)
                    dt = datetime.fromisoformat(value)
                    payload[key] = dt
                except ValueError:
                    pass # Not a datetime string, ignore
        return payload

    # --- Zettel Handlers ---
    def _handle_zettel_created(self, db: Session, payload: Dict[str, Any]):
        print(f"DEBUG(EventProcessor): _handle_zettel_created received payload: {payload}")
        try:
            zettel = ZettelReadModel(**payload) # Pass payload to model constructor
            db.add(zettel)
            print(f"DEBUG(EventProcessor): Added zettel to session: {zettel.id}")
            db.commit()
            print(f"DEBUG(EventProcessor): Committed zettel to database: {zettel.id}")
        except Exception as e:
            logger.error(f"Error creating ZettelReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise # Re-raise to prevent silent failures

    def _handle_zettel_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).update(payload)

    def _handle_zettel_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).delete()

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
        except Exception as e:
            logger.error(f"Error creating ProjectReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_project_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).update(payload)

    def _handle_project_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()
    
    # --- Area Handlers ---
    def _handle_area_created(self, db: Session, payload: Dict[str, Any]):
        try:
            area = AreaReadModel(**payload)
            db.add(area)
        except Exception as e:
            logger.error(f"Error creating AreaReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_area_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).update(payload)

    def _handle_area_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()
    
    # --- Resource Handlers ---
    def _handle_resource_created(self, db: Session, payload: Dict[str, Any]):
        try:
            resource = ResourceReadModel(**payload)
            db.add(resource)
        except Exception as e:
            logger.error(f"Error creating ResourceReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_resource_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).update(payload)

    def _handle_resource_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).delete()

    # --- Task Handlers ---
    def _handle_task_created(self, db: Session, payload: Dict[str, Any]):
        try:
            task = TaskReadModel(**payload)
            db.add(task)
        except Exception as e:
            logger.error(f"Error creating TaskReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_task_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).update(payload)

    def _handle_task_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()
    
    # --- Goal Handlers ---
    def _handle_goal_created(self, db: Session, payload: Dict[str, Any]):
        try:
            goal = GoalReadModel(**payload)
            db.add(goal)
        except Exception as e:
            logger.error(f"Error creating GoalReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_goal_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).update(payload)

    def _handle_goal_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()
    
    # --- Reflection Handlers ---
    def _handle_reflection_created(self, db: Session, payload: Dict[str, Any]):
        try:
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)
        except Exception as e:
            logger.error(f"Error creating ReflectionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_reflection_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).update(payload)

    def _handle_reflection_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()
    
    # --- Journal Entry Handlers ---
    def _handle_journal_entry_created(self, db: Session, payload: Dict[str, Any]):
        try:
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)
        except Exception as e:
            logger.error(f"Error creating JournalEntryReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_journal_entry_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).update(payload)

    def _handle_journal_entry_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
        except Exception as e:
            logger.error(f"Error creating EmotionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_emotion_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).update(payload)

    def _handle_emotion_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()
    
    # --- Belief Handlers ---
    def _handle_belief_created(self, db: Session, payload: Dict[str, Any]):
        try:
            belief = BeliefReadModel(**payload)
            db.add(belief)
        except Exception as e:
            logger.error(f"Error creating BeliefReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_belief_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).update(payload)

    def _handle_belief_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()
    
    # --- Trigger Handlers ---
    def _handle_trigger_created(self, db: Session, payload: Dict[str, Any]):
        try:
            trigger = TriggerReadModel(**payload)
            db.add(trigger)
        except Exception as e:
            logger.error(f"Error creating TriggerReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_trigger_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).update(payload)

    def _handle_trigger_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()


    # --- Query Methods ---
    def get_read_model(self, model_type: Type[Base], item_id: str) -> Optional[Dict[str, Any]]:
        with self._get_db() as db:
            item = db.query(model_type).filter(model_type.id == item_id).first()
            if item:
                return item.__dict__
            return None

    def get_all_read_models(self, model_type: Type[Base]) -> List[Dict[str, Any]]:
        with self._get_db() as db:
            items = db.query(model_type).all()
            return [item.__dict__ for item in items]
