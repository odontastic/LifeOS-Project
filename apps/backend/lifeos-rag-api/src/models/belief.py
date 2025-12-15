from typing import List, Literal
from pydantic import BaseModel, Field

class Belief(BaseModel):
    id: str
    type: Literal["belief"]
    statement: str
    status: Literal["limiting", "empowering"]
    related_entries: List[str] = Field(default_factory=list)
