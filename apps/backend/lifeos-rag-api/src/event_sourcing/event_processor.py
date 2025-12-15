import os
import json
from datetime import datetime
from typing import Dict, Any, Type, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import logging # Import logging

from event_sourcing.event_store import EventStore
from database import (
    Base, StoredEvent,
    ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
    TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
    EmotionReadModel, BeliefReadModel, TriggerReadModel
)
from models.zettel import Zettel # Import Pydantic models for type checking and conversion
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


# Load environment variables
load_dotenv()
# SQLITE_READ_MODELS_DB_PATH is now managed by the injected engine for tests
# os.makedirs(os.path.dirname(SQLITE_READ_MODELS_DB_PATH), exist_ok=True)

logger = logging.getLogger(__name__) # Initialize logger

class EventProcessor:
    def __init__(self, event_store: EventStore, engine): # Requires an engine to be passed
        self.event_store = event_store
        self.engine = engine
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

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
