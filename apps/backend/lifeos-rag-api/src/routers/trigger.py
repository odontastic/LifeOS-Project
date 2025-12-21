from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user




from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import TriggerReadModel
from models.trigger import Trigger # Import the Trigger Pydantic model

router = APIRouter()

@router.post("/", response_model=Trigger, status_code=status.HTTP_201_CREATED)
async def create_trigger(
    trigger: Trigger, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    payload = trigger.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="TriggerCreated",
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
    return trigger

@router.get("/{trigger_id}", response_model=Trigger)
async def read_trigger(
    trigger_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    trigger_data = event_processor.get_read_model(TriggerReadModel, trigger_id)
    if not trigger_data or trigger_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")
    return Trigger(**trigger_data)

@router.get("/", response_model=List[Trigger])
async def list_triggers(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_triggers_data = event_processor.get_all_read_models(TriggerReadModel)
    user_triggers = [Trigger(**data) for data in all_triggers_data if data.get("username") == username]
    return user_triggers

@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(
    trigger_id: str, 
    trigger: Trigger, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if trigger_id != trigger.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trigger ID in path and body do not match")
    
    trigger_data = event_processor.get_read_model(TriggerReadModel, trigger_id)
    if not trigger_data or trigger_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")

    payload = trigger.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="TriggerUpdated",
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
    return trigger

@router.delete("/{trigger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trigger(
    trigger_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    trigger_data = event_processor.get_read_model(TriggerReadModel, trigger_id)
    if not trigger_data or trigger_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")

    event = EventPydantic(
        event_type="TriggerDeleted",
        payload={"id": trigger_id, "username": username},
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
    return {"message": "Trigger deleted successfully"}