import os
from dotenv import load_dotenv
from arango import ArangoClient
from arango.exceptions import ArangoClientError
import logging

# Load environment variables
load_dotenv(dotenv_path='apps/backend/lifeos-rag-api/.env')

ARANGODB_HOST = os.getenv("ARANGODB_HOST")
ARANGODB_DB_NAME = os.getenv("ARANGODB_DB_NAME")
ARANGODB_USER = os.getenv("ARANGODB_USER")
ARANGODB_PASSWORD = os.getenv("ARANGODB_PASSWORD")

logger = logging.getLogger(__name__)

# List of collections to be cleared/truncated
# This should be kept in sync with the collections used in EventProcessor and graph_db
COLLECTIONS_TO_TRUNCATE = [
    "LlamaNodes",
    "projects",
    "areas",
    "tasks",
    "goals",
    "reflections",
    "journal_entries",
    "emotions",
    "beliefs",
    "triggers",
    "contacts",
    # Edge collections
    "linked_emotion_to_contact",
    "linked_emotion_to_task",
    "links_knowledge_node",
    "generated_from"
]

def clear_arangodb_collections():
    """Connects to ArangoDB and truncates specified collections."""
    if not ARANGODB_HOST or not ARANGODB_DB_NAME or not ARANGODB_USER or not ARANGODB_PASSWORD:
        logger.error("Error: ArangoDB environment variables not fully set.")
        return

    try:
        client = ArangoClient(hosts=ARANGODB_HOST)
        db = client.db(ARANGODB_DB_NAME, username=ARANGODB_USER, password=ARANGODB_PASSWORD)
        logger.info(f"Successfully connected to ArangoDB database '{ARANGODB_DB_NAME}'.")

        for collection_name in COLLECTIONS_TO_TRUNCATE:
            try:
                if db.has_collection(collection_name):
                    collection = db.collection(collection_name)
                    collection.truncate()
                    logger.info(f"Collection '{collection_name}' truncated successfully.")
                else:
                    logger.info(f"Collection '{collection_name}' does not exist, skipping.")
            except Exception as e:
                logger.error(f"An error occurred while trying to truncate collection '{collection_name}': {e}")
    
    except ArangoClientError as e:
        logger.error(f"Failed to connect to ArangoDB client at {ARANGODB_HOST}: {e}")
    except Exception as e:
        logger.error(f"Failed to connect to ArangoDB database '{ARANGODB_DB_NAME}' or perform operations: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting ArangoDB cleanup...")
    clear_arangodb_collections()
    logger.info("ArangoDB cleanup finished.")