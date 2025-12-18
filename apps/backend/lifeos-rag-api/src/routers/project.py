from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import ProjectReadModel
from models.project import Project # Import the Project Pydantic model

router = APIRouter()

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: Project, 
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    payload = project.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ProjectCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return project

@router.get("/{project_id}", response_model=Project)
async def read_project(
    project_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    project_data = event_processor.get_read_model(ProjectReadModel, project_id)
    if not project_data or project_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return Project(**project_data)

@router.get("/", response_model=List[Project])
async def list_projects(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_projects_data = event_processor.get_all_read_models(ProjectReadModel)
    user_projects = [Project(**data) for data in all_projects_data if data.get("username") == username]
    return user_projects

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str, 
    project: Project, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if project_id != project.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project ID in path and body do not match")
    
    project_data = event_processor.get_read_model(ProjectReadModel, project_id)
    if not project_data or project_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    payload = project.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="ProjectUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    project_data = event_processor.get_read_model(ProjectReadModel, project_id)
    if not project_data or project_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    event = EventPydantic(
        event_type="ProjectDeleted",
        payload={"id": project_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Project deleted successfully"}