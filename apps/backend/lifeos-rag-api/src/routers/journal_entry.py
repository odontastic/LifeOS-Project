from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user




from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import JournalEntryReadModel
from models.journal_entry import JournalEntry # Import the JournalEntry Pydantic model

router = APIRouter()

@router.post("/", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    journal_entry: JournalEntry, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    payload = journal_entry.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="JournalEntryCreated",
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
    return journal_entry

@router.get("/{journal_entry_id}", response_model=JournalEntry)
async def read_journal_entry(
    journal_entry_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    journal_entry_data = event_processor.get_read_model(JournalEntryReadModel, journal_entry_id)
    if not journal_entry_data or journal_entry_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")
    return JournalEntry(**journal_entry_data)

@router.get("/", response_model=List[JournalEntry])
async def list_journal_entries(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_journal_entries_data = event_processor.get_all_read_models(JournalEntryReadModel)
    user_journal_entries = [JournalEntry(**data) for data in all_journal_entries_data if data.get("username") == username]
    return user_journal_entries

@router.put("/{journal_entry_id}", response_model=JournalEntry)
async def update_journal_entry(
    journal_entry_id: str, 
    journal_entry: JournalEntry, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if journal_entry_id != journal_entry.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JournalEntry ID in path and body do not match")
    
    journal_entry_data = event_processor.get_read_model(JournalEntryReadModel, journal_entry_id)
    if not journal_entry_data or journal_entry_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")

    payload = journal_entry.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="JournalEntryUpdated",
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
    return journal_entry

@router.delete("/{journal_entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    journal_entry_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    journal_entry_data = event_processor.get_read_model(JournalEntryReadModel, journal_entry_id)
    if not journal_entry_data or journal_entry_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")

    event = EventPydantic(
        event_type="JournalEntryDeleted",
        payload={"id": journal_entry_id, "username": username},
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
    return {"message": "JournalEntry deleted successfully"}