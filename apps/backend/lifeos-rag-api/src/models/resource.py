from typing import List, Literal
from pydantic import BaseModel, Field

class Resource(BaseModel):
    id: str
    type: Literal["resource"]
    title: str
    format: Literal["link", "file", "zettel", "mixed"]
    body: str
    tags: List[str] = Field(default_factory=list)
    related_zettels: List[str] = Field(default_factory=list)
    horizon: Literal["resources"]
