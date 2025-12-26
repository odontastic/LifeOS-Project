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

def get_arangodb_client():
    """
    Returns an ArangoDB client instance.
    """
    try:
        client = ArangoClient(hosts=ARANGODB_HOST)
        return client
    except ArangoClientError as e:
        logger.error(f"Failed to connect to ArangoDB client at {ARANGODB_HOST}: {e}")
        return None

def get_db_instance():
    """
    Returns a database instance, creating it if it doesn't exist.
    """
    client = get_arangodb_client()
    if not client:
        return None

    try:
        # Connect to _system database to create/access other databases
        sys_db = client.db("_system", username=ARANGODB_USER, password=ARANGODB_PASSWORD)
        
        if not sys_db.has_database(ARANGODB_DB_NAME): # Use ARANGODB_DB_NAME
            sys_db.create_database(ARANGODB_DB_NAME)
            logger.info(f"Database '{ARANGODB_DB_NAME}' created.")
        
        db = client.db(ARANGODB_DB_NAME, username=ARANGODB_USER, password=ARANGODB_PASSWORD)
        logger.info(f"Connected to ArangoDB database '{ARANGODB_DB_NAME}'.")
        return db
    except Exception as e:
        logger.error(f"Failed to get ArangoDB database '{ARANGODB_DB_NAME}': {e}")
        return None

# --- Example Graph Setup for LifeOS ---
LIFEOS_GRAPH_NAME = "lifeos_knowledge_graph"

# Edge definitions for the LifeOS knowledge graph
LIFEOS_EDGE_DEFINITIONS = [
    {
        "edge_collection": "linked_emotion_to_contact",
        "from_vertex_collections": ["EmotionEntry"], # These should be the actual collection names for read models
        "to_vertex_collections": ["ContactProfile"] # These should be the actual collection names for read models
    },
    {
        "edge_collection": "linked_emotion_to_task",
        "from_vertex_collections": ["EmotionEntry"],
        "to_vertex_collections": ["TaskItem"]
    },
    {
        "edge_collection": "links_knowledge_node",
        "from_vertex_collections": ["KnowledgeNode"],
        "to_vertex_collections": ["KnowledgeNode"]
    },
    {
        "edge_collection": "generated_from",
        "from_vertex_collections": ["SystemInsight"],
        "to_vertex_collections": ["EmotionEntry", "ContactProfile", "TaskItem", "KnowledgeNode"]
    },
]

def setup_arango_graph(db, graph_name: str, edge_definitions: list):
    """
    Sets up a named graph in ArangoDB with specified edge definitions.
    """
    try:
        if not db.has_graph(graph_name):
            graph = db.create_graph(graph_name)
            for edge_def in edge_definitions:
                graph.create_edge_definition(
                    edge_collection=edge_def["edge_collection"],
                    from_vertex_collections=edge_def["from_vertex_collections"],
                    to_vertex_collections=edge_def["to_vertex_collections"]
                )
            logger.info(f"Graph '{graph_name}' created with edge definitions.")
        else:
            graph = db.graph(graph_name)
            # Check for missing edge definitions and add them
            existing_edge_defs = {ed['edge_collection'] for ed in graph.edge_definitions()}
            for edge_def in edge_definitions:
                if edge_def["edge_collection"] not in existing_edge_defs:
                    graph.create_edge_definition(
                        edge_collection=edge_def["edge_collection"],
                        from_vertex_collections=edge_def["from_vertex_collections"],
                        to_vertex_collections=edge_def["to_vertex_collections"]
                    )
                    logger.info(f"Added edge definition '{edge_def['edge_collection']}' to graph '{graph_name}'.")
        return graph
    except Exception as e:
        logger.error(f"Failed to set up graph '{graph_name}': {e}")
        return None

def init_lifeos_graph():
    """
    Initializes the LifeOS knowledge graph in ArangoDB.
    """
    db = get_db_instance()
    if db:
        # Note: ARANGODB_DB from config is used by get_db_instance and setup_arango_graph indirectly
        return setup_arango_graph(db, LIFEOS_GRAPH_NAME, LIFEOS_EDGE_DEFINITIONS)
    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing ArangoDB graph for LifeOS...")
    graph = init_lifeos_graph()
    if graph:
        logger.info("ArangoDB graph initialized successfully.")
    else:
        logger.error("Failed to initialize ArangoDB graph.")
