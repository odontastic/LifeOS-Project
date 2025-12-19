from sqlalchemy.engine import Engine
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from qdrant_client import QdrantClient
from arango import ArangoClient
import logging

logger = logging.getLogger(__name__)

# Global instances - will be initialized in main.py's startup event
event_store_instance: EventStore = None
event_processor_instance: EventProcessor = None
_qdrant_client_instance: QdrantClient = None
_arangodb_graph = None # ArangoDB graph instance

async def initialize_dependencies(engine: Engine, qdrant_url: str, qdrant_api_key: str, arangodb_host: str, arangodb_db: str, arangodb_user: str, arangodb_password: str):
    global event_store_instance, event_processor_instance, _qdrant_client_instance, _arangodb_graph

    # Initialize EventStore
    event_store_instance = EventStore(engine=engine)

    # Initialize Qdrant client
    try:
        _qdrant_client_instance = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        logger.info("Qdrant client initialized successfully in dependencies.")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client in dependencies: {e}")

    # Initialize ArangoDB client and database (not the graph directly here)
    try:
        # ArangoClient handles connection pool to the ArangoDB server
        arango_client = ArangoClient(hosts=arangodb_host)
        sys_db = arango_client.db('_system', username=arangodb_user, password=arangodb_password)
        
        # Check if the desired database exists, create if not
        if not sys_db.has_database(arangodb_db):
            sys_db.create_database(arangodb_db)
        
        # Get the database instance
        _arangodb_graph = arango_client.db(arangodb_db, username=arangodb_user, password=arangodb_password)
        logger.info("ArangoDB client and database initialized successfully in dependencies.")

    except Exception as e:
        logger.error(f"Failed to initialize ArangoDB client/database in dependencies: {e}")
        _arangodb_graph = None # Ensure it's None if initialization fails

    # Initialize EventProcessor
    event_processor_instance = EventProcessor(
        event_store=event_store_instance,
        engine=engine,
        qdrant_client=_qdrant_client_instance,
        arangodb_db=_arangodb_graph # Pass the initialized ArangoDB database object
    )
    event_processor_instance.replay_events()
    logger.info("Event processor replayed all events to build read models in dependencies.")


# Dependency to get the EventStore instance
def get_event_store() -> EventStore:
    if event_store_instance is None:
        raise RuntimeError("EventStore not initialized. Ensure startup_event runs.")
    return event_store_instance

# Dependency to get the EventProcessor instance
def get_event_processor() -> EventProcessor:
    if event_processor_instance is None:
        raise RuntimeError("EventProcessor not initialized. Ensure startup_event runs.")
    return event_processor_instance

# Dependency to get the Qdrant client instance
def get_qdrant_client() -> QdrantClient:
    if _qdrant_client_instance is None:
        raise RuntimeError("Qdrant client not initialized. Ensure startup_event runs.")
    return _qdrant_client_instance

# Dependency to get the ArangoDB graph instance
def get_arangodb_db():
    if _arangodb_graph is None:
        raise RuntimeError("ArangoDB client not initialized. Ensure startup_event runs.")
    return _arangodb_graph
