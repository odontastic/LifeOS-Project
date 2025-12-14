    interaction_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

# --- Task Specific Models ---
class TaskStateChangedEvent(BaseModel):
    task_id: UUID
    status: str
    priority: int
    energy_requirement: str
    context_tags: Optional[List[str]] = None
