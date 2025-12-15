from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
import uuid

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Any
    schema_version: str = "1.0" # Default version
