from unittest.mock import MagicMock
import sys
from typing import Literal

# Mock OpenAI before importing extractor
sys.modules["llama_index.llms.openai"] = MagicMock()
sys.modules["llama_index.llms.openai"].OpenAI = MagicMock()

# Import the module to test
# Check if running as script
if __name__ == "__main__" and __package__ is None:
    from extractor import get_schema_extractor, entities, relations, validation_schema
else:
    from .extractor import get_schema_extractor, entities, relations, validation_schema


def test_configuration():
    print("Verifying Extractor Configuration...")
    
    # Check Entities
    expected_entities = {
        "User", "JournalEntry", "Emotion", "Belief", "Trigger", "CopingMechanism", "Episode", "Pattern", "SessionSummary",
        "Zettel", "Project", "Area", "Resource", "Task", "Reflection", "Goal"
    }
    # entities is a typing.Literal, so we check __args__
    actual_entities = set(entities.__args__)
    
    missing = expected_entities - actual_entities
    extra = actual_entities - expected_entities
    
    if missing:
        print(f"❌ Missing entities: {missing}")
    if extra:
        print(f"⚠️ Extra entities: {extra}")
    if not missing:
        print("✅ Entities configuration looks correct.")

    # Check Relations
    expected_relations = {
        "AUTHORED_BY", "RELATES_TO", "TRIGGERED_BY", "PRACTICED", "PART_OF", "MENTIONS", "SUMMARIZES",
        "HAS_ACTION", "RESPONSIBLE_FOR", "SUPPORTS"
    }
    actual_relations = set(relations.__args__)
    
    missing_rels = expected_relations - actual_relations
    if missing_rels:
        print(f"❌ Missing relations: {missing_rels}")
    else:
        print("✅ Relations configuration looks correct.")

    # Check Validation Schema
    if "Project" in validation_schema and "HAS_ACTION" in validation_schema["Project"]:
        print("✅ Validation Schema includes Productivity rules (Project -> HAS_ACTION).")
    else:
        print("❌ Validation Schema missing Productivity rules.")

    print("\nInitialization Test:")
    try:
        extractor = get_schema_extractor()
        print("✅ get_schema_extractor() called successfully (with mocked LLM).")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")

if __name__ == "__main__":
    test_configuration()
