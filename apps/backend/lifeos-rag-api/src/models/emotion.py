from typing import List, Literal
from pydantic import BaseModel, Field

class Emotion(BaseModel):
    id: str
    type: Literal["emotion"]
    name: str
    intensity: float # Assuming intensity can be a float
    valence: Literal["positive", "negative", "neutral"]
    related_entries: List[str] = Field(default_factory=list)
