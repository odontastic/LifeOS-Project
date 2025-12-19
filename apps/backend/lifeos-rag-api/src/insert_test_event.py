import uuid
import json
from datetime import datetime, timezone
import sys
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, StoredEvent
from models.resource import Resource

SCRIPT_DATABASE_URL = "sqlite:///lifeos_core.db"

engine = create_engine(
    SCRIPT_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_test_resource_created_event():
    print(f"Python version: {sys.version}")
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
    print(f"SCRIPT_DATABASE_URL: {SCRIPT_DATABASE_URL}")

    # Ensure the table exists before inserting
    Base.metadata.create_all(engine) # Create tables if they don't exist
    print("Tables created/checked successfully.")

    # 1. Define the resource data using the Pydantic model
    resource_data = Resource(
        id=str(uuid.uuid4()), # Use a new UUID for each test
        username="testuser",
        type="resource", # ADDED THIS LINE
        title="Manually Inserted Resource",
        format="link",
        body="This resource was manually inserted for testing replay.",
        tags=["manual", "test"],
        related_zettels=[],
        horizon="resources"
    )

    # 2. Create the StoredEvent payload
    event_payload = resource_data.model_dump_json() # Use model_dump_json for direct JSON string

    # 3. Create the StoredEvent object
    stored_event = StoredEvent(
        event_id=str(uuid.uuid4()),
        event_type="ResourceCreated",
        timestamp=datetime.now(timezone.utc),
        payload=event_payload,
        schema_version="1.0"
    )

    # 4. Insert into the database
    db = SessionLocal()
    try:
        db.add(stored_event)
        db.commit()
        db.refresh(stored_event)
        print(f"Successfully inserted ResourceCreated event with ID: {stored_event.event_id}")
    except Exception as e:
        db.rollback()
        print(f"Error inserting event: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_resource_created_event()