import re
from typing import List, Dict, Any, Tuple
from llama_index.core.graph_stores.types import GraphStore
from llama_index.core.schema import Node
from llama_index.core.graph_stores.types import Relationship

# Define which node labels should be checked for duplicates and what property to use as a unique key.
DEDUPE_CONFIG = {
    "User": "id",
    "Episode": "id",
    "Goal": "id",
    "Belief": "id",
    "Trigger": "id",
}

def normalize_text(text: str) -> str:
    """
    Normalizes text by converting to lowercase and removing non-alphanumeric characters (keeps spaces).
    """
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower().strip()

async def find_existing_node(graph_store: GraphStore, node: Node, normalized_value: str) -> Dict[str, Any]:
    """
    Queries the graph store to find an existing node that matches the given node
    based on a normalized property value.
    """
    label = node.label
    prop_key = DEDUPE_CONFIG[label]
    normalized_prop_key = f"normalized_{prop_key}"

    query = f"MATCH (n:{label} {{{normalized_prop_key}: $normalized_value}}) RETURN n"
    params = {"normalized_value": normalized_value}

    result, _ = await graph_store.arun_cypher_query(query, params)

    if result and len(result) > 0:
        return result[0][0]
    return None

async def deduplicate_and_merge(
    nodes: List[Node],
    relationships: List[Relationship],
    graph_store: GraphStore
) -> Tuple[List[Node], List[Relationship]]:
    """
    Processes extracted nodes and relationships to deduplicate entities against the
    existing graph using normalized properties, merging relationships to point to
    existing nodes where matches are found.
    """
    new_nodes = []
    node_map = {}  # Maps old temporary node IDs to new or existing node IDs

    # 1. Iterate through new nodes to find duplicates
    for node in nodes:
        label = node.label
        if label not in DEDUPE_CONFIG:
            node_map[node.id_] = node.id_
            new_nodes.append(node)
            continue

        prop_key = DEDUPE_CONFIG[label]
        if prop_key not in node.properties:
            node_map[node.id_] = node.id_
            new_nodes.append(node)
            continue

        prop_value = node.properties[prop_key]
        normalized_value = normalize_text(prop_value)

        existing_node = await find_existing_node(graph_store, node, normalized_value)

        if existing_node:
            # A duplicate was found. Map the old temp ID to the existing node's ID.
            existing_node_id = existing_node.get('element_id') or existing_node.get('id')
            node_map[node.id_] = existing_node_id
        else:
            # This is a new node. Add the normalized property before insertion.
            normalized_prop_key = f"normalized_{prop_key}"
            node.properties[normalized_prop_key] = normalized_value
            node_map[node.id_] = node.id_
            new_nodes.append(node)

    # 2. Re-wire relationships to point to the correct node IDs
    updated_relationships = []
    for rel in relationships:
        source_id = node_map.get(rel.source_node.id_, rel.source_node.id_)
        target_id = node_map.get(rel.target_node.id_, rel.target_node.id_)

        # Create a new Relationship object with the potentially updated source/target IDs
        updated_rel = Relationship(
            source_node_id=source_id,
            target_node_id=target_id,
            label=rel.label,
            properties=rel.properties,
        )
        updated_relationships.append(updated_rel)

    return new_nodes, updated_relationships
