from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import GoalReadModel
from models.goal import Goal # Import the Goal Pydantic model

router = APIRouter()

@router.post("/", response_model=Goal, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal: Goal, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    payload = goal.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="GoalCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    stored_event = event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor._apply_event(stored_event)
    return goal

@router.get("/{goal_id}", response_model=Goal)
async def read_goal(
    goal_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    goal_data = event_processor.get_read_model(GoalReadModel, goal_id)
    if not goal_data or goal_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return Goal(**goal_data)

@router.get("/", response_model=List[Goal])
async def list_goals(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_goals_data = event_processor.get_all_read_models(GoalReadModel)
    user_goals = [Goal(**data) for data in all_goals_data if data.get("username") == username]
    return user_goals

@router.put("/{goal_id}", response_model=Goal)
async def update_goal(
    goal_id: str, 
    goal: Goal, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if goal_id != goal.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Goal ID in path and body do not match")
    
    goal_data = event_processor.get_read_model(GoalReadModel, goal_id)
    if not goal_data or goal_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    payload = goal.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="GoalUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    stored_event = event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor._apply_event(stored_event)
    return goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    goal_data = event_processor.get_read_model(GoalReadModel, goal_id)
    if not goal_data or goal_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    event = EventPydantic(
        event_type="GoalDeleted",
        payload={"id": goal_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    stored_event = event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    # Immediately apply event to rebuild/update read model
    event_processor._apply_event(stored_event)
    return {"message": "Goal deleted successfully"}