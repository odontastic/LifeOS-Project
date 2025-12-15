from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from datetime import datetime, timezone

from main import get_event_store, get_event_processor
from auth import get_current_user
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import ZettelReadModel
from schemas import Zettel, ZettelCreate, ZettelUpdate # Import new schemas

router = APIRouter()

@router.post("/", response_model=Zettel, status_code=status.HTTP_201_CREATED)
async def create_zettel(
    zettel_create: ZettelCreate, # Use ZettelCreate for input
    event_store: EventStore = Depends(get_event_store),
    username: str = Depends(get_current_user)
):
    new_zettel_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    
    # Construct the full Zettel model instance with generated fields and username
    zettel = Zettel(
        id=new_zettel_id,
        created_at=now,
        updated_at=now,
        username=username,
        **zettel_create.model_dump() # Unpack fields from ZettelCreate
    )

    payload = zettel.model_dump()
    event = EventPydantic(
        event_type="ZettelCreated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return zettel

@router.get("/{zettel_id}", response_model=Zettel)
async def read_zettel(
    zettel_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    zettel_data = event_processor.get_read_model(ZettelReadModel, zettel_id)
    if not zettel_data or zettel_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zettel not found")
    return Zettel(**zettel_data)

@router.get("/", response_model=List[Zettel])
async def list_zettels(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_zettels_data = event_processor.get_all_read_models(ZettelReadModel)
    # Filter for current user
    user_zettels = [Zettel(**data) for data in all_zettels_data if data.get("username") == username]
    return user_zettels

@router.put("/{zettel_id}", response_model=Zettel)
async def update_zettel(
    zettel_id: str, 
    zettel_update: ZettelUpdate, # Use ZettelUpdate for input
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if zettel_id != zettel_update.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Zettel ID in path and body do not match")
    
    # Verify ownership before updating
    existing_zettel_data = event_processor.get_read_model(ZettelReadModel, zettel_id)
    if not existing_zettel_data or existing_zettel_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zettel not found")

    # Construct an updated Zettel model
    updated_zettel_dict = existing_zettel_data.copy()
    updated_zettel_dict.update(zettel_update.model_dump(exclude_unset=True))
    updated_zettel_dict["updated_at"] = datetime.now(timezone.utc) # Update timestamp
    updated_zettel_dict["username"] = username # Ensure username remains consistent

    updated_zettel = Zettel(**updated_zettel_dict)

    payload = updated_zettel.model_dump()
    event = EventPydantic(
        event_type="ZettelUpdated",
        payload=payload,
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return updated_zettel # Return the updated Zettel model

@router.delete("/{zettel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zettel(
    zettel_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    # Verify ownership before deleting
    zettel_data = event_processor.get_read_model(ZettelReadModel, zettel_id)
    if not zettel_data or zettel_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zettel not found")

    event = EventPydantic(
        event_type="ZettelDeleted",
        payload={"id": zettel_id, "username": username},
        event_id=str(uuid.uuid4())
    )
    event_store.append_event(
        event_id=event.event_id,
        event_type=event.event_type,
        payload=event.payload,
        schema_version=event.schema_version
    )
    return {"message": "Zettel deleted successfully"}