import uuid
import json
from datetime import datetime
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, EmotionEntryModel, ContactProfileModel, TaskItemModel, KnowledgeNodeModel, SystemInsightModel

# --- Database Setup for Core Entities ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./lifeos_core.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables
Base.metadata.create_all(bind=engine)

# --- Generic CRUD Operations ---

def create_item(db_session, model, schema_item):
    # Convert lists/UUIDs in schema_item to JSON strings for storage
    item_data = schema_item.model_dump()
    for key, value in item_data.items():
        if isinstance(value, (list)):
            item_data[key] = json.dumps([str(x) for x in value]) if isinstance(value, list) else str(value)
        elif isinstance(value, datetime):
            item_data[key] = value # Store datetime objects directly for SQLAlchemy
        elif isinstance(value, uuid.UUID): # Convert UUID to string for storage
            item_data[key] = str(value)
    
    db_item = model(**item_data)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item.to_dict() # Return as dict

def get_item_by_id(db_session, model, item_id: uuid.UUID):
    item = db_session.query(model).filter(model.id == item_id).first()
    if item:
        return item.to_dict()
    return None

def get_items(db_session, model, skip: int = 0, limit: int = 100):
    return [item.to_dict() for item in db_session.query(model).offset(skip).limit(limit).all()]

def update_item(db_session, model, item_id: uuid.UUID, schema_item):
    db_item = db_session.query(model).filter(model.id == item_id).first()
    if not db_item:
        return None
    
    update_data = schema_item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if isinstance(value, (list)):
            setattr(db_item, key, json.dumps([str(x) for x in value]) if isinstance(value, list) else str(value))
        elif isinstance(value, datetime):
            setattr(db_item, key, value) # Store datetime objects directly
        elif isinstance(value, uuid.UUID): # Convert UUID to string for storage
            setattr(db_item, key, str(value))
        else:
            setattr(db_item, key, value)
    
    db_session.commit()
    db_session.refresh(db_item)
    return db_item.to_dict()

def delete_item(db_session, model, item_id: uuid.UUID):
    db_item = db_session.query(model).filter(model.id == item_id).first()
    if db_item:
        db_session.delete(db_item)
        db_session.commit()
        return True
    return False

# --- Dependency to get DB session ---
def get_db_core_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()