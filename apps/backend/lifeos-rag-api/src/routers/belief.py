from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from main import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import BeliefReadModel
from models.belief import Belief # Import the Belief Pydantic model

router = APIRouter()

@router.post("/", response_model=Belief, status_code=status.HTTP_201_CREATED)
async def create_belief(
    belief: Belief, 
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    payload = belief.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="BeliefCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return belief

@router.get("/{belief_id}", response_model=Belief)
async def read_belief(
    belief_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    belief_data = event_processor.get_read_model(BeliefReadModel, belief_id)
    if not belief_data or belief_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belief not found")
    return Belief(**belief_data)

@router.get("/", response_model=List[Belief])
async def list_beliefs(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_beliefs_data = event_processor.get_all_read_models(BeliefReadModel)
    user_beliefs = [Belief(**data) for data in all_beliefs_data if data.get("username") == username]
    return user_beliefs

@router.put("/{belief_id}", response_model=Belief)
async def update_belief(
    belief_id: str, 
    belief: Belief, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if belief_id != belief.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belief ID in path and body do not match")
    
    belief_data = event_processor.get_read_model(BeliefReadModel, belief_id)
    if not belief_data or belief_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belief not found")

    payload = belief.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="BeliefUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return belief

@router.delete("/{belief_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_belief(
    belief_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    belief_data = event_processor.get_read_model(BeliefReadModel, belief_id)
    if not belief_data or belief_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belief not found")

    event = EventPydantic(
        event_type="BeliefDeleted",
        payload={"id": belief_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Belief deleted successfully"}