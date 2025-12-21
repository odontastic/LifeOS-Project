from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user




from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import ReflectionReadModel
from models.reflection import Reflection # Import the Reflection Pydantic model

router = APIRouter()

@router.post("/", response_model=Reflection, status_code=status.HTTP_201_CREATED)
async def create_reflection(
    reflection: Reflection, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    payload = reflection.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ReflectionCreated",
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
    return reflection

@router.get("/{reflection_id}", response_model=Reflection)
async def read_reflection(
    reflection_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    reflection_data = event_processor.get_read_model(ReflectionReadModel, reflection_id)
    if not reflection_data or reflection_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reflection not found")
    return Reflection(**reflection_data)

@router.get("/", response_model=List[Reflection])
async def list_reflections(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_reflections_data = event_processor.get_all_read_models(ReflectionReadModel)
    user_reflections = [Reflection(**data) for data in all_reflections_data if data.get("username") == username]
    return user_reflections

@router.put("/{reflection_id}", response_model=Reflection)
async def update_reflection(
    reflection_id: str, 
    reflection: Reflection, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if reflection_id != reflection.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reflection ID in path and body do not match")
    
    reflection_data = event_processor.get_read_model(ReflectionReadModel, reflection_id)
    if not reflection_data or reflection_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reflection not found")

    payload = reflection.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ReflectionUpdated",
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
    return reflection

@router.delete("/{reflection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reflection(
    reflection_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    reflection_data = event_processor.get_read_model(ReflectionReadModel, reflection_id)
    if not reflection_data or reflection_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reflection not found")

    event = EventPydantic(
        event_type="ReflectionDeleted",
        payload={"id": reflection_id, "username": username},
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
    return {"message": "Reflection deleted successfully"}