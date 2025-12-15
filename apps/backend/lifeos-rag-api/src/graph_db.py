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

# --- Vertex and Edge Operations ---
def insert_vertex(graph, collection_name: str, data: dict):
    """
    Inserts a vertex into the specified collection.
    """
    try:
        collection = graph.vertex_collection(collection_name)
        if not collection.has(data["_key"]): # ArangoDB uses _key for document handle
            result = collection.insert(data)
            logger.debug(f"Inserted vertex into '{collection_name}': {result['_key']}")
            return result
        logger.debug(f"Vertex with _key '{data['_key']}' already exists in '{collection_name}'. Skipping.")
        return collection.get(data["_key"]) # Return existing document
    except DocumentInsertError as e:
        logger.error(f"Failed to insert vertex into '{collection_name}': {e}")
        return None
    except CollectionPropertiesError as e:
        logger.warning(f"Collection '{collection_name}' does not exist in graph '{graph.name}'. Attempting to create.")
        db = graph.db
        if not db.has_collection(collection_name):
            db.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")
            return insert_vertex(graph, collection_name, data) # Retry insertion
        logger.error(f"Collection '{collection_name}' does not exist and could not be created or is not a vertex collection: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while inserting vertex into '{collection_name}': {e}")
        return None

def insert_edge(graph, edge_collection_name: str, from_vertex_key: str, to_vertex_key: str, data: dict = None):
    """
    Inserts an edge between two vertices.
    """
    try:
        edge_collection = graph.edge_collection(edge_collection_name)
        # Assuming _key is passed in data for from/to, or can be constructed
        edge_data = data if data is not None else {}
        
        # Check if edge already exists to prevent duplicates (simplified check)
        # A more robust check might query for existing edges between specific _from and _to
        # For now, rely on ArangoDB to handle unique key constraints if _key is provided in data
        
        # Ensure _from and _to are correct ArangoDB document handles (collection/key)
        # This requires knowing the vertex collection names
        # Simplified: assume from_vertex_key and to_vertex_key are _key values, and we'll construct _from/_to later.
        
        # To insert an edge, we need the full document IDs like "collection_name/key"
        from_doc_id = f"{data['from_collection']}/{from_vertex_key}" if 'from_collection' in data else from_vertex_key
        to_doc_id = f"{data['to_collection']}/{to_vertex_key}" if 'to_collection' in data else to_vertex_key
        
        # Remove temporary collection names from data
        edge_data.pop('from_collection', None)
        edge_data.pop('to_collection', None)

        result = edge_collection.insert({"_from": from_doc_id, "_to": to_doc_id, **edge_data})
        logger.debug(f"Inserted edge into '{edge_collection_name}': {result['_key']}")
        return result
    except DocumentInsertError as e:
        if "unique constraint violated" in str(e):
            logger.debug(f"Edge already exists between {from_doc_id} and {to_doc_id}. Skipping.")
            return None # Or retrieve existing edge
        logger.error(f"Failed to insert edge into '{edge_collection_name}': {e}")
        return None
    except CollectionPropertiesError as e:
        logger.warning(f"Edge collection '{edge_collection_name}' does not exist in graph '{graph.name}'. Check graph setup.")
        logger.error(f"Failed to insert edge into '{edge_collection_name}': {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while inserting edge into '{edge_collection_name}': {e}")
        return None
