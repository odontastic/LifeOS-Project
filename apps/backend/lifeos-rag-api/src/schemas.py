import uuid
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field

# --- Schema Definitions ---

# Base Zettel model, representing the full state of a Zettel
class Zettel(BaseModel):
    id: str
    type: Literal["zettel"]
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    links: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["none", "vision", "goals", "principles"]
    contexts: List[str] = Field(default_factory=list)
    username: str # This is now part of the full Zettel model

# Model for creating a new Zettel (does not include ID, created_at, updated_at, username)
class ZettelCreate(BaseModel):
    type: Literal["zettel"] = "zettel"
    title: str
    body: str
    links: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["none", "vision", "goals", "principles"] = "none"
    contexts: List[str] = Field(default_factory=list)

# Model for updating an existing Zettel (all fields optional, except id for consistency)
class ZettelUpdate(BaseModel):
    id: str # ID is required for update
    type: Optional[Literal["zettel"]] = None
    title: Optional[str] = None
    body: Optional[str] = None
    links: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    horizon: Optional[Literal["none", "vision", "goals", "principles"]] = None
    contexts: Optional[List[str]] = None
    # username should not be updatable by request body

# Base Project model, representing the full state of a Project
class Project(BaseModel):
    id: str
    username: str
    type: Literal["project"]
    title: str
    desired_outcome: str
    why_it_matters: str
    success_criteria: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    status: str
    area: Optional[str] = None
    related_zettels: List[str] = Field(default_factory=list)
    horizon: str

# Model for creating a new Project (does not include ID, username)
class ProjectCreate(BaseModel):
    type: Literal["project"] = "project"
    title: str
    desired_outcome: str
    why_it_matters: str
    success_criteria: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    status: str = "active"
    area: Optional[str] = None
    related_zettels: List[str] = Field(default_factory=list)
    horizon: str = "goals"

# Model for updating an existing Project (all fields optional, except id for consistency)
class ProjectUpdate(BaseModel):
    id: str # ID is required for update
    type: Optional[Literal["project"]] = None
    title: Optional[str] = None
    desired_outcome: Optional[str] = None
    why_it_matters: Optional[str] = None
    success_criteria: Optional[List[str]] = None
    next_actions: Optional[List[str]] = None
    status: Optional[str] = None
    area: Optional[str] = None
    related_zettels: Optional[List[str]] = None
    horizon: Optional[str] = None

class EmotionEntry(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    primary_emotion: str
    secondary_emotions: Optional[List[str]] = None
    valence: float = Field(..., ge=-1.0, le=1.0) # -1.0 (negative) to 1.0 (positive)
    arousal: float = Field(..., ge=-1.0, le=1.0) # -1.0 (low) to 1.0 (high)
    intensity: float = Field(..., ge=0.0, le=1.0) # 0.0 (low) to 1.0 (high)
    context_tags: Optional[List[str]] = None
    note: Optional[str] = None

class EmotionLoggedEvent(BaseModel):
    emotion_id: UUID
    primary_emotion: str
    valence: float
    arousal: float
    context_tags: Optional[List[str]] = None

class CalmCompassActionEvent(BaseModel):
    action_id: UUID = Field(default_factory=uuid.uuid4)
    recommendation_id: UUID
    action_type: str # e.g., "suggested_activity", "guided_meditation", "journal_prompt"
    status: str # e.g., "initiated", "completed", "skipped"
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class InsightCreatedEvent(BaseModel):
    insight_id: UUID
    insight_type: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class ContactProfile(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: str
    relation_type: Optional[str] = None
    sentiment_summary: Optional[str] = None
    open_loops: Optional[List[str]] = None
    context_history: Optional[List[str]] = None
    last_interaction: Optional[datetime] = None

class ContactUpdatedEvent(BaseModel):
    contact_id: UUID
    name: str
    sentiment_summary: Optional[str] = None
    open_loops: Optional[List[str]] = None

class ContactCreatedEvent(BaseModel):
    id: UUID
    name: str
    relation_type: Optional[str] = None
    sentiment_summary: Optional[str] = None
    open_loops: Optional[List[str]] = None
    context_history: Optional[List[str]] = None
    last_interaction: Optional[datetime] = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class ContactDeletedEvent(BaseModel):
    contact_id: UUID

class TaskItem(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: Optional[str] = None
    status: str = "pending" # e.g., "pending", "in_progress", "completed", "blocked"
    priority: int = 0 # e.g., 0 (low), 1 (medium), 2 (high)
    due_date: Optional[datetime] = None
    energy_requirement: Optional[str] = None # e.g., "low", "medium", "high"
    context_tags: Optional[List[str]] = None

class TaskStateChangedEvent(BaseModel):
    task_id: UUID
    status: str
    priority: int
    energy_requirement: Optional[str] = None
    context_tags: Optional[List[str]] = None

class KnowledgeNode(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str
    content: str
    node_type: str # e.g., "para_project", "para_area", "para_resource", "para_archive"
    tags: Optional[List[str]] = None
    related_nodes: Optional[List[UUID]] = None

class NodeCreatedEvent(BaseModel):
    node_id: str
    text: str
    metadata: Dict[str, Any]
    collection_name: str

class EdgeCreatedEvent(BaseModel):
    from_node_id: str
    to_node_id: str
    label: str
    properties: Dict[str, Any]
    from_collection: str
    to_collection: str
    edge_collection_name: str

class KnowledgeNodeEvent(BaseModel):
    id: UUID
    title: str
    content: str
    node_type: str
    tags: Optional[List[str]] = None
    related_nodes: Optional[List[UUID]] = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class SystemInsight(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    insight_type: str # e.g., "feedback_loop", "pattern_detection", "recommendation"
    message: str
    action_recommendations: Optional[List[str]] = None
    feedback_rating: Optional[int] = None # 1-5 rating from user
    feedback_comment: Optional[str] = None
    # Decay Profile Fields
    half_life_days: Optional[int] = None
    decay_start_date: Optional[datetime] = None
    last_reaffirmed_date: Optional[datetime] = None

class CalmFeedbackRequest(BaseModel):
    insight_id: UUID
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class SystemInsightFeedbackEvent(BaseModel):
    insight_id: UUID
    feedback_rating: int
    feedback_comment: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class InsightDecayedEvent(BaseModel):
    insight_id: UUID
    decay_status: float
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class RelationLoggedEvent(BaseModel):
    contact_id: UUID
    interaction_date: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))
    notes: Optional[str] = None

class RelationLogRequest(BaseModel):
    contact_id: UUID
    interaction_date: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))
    notes: Optional[str] = None