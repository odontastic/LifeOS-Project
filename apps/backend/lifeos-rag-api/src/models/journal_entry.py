from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field

class JournalEntry(BaseModel):
    id: str
    type: Literal["journal_entry"]
    body: str
    mood_rating: float  # Assuming mood_rating can be a float
    emotions: List[str] = Field(default_factory=list)
    beliefs: List[str] = Field(default_factory=list)
    created_at: datetime
