import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, AsyncGenerator # Added AsyncGenerator

from arango.database import StandardDatabase
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import (
    Base, StoredEvent,
    ZettelReadModel, ProjectReadModel, AreaReadModel, ResourceReadModel,
    TaskReadModel, GoalReadModel, ReflectionReadModel, JournalEntryReadModel,
    EmotionReadModel, BeliefReadModel, TriggerReadModel
)
from event_sourcing.event_store import EventStore
from services.qdrant_service import QdrantService # New import
from services.arangodb_service import ArangoDBService # New import
from models.area import Area
from models.belief import Belief
from models.emotion import Emotion
from models.goal import Goal
from models.journal_entry import JournalEntry
from models.project import Project
from models.reflection import Reflection
from models.resource import Resource
from models.task import Task
from models.trigger import Trigger
from models.zettel import Zettel


# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EventProcessor:
    def __init__(self, event_store: EventStore, engine, qdrant_client: QdrantClient, arangodb_db: StandardDatabase):
        self.event_store = event_store
        self.engine = engine
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.qdrant_client = qdrant_client
        self.arangodb_db = arangodb_db
        self.qdrant_service = QdrantService(qdrant_client) # New service instantiation
        self.arangodb_service = ArangoDBService(arangodb_db) # New service instantiation

        self.event_handlers: Dict[str, callable] = {
            "ZettelCreated": self._handle_zettel_created_qdrant_and_readmodel,
            "ZettelUpdated": self._handle_zettel_updated_qdrant_and_readmodel,
            "ZettelDeleted": self._handle_zettel_deleted_qdrant_and_readmodel,
            "ProjectCreated": self._handle_project_created_arangodb_and_readmodel,
            "ProjectUpdated": self._handle_project_updated_arangodb_and_readmodel,
            "ProjectDeleted": self._handle_project_deleted_arangodb_and_readmodel,
            "AreaCreated": self._handle_area_created_arangodb_and_readmodel,
            "AreaUpdated": self._handle_area_updated_arangodb_and_readmodel,
            "AreaDeleted": self._handle_area_deleted_arangodb_and_readmodel,
            "ResourceCreated": self._handle_resource_created_qdrant_and_readmodel,
            "ResourceUpdated": self._handle_resource_updated_qdrant_and_readmodel,
            "ResourceDeleted": self._handle_resource_deleted_qdrant_and_readmodel,
            "TaskCreated": self._handle_task_created_arangodb_and_readmodel,
            "TaskUpdated": self._handle_task_updated_arangodb_and_readmodel,
            "TaskDeleted": self._handle_task_deleted_arangodb_and_readmodel,
            "GoalCreated": self._handle_goal_created_arangodb_and_readmodel,
            "GoalUpdated": self._handle_goal_updated_arangodb_and_readmodel,
            "GoalDeleted": self._handle_goal_deleted_arangodb_and_readmodel,
            "ReflectionCreated": self._handle_reflection_created_arangodb_and_readmodel,
            "ReflectionUpdated": self._handle_reflection_updated_arangodb_and_readmodel,
            "ReflectionDeleted": self._handle_reflection_deleted_arangodb_and_readmodel,
            "JournalEntryCreated": self._handle_journal_entry_created_arangodb_and_readmodel,
            "JournalEntryUpdated": self._handle_journal_entry_updated_arangodb_and_readmodel,
            "JournalEntryDeleted": self._handle_journal_entry_deleted_arangodb_and_readmodel,
            "EmotionCreated": self._handle_emotion_created_arangodb_and_readmodel,
            "EmotionUpdated": self._handle_emotion_updated_arangodb_and_readmodel,
            "EmotionDeleted": self._handle_emotion_deleted_arangodb_and_readmodel,
            "BeliefCreated": self._handle_belief_created_arangodb_and_readmodel,
            "BeliefUpdated": self._handle_belief_updated_arangodb_and_readmodel,
            "BeliefDeleted": self._handle_belief_deleted_arangodb_and_readmodel,
            "TriggerCreated": self._handle_trigger_created_arangodb_and_readmodel,
            "TriggerUpdated": self._handle_trigger_updated_arangodb_and_readmodel,
            "TriggerDeleted": self._handle_trigger_deleted_arangodb_and_readmodel,
        }

    async def _get_db(self) -> AsyncGenerator[Session, None]: # Converted to async generator
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def _apply_event(self, event: StoredEvent):
        handler = self.event_handlers.get(event.event_type)
        if handler:
            payload = json.loads(event.payload) # Deserialize JSON payload
            async for db in self._get_db(): # Use async for to get db session
                await handler(db, payload)
                await db.commit() # Await commit for async session

    async def replay_events(self):
        """Fetches all events from the event store and applies them to rebuild the read models."""
        async for db in self._get_db(): # Use async for to get db session
            # Clear existing read models before replaying
            for table in reversed(Base.metadata.sorted_tables): # Delete in reverse order for foreign key constraints
                await db.execute(table.delete()) # Await execute
            await db.commit() # Await commit

        events = self.event_store.get_all_events()
        for event in events:
            await self._apply_event(event) # Await _apply_event


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
    # --- Qdrant & ReadModel Combined Handlers (for Zettel) ---
    async def _handle_zettel_created_qdrant_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            zettel = ZettelReadModel(**payload)
            db.add(zettel)

            # Update Qdrant
            content = payload.get("body", "") # Assuming 'body' for Zettel content
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_notes")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_notes",
                    doc_id=doc_id,
                    content=content, # This will be embedded by QdrantService
                    metadata=payload # Pass entire payload as metadata
                )
        except Exception as e:
            logger.error(f"Error processing ZettelCreated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_zettel_updated_qdrant_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ZettelReadModel).filter(ZettelReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update Qdrant
            content = payload.get("body", "")
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_notes")
                await self.qdrant_service.upsert_vector( # Upsert handles update if doc_id exists
                    collection_name="lifeos_notes",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ZettelUpdated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

        except Exception as e:
            logger.error(f"Error processing ZettelDeleted event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

    # --- Qdrant & ReadModel Combined Handlers (for Resource) ---


            # Update Qdrant
            content = payload.get("body", "") # Assuming 'body' for Resource content
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_resources")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ResourceCreated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_resource_updated_qdrant_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ResourceReadModel).filter(ResourceReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update Qdrant
            content = payload.get("body", "")
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_resources")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ResourceUpdated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise
    # -- ArangoDB & ReadModel Combined Handlers (for Project) --
    async def _handle_project_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            project = ProjectReadModel(**payload)
            db.add(project)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("projects")
                await self.arangodb_service.upsert_vertex(
                    collection_name="projects",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_project_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ProjectReadModel).filter(ProjectReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("projects")
                await self.arangodb_service.upsert_vertex(
                    collection_name="projects",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise


            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="projects",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Area) --
    async def _handle_area_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            area = AreaReadModel(**payload)
            db.add(area)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("areas")
                await self.arangodb_service.upsert_vertex(
                    collection_name="areas",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_area_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(AreaReadModel).filter(AreaReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("areas")
                await self.arangodb_service.upsert_vertex(
                    collection_name="areas",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise



            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="areas",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Task) --
    async def _handle_task_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            task = TaskReadModel(**payload)
            db.add(task)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("tasks")
                await self.arangodb_service.upsert_vertex(
                    collection_name="tasks",
                    vertex_data=payload,
                    key=doc_id
                )
            # Handle potential edge for project relationship
            project_id = payload.get("project")
            if project_id and doc_id:
                await self.arangodb_service.create_collection_if_not_exists("contains", edge=True)
                await self.arangodb_service.upsert_edge(
                    collection_name="contains",
                    from_vertex_key=f"projects/{project_id}",
                    to_vertex_key=f"tasks/{doc_id}",
                    edge_data={"relation": "contains_task"}
                )
        except Exception as e:
            logger.error(f"Error processing TaskCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_task_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(TaskReadModel).filter(TaskReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("tasks")
                await self.arangodb_service.upsert_vertex(
                    collection_name="tasks",
                    vertex_data=payload,
                    key=doc_id
                )
            # Handle potential edge for project relationship
            project_id = payload.get("project")
            if project_id and doc_id:
                await self.arangodb_service.create_collection_if_not_exists("contains", edge=True)
                await self.arangodb_service.upsert_edge(
                    collection_name="contains",
                    from_vertex_key=f"projects/{project_id}",
                    to_vertex_key=f"tasks/{doc_id}",
                    edge_data={"relation": "contains_task"}
                )
            else: # If project is removed, ensure edge is deleted (this is a simple check, more robust needed for all edge cases)
                # This part is complex. For now, we'll focus on creation/update.
                # A full solution would query existing edges and delete if no longer present.
                pass
        except Exception as e:
            logger.error(f"Error processing TaskUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise


            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="tasks",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing TaskDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Goal) --
    async def _handle_goal_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            goal = GoalReadModel(**payload)
            db.add(goal)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("goals")
                await self.arangodb_service.upsert_vertex(
                    collection_name="goals",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_goal_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(GoalReadModel).filter(GoalReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("goals")
                await self.arangodb_service.upsert_vertex(
                    collection_name="goals",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise



            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="goals",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Reflection) --
    async def _handle_reflection_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("reflections")
                await self.arangodb_service.upsert_vertex(
                    collection_name="reflections",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_reflection_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("reflections")
                await self.arangodb_service.upsert_vertex(
                    collection_name="reflections",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="reflections",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Journal Entry) --
    async def _handle_journal_entry_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("journal_entries")
                await self.arangodb_service.upsert_vertex(
                    collection_name="journal_entries",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise



            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("journal_entries")
                await self.arangodb_service.upsert_vertex(
                    collection_name="journal_entries",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise


            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="journal_entries",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Emotion) --
    async def _handle_emotion_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            emotion = EmotionReadModel(**payload)
            db.add(emotion)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("emotions")
                await self.arangodb_service.upsert_vertex(
                    collection_name="emotions",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing EmotionCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("emotions")
                await self.arangodb_service.upsert_vertex(
                    collection_name="emotions",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing EmotionUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_emotion_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any


            # Delete from Qdrant
            doc_id = payload.get("id")
            if doc_id:
                await self.qdrant_service.delete_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ResourceDeleted event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise


    # --- Qdrant & ReadModel Combined Handlers (for Zettel) ---
    async def _handle_zettel_created_qdrant_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            zettel = ZettelReadModel(**payload)
            db.add(zettel)

            # Update Qdrant
            content = payload.get("body", "") # Assuming 'body' for Zettel content
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_notes")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_notes",
                    doc_id=doc_id,
                    content=content, # This will be embedded by QdrantService
                    metadata=payload # Pass entire payload as metadata
                )
        except Exception as e:
            logger.error(f"Error processing ZettelCreated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise



            # Update Qdrant
            content = payload.get("body", "")
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_notes")
                await self.qdrant_service.upsert_vector( # Upsert handles update if doc_id exists
                    collection_name="lifeos_notes",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ZettelUpdated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

            # Delete from Qdrant
            doc_id = payload.get("id")
            if doc_id:
                await self.qdrant_service.delete_vector(
                    collection_name="lifeos_notes",
                    doc_id=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ZettelDeleted event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise

    # --- Qdrant & ReadModel Combined Handlers (for Resource) ---
    async def _handle_resource_created_qdrant_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            resource = ResourceReadModel(**payload)
            db.add(resource)

            # Update Qdrant
            content = payload.get("body", "") # Assuming 'body' for Resource content
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_resources")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ResourceCreated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise



            # Update Qdrant
            content = payload.get("body", "")
            doc_id = payload.get("id")
            if content and doc_id:
                await self.qdrant_service.create_collection_if_not_exists("lifeos_resources")
                await self.qdrant_service.upsert_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id,
                    content=content,
                    metadata=payload
                )
        except Exception as e:
            logger.error(f"Error processing ResourceUpdated event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise


            # Delete from Qdrant
            doc_id = payload.get("id")
            if doc_id:
                await self.qdrant_service.delete_vector(
                    collection_name="lifeos_resources",
                    doc_id=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ResourceDeleted event for Qdrant (payload: {payload}): {e}", exc_info=True)
            raise


    # --- Zettel Handlers ---

    # --- Project Handlers ---
    def _handle_project_created(self, db: Session, payload: Dict[str, Any]):
        try:
            project = ProjectReadModel(**payload)
            db.add(project)
        except Exception as e:
            logger.error(f"Error creating ProjectReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise

    
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
    
    # --- Emotion Handlers ---
    def _handle_emotion_created(self, db: Session, payload: Dict[str, Any]):
        try:
            emotion = EmotionReadModel(**payload)
            db.add(emotion)
        except Exception as e:
            logger.error(f"Error creating EmotionReadModel from payload: {payload}, Error: {e}", exc_info=True)
            raise


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
