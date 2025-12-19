import os
import json
from datetime import datetime
from typing import Dict, Any, Type, List, Optional, AsyncGenerator
from pydantic import BaseModel

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
from services.qdrant_service import QdrantService
from services.arangodb_service import ArangoDBService



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
            "KnowledgeNodeCreated": Zettel, # PHASE4: Will have a read model in Phase 4 - used Zettel as placeholder.
            "KnowledgeNodeUpdated": Zettel, # PHASE4: Will have a read model in Phase 4 - used Zettel as placeholder.
            "KnowledgeNodeDeleted": Zettel, # PHASE4: Will have a read model in Phase 4 - used Zettel as placeholder.
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
        # PHASE4: Replace stub with real read model persistence
        logger.info(f"Phase3 stub: KnowledgeNodeCreated received for ID {payload.get('id')}; no read model persisted", extra={"event_id": payload.get('id')})

    def _handle_knowledge_node_updated(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Replace stub with real read model persistence
        logger.info(f"Phase3 stub: KnowledgeNodeUpdated received for ID {payload.get('id')}; no read model persisted", extra={"event_id": payload.get('id')})

    def _handle_knowledge_node_deleted(self, db: Session, payload: Dict[str, Any]):
        # PHASE4: Replace stub with real read model persistence
        logger.info(f"Phase3 stub: KnowledgeNodeDeleted received for ID {payload.get('id')}; no read model persisted", extra={"event_id": payload.get('id')})

    # --- Zettel Handlers ---
    def _handle_zettel_created(self, db: Session, payload: Dict[str, Any]):
        try:
            zettel = ZettelReadModel(**payload) # Pass payload to model constructor
            db.add(zettel)
            logger.info(f"REAL persist: ZettelCreated - Created ZettelReadModel for ID {zettel.id}", extra={"event_id": zettel.id})
        except Exception as e:
            logger.error(f"Error creating ZettelReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise # Re-raise to prevent silent failures

    def _handle_zettel_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: ZettelUpdated - Updated ZettelReadModel for ID {payload.get('id')}")


    def _handle_zettel_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ZettelReadModel).filter(ZettelReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: ZettelDeleted - Deleted ZettelReadModel for ID {payload.get('id')}")

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
            logger.info(f"REAL persist: ProjectCreated - Created ProjectReadModel for ID {project.id}", extra={"event_id": project.id})
        except Exception as e:
            logger.error(f"Error creating ProjectReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_project_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: ProjectUpdated - Updated ProjectReadModel for ID {payload.get('id')}")

    def _handle_project_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: ProjectDeleted - Deleted ProjectReadModel for ID {payload.get('id')}")
    
    # --- Area Handlers ---
    def _handle_area_created(self, db: Session, payload: Dict[str, Any]):
        try:
            area = AreaReadModel(**payload)
            db.add(area)
            logger.info(f"REAL persist: AreaCreated - Created AreaReadModel for ID {area.id}", extra={"event_id": area.id})
        except Exception as e:
            logger.error(f"Error creating AreaReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_area_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: AreaUpdated - Updated AreaReadModel for ID {payload.get('id')}")

    def _handle_area_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: AreaDeleted - Deleted AreaReadModel for ID {payload.get('id')}")
    
    # --- Resource Handlers ---
    def _handle_resource_created(self, db: Session, payload: Dict[str, Any]):
        try:
            resource = ResourceReadModel(**payload)
            db.add(resource)
            logger.info(f"REAL persist: ResourceCreated - Created ResourceReadModel for ID {resource.id}", extra={"event_id": resource.id})
        except Exception as e:
            logger.error(f"Error creating ResourceReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_resource_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: ResourceUpdated - Updated ResourceReadModel for ID {payload.get('id')}")

    def _handle_resource_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ResourceReadModel).filter(ResourceReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: ResourceDeleted - Deleted ResourceReadModel for ID {payload.get('id')}")

    # --- Task Handlers ---
    def _handle_task_created(self, db: Session, payload: Dict[str, Any]):
        try:
            task = TaskReadModel(**payload)
            db.add(task)
            logger.info(f"REAL persist: TaskCreated - Created TaskReadModel for ID {task.id}", extra={"event_id": task.id})
        except Exception as e:
            logger.error(f"Error creating TaskReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_task_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: TaskUpdated - Updated TaskReadModel for ID {payload.get('id')}")

    def _handle_task_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: TaskDeleted - Deleted TaskReadModel for ID {payload.get('id')}")
    
    # --- Goal Handlers ---
    def _handle_goal_created(self, db: Session, payload: Dict[str, Any]):
        try:
            goal = GoalReadModel(**payload)
            db.add(goal)
            logger.info(f"REAL persist: GoalCreated - Created GoalReadModel for ID {goal.id}", extra={"event_id": goal.id})
        except Exception as e:
            logger.error(f"Error creating GoalReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_goal_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: GoalUpdated - Updated GoalReadModel for ID {payload.get('id')}")

    def _handle_goal_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: GoalDeleted - Deleted GoalReadModel for ID {payload.get('id')}")
    
    # --- Reflection Handlers ---
    def _handle_reflection_created(self, db: Session, payload: Dict[str, Any]):
        try:
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)
            logger.info(f"REAL persist: ReflectionCreated - Created ReflectionReadModel for ID {reflection.id}", extra={"event_id": reflection.id})
        except Exception as e:
            logger.error(f"Error creating ReflectionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_reflection_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: ReflectionUpdated - Updated ReflectionReadModel for ID {payload.get('id')}")

    def _handle_reflection_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: ReflectionDeleted - Deleted ReflectionReadModel for ID {payload.get('id')}")
    
    # --- Journal Entry Handlers ---
    def _handle_journal_entry_created(self, db: Session, payload: Dict[str, Any]):
        try:
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)
            logger.info(f"REAL persist: JournalEntryCreated - Created JournalEntryReadModel for ID {journal_entry.id}", extra={"event_id": journal_entry.id})
        except Exception as e:
            logger.error(f"Error creating JournalEntryReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_journal_entry_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: JournalEntryUpdated - Updated JournalEntryReadModel for ID {payload.get('id')}")

    def _handle_journal_entry_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: JournalEntryDeleted - Deleted JournalEntryReadModel for ID {payload.get('id')}")
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
            logger.info(f"REAL persist: EmotionCreated - Created EmotionReadModel for ID {emotion.id}", extra={"event_id": emotion.id})
        except Exception as e:
            logger.error(f"Error creating EmotionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_emotion_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: EmotionUpdated - Updated EmotionReadModel for ID {payload.get('id')}")

    def _handle_emotion_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: EmotionDeleted - Deleted EmotionReadModel for ID {payload.get('id')}")
    
    # --- Belief Handlers ---
    def _handle_belief_created(self, db: Session, payload: Dict[str, Any]):
        try:
            belief = BeliefReadModel(**payload)
            db.add(belief)
            logger.info(f"REAL persist: BeliefCreated - Created BeliefReadModel for ID {belief.id}", extra={"event_id": belief.id})
        except Exception as e:
            logger.error(f"Error creating BeliefReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_belief_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: BeliefUpdated - Updated BeliefReadModel for ID {payload.get('id')}")

    def _handle_belief_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: BeliefDeleted - Deleted BeliefReadModel for ID {payload.get('id')}")
    
    # --- Trigger Handlers ---
    def _handle_trigger_created(self, db: Session, payload: Dict[str, Any]):
        try:
            trigger = TriggerReadModel(**payload)
            db.add(trigger)
            logger.info(f"REAL persist: TriggerCreated - Created TriggerReadModel for ID {trigger.id}", extra={"event_id": trigger.id})
        except Exception as e:
            logger.error(f"Error creating TriggerReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    def _handle_trigger_updated(self, db: Session, payload: Dict[str, Any]):
        payload = EventProcessor._convert_str_to_datetime(payload) # Convert datetime strings
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).update(payload)
        logger.info(f"REAL persist: TriggerUpdated - Updated TriggerReadModel for ID {payload.get('id')}")

    def _handle_trigger_deleted(self, db: Session, payload: Dict[str, Any]):
        db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()
        logger.info(f"REAL persist: TriggerDeleted - Deleted TriggerReadModel for ID {payload.get('id')}")

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
            logger.info(f"REAL persist: SystemInsightFeedbackCreated - Updated system insight {insight_feedback_event.id} in SQLite")
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
            logger.info(f"REAL persist: ContactCreated - Created/Updated contact {contact_profile.id} in ArangoDB")
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
            logger.info(f"REAL persist: ContactCreated - Created/Updated contact {contact_profile.id} in SQLite")
        except Exception as e:
            logger.error(f"SQLite: Failed to create/update contact {contact_profile.id}: {e}", exc_info=True)
            db.rollback() # Rollback transaction if SQLite update fails
            raise

    def _handle_contact_updated(self, db: Session, payload: Dict[str, Any]):
        # PHASE3: Stub handler - implement actual read model update in Phase 4
        logger.info(f"Phase3 stub: ContactUpdated received for ID {payload.get('id')}; no read model persisted", extra={"event_id": payload.get('id')})

    def _handle_contact_deleted(self, db: Session, payload: Dict[str, Any]):
        # PHASE3: Stub handler - implement actual read model deletion in Phase 4
        logger.info(f"Phase3 stub: ContactDeleted received for ID {payload.get('id')}; no read model persisted", extra={"event_id": payload.get('id')})


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