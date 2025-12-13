from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import uuid
import json

# --- Database Setup for Event Store ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./lifeos_events.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Event Model ---
class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    payload = Column(Text, nullable=False) # Store payload as JSON string
    schema_version = Column(String, nullable=False)

# Create database tables
Base.metadata.create_all(bind=engine)

# --- Event Store Operations ---
def get_db_event_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def append_event(db_session, event_type: str, payload: dict, schema_version: str):
    new_event = Event(
        event_type=event_type,
        payload=json.dumps(payload),
        schema_version=schema_version
    )
    db_session.add(new_event)
    db_session.commit()
    db_session.refresh(new_event)
    return new_event

def get_events_by_type(db_session, event_type: str, limit: int = 100, offset: int = 0):
    return db_session.query(Event).filter(Event.event_type == event_type).order_by(Event.timestamp).offset(offset).limit(limit).all()

def get_all_events(db_session, limit: int = 100, offset: int = 0):
    return db_session.query(Event).order_by(Event.timestamp).offset(offset).limit(limit).all()
