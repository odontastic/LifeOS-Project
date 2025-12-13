import os
import logging
from typing import Set
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

from .config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, QDRANT_URL

logger = logging.getLogger(__name__)

class DataReconciler:
    def __init__(self):
        self.neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        self.qdrant_client = QdrantClient(host=QDRANT_URL.split('//')[1].split(':')[0], port=6333) # Assuming default Qdrant port

    def __del__(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()

    def get_neo4j_node_ids(self) -> Set[str]:
        """Retrieves all node IDs from Neo4j."""
        query = "MATCH (n) RETURN n.id AS id"
        with self.neo4j_driver.session() as session:
            result = session.run(query)
            return {r["id"] for r in result if r["id"] is not None}

    def get_qdrant_point_ids(self, collection_name: str) -> Set[str]:
        """Retrieves all point IDs from a specific Qdrant collection."""
        try:
            scroll_result = self.qdrant_client.scroll(
                collection_name=collection_name,
                limit=10000, # Adjust limit based on expected data size
                with_payload=False,
                with_vectors=False
            )
            # scroll_result returns tuples of (PointStruct, optional[bool])
            return {str(point.id) for point, _ in scroll_result[0]}
        except Exception as e:
            logger.error(f"Error fetching Qdrant IDs for collection {collection_name}: {e}")
            return set()

    def reconcile_data(self, qdrant_collection_name: str):
        """Reconciles IDs between Neo4j and a Qdrant collection."""
        logger.info(f"Starting reconciliation for Qdrant collection: {qdrant_collection_name}")

        neo4j_ids = self.get_neo4j_node_ids()
        qdrant_ids = self.get_qdrant_point_ids(qdrant_collection_name)

        # IDs in Neo4j but not in Qdrant (potential missing vectors)
        neo4j_only_ids = neo4j_ids - qdrant_ids
        if neo4j_only_ids:
            logger.warning(f"Found {len(neo4j_only_ids)} IDs in Neo4j but not in Qdrant '{qdrant_collection_name}': {list(neo4j_only_ids)[:10]}...")
            # TODO: Implement re-ingestion or specific handling for these IDs

        # IDs in Qdrant but not in Neo4j (potential dangling vectors)
        qdrant_only_ids = qdrant_ids - neo4j_ids
        if qdrant_only_ids:
            logger.warning(f"Found {len(qdrant_only_ids)} IDs in Qdrant '{qdrant_collection_name}' but not in Neo4j: {list(qdrant_only_ids)[:10]}...")
            # TODO: Implement deletion from Qdrant for these IDs
            # self.qdrant_client.delete(collection_name=qdrant_collection_name, points=list(qdrant_only_ids))
            # logger.info(f"Deleted {len(qdrant_only_ids)} dangling points from Qdrant collection '{qdrant_collection_name}'.")
        
        if not neo4j_only_ids and not qdrant_only_ids:
            logger.info("No discrepancies found. Data is consistent.")
        else:
            logger.info("Reconciliation process completed with discrepancies noted.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reconciler = DataReconciler()
    # Assuming 'lifeos_notes' is the primary collection for graph nodes
    reconciler.reconcile_data(qdrant_collection_name="lifeos_notes")
    # If you have other Qdrant collections that need reconciliation, call it again
    # reconciler.reconcile_data(qdrant_collection_name="lifeos_resources")
