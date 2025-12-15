from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str
    type: Literal["task"]
    title: str
    description: str
    status: Literal["next", "waiting", "scheduled", "done"]
    due: Optional[datetime] = None
    context: str
    project: Optional[str] = None
    area: Optional[str] = None
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["actions"]
