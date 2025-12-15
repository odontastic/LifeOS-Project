import json
from typing import List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database import Base, StoredEvent

class EventStore:
    def __init__(self, engine): # Requires an engine to be passed
        self.engine = engine
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def append_event(self, event_id: str, event_type: str, payload: Dict[str, Any], schema_version: str):
        db = self.SessionLocal()
        try:
            stored_event = StoredEvent(
                event_id=event_id,
                event_type=event_type,
                payload=json.dumps(payload, default=str), # Store as JSON string
                schema_version=schema_version
            )
            db.add(stored_event)
            db.commit()
            db.refresh(stored_event)
            return stored_event
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_all_events(self) -> List[StoredEvent]:
        db = self.SessionLocal()
        try:
            return db.query(StoredEvent).order_by(StoredEvent.timestamp).all()
        finally:
            db.close()