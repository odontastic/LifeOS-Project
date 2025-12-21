from arango.database import StandardDatabase
from arango.exceptions import DocumentInsertError, DocumentDeleteError, DocumentUpdateError, CollectionCreateError
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ArangoDBService:
    def __init__(self, arangodb_db: StandardDatabase):
        self.db = arangodb_db

    def create_collection_if_not_exists(self, collection_name: str, edge: bool = False):
        """Ensures a collection (or edge collection) exists, creates it if not."""
        try:
            if not self.db.has_collection(collection_name):
                if edge:
                    self.db.create_edge_collection(collection_name)
                    logger.info(f"ArangoDB edge collection '{collection_name}' created.")
                else:
                    self.db.create_collection(collection_name)
                    logger.info(f"ArangoDB document collection '{collection_name}' created.")
            else:
                logger.debug(f"ArangoDB collection '{collection_name}' already exists.")
        except CollectionCreateError as e:
            logger.error(f"Error creating ArangoDB collection '{collection_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error checking/creating ArangoDB collection '{collection_name}': {e}")
            raise

    def upsert_vertex(self, collection_name: str, vertex_data: Dict[str, Any], key: Optional[str] = None):
        """
        Inserts or updates a vertex in the specified collection.
        If key is provided, it attempts to update an existing vertex or insert a new one with that key.
        """
        try:
            # Ensure collection exists before upserting
            self.create_collection_if_not_exists(collection_name)
            
            collection = self.db.collection(collection_name)
            if key:
                vertex_data['_key'] = str(key) # Ensure key is a string
            
            # ArangoDB's `insert` with `overwrite=True` or `_key` handling behaves as upsert for document collections
            result = collection.insert(vertex_data, overwrite=True, return_new=True)
            logger.info(f"Upserted vertex with key '{result['_key']}' in collection '{collection_name}'.")
            return result
        except DocumentInsertError as e:
            logger.error(f"Error upserting vertex in collection '{collection_name}' with data {vertex_data}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error upserting vertex in collection '{collection_name}': {e}")
            raise

    def delete_vertex(self, collection_name: str, key: str):
        """Deletes a vertex from the specified collection by its key."""
        try:
            collection = self.db.collection(collection_name)
            collection.delete(str(key), return_old=False)
            logger.info(f"Deleted vertex with key '{key}' from collection '{collection_name}'.")
        except DocumentDeleteError as e:
            logger.error(f"Error deleting vertex with key '{key}' from collection '{collection_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting vertex with key '{key}' from collection '{collection_name}': {e}")
            raise

    def upsert_edge(self, collection_name: str, from_vertex_key: str, to_vertex_key: str, edge_data: Optional[Dict[str, Any]] = None):
        """
        Inserts or updates an edge in the specified edge collection.
        Requires _from and _to attributes.
        """
        try:
            # Ensure edge collection exists
            self.create_collection_if_not_exists(collection_name, edge=True)
            
            edge_collection = self.db.edge_collection(collection_name)
            
            full_edge_data = {
                '_from': str(from_vertex_key),
                '_to': str(to_vertex_key),
                **(edge_data if edge_data else {}) # Merge additional edge data
            }
            
            # Create a unique key for the edge if not provided, to enable upsert logic
            # A common pattern is to combine _from and _to
            edge_key = f"{from_vertex_key}_{to_vertex_key}".replace("/", "_") 
            full_edge_data['_key'] = edge_key

            result = edge_collection.insert(full_edge_data, overwrite=True, return_new=True)
            logger.info(f"Upserted edge with key '{result['_key']}' in collection '{collection_name}'.")
            return result
        except DocumentInsertError as e:
            logger.error(f"Error upserting edge in collection '{collection_name}' from '{from_vertex_key}' to '{to_vertex_key}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error upserting edge in collection '{collection_name}': {e}")
            raise

    def delete_edge(self, collection_name: str, key: str):
        """Deletes an edge from the specified edge collection by its key."""
        try:
            edge_collection = self.db.edge_collection(collection_name)
            edge_collection.delete(str(key), return_old=False)
            logger.info(f"Deleted edge with key '{key}' from collection '{collection_name}'.")
        except DocumentDeleteError as e:
            logger.error(f"Error deleting edge with key '{key}' from collection '{collection_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting edge with key '{key}' from collection '{collection_name}': {e}")
            raise

    # --- Specific Model Handlers for EventProcessor ---
    
    def update_system_insight(self, insight_id: str, user_id: str, feedback_type: str, comment: str, timestamp: Any):
        """Updates a SystemInsight vertex with feedback data."""
        data = {
            "user_id": user_id,
            "feedback_type": feedback_type,
            "comment": comment,
            "timestamp": timestamp,
            "updated_at": timestamp
        }
        return self.upsert_vertex("SystemInsight", data, key=insight_id)

    def create_or_update_contact(self, contact_id: str, user_id: str, name: str, email: Optional[str], phone: Optional[str], created_at: Any, updated_at: Any):
        """Creates or updates a ContactProfile vertex."""
        data = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "created_at": created_at,
            "updated_at": updated_at
        }
        return self.upsert_vertex("ContactProfile", data, key=contact_id)
