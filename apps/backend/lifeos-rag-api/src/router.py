from typing import List
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import QueryEngineTool

def get_router_query_engine(graph_query_engine, resource_query_engine):
    """
    Creates and returns a RouterQueryEngine that can route queries to either
    the main graph index or the external resource index.
    """
    # Create tools for each of the query engines
    graph_tool = QueryEngineTool.from_defaults(
        query_engine=graph_query_engine,
        name="graph_tool",
        description="Use this tool to answer questions about the user's journal entries, emotions, beliefs, and other personal experiences.",
    )
    resource_tool = QueryEngineTool.from_defaults(
        query_engine=resource_query_engine,
        name="resource_tool",
        description="Use this tool to answer questions about general knowledge, CBT techniques, and other psychoeducational topics.",
    )

    # Create the router query engine
    query_engine = RouterQueryEngine(
        selector=PydanticSingleSelector.from_defaults(),
        query_engine_tools=[graph_tool, resource_tool],
    )

    return query_engine
