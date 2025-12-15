from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Goal(BaseModel):
    id: str
    type: Literal["goal"]
    title: str
    description: str
    deadline: Optional[datetime] = None
    success_criteria: List[str] = Field(default_factory=list)
    related_projects: List[str] = Field(default_factory=list)
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["goals"]
