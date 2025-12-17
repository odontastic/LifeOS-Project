from arango import ArangoClient
from arango.exceptions import DocumentInsertError, ArangoClientError, CollectionPropertiesError
import logging

from config import ARANGODB_HOST, ARANGODB_DB, ARANGODB_USER, ARANGODB_PASSWORD

logger = logging.getLogger(__name__)

# --- ArangoDB Client Setup ---
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
        
        if not sys_db.has_database(ARANGODB_DB):
            sys_db.create_database(ARANGODB_DB)
            logger.info(f"Database '{ARANGODB_DB}' created.")
        
        db = client.db(ARANGODB_DB, username=ARANGODB_USER, password=ARANGODB_PASSWORD)
        logger.info(f"Connected to ArangoDB database '{ARANGODB_DB}'.")
        return db
    except Exception as e:
        logger.error(f"Failed to get ArangoDB database '{ARANGODB_DB}': {e}")
        return None

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

# --- Example Graph Setup for LifeOS ---
LIFEOS_GRAPH_NAME = "lifeos_knowledge_graph"

# Edge definitions for the LifeOS knowledge graph
# This will evolve as more modules are integrated
LIFEOS_EDGE_DEFINITIONS = [
    {
        "edge_collection": "linked_emotion_to_contact",
        "from_vertex_collections": ["EmotionEntry"],
        "to_vertex_collections": ["ContactProfile"]
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
    # Add more edge definitions as relationships between entities are identified
]

def init_lifeos_graph():
    """
    Initializes the LifeOS knowledge graph in ArangoDB.
    """
    db = get_db_instance()
    if db:
        return setup_arango_graph(db, LIFEOS_GRAPH_NAME, LIFEOS_EDGE_DEFINITIONS)
    return None


