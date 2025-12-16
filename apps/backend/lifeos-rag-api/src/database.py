import uuid
from datetime import datetime, timezone
import json

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON

# --- Base and Engine ---
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./lifeos_core.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Custom Types ---
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

# --- Models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)

class StoredEvent(Base):
    __tablename__ = 'event_log'
    event_id = Column(String, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    payload = Column(Text, nullable=False)
    schema_version = Column(String, nullable=False)

    def __repr__(self):
        return f"<StoredEvent(event_id='{self.event_id}', event_type='{self.event_type}')>"

class ZettelReadModel(Base):
    __tablename__ = "zettels"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="zettel")
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    links = Column(SQLiteJSON, default=[])
    tags = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)
    contexts = Column(SQLiteJSON, default=[])

class ProjectReadModel(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="project")
    title = Column(String, nullable=False)
    desired_outcome = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    success_criteria = Column(SQLiteJSON, default=[])
    next_actions = Column(SQLiteJSON, default=[])
    status = Column(String, nullable=False)
    area = Column(String, nullable=True)
    related_zettels = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)

class AreaReadModel(Base):
    __tablename__ = "areas"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="area")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    health_metric = Column(String, nullable=False)
    active_projects = Column(SQLiteJSON, default=[])
    active_tasks = Column(SQLiteJSON, default=[])
    related_resources = Column(SQLiteJSON, default=[])
    related_zettels = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)

class ResourceReadModel(Base):
    __tablename__ = "resources"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="resource")
    title = Column(String, nullable=False)
    format = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(SQLiteJSON, default=[])
    related_zettels = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)

class TaskReadModel(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="task")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    due = Column(DateTime, nullable=True)
    context = Column(Text, nullable=False)
    project = Column(String, nullable=True)
    area = Column(String, nullable=True)
    related_zettels = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)

class GoalReadModel(Base):
    __tablename__ = "goals"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="goal")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    deadline = Column(DateTime, nullable=True)
    success_criteria = Column(SQLiteJSON, default=[])
    related_projects = Column(SQLiteJSON, default=[])
    related_zettels = Column(SQLiteJSON, default=[])
    horizon = Column(String, nullable=False)

class ReflectionReadModel(Base):
    __tablename__ = "reflections"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="reflection")
    body = Column(Text, nullable=False)
    insights = Column(SQLiteJSON, default=[])
    generated_zettels = Column(SQLiteJSON, default=[])
    related_areas = Column(SQLiteJSON, default=[])
    related_projects = Column(SQLiteJSON, default=[])
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class JournalEntryReadModel(Base):
    __tablename__ = "journal_entries"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="journal_entry")
    body = Column(Text, nullable=False)
    mood_rating = Column(Float, nullable=False)
    emotions = Column(SQLiteJSON, default=[])
    beliefs = Column(SQLiteJSON, default=[])
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class EmotionReadModel(Base):
    __tablename__ = "emotions"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="emotion")
    name = Column(String, nullable=False)
    intensity = Column(Float, nullable=False)
    valence = Column(String, nullable=False)
    related_entries = Column(SQLiteJSON, default=[])

class BeliefReadModel(Base):
    __tablename__ = "beliefs"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="belief")
    statement = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    related_entries = Column(SQLiteJSON, default=[])

class TriggerReadModel(Base):
    __tablename__ = "triggers"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    type = Column(String, default="trigger")
    description = Column(Text, nullable=False)
    related_emotions = Column(SQLiteJSON, default=[])

class EmotionEntryModel(Base):
    __tablename__ = "emotion_entries"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    primary_emotion = Column(String, nullable=False)
    secondary_emotions = Column(Text) # Stored as JSON string
    valence = Column(Float, nullable=False) # Changed from Integer to Float
    arousal = Column(Float, nullable=False) # Changed from Integer to Float
    intensity = Column(Float, nullable=False) # Changed from Integer to Float
    somatic_markers = Column(Text) # Stored as JSON string
    context_tags = Column(Text) # Stored as JSON string
    notes = Column(Text)
    linked_contact_id = Column(GUID, index=True)
    linked_task_id = Column(GUID, index=True)
    action_prompt = Column(Text)
    processed = Column(Boolean, default=False)

class ContactProfileModel(Base):
    __tablename__ = "contact_profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False)
    importance_level = Column(Integer, nullable=False)
    last_interaction = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    open_loops = Column(Text) # Stored as JSON string
    sentiment_summary = Column(Text)
    next_follow_up = Column(DateTime)
    context_history = Column(Text) # Linked EmotionEntry IDs, stored as JSON string

class TaskItemModel(Base):
    __tablename__ = "task_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(GUID, index=True)
    context_tags = Column(Text) # Stored as JSON string
    status = Column(String, nullable=False)  # 'open','in_progress','completed','blocked'
    priority = Column(Integer, nullable=False)
    due_date = Column(DateTime)
    linked_emotion_ids = Column(Text) # Stored as JSON string
    linked_contact_ids = Column(Text) # Stored as JSON string
    energy_requirement = Column(String)  # 'low','medium','high'

class KnowledgeNodeModel(Base):
    __tablename__ = "knowledge_nodes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text, nullable=False) # Stored as JSON string
    links = Column(Text) # Bidirectional connections, stored as JSON string
    para_category = Column(String, nullable=False)  # project/area/resource/archive
    emotion_links = Column(Text) # Stored as JSON string
    last_reviewed = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
