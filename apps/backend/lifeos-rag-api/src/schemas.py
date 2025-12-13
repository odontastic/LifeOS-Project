from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import uuid

# --- Shared Base Model ---

class BaseNode(BaseModel):
    """
    Base node for all entities in the LifeOS Knowledge Graph.
    Implements the Dual-Store pattern: this ID is used in both Neo4j and Qdrant.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique UUID for the entity (shared across Neo4j/Qdrant)")
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat(), description="Creation timestamp (ISO ISO 8601)")
    updated_at: Optional[str] = Field(default=None, description="Last update timestamp")
    
    # Universal Metadata (Phase 2 Spec)
    life_domain: Optional[str] = Field(None, description="e.g. 'Personal', 'Work', 'Relationship', 'Health'")
    life_stage: Optional[str] = Field(None, description="e.g. 'College', 'Early Career', 'Fatherhood'")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence score of extraction (0-1)")

# --- Therapeutic System Models (Core) ---

class JournalEntry(BaseNode):
    """A single temporal reflection or log."""
    type: Literal["journal_entry"] = "journal_entry"
    body: str
    sentiment_score: Optional[float] = None
    mood_rating: Optional[float] = Field(None, ge=1, le=10)
    # Relationships managed via edges, but IDs stored here for convenience if needed
    
class Emotion(BaseNode):
    """Specific emotion mentioned or inferred."""
    type: Literal["emotion"] = "emotion"
    name: str = Field(..., description="e.g. 'Anxiety', 'Joy', 'Frustration'")
    valence: Literal["positive", "negative", "neutral"]
    intensity: float = Field(..., ge=1, le=10, description="Subjective intensity")

class Belief(BaseNode):
    """Core belief or thought pattern."""
    type: Literal["belief"] = "belief"
    statement: str
    status: Literal["active", "challenged", "transformed"] = "active"
    stability: Literal["stable", "transient"] = "stable"

class Trigger(BaseNode):
    """Event or stimuli causing emotional reaction."""
    type: Literal["trigger"] = "trigger"
    description: str

class CopingMechanism(BaseNode):
    """Action or thought process for managing emotions."""
    type: Literal["coping_mechanism"] = "coping_mechanism"
    name: str
    description: str
    effectiveness: Optional[float] = None

class Episode(BaseNode):
    """Significant temporal event or period."""
    type: Literal["episode"] = "episode"
    title: str
    description: str
    date: Optional[str] = None

class Pattern(BaseNode):
    """Recurring theme or behavior observed over time."""
    type: Literal["pattern"] = "pattern"
    name: str
    description: str
    recurrence_frequency: Optional[str] = None

class SessionSummary(BaseNode):
    """Summary of a coaching/therapy session."""
    type: Literal["session_summary"] = "session_summary"
    summary: str
    date: str

class Goal(BaseNode):
    """Personal or professional goal."""
    type: Literal["goal"] = "goal"
    title: str
    description: str
    deadline: Optional[str] = None
    status: Literal["active", "completed", "dropped"] = "active"

# --- Productivity System Models (PARA + GTD + Zettelkasten) ---

class Zettel(BaseNode):
    """Atomic knowledge note."""
    type: Literal["zettel"] = "zettel"
    title: str
    body: str
    links: List[str] = Field(default_factory=list, description="IDs of related Zettels")
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["none", "vision", "goals", "principles"] = "none"
    contexts: List[str] = Field(default_factory=list, description="GTD contexts")

class Project(BaseNode):
    """Goal-oriented outcome with multiple steps."""
    type: Literal["project"] = "project"
    title: str
    desired_outcome: str
    why_it_matters: str
    status: Literal["active", "paused", "done"] = "active"
    area_id: Optional[str] = Field(None, description="ID of parent Area")
    horizon: Literal["projects"] = "projects"

class Area(BaseNode):
    """Ongoing responsibility or life domain."""
    type: Literal["area"] = "area"
    title: str
    description: str
    health_metric: str = Field(..., description="Current status e.g. 'Stable / Needs Attention'")
    horizon: Literal["areas"] = "areas"

class Resource(BaseNode):
    """Reference material and knowledge assets."""
    type: Literal["resource"] = "resource"
    title: str
    format: Literal["link", "file", "zettel", "mixed"]
    body: str
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["resources"] = "resources"

class Task(BaseNode):
    """Concrete next action."""
    type: Literal["task"] = "task"
    title: str
    description: str
    status: Literal["next", "waiting", "scheduled", "done"] = "next"
    due: Optional[str] = None
    context: str = Field(..., description="GTD Context e.g. @Computer, @Home")
    project_id: Optional[str] = Field(None, description="ID of parent Project")
    area_id: Optional[str] = Field(None, description="ID of parent Area")
    horizon: Literal["actions"] = "actions"

class Reflection(BaseNode):
    """Periodical review note."""
    type: Literal["reflection"] = "reflection"
    body: str
    insights: List[str] = Field(default_factory=list)
