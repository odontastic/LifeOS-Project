from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field

class Reflection(BaseModel):
    id: str
    type: Literal["reflection"]
    body: str
    insights: List[str] = Field(default_factory=list)
    generated_zettels: List[str] = Field(default_factory=list)
    related_areas: List[str] = Field(default_factory=list)
    related_projects: List[str] = Field(default_factory=list)
    created_at: datetime
