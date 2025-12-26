import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv(dotenv_path='apps/backend/lifeos-rag-api/.env')

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# List of collections to be cleared/deleted
# This should be kept in sync with the collections used in EventProcessor
COLLECTIONS_TO_DELETE = [
    "zettels",
    "projects",
    "areas",
    "resources",
    "tasks",
    "goals",
    "reflections",
    "journal_entries",
    "lifeos_resources", # This was the old collection name, might still exist
]

def clear_qdrant_collections():
    """Connects to Qdrant and deletes specified collections."""
    if not QDRANT_URL:
        print("Error: QDRANT_URL environment variable not set.")
        return

    try:
        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        print("Successfully connected to Qdrant.")

        for collection_name in COLLECTIONS_TO_DELETE:
            try:
                # Check if collection exists before trying to delete
                # This now returns a `CollectionInfo` object, check its `status`
                collection_info = qdrant_client.get_collection(collection_name=collection_name)
                if collection_info:
                     qdrant_client.delete_collection(collection_name=collection_name)
                     print(f"Collection '{collection_name}' deleted successfully.")
                else:
                     print(f"Collection '{collection_name}' does not exist, skipping.")
            except Exception as e:
                # Handle cases where the collection doesn't exist gracefully
                if "not found" in str(e).lower() or "404" in str(e):
                    print(f"Collection '{collection_name}' does not exist, skipping.")
                else:
                    print(f"An error occurred while trying to delete collection '{collection_name}': {e}")
    
    except Exception as e:
        print(f"Failed to connect to Qdrant or perform operations: {e}")

if __name__ == "__main__":
    print("Starting Qdrant cleanup...")
    clear_qdrant_collections()
    print("Qdrant cleanup finished.")
