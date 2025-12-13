from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# --- Shared Base Model ---

class BaseNode(BaseModel):
    id: str = Field(..., description="Unique UUID for the entity")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

# --- Productivity System Models (PARA + GTD + Zettelkasten) ---

class Zettel(BaseNode):
    """Atomic knowledge note."""
    type: Literal["zettel"] = "zettel"
    title: str
    body: str
    links: List[str] = Field(default_factory=list, description="IDs of related Zettels or entities")
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["none", "vision", "goals", "principles"] = "none"
    contexts: List[str] = Field(default_factory=list, description="GTD contexts")

class Project(BaseNode):
    """Goal-oriented outcome with multiple steps."""
    type: Literal["project"] = "project"
    title: str
    desired_outcome: str
    why_it_matters: str
    success_criteria: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list, description="IDs of Tasks")
    status: Literal["active", "paused", "done"] = "active"
    area: Optional[str] = Field(default=None, description="ID of parent Area")
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["projects"] = "projects"

class Area(BaseNode):
    """Ongoing responsibility or life domain."""
    type: Literal["area"] = "area"
    title: str
    description: str
    health_metric: str = Field(..., description="Current status e.g. 'Stable / Needs Attention'")
    active_projects: List[str] = Field(default_factory=list, description="IDs of active Projects")
    active_tasks: List[str] = Field(default_factory=list, description="IDs of active Tasks")
    related_resources: List[str] = Field(default_factory=list, description="IDs of Resources")
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["areas"] = "areas"

class Resource(BaseNode):
    """Reference material and knowledge assets."""
    type: Literal["resource"] = "resource"
    title: str
    format: Literal["link", "file", "zettel", "mixed"]
    body: str
    tags: List[str] = Field(default_factory=list)
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["resources"] = "resources"

class Task(BaseNode):
    """Concrete next action."""
    type: Literal["task"] = "task"
    title: str
    description: str
    status: Literal["next", "waiting", "scheduled", "done"] = "next"
    due: Optional[datetime] = None
    context: str = Field(..., description="GTD Context e.g. @Computer, @Home")
    project: Optional[str] = Field(default=None, description="ID of parent Project")
    area: Optional[str] = Field(default=None, description="ID of parent Area")
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["actions"] = "actions"

class Goal(BaseNode):
    """Higher-level objective."""
    type: Literal["goal"] = "goal"
    title: str
    description: str
    deadline: Optional[datetime] = None
    success_criteria: List[str] = Field(default_factory=list)
    related_projects: List[str] = Field(default_factory=list)
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["goals"] = "goals"

class Reflection(BaseNode):
    """Periodical review note."""
    type: Literal["reflection"] = "reflection"
    body: str
    insights: List[str] = Field(default_factory=list)
    generated_zettels: List[str] = Field(default_factory=list, description="IDs of Zettels created from this reflection")
    related_areas: List[str] = Field(default_factory=list)
    related_projects: List[str] = Field(default_factory=list)

# --- Therapeutic System Models (Coaching) ---

class JournalEntry(BaseNode):
    """A single journal entry."""
    type: Literal["journal_entry"] = "journal_entry"
    body: str
    mood_rating: Optional[float] = Field(None, ge=1, le=10)
    emotions: List[str] = Field(default_factory=list, description="IDs of Emotion nodes")
    beliefs: List[str] = Field(default_factory=list, description="IDs of Belief nodes")

class Emotion(BaseNode):
    """Specific emotion mentioned or inferred."""
    type: Literal["emotion"] = "emotion"
    name: str
    intensity: Optional[float] = None
    valence: Literal["positive", "negative", "neutral"]
    related_entries: List[str] = Field(default_factory=list)

class Belief(BaseNode):
    """Core belief or thought pattern."""
    type: Literal["belief"] = "belief"
    statement: str
    status: Literal["limiting", "empowering"]
    related_entries: List[str] = Field(default_factory=list)

class Trigger(BaseNode):
    """Event causing emotional reaction."""
    type: Literal["trigger"] = "trigger"
    description: str
    related_emotions: List[str] = Field(default_factory=list)

class CopingMechanism(BaseNode):
    """Action or thought process for managing emotions."""
    type: Literal["coping_mechanism"] = "coping_mechanism"
    description: str
