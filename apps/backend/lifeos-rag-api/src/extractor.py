import os
from typing import Literal
from dotenv import load_dotenv
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.core.prompts import PromptTemplate
from llm_config import get_llm

# Load environment variables
load_dotenv()

EXTRACTION_PROMPT_VERSION = "1.0.0"

# --- Custom Prompt for Confidence Score ---
EXTRACTION_PROMPT_TEMPLATE = """
You are a highly intelligent knowledge graph builder.
Given the text below, extract entities and relationships according to the provided schema.

For each extracted relationship, you MUST provide a confidence score on a scale of 0 to 1.
A score of 1.0 means you are absolutely certain.
A score of 0.0 means you are completely uncertain.

Output the results as a single, valid JSON array of objects. Each object should have the following format:
{{
  "subject": "<name of subject entity>",
  "relationship": "<name of relationship>",
  "object": "<name of object entity>",
  "confidence": <confidence_score_float>
}}

Do NOT return any objects that you are not reasonably confident about (e.g., confidence < 0.5).
Do not add any explanations or introductory text. Just the JSON array.

Schema:
Entities: {entities}
Relationships: {relations}

Text:
{text}
"""


# --- Schema Definition ---
# TODO: Implement Extraction Quality Control. The current implementation ingests
# all extracted data without any quality checks. A confidence score should be
# added to each extracted node and relationship, and a threshold should be used
# to filter out low-confidence extractions.

# Using typing.Literal to define the strict schema for entities and relationships
# Includes both Therapeutic (Journaling) and Productivity (PARA+GTD) modules
entities = Literal[
    "User", "JournalEntry", "Emotion", "Belief", "Trigger", "CopingMechanism", "Episode", "Pattern", "SessionSummary",
    "Zettel", "Project", "Area", "Resource", "Task", "Reflection", "Goal"
]

relations = Literal[
    "AUTHORED_BY", "RELATES_TO", "TRIGGERED_BY", "PRACTICED", "PART_OF", "MENTIONS", "SUMMARIZES",
    "HAS_ACTION", "RESPONSIBLE_FOR", "SUPPORTS"
]

# A validation schema to enforce which relationships can connect which entities
validation_schema = {
    # Therapeutic Module
    "User": ["PRACTICED", "RELATES_TO"],
    "JournalEntry": ["AUTHORED_BY", "PART_OF", "MENTIONS", "RELATES_TO"],
    "Emotion": ["TRIGGERED_BY", "RELATES_TO"],
    "Belief": ["RELATES_TO"],
    "Trigger": ["RELATES_TO"],
    "CopingMechanism": [],
    "Episode": [],
    "Pattern": [],
    "SessionSummary": ["SUMMARIZES"],

    # Productivity Module
    "Zettel": ["RELATES_TO", "SUPPORTS"],
    "Project": ["HAS_ACTION", "RELATES_TO"],
    "Area": ["RESPONSIBLE_FOR", "RELATES_TO"],
    "Resource": ["RELATES_TO"],
    "Task": ["RELATES_TO"],
    "Reflection": ["RELATES_TO"],
    "Goal": ["RELATES_TO"],
}

# --- Extractor Initialization ---

def get_schema_extractor():
    """
    Initializes and returns the SchemaLLMPathExtractor configured with our
    combined Therapeutic + Productivity schema.
    """
    # Use the configurable LLM provider (Local or OpenRouter)
    llm = get_llm()

    extractor = SchemaLLMPathExtractor(
        llm=llm,
        prompt_template=EXTRACTION_PROMPT_TEMPLATE,
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
        print("Extractor configured with the combined Therapeutic + Productivity schema.")
        print("---------------------\n")
    except Exception as e:
        print(f"Failed to initialize extractor: {e}")
