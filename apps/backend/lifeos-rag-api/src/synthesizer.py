from typing import Any, Dict
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate

# A Pydantic model for the structured output
from pydantic import BaseModel

class MentalModel(BaseModel):
    """A structured mental model for understanding a user's situation."""
    challenge: str
    core_value_conflict: str
    proposed_framework: str
    actionable_advice: str

DEFAULT_SYNTHESIS_PROMPT = PromptTemplate(
    "You are a compassionate and insightful AI life coach. Your goal is to help the user "
    "understand their situation by synthesizing the provided context into a structured mental model.\n\n"
    "## Context\n"
    "The user is currently facing the following situation:\n"
    "{context_str}\n\n"
    "## Instructions\n"
    "Based on the context, please generate a structured mental model that includes:\n"
    "1.  **challenge:** A brief, one-sentence summary of the core challenge the user is facing.\n"
    "2.  **core_value_conflict:** An analysis of the conflict between the user's desires and their core values.\n"
    "3.  **proposed_framework:** A relevant psychological or philosophical framework (e.g., 'Locus of Control', 'Cognitive Dissonance') that can help the user understand their situation.\n"
    "4.  **actionable_advice:** A single, concrete piece of advice the user can act on.\n\n"
    "## Output\n"
    "Please provide your output in a JSON format that adheres to the `MentalModel` schema."
)

class FrameworkSynthesizer:
    """
    A synthesizer that takes retrieved context and generates a structured mental model.
    """
    def __init__(self, llm=None, prompt_template=None):
        self.llm = llm or OpenAI(model="gpt-4-turbo")
        self.prompt_template = prompt_template or DEFAULT_SYNTHESIS_PROMPT

    def synthesize(self, context: str) -> Dict[str, Any]:
        """
        Generates a structured mental model from the given context.
        """
        prompt = self.prompt_template.format(context_str=context)
        response = self.llm.complete(prompt)

        # In a real implementation, you would use a JSON output parser here.
        # For now, we will assume the LLM returns a valid JSON string.
        try:
            mental_model = MentalModel.parse_raw(response.text)
            return mental_model.dict()
        except Exception as e:
            # Fallback for when the LLM does not return valid JSON
            return {
                "error": "Failed to generate a structured mental model.",
                "details": str(e),
                "raw_response": response.text,
            }

if __name__ == "__main__":
    # This block is for demonstrating that the FrameworkSynthesizer can be initialized.
    # To fully test the synthesizer, you will need to have an OpenAI API key set up
    # in your environment.
    print("This script is for initializing the FrameworkSynthesizer.")
    print("To test the synthesizer, please set the OPENAI_API_KEY environment variable.")
    # The following code is commented out to prevent authentication errors when running locally.
    # print("Testing the FrameworkSynthesizer...")
    # synthesizer = FrameworkSynthesizer()
    # sample_context = (
    #     "The user is feeling stressed about a project deadline. They have a core belief "
    #     "that they need to be perfect, which is causing them to procrastinate. This is "
    #     "in conflict with their desire to do a good job and their core value of diligence."
    # )
    # mental_model = synthesizer.synthesize(sample_context)
    # print("\n--- Generated Mental Model ---")
    # import json
    # print(json.dumps(mental_model, indent=2))
    # print("----------------------------\n")
