import json
from datetime import datetime
from typing import Dict, Any, Type, List, Optional
from pydantic import BaseModel

from arango.database import StandardDatabase
from qdrant_client import QdrantClient
from sqlalchemy.orm import sessionmaker, Session
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
from schemas import (
    SystemInsightFeedbackEvent, ContactProfile,
    RelationLoggedEvent, NodeCreatedEvent, EdgeCreatedEvent
)
from services.qdrant_service import QdrantService
from services.arangodb_service import ArangoDBService



logger = logging.getLogger(__name__) # Initialize logger

class EventProcessor:
    """
    Phase 3 EventProcessor:
    - Maintains read models in SQLite (SQLAlchemy) and ArangoDB.
    - OPERATING CONSTRAINT: Handlers are synchronous and may block the async event loop.
    - NO DIRECT DB WRITES outside of this processor are permitted in Phase 3.
    """
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
            "KnowledgeNodeCreated": Zettel, # PHASE4: Dedicated read model in Phase 4 - currently using Zettel as placeholder.
            "KnowledgeNodeUpdated": Zettel, # PHASE4: Dedicated read model in Phase 4 - currently using Zettel as placeholder.
            "KnowledgeNodeDeleted": Zettel, # PHASE4: Dedicated read model in Phase 4 - currently using Zettel as placeholder.
            "RelationLogged": RelationLoggedEvent,
            "NodeCreated": NodeCreatedEvent,
            "EdgeCreated": EdgeCreatedEvent,
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
            "ContactUpdated": self._handle_contact_updated,
            "ContactDeleted": self._handle_contact_deleted,
            "KnowledgeNodeCreated": self._handle_knowledge_node_created, # PHASE4: Stub handler
            "KnowledgeNodeUpdated": self._handle_knowledge_node_updated, # PHASE4: Stub handler
            "KnowledgeNodeDeleted": self._handle_knowledge_node_deleted, # PHASE4: Stub handler
            "RelationLogged": self._handle_relation_logged,
            "NodeCreated": self._handle_node_created,
            "EdgeCreated": self._handle_edge_created,
        }

    def _get_db(self) -> Session:
        return self.SessionLocal()

    def _apply_event(self, event: StoredEvent):
        handler = self.event_handlers.get(event.event_type)
        if handler:
            payload = json.loads(event.payload) # Deserialize JSON payload
            logger.debug(f"Applying event: {event.event_type} with payload: {payload}", extra={"event_id": event.event_id, "event_type": event.event_type})
            db = self.SessionLocal() # Explicitly create session
            try:
                handler(db, payload)
                db.commit() # Commit changes
            except Exception as e:
                db.rollback()
                logger.error(f"Error applying event {event.event_type} (ID: {event.event_id}): {e}", exc_info=True)
                raise
            finally:
                db.close() # Explicitly close session
        else:
            logger.warning(f"[Phase 3][N/A] No handler found for event type: {event.event_type} — ignored", extra={"event_id": event.event_id, "event_type": event.event_type, "phase": 3, "outcome": "ignored"})

    def replay_events(self):
        """Fetches all events from the event store and applies them to rebuild the read models."""
        logger.debug("EventProcessor: Replaying all events to rebuild read models.") # Added logging
        with self._get_db() as db: # Creates a new session for the EventProcessor's engine
            # Clear existing read models before replaying
            for table in reversed(Base.metadata.sorted_tables): # Delete in reverse order for foreign key constraints
                db.execute(table.delete())
            db.commit()
        
        events = self.event_store.get_all_events()
        logger.debug(f"EventProcessor: Found {len(events)} events in the event store.") # Added logging
        for event in events:
            logger.debug(f"EventProcessor: Replaying event: {event.event_type} (ID: {event.event_id})", extra={"event_id": event.event_id, "event_type": event.event_type}) # Added logging
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
    
    # --- KnowledgeNode Stub Handlers (PHASE4: Replace with real persistence) ---
    def _handle_knowledge_node_created(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model persistence
        logger.info(f"[Phase 3][STUB] KnowledgeNodeCreated received for ID {payload.get('id')} — no persistence", extra={"event_id": payload.get('id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_knowledge_node_updated(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model persistence
        logger.info(f"[Phase 3][STUB] KnowledgeNodeUpdated received for ID {payload.get('id')} — no persistence", extra={"event_id": payload.get('id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_knowledge_node_deleted(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model persistence.
        # NOTE: Emission for KnowledgeNodeDeleted is deferred to Phase 4.
        logger.info(f"[Phase 3][STUB] KnowledgeNodeDeleted received for ID {payload.get('id')} — no persistence", extra={"event_id": payload.get('id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_relation_logged(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model persistence
        logger.info(f"[Phase 3][STUB] RelationLogged received for ID {payload.get('contact_id')} — no persistence", extra={"event_id": payload.get('contact_id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_node_created(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real ArangoDB persistence
        logger.info(f"[Phase 3][STUB] NodeCreated received for ID {payload.get('node_id')} — no persistence", extra={"event_id": payload.get('node_id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_edge_created(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real ArangoDB persistence
        logger.info(f"[Phase 3][STUB] EdgeCreated received — no persistence", extra={"handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    # --- Zettel Handlers ---
    def _handle_zettel_created(self, db: Session, payload: Dict[str, Any]):
        try:
            zettel = ZettelReadModel(**payload) # Pass payload to model constructor
            db.add(zettel)
            logger.info(f"[Phase 3][REAL] ZettelCreated - Created ZettelReadModel for ID {zettel.id} — processed", extra={"event_id": zettel.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ZettelCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise # Re-raise to prevent silent failures

    def _handle_zettel_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] ZettelUpdated - Updated ZettelReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ZettelUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_zettel_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] ZettelDeleted - Deleted ZettelReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ZettelDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
            logger.info(f"[Phase 3][REAL] ProjectCreated - Created ProjectReadModel for ID {project.id} — processed", extra={"event_id": project.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ProjectCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_project_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] ProjectUpdated - Updated ProjectReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ProjectUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_project_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] ProjectDeleted - Deleted ProjectReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ProjectDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Area Handlers ---
    def _handle_area_created(self, db: Session, payload: Dict[str, Any]):
        try:
            area = AreaReadModel(**payload)
            db.add(area)
            logger.info(f"[Phase 3][REAL] AreaCreated - Created AreaReadModel for ID {area.id} — processed", extra={"event_id": area.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] AreaCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_area_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] AreaUpdated - Updated AreaReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] AreaUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_area_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] AreaDeleted - Deleted AreaReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] AreaDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Resource Handlers ---
    def _handle_resource_created(self, db: Session, payload: Dict[str, Any]):
        try:
            resource = ResourceReadModel(**payload)
            db.add(resource)
            logger.info(f"[Phase 3][REAL] ResourceCreated - Created ResourceReadModel for ID {resource.id} — processed", extra={"event_id": resource.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ResourceCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_resource_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] ResourceUpdated - Updated ResourceReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ResourceUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_resource_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] ResourceDeleted - Deleted ResourceReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ResourceDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    # --- Task Handlers ---
    def _handle_task_created(self, db: Session, payload: Dict[str, Any]):
        try:
            task = TaskReadModel(**payload)
            db.add(task)
            logger.info(f"[Phase 3][REAL] TaskCreated - Created TaskReadModel for ID {task.id} — processed", extra={"event_id": task.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TaskCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_task_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] TaskUpdated - Updated TaskReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TaskUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_task_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] TaskDeleted - Deleted TaskReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TaskDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Goal Handlers ---
    def _handle_goal_created(self, db: Session, payload: Dict[str, Any]):
        try:
            goal = GoalReadModel(**payload)
            db.add(goal)
            logger.info(f"[Phase 3][REAL] GoalCreated - Created GoalReadModel for ID {goal.id} — processed", extra={"event_id": goal.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] GoalCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_goal_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] GoalUpdated - Updated GoalReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] GoalUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_goal_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] GoalDeleted - Deleted GoalReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] GoalDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Reflection Handlers ---
    def _handle_reflection_created(self, db: Session, payload: Dict[str, Any]):
        try:
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)
            logger.info(f"[Phase 3][REAL] ReflectionCreated - Created ReflectionReadModel for ID {reflection.id} — processed", extra={"event_id": reflection.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ReflectionCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_reflection_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] ReflectionUpdated - Updated ReflectionReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ReflectionUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_reflection_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] ReflectionDeleted - Deleted ReflectionReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ReflectionDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Journal Entry Handlers ---
    def _handle_journal_entry_created(self, db: Session, payload: Dict[str, Any]):
        try:
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)
            logger.info(f"[Phase 3][REAL] JournalEntryCreated - Created JournalEntryReadModel for ID {journal_entry.id} — processed", extra={"event_id": journal_entry.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] JournalEntryCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_journal_entry_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] JournalEntryUpdated - Updated JournalEntryReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] JournalEntryUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_journal_entry_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] JournalEntryDeleted - Deleted JournalEntryReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] JournalEntryDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
            logger.info(f"[Phase 3][REAL] EmotionCreated - Created EmotionReadModel for ID {emotion.id} — processed", extra={"event_id": emotion.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] EmotionCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_emotion_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] EmotionUpdated - Updated EmotionReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] EmotionUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_emotion_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] EmotionDeleted - Deleted EmotionReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] EmotionDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Belief Handlers ---
    def _handle_belief_created(self, db: Session, payload: Dict[str, Any]):
        try:
            belief = BeliefReadModel(**payload)
            db.add(belief)
            logger.info(f"[Phase 3][REAL] BeliefCreated - Created BeliefReadModel for ID {belief.id} — processed", extra={"event_id": belief.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] BeliefCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_belief_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] BeliefUpdated - Updated BeliefReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] BeliefUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_belief_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] BeliefDeleted - Deleted BeliefReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] BeliefDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise
    
    # --- Trigger Handlers ---
    def _handle_trigger_created(self, db: Session, payload: Dict[str, Any]):
        try:
            trigger = TriggerReadModel(**payload)
            db.add(trigger)
            logger.info(f"[Phase 3][REAL] TriggerCreated - Created TriggerReadModel for ID {trigger.id} — processed", extra={"event_id": trigger.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TriggerCreated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_trigger_updated(self, db: Session, payload: Dict[str, Any]):
        try:
            payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
            db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).update(payload)
            logger.info(f"[Phase 3][REAL] TriggerUpdated - Updated TriggerReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TriggerUpdated error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

    def _handle_trigger_deleted(self, db: Session, payload: Dict[str, Any]):
        try:
            db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()
            logger.info(f"[Phase 3][REAL] TriggerDeleted - Deleted TriggerReadModel for ID {payload.get('id')} — processed", extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] TriggerDeleted error for ID {payload.get('id')} — error: {e}", exc_info=True, extra={"event_id": payload.get('id'), "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            raise

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
            logger.info(f"[Phase 3][REAL] SystemInsightFeedbackCreated - Updated system insight {insight_feedback_event.id} in ArangoDB — processed", extra={"event_id": insight_feedback_event.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] SystemInsightFeedbackCreated error (ArangoDB) for ID {insight_feedback_event.id} — error: {e}", exc_info=True, extra={"event_id": insight_feedback_event.id, "handler_mode": "REAL", "phase": 3, "outcome": "error"})
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
            logger.info(f"[Phase 3][REAL] SystemInsightFeedbackCreated - Updated system insight {insight_feedback_event.id} in SQLite — processed", extra={"event_id": insight_feedback_event.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] SystemInsightFeedbackCreated error (SQLite) for ID {insight_feedback_event.id} — error: {e}", exc_info=True, extra={"event_id": insight_feedback_event.id, "handler_mode": "REAL", "phase": 3, "outcome": "error"})
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
            logger.info(f"[Phase 3][REAL] ContactCreated - Created/Updated contact {contact_profile.id} in ArangoDB — processed", extra={"event_id": contact_profile.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ContactCreated error (ArangoDB) for ID {contact_profile.id} — error: {e}", exc_info=True, extra={"event_id": contact_profile.id, "handler_mode": "REAL", "phase": 3, "outcome": "error"})
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
            logger.info(f"[Phase 3][REAL] ContactCreated - Created/Updated contact {contact_profile.id} in SQLite — processed", extra={"event_id": contact_profile.id, "handler_mode": "REAL", "phase": 3, "outcome": "processed"})
        except Exception as e:
            logger.error(f"[Phase 3][REAL] ContactCreated error (SQLite) for ID {contact_profile.id} — error: {e}", exc_info=True, extra={"event_id": contact_profile.id, "handler_mode": "REAL", "phase": 3, "outcome": "error"})
            db.rollback() # Rollback transaction if SQLite update fails
            raise

    def _handle_contact_updated(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model update
        logger.info(f"[Phase 3][STUB] ContactUpdated received for ID {payload.get('id')} — no persistence", extra={"event_id": payload.get('id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})

    def _handle_contact_deleted(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Read models implemented in Phase 4 - Replace stub with real read model deletion
        logger.info(f"[Phase 3][STUB] ContactDeleted received for ID {payload.get('id')} — no persistence", extra={"event_id": payload.get('id'), "handler_mode": "STUB", "phase": 3, "outcome": "processed"})


    # --- Query Methods ---
    def get_read_model(self, model_type: Type[Base], item_id: str) -> Optional[Dict[str, Any]]:
        logger.debug(f"Attempting to retrieve {model_type.__name__} with ID: {item_id}")
        db = self.SessionLocal() # Explicitly create session
        try:
            item = db.query(model_type).filter(model_type.id == item_id).first()
            logger.debug(f"Retrieved item: {item.id if item else 'None'}")
            if item:
                return item.__dict__
            return None
        finally:
            db.close() # Explicitly close session

    def get_all_read_models(self, model_type: Type[Base]) -> List[Dict[str, Any]]:
        with self._get_db() as db:
            items = db.query(model_type).all()
            return [item.__dict__ for item in items]