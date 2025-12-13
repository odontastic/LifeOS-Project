from datetime import datetime, timedelta
from typing import Dict, Any
import dateparser
import json
import logging

from llama_index.core.llms import ChatMessage, MessageRole
from .llm_config import get_llm # Assuming get_llm returns a standard LLM client

logger = logging.getLogger(__name__)

# Define possible semantic entities to extract
SEMANTIC_ENTITIES = ["life_domain", "life_stage", "episode"]

SEMANTIC_EXTRACTION_PROMPT = """
You are an expert at identifying and extracting semantic filters from natural language queries.
Your task is to extract relevant concepts such as 'life_stage', 'life_domain', or 'episode' from the user's query.

Respond with a JSON object where keys are the semantic filter types and values are the extracted concepts.
If no relevant semantic filters are found, return an empty JSON object {{}}.
Do not include any other text or explanation.

Example:
Query: "What have I learned about relationships in college?"
Response: {{"life_domain": "Relationships", "life_stage": "College"}}

Query: "Show me my journal entries about work during my first job."
Response: {{"life_domain": "Work", "episode": "First Job"}}

Query: "Summarize my feelings last week."
Response: {{}}

Query: "{query}"
Response: 
"""

def extract_semantic_filters_with_llm(query: str) -> Dict[str, Any]:
    """
    Uses an LLM to extract non-date, semantic filters from a query.
    
    For example, "in college" -> {"life_stage": "College"}
    """
    llm = get_llm()
    prompt = SEMANTIC_EXTRACTION_PROMPT.format(query=query)
    
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
        ChatMessage(role=MessageRole.USER, content=prompt),
    ]

    try:
        response = llm.chat(messages)
        # Assuming the LLM responds with a JSON string
        semantic_filters = json.loads(response.message.content)
        # Validate extracted entities against SEMANTIC_ENTITIES
        valid_filters = {k: v for k, v in semantic_filters.items() if k in SEMANTIC_ENTITIES}
        if len(valid_filters) != len(semantic_filters):
            logger.warning(f"LLM extracted invalid semantic filters: {semantic_filters}. Validated: {valid_filters}")
        return valid_filters
    except Exception as e:
        logger.error(f"Failed to extract semantic filters with LLM: {e}", exc_info=True)
        return {}

def parse_time_references(query: str) -> Dict[str, Any]:
    """
    Parses a query for both natural language time references and semantic filters.

    Args:
        query: The user's query string.

    Returns:
        A dictionary containing filter parameters (e.g., start_date, life_stage).
    """
    # 1. Parse natural language dates (e.g., "last week", "since august")
    # Settings to prefer dates in the past.
    settings = {'PREFER_DATES_FROM': 'past'}
    found_dates = dateparser.search.search_dates(query, settings=settings)

    date_filters = {}
    if found_dates:
        # For simplicity, assume the first found date is the primary filter.
        # A more complex implementation could handle ranges.
        # e.g., "between last week and yesterday"
        primary_date = found_dates[0][1]
        
        # Heuristic to determine if it's a range or a single point.
        # "since", "after", "from" -> start_date
        if any(kw in query.lower() for kw in ["since", "after", "from"]):
            date_filters["start_date"] = primary_date.isoformat()
        # "before", "until" -> end_date
        elif any(kw in query.lower() for kw in ["before", "until", "up to"]):
            date_filters["end_date"] = primary_date.isoformat()
        # "in", "on", "during" -> approximate range (e.g., a full day)
        elif any(kw in query.lower() for kw in ["in", "on", "during"]):
            date_filters["start_date"] = primary_date.replace(hour=0, minute=0, second=0).isoformat()
            date_filters["end_date"] = primary_date.replace(hour=23, minute=59, second=59).isoformat()
        else:
            # Default to a start date for simple references like "last week"
            date_filters["start_date"] = primary_date.isoformat()

    # 2. Extract semantic filters (e.g., life stages)
    semantic_filters = extract_semantic_filters_with_llm(query)
    
    # 3. Combine filters
    all_filters = {**date_filters, **semantic_filters}
    
    return all_filters

if __name__ == "__main__":
    print("Testing the Temporal Middleware...")

    queries = [
        "What have I learned about my anxiety since last month?",
        "Show me journal entries about work before 2024-01-01.",
        "How did I feel during my first job?",
        "What was happening in college around May 2015?",
        "Summarize my thoughts on relationships in the last 6 months.",
    ]

    for query in queries:
        filters = parse_time_references(query)
        print(f"\nQuery: '{query}'")
        print(f"Parsed Filters: {filters}")

    print("\nTemporal Middleware test complete.")
