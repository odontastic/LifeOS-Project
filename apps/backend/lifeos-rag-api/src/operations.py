import logging
from typing import Optional, Dict, Any, List
from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
from llama_index.core.graph_stores.types import Relation

from .graph import get_property_graph_index
from .schemas import BaseNode, Zettel, Project, Area, Resource, Task, Reflection, Goal, JournalEntry, Emotion, Belief, Trigger, CopingMechanism

logger = logging.getLogger(__name__)

class GraphOperations:
    def __init__(self):
        self.index = get_property_graph_index()
        # Ensure we have a retriever/query engine if we need to fetch items?
        # For operations, we primarily need the property_graph_store

    def create_entity(self, entity: BaseNode) -> str:
        """
        Creates a new entity in the Knowledge Graph.
        Converts the Pydantic model to a LlamaIndex TextNode and inserts it.
        Returns the entity ID.
        """
        # 1. Prepare metadata from the entity fields
        # Exclude 'id' and 'body' from metadata if they are identifying or main content
        metadata = entity.model_dump(exclude_none=True)
        
        # Determine the main text content. 
        # For most nodes, it's 'body', 'description', or 'title'.
        text_content = ""
        if hasattr(entity, "body") and entity.body:
            text_content = entity.body
        elif hasattr(entity, "description") and entity.description:
            text_content = entity.description
        elif hasattr(entity, "statement") and entity.statement: # For Beliefs
            text_content = entity.statement
        elif hasattr(entity, "title"):
            text_content = entity.title
        else:
            text_content = str(entity)

        # 2. Create LlamaIndex TextNode
        # We explicitly set the node ID to match the entity ID
        node = TextNode(
            text=text_content,
            id_=entity.id,
            metadata=metadata
        )
        
        # 3. Insert into the index
        # insert_nodes handles both vector store and graph store insertion
        self.index.insert_nodes([node])
        
        logger.info(f"Created entity {entity.type}:{entity.id}")
        return entity.id

    def link_entities(self, source_id: str, target_id: str, relation_type: str) -> None:
        """
        Creates a directional relationship between two entities.
        source_id -[relation_type]-> target_id
        """
        # We can construct a Relation object
        # Note: LlamaIndex PropertyGraphIndex manages relations via the store or `insert_nodes` with relations.
        # But `insert_nodes` expects nodes to implicitly have relations or extracting them.
        # Direct edge insertion might need access to the underlying graph store.
        
        # Getting the underlying store
        graph_store = self.index.property_graph_store
        
        # We need to ensure nodes exist, but for now we assume they do or the store handles it.
        # We create a Relation
        relation = Relation(
            source_id=source_id,
            target_id=target_id,
            label=relation_type,
        )
        
        # Insert the relationship (works if the store supports it directly)
        # Note: LlamaIndex `PropertyGraphStore` usually has `upsert_relations` or `put` methods?
        # Let's use the high level `insert_relationships` if available or `upsert_relations`.
        # PropertyGraphStore protocol usually has `upsert_relations`.
        
        # Actually `PropertyGraphIndex` does not expose `upsert_relations` directly in high level API easily 
        # without passing the nodes. exist.
        # But we can access `graph_store.upsert_relations`.
        
        graph_store.upsert_relations([relation])
        logger.info(f"Linked {source_id} -[{relation_type}]-> {target_id}")

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves an entity's metadata/properties from the graph.
        """
        # We can try retrieving from the vector store or graph store.
        # Graph store `get` depends on implementation.
        # Let's try vector_store.get_nodes if available, or graph_store.get(ids=...)
        
        nodes = self.index.vector_store.get_nodes([entity_id])
        if nodes and len(nodes) > 0:
            return nodes[0].metadata
        return None

# --- Convenience Functions ---

def create_zettel(data: Zettel) -> str:
    ops = GraphOperations()
    return ops.create_entity(data)

def create_project(data: Project) -> str:
    ops = GraphOperations()
    return ops.create_entity(data)

def create_task(data: Task) -> str:
    ops = GraphOperations()
    return ops.create_entity(data)

def convert_zettel_to_project(zettel_id: str, project_data: Project) -> str:
    """
    Bridging Rule: Converts a Zettel concept into an active Project.
    1. Create the Project.
    2. Link Zettel -[SUPPORTS]-> Project
    3. Link Project -[RELATES_TO]-> Zettel
    """
    ops = GraphOperations()
    
    # Create Project
    project_id = ops.create_entity(project_data)
    
    # Create bidirectional links
    ops.link_entities(zettel_id, project_id, "SUPPORTS")
    ops.link_entities(project_id, zettel_id, "RELATES_TO")
    
    return project_id
