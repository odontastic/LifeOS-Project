from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from dependencies import get_event_store, get_event_processor
from auth import get_current_user




from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from event_sourcing.models import Event as EventPydantic
from database import EmotionReadModel
from models.emotion import Emotion # Import the Emotion Pydantic model

router = APIRouter()

@router.post("/", response_model=Emotion, status_code=status.HTTP_201_CREATED)
async def create_emotion(
    emotion: Emotion, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    payload = emotion.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="EmotionCreated",
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
    return emotion

@router.get("/{emotion_id}", response_model=Emotion)
async def read_emotion(
    emotion_id: str, 
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    emotion_data = event_processor.get_read_model(EmotionReadModel, emotion_id)
    if not emotion_data or emotion_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emotion not found")
    return Emotion(**emotion_data)

@router.get("/", response_model=List[Emotion])
async def list_emotions(
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    all_emotions_data = event_processor.get_all_read_models(EmotionReadModel)
    user_emotions = [Emotion(**data) for data in all_emotions_data if data.get("username") == username]
    return user_emotions

@router.put("/{emotion_id}", response_model=Emotion)
async def update_emotion(
    emotion_id: str, 
    emotion: Emotion, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    if emotion_id != emotion.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Emotion ID in path and body do not match")
    
    emotion_data = event_processor.get_read_model(EmotionReadModel, emotion_id)
    if not emotion_data or emotion_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emotion not found")

    payload = emotion.model_dump()
    payload["username"] = username
    event = EventPydantic(
        event_type="EmotionUpdated",
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
    return emotion

@router.delete("/{emotion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emotion(
    emotion_id: str, 
    event_store: EventStore = Depends(get_event_store),
    event_processor: EventProcessor = Depends(get_event_processor),
    username: str = Depends(get_current_user)
):
    emotion_data = event_processor.get_read_model(EmotionReadModel, emotion_id)
    if not emotion_data or emotion_data.get("username") != username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emotion not found")

    event = EventPydantic(
        event_type="EmotionDeleted",
        payload={"id": emotion_id, "username": username},
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
    return {"message": "Emotion deleted successfully"}