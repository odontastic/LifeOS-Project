from typing import List, Literal
from pydantic import BaseModel, Field

class Area(BaseModel):
    id: str
    type: Literal["area"]
    title: str
    description: str
    health_metric: Literal["Stable", "Needs Attention"]
    active_projects: List[str] = Field(default_factory=list)
    active_tasks: List[str] = Field(default_factory=list)
    related_resources: List[str] = Field(default_factory=list)
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["areas"]
