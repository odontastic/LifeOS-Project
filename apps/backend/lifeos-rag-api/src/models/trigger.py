from typing import List, Literal
from pydantic import BaseModel, Field

class Trigger(BaseModel):
    id: str
    type: Literal["trigger"]
    description: str
    related_emotions: List[str] = Field(default_factory=list)
