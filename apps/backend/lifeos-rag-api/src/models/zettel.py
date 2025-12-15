from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Zettel(BaseModel):
    id: str
    type: Literal["zettel"]
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    links: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    horizon: Literal["none", "vision", "goals", "principles"]
    contexts: List[str] = Field(default_factory=list)
    username: str
