import os
import uuid
import json
from datetime import datetime, timezone # Added timezone for UTC

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
# Qdrant related imports are no longer needed for direct interaction
# from llama_index.vector_stores.qdrant import QdrantVectorStore
# from qdrant_client import QdrantClient

# Event sourcing imports
from event_sourcing.event_store import EventStore
from event_sourcing.models import Event as EventPydantic # Alias to avoid conflict if Document is also used from Pydantic
from database import engine # For EventStore
from models.resource import Resource # For Resource Pydantic model


# Load environment variables
load_dotenv()

RESOURCE_DIR = "./resources"
QDRANT_COLLECTION_NAME = "lifeos_resources"

# Initialize EventStore globally for the script
event_store_instance = EventStore(engine=engine)

def create_resource_events():
    """
    Loads documents from the `resources/` directory, creates ResourceCreated events,
    and appends them to the event store.
    """
    # Load documents from the resources directory
    reader = SimpleDirectoryReader(RESOURCE_DIR)
    documents = reader.load_data()

    print(f"Number of documents read: {len(documents)}")

    for doc in documents:
        resource_id = str(uuid.uuid4())
        resource_content = doc.text
        resource_title = doc.metadata.get('file_name', f"Resource {resource_id[:8]}")
        resource_format = "file" # Defaulting to file format for now

        resource_data = Resource(
            id=resource_id,
            type="resource",
            title=resource_title,
            format=resource_format,
            body=resource_content,
            tags=[],
            related_zettels=[],
            horizon="resources"
        )

        event_payload = resource_data.model_dump()

        if isinstance(event_payload, str):
            event_payload = json.loads(event_payload)

        resource_created_event = EventPydantic(
            event_id=str(uuid.uuid4()),
            event_type="ResourceCreated",
            timestamp=datetime.now(timezone.utc),
            payload=event_payload,
            schema_version="1.0"
        )

        event_store_instance.append_event(
            event_id=resource_created_event.event_id,
            event_type=resource_created_event.event_type,
            payload=resource_created_event.payload,
            schema_version=resource_created_event.schema_version
        )
        print(f"Appended ResourceCreated event for resource_id: {resource_id}")

    print(f"Successfully created ResourceCreated events for all document and appended to the event store.")

if __name__ == "__main__":
    print("Creating ResourceCreated events from external resources...")
    create_resource_events()
    print("Script finished. Resources have been added to the event store Run event processor replay if needed.")
