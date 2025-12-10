import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

RESOURCE_DIR = "./resources"
QDRANT_COLLECTION_NAME = "lifeos_resources"

def create_resource_index():
    """
    Loads documents from the `resources/` directory, creates a VectorStoreIndex,
    and persists it to a new Qdrant collection.
    """
    # Initialize Qdrant client and vector store
    qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME
    )

    # Load documents from the resources directory
    reader = SimpleDirectoryReader(RESOURCE_DIR)
    documents = reader.load_data()

    # Create the VectorStoreIndex from the documents
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=vector_store.storage_context,
    )

    print(f"Successfully created and persisted the resource index in the '{QDRANT_COLLECTION_NAME}' collection.")
    print(f"Number of documents indexed: {len(documents)}")

    return index

if __name__ == "__main__":
    print("Creating the external resource index...")
    # This script should be run in an environment where Qdrant is accessible.
    # It is intended to be run as a one-off script to populate the index.
    # To run, execute `docker-compose up -d` and then run this script inside the `backend-api` container.
    # create_resource_index()
    print("Script finished. To run the indexing, uncomment the `create_resource_index()` call and execute this script in the correct environment.")
