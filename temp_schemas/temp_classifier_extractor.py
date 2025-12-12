import json
import uuid
from datetime import datetime

def generate_classification_and_extraction(input_note):
    """
    Simulates an LLM classifier and action extractor given an input note.
    This function will be replaced by actual LLM calls in a real implementation.
    """
    title = input_note.get("title", "")
    body = input_note.get("body", "")
    source = input_note.get("source", "manual")

    # --- Classification Logic (Simulated) ---
    # Determine type based on keywords or structure
    if "todo" in body.lower() or "next step" in body.lower():
        entity_type = "task"
        confidence = 0.9
    elif "idea" in body.lower() or "concept" in body.lower() or "theory" in body.lower():
        entity_type = "zettel"
        confidence = 0.85
    elif "project" in title.lower() or "outcome" in body.lower() or "deliverable" in body.lower():
        entity_type = "project"
        confidence = 0.95
    elif "area" in title.lower() or "responsibility" in body.lower():
        entity_type = "area"
        confidence = 0.9
    elif "reflection" in title.lower() or "mood" in body.lower() or "insights" in body.lower():
        entity_type = "reflection"
        confidence = 0.88
    elif "book" in title.lower() or "article" in body.lower() or "reference" in body.lower():
        entity_type = "resource"
        confidence = 0.8
    else:
        entity_type = "zettel" # Default to zettel if unclear
        confidence = 0.7

    # --- Extraction Logic (Simulated) ---
    suggested_title = title if title else body.split('\n')[0][:50] + "..."
    suggested_tags = []
    if entity_type == "zettel":
        suggested_tags.append("unprocessed_idea")
    if "urgent" in body.lower():
        suggested_tags.append("urgent")

    suggested_area_id = None
    suggested_project_id = None

    import re
    # ... (rest of the function remains the same until actionables extraction)
    
    import re
    # ... (rest of the function remains the same until actionables extraction)

    actionables = []

    # Regex to find all "Next step:" actionables
    next_step_pattern = re.compile(r"(?:next step:|next_step:)\s*(.*?)(?=\s*(?:next step:|next_step:|todo:|$))", re.IGNORECASE | re.DOTALL)
    for match in next_step_pattern.finditer(body):
        desc = match.group(1).strip()
        if desc:
            actionables.append({
                "desc": desc,
                "estimate": "30m",
                "context": "@Computer",
                "energy": "medium"
            })

    # Regex to find all "Todo:" actionables
    todo_pattern = re.compile(r"Todo:\s*(.*?)(?=\s*(?:next step:|next_step:|todo:|$))", re.IGNORECASE | re.DOTALL)
    for match in todo_pattern.finditer(body):
        desc = match.group(1).strip()
        if desc:
            actionables.append({
                "desc": desc,
                "estimate": "15m",
                "context": "@Home",
                "energy": "low"
            })
# ... (rest of the function remains the same)    
    # ... (rest of the function remains the same)

    output = {
        "type": entity_type,
        "confidence": confidence,
        "suggested_title": suggested_title,
        "suggested_tags": suggested_tags,
        "suggested_area_id": suggested_area_id,
        "suggested_project_id": suggested_project_id,
        "actionables": actionables
    }
    return output

if __name__ == "__main__":
    # Example Usage:
    mock_input_note_1 = {
        "title": "Idea for new feature",
        "body": "This is a great idea for a new feature in the LifeOS. It could involve integrating voice commands. Next step: Research existing voice command libraries.",
        "source": "mobile"
    }

    mock_input_note_2 = {
        "title": "Weekly meeting notes",
        "body": "Discussed Q1 roadmap. Todo: Follow up with John on API design. Todo: Draft initial UI mockups. Decision was made to prioritize search functionality.",
        "source": "meeting_notes"
    }
    
    mock_input_note_3 = {
        "title": "Thoughts on Neuroplasticity",
        "body": "The concept of neuroplasticity suggests that the brain is not fixed. This has profound implications for habit formation and personal growth. Need to explore links to Zettelkasten. Concept: Brain plasticity and learning.",
        "source": "brainstorm"
    }
    
    mock_input_note_4 = {
        "title": "New Project Proposal: AI Coach Integration",
        "body": "This project aims to integrate an AI Coach capable of daily nudges and weekly reviews. Desired Outcome: Users report increased adherence to personal growth routines. Why it matters: Enhances user engagement and long-term transformation. Success Criteria: 80% user retention over 3 months. Next step: Define core nudges.",
        "source": "email"
    }


    print("--- Mock Input 1 ---")
    output_1 = generate_classification_and_extraction(mock_input_note_1)
    print(json.dumps(output_1, indent=2))

    print("\n--- Mock Input 2 ---")
    output_2 = generate_classification_and_extraction(mock_input_note_2)
    print(json.dumps(output_2, indent=2))
    
    print("\n--- Mock Input 3 ---")
    output_3 = generate_classification_and_extraction(mock_input_note_3)
    print(json.dumps(output_3, indent=2))

    print("\n--- Mock Input 4 ---")
    output_4 = generate_classification_and_extraction(mock_input_note_4)
    print(json.dumps(output_4, indent=2))
