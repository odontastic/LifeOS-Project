import os
from typing import Literal
from dotenv import load_dotenv
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.llms.openai import OpenAI

# Load environment variables
load_dotenv()

# --- Schema Definition ---
# TODO: Implement Extraction Quality Control. The current implementation ingests
# all extracted data without any quality checks. A confidence score should be
# added to each extracted node and relationship, and a threshold should be used
# to filter out low-confidence extractions.

# Using typing.Literal to define the strict schema for entities and relationships
entities = Literal[
    "User", "JournalEntry", "Emotion", "Belief", "Trigger",
    "CopingMechanism", "Goal", "Episode", "Pattern", "SessionSummary"
]

relations = Literal[
    "AUTHORED_BY", "RELATES_TO", "TRIGGERED_BY", "PRACTICED",
    "PART_OF", "MENTIONS", "SUMMARIZES"
]

# A validation schema to enforce which relationships can connect which entities
validation_schema = {
    "User": ["PRACTICED", "RELATES_TO"],
    "JournalEntry": ["AUTHORED_BY", "PART_OF", "MENTIONS", "RELATES_TO"],
    "Emotion": ["TRIGGERED_BY", "RELATES_TO"],
    "Belief": ["RELATES_TO"],
    "Trigger": ["RELATES_TO"],
    "CopingMechanism": [],
    "Goal": [],
    "Episode": [],
    "Pattern": [],
    "SessionSummary": ["SUMMARIZES"],
}

# --- Extractor Initialization ---

def get_schema_extractor():
    """
    Initializes and returns the SchemaLLMPathExtractor configured with our
    therapeutic schema. This extractor is designed to be passed into a
    PropertyGraphIndex.
    """
    # Note: Ensure OPENAI_API_KEY is set in your .env file
    llm = OpenAI(model="gpt-4-turbo", temperature=0.1)

    extractor = SchemaLLMPathExtractor(
        llm=llm,
        possible_entities=entities,
        possible_relations=relations,
        kg_validation_schema=validation_schema,
        strict=True,  # Enforce the schema strictly
    )

    return extractor

# --- Testing ---

if __name__ == "__main__":
    # This block is for demonstrating that the extractor can be initialized.
    # The actual extraction process is now handled by the PropertyGraphIndex.
    print("Testing the initialization of the SchemaLLMPathExtractor...")

    try:
        extractor = get_schema_extractor()
        print("SchemaLLMPathExtractor initialized successfully.")
        # The attributes `possible_entities`, `possible_relations`, and `strict` are no longer
        # directly accessible on the extractor object in the current version of LlamaIndex.
        # The configuration is now internal to the object.
        print("\n--- Configuration ---")
        print("Extractor configured with the therapeutic schema.")
        print("---------------------\n")
    except Exception as e:
        print(f"Failed to initialize extractor: {e}")
