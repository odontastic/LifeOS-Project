# A list of keywords that may indicate a user is in crisis.
# This list is not exhaustive and should be expanded upon.
CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "want to die", "hopeless",
    "self-harm", "cutting", "hurting myself", "end my life",
    "overdose", "depressed", "can't go on"
]

DEFAULT_DISCLAIMER = (
    "It sounds like you are going through a difficult time. "
    "Please consider reaching out to a professional for help. "
    "You can connect with people who can support you by calling or texting 988 anytime in the US and Canada. "
    "In the UK, you can call 111."
)

def detect_crisis_language(text: str) -> bool:
    """
    Detects crisis language in a given text using a keyword-based approach.

    Args:
        text: The input text to analyze.

    Returns:
        True if crisis language is detected, False otherwise.
    """
    lower_text = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in lower_text:
            return True
    return False
