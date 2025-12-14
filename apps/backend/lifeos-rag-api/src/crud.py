from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # Use generic UUID for SQLite
from sqlalchemy.types import TypeDecorator, CHAR
import uuid
import json
from datetime import datetime
from typing import List, Optional

# Define a custom UUID type for SQLAlchemy (compatible with SQLite)
class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)

# --- Database Setup for Core Entities ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./lifeos_core.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Models mirroring schemas.py entities ---

class EmotionEntryModel(Base):
    __tablename__ = "emotion_entries"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    primary_emotion = Column(String, nullable=False)
    secondary_emotions = Column(Text) # Stored as JSON string
    valence = Column(Integer, nullable=False)
    arousal = Column(Integer, nullable=False)
    intensity = Column(Integer, nullable=False)
    somatic_markers = Column(Text) # Stored as JSON string
    context_tags = Column(Text) # Stored as JSON string
    notes = Column(Text)
    linked_contact_id = Column(GUID, index=True)
    linked_task_id = Column(GUID, index=True)
    action_prompt = Column(Text)
    processed = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat(),
            "primary_emotion": self.primary_emotion,
            "secondary_emotions": json.loads(self.secondary_emotions) if self.secondary_emotions else None,
            "valence": self.valence,
            "arousal": self.arousal,
            "intensity": self.intensity,
            "somatic_markers": json.loads(self.somatic_markers) if self.somatic_markers else None,
            "context_tags": json.loads(self.context_tags) if self.context_tags else None,
            "notes": self.notes,
            "linked_contact_id": str(self.linked_contact_id) if self.linked_contact_id else None,
            "linked_task_id": str(self.linked_task_id) if self.linked_task_id else None,
            "action_prompt": self.action_prompt,
            "processed": self.processed,
        }

class ContactProfileModel(Base):
    __tablename__ = "contact_profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False)
    importance_level = Column(Integer, nullable=False)
    last_interaction = Column(DateTime)
    open_loops = Column(Text) # Stored as JSON string
    sentiment_summary = Column(Text)
    next_follow_up = Column(DateTime)
    context_history = Column(Text) # Linked EmotionEntry IDs, stored as JSON string

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "relationship_type": self.relationship_type,
            "importance_level": self.importance_level,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
            "open_loops": json.loads(self.open_loops) if self.open_loops else None,
            "sentiment_summary": self.sentiment_summary,
            "next_follow_up": self.next_follow_up.isoformat() if self.next_follow_up else None,
            "context_history": json.loads(self.context_history) if self.context_history else None,
        }

class TaskItemModel(Base):
    __tablename__ = "task_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(GUID, index=True)
    context_tags = Column(Text) # Stored as JSON string
    status = Column(String, nullable=False)  # 'open','in_progress','done'
    priority = Column(Integer, nullable=False)
    due_date = Column(DateTime)
    linked_emotion_ids = Column(Text) # Stored as JSON string
    linked_contact_ids = Column(Text) # Stored as JSON string
    energy_requirement = Column(String)  # 'low','medium','high'

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "project_id": str(self.project_id) if self.project_id else None,
            "context_tags": json.loads(self.context_tags) if self.context_tags else None,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "linked_emotion_ids": json.loads(self.linked_emotion_ids) if self.linked_emotion_ids else None,
            "linked_contact_ids": json.loads(self.linked_contact_ids) if self.linked_contact_ids else None,
            "energy_requirement": self.energy_requirement,
        }

class KnowledgeNodeModel(Base):
    __tablename__ = "knowledge_nodes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text, nullable=False) # Stored as JSON string
    links = Column(Text) # Bidirectional connections, stored as JSON string
    para_category = Column(String, nullable=False)  # project/area/resource/archive
    emotion_links = Column(Text) # Stored as JSON string
    last_reviewed = Column(DateTime)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "tags": json.loads(self.tags) if self.tags else None,
            "links": json.loads(self.links) if self.links else None,
            "para_category": self.para_category,
            "emotion_links": json.loads(self.emotion_links) if self.emotion_links else None,
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
        }

class SystemInsightModel(Base):
    __tablename__ = "system_insights"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    insight_type = Column(String, nullable=False)  # 'pattern','recommendation','summary'
    generated_from = Column(Text, nullable=False) # Source object UUIDs, stored as JSON string
    model_version = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False) # Assuming 0-100 for storage as integer
    message = Column(Text, nullable=False)
    action_recommendations = Column(Text) # Stored as JSON string
    feedback_rating = Column(Integer) # User feedback rating (e.g., 1-5)
    feedback_comment = Column(Text) # User feedback comment
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "insight_type": self.insight_type,
            "generated_from": json.loads(self.generated_from) if self.generated_from else None,
            "model_version": self.model_version,
            "confidence": self.confidence,
            "message": self.message,
            "action_recommendations": json.loads(self.action_recommendations) if self.action_recommendations else None,
            "feedback_rating": self.feedback_rating,
            "feedback_comment": self.feedback_comment,
        }

# Create database tables
Base.metadata.create_all(bind=engine)

# --- Generic CRUD Operations ---

def create_item(db_session, model, schema_item):
    # Convert lists/UUIDs in schema_item to JSON strings for storage
    item_data = schema_item.model_dump()
    for key, value in item_data.items():
        if isinstance(value, (list, uuid.UUID)):
            item_data[key] = json.dumps([str(x) for x in value]) if isinstance(value, list) else str(value)
        elif isinstance(value, datetime):
            item_data[key] = value.isoformat() # Store datetime as ISO string or let SQLAlchemy handle
    
    db_item = model(**item_data)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item.to_dict() # Return as dict

def get_item_by_id(db_session, model, item_id: uuid.UUID):
    item = db_session.query(model).filter(model.id == item_id).first()
    if item:
        return item.to_dict()
    return None

def get_items(db_session, model, skip: int = 0, limit: int = 100):
    return [item.to_dict() for item in db_session.query(model).offset(skip).limit(limit).all()]

def update_item(db_session, model, item_id: uuid.UUID, schema_item):
    db_item = db_session.query(model).filter(model.id == item_id).first()
    if not db_item:
        return None
    
    update_data = schema_item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if isinstance(value, (list, uuid.UUID)):
            setattr(db_item, key, json.dumps([str(x) for x in value]) if isinstance(value, list) else str(value))
        elif isinstance(value, datetime):
            setattr(db_item, key, value.isoformat())
        else:
            setattr(db_item, key, value)
    
    db_session.commit()
    db_session.refresh(db_item)
    return db_item.to_dict()

def delete_item(db_session, model, item_id: uuid.UUID):
    db_item = db_session.query(model).filter(model.id == item_id).first()
    if db_item:
        db_session.delete(db_item)
        db_session.commit()
        return True
    return False

# --- Dependency to get DB session ---
def get_db_core_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()