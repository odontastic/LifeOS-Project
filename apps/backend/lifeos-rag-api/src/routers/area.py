from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import AreaReadModel
from models.area import Area # Import the Area Pydantic model

router = APIRouter()

@router.post("/", response_model=Area, status_code=status.HTTP_201_CREATED)
async def create_area(
    area: Area, 
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    payload = area.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="AreaCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return area

@router.get("/{area_id}", response_model=Area)
async def read_area(
    area_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    area_data = event_processor.get_read_model(AreaReadModel, area_id)
    if not area_data or area_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return Area(**area_data)

@router.get("/", response_model=List[Area])
async def list_areas(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_areas_data = event_processor.get_all_read_models(AreaReadModel)
    user_areas = [Area(**data) for data in all_areas_data if data.get("username") == username]
    return user_areas

@router.put("/{area_id}", response_model=Area)
async def update_area(
    area_id: str, 
    area: Area, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if area_id != area.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area ID in path and body do not match")
    
    area_data = event_processor.get_read_model(AreaReadModel, area_id)
    if not area_data or area_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    payload = area.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="AreaUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return area

@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_area(
    area_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    area_data = event_processor.get_read_model(AreaReadModel, area_id)
    if not area_data or area_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    event = EventPydantic(
        event_type="AreaDeleted",
        payload={"id": area_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Area deleted successfully"}