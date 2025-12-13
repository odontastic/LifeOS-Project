from datetime import datetime, timedelta
from typing import Dict, Any
import dateparser

def extract_semantic_filters_with_llm(query: str) -> Dict[str, Any]:
    """
    (Placeholder) Uses an LLM to extract non-date, semantic filters from a query.
    
    For example, "in college" -> {"life_stage": "College"}
    
    This needs to be implemented.
    """
    # TODO: Use a focused LLM call to extract entities like 'life_stage' or 'episode'
    # from the user's query to use as filters.
    semantic_filters = {}
    if "in college" in query.lower():
        semantic_filters["life_stage"] = "College"
    if "during my first job" in query.lower():
        semantic_filters["episode"] = "First Job"
        
    return semantic_filters

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
