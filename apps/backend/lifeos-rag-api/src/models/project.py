from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Project(BaseModel):
    id: str
    type: Literal["project"]
    title: str
    desired_outcome: str
    why_it_matters: str
    success_criteria: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    status: Literal["active", "paused", "done"]
    area: Optional[str] = None
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["projects"]
