import logging
import json
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .event_store import get_db_event_session, append_event, get_events_by_type, get_all_events
from .schemas import EmotionLoggedEvent, CalmCompassActionEvent, InsightCreatedEvent, ContactUpdatedEvent

logger = logging.getLogger(__name__)

class EmotionContextBus:
    """
    The EmotionContextBus handles the emission and storage of events
    within the LifeOS system, adhering to the Event-First Design principle.
    Events are stored in a SQLite-backed append-only log.
    """
    def __init__(self, db_session_generator=get_db_event_session):
        self.db_session_generator = db_session_generator
        # Map event types to their Pydantic schema for validation
        self.event_schemas = {
            "emotion_logged": EmotionLoggedEvent,
            "calm_compass_action": CalmCompassActionEvent,
            "insight_created": InsightCreatedEvent,
            "contact_updated": ContactUpdatedEvent,
            # Add other event types here as they are defined
        }

    def emit(self, event_type: str, payload: BaseModel, schema_version: str = "1.0"):
        """
        Emits an event by validating its payload against its schema,
        converting it to JSON, and appending it to the SQLite event log.
        """
        if event_type not in self.event_schemas:
            logger.error(f"Attempted to emit unregistered event type: {event_type}")
            return

        # Ensure payload conforms to the expected schema
        try:
            # Re-instantiate the payload to ensure validation is run
            # and to get a clean dictionary representation
            validated_payload = self.event_schemas[event_type](**payload.model_dump())
            payload_json = validated_payload.model_dump_json()
        except Exception as e:
            logger.error(f"Payload validation failed for event '{event_type}': {e}")
            return

        with next(self.db_session_generator()) as db:
            try:
                append_event(db, event_type, json.loads(payload_json), schema_version)
                event_id = getattr(payload, 'id', 'N/A')
                logger.info(f"Event '{event_type}' emitted and stored with ID: {event_id}")
            except Exception as e:
                logger.error(f"Failed to store event '{event_type}' in event log: {e}")
    
    # Placeholder for a method to retrieve events for "subscribers"
    def get_events(self, event_type: Optional[str] = None, limit: int = 100, offset: int = 0):
        with next(self.db_session_generator()) as db:
            if event_type:
                return [json.loads(event.payload) for event in get_events_by_type(db, event_type, limit, offset)]
            return [json.loads(event.payload) for event in get_all_events(db, limit, offset)]

# Instantiate the bus (global or per-request depending on FastAPI context)
# For simplicity, a global instance for now.
event_bus = EmotionContextBus()
