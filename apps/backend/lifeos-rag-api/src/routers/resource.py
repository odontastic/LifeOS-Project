from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import ResourceReadModel
from models.resource import Resource # Import the Resource Pydantic model

router = APIRouter()

@router.post("/", response_model=Resource, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource: Resource, 
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    payload = resource.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ResourceCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return resource

@router.get("/{resource_id}", response_model=Resource)
async def read_resource(
    resource_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    resource_data = event_processor.get_read_model(ResourceReadModel, resource_id)
    if not resource_data or resource_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return Resource(**resource_data)

@router.get("/", response_model=List[Resource])
async def list_resources(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_resources_data = event_processor.get_all_read_models(ResourceReadModel)
    user_resources = [Resource(**data) for data in all_resources_data if data.get("username") == username]
    return user_resources

@router.put("/{resource_id}", response_model=Resource)
async def update_resource(
    resource_id: str, 
    resource: Resource, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if resource_id != resource.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource ID in path and body do not match")
    
    resource_data = event_processor.get_read_model(ResourceReadModel, resource_id)
    if not resource_data or resource_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    payload = resource.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ResourceUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    resource_data = event_processor.get_read_model(ResourceReadModel, resource_id)
    if not resource_data or resource_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    event = EventPydantic(
        event_type="ResourceDeleted",
        payload={"id": resource_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Resource deleted successfully"}