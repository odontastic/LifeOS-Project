import os
from dotenv import load_dotenv
from llama_index.core import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Load environment variables from .env file
load_dotenv()

def get_property_graph_index(kg_extractors=None):
    """
    Initializes and returns the PropertyGraphIndex, connecting to Neo4j and Qdrant.
    """
    # Initialize Qdrant client and vector store
    qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="lifeos_notes")

    # Initialize Neo4j graph store
    graph_store = Neo4jPropertyGraphStore(
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        url=os.getenv("NEO4J_URI"),
    )

    # Create the PropertyGraphIndex
    index = PropertyGraphIndex(
        nodes=[],  # We will populate this during ingestion
        edges=[],  # We will populate this during ingestion
        property_graph_store=graph_store,
        vector_store=vector_store,
        kg_extractors=kg_extractors,
    )

    return index

if __name__ == "__main__":
    # This block is for demonstrating that the get_property_graph_index function can be called.
    # To fully test the connection, run this script in an environment where the
    # Qdrant and Neo4j databases are accessible (e.g., inside the Docker container).
    print("This script is for initializing the PropertyGraphIndex.")
    print("To test the connection to the databases, please run `docker-compose up` and then")
    print("execute this script within the `backend-api` container.")
    # The following code is commented out to prevent connection errors when running locally.
    # print("Initializing PropertyGraphIndex...")
    # index = get_property_graph_index()
    # print("PropertyGraphIndex initialized successfully.")
    # print(f"Graph Store: {index.property_graph_store}")
    # print(f"Vector Store: {index.vector_store}")
