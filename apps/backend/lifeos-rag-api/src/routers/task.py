from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from main import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import TaskReadModel
from models.task import Task # Import the Task Pydantic model

router = APIRouter()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: Task, 
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    payload = task.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="TaskCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return task

@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    task_data = event_processor.get_read_model(TaskReadModel, task_id)
    if not task_data or task_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Task(**task_data)

@router.get("/", response_model=List[Task])
async def list_tasks(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_tasks_data = event_processor.get_all_read_models(TaskReadModel)
    user_tasks = [Task(**data) for data in all_tasks_data if data.get("username") == username]
    return user_tasks

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str, 
    task: Task, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if task_id != task.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task ID in path and body do not match")
    
    task_data = event_processor.get_read_model(TaskReadModel, task_id)
    if not task_data or task_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    payload = task.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="TaskUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    task_data = event_processor.get_read_model(TaskReadModel, task_id)
    if not task_data or task_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    event = EventPydantic(
        event_type="TaskDeleted",
        payload={"id": task_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Task deleted successfully"}