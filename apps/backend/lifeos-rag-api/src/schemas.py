from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# --- 4.1 EmotionEntry ---
class EmotionEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4) # Auto-generate UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow) # Auto-generate UTC timestamp
    primary_emotion: str  # 'anger', 'joy', etc.
    secondary_emotions: Optional[List[str]] = None
    valence: int  # 1–10
    arousal: int  # 1–10
    intensity: int  # composite metric
    somatic_markers: Optional[List[str]] = None  # e.g. 'tight_chest', 'warm_face'
    context_tags: Optional[List[str]] = None  # e.g. ['family','coding']
    notes: Optional[str] = None
    linked_contact_id: Optional[UUID] = None
    linked_task_id: Optional[UUID] = None
    action_prompt: Optional[str] = None  # AI-generated suggestion
    processed: bool = False

# --- 4.2 ContactProfile (Connection Engine) ---
class ContactProfile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    relationship_type: str  # spouse, friend, child
    importance_level: int  # 1–5
    last_interaction: Optional[datetime] = None
    open_loops: Optional[List[str]] = None  # e.g. ['tax stress','hip pain']
    sentiment_summary: Optional[str] = None
    next_follow_up: Optional[datetime] = None
    context_history: Optional[List[UUID]] = None  # linked EmotionEntry IDs

# --- 4.3 TaskItem ---
class TaskItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    project_id: Optional[UUID] = None
    context_tags: Optional[List[str]] = None
    status: str  # 'open','in_progress','done'
    priority: int
    due_date: Optional[datetime] = None
    linked_emotion_ids: Optional[List[UUID]] = None
    linked_contact_ids: Optional[List[UUID]] = None
    energy_requirement: str  # 'low','medium','high'

# --- 4.4 KnowledgeNode (Zettelkasten / PARA) ---
class KnowledgeNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    tags: List[str]
    links: Optional[List[UUID]] = None  # bidirectional connections
    para_category: str  # project/area/resource/archive
    emotion_links: Optional[List[UUID]] = None
    last_reviewed: Optional[datetime] = None

# --- 4.5 SystemInsight (AI Layer) ---
class SystemInsight(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    insight_type: str  # 'pattern','recommendation','summary'
    generated_from: List[UUID]  # source objects
    model_version: str
    confidence: float
    message: str
    action_recommendations: Optional[List[str]] = None

# --- Event Payloads ---
class EmotionLoggedEvent(BaseModel):
    emotion_id: UUID
    primary_emotion: str
    valence: int
    arousal: int
    context_tags: Optional[List[str]] = None

class CalmCompassActionEvent(BaseModel):
    quadrant: str
    entry_id: UUID
    protocol: str

class InsightCreatedEvent(BaseModel):
    insight_id: UUID
    insight_type: str
    generated_from: List[UUID]
    message: str

class ContactUpdatedEvent(BaseModel):
    contact_id: UUID
    name: str
    sentiment_summary: Optional[str] = None
    open_loops: Optional[List[str]] = None