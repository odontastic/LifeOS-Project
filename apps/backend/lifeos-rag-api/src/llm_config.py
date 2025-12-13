# llm_config.py
"""Central configuration for LLM provider.

The backend can use either:
- a **local SLM** (e.g., Ollama) exposing an OpenAI‑compatible API, or
- **OpenRouter** for remote model access.

Environment variables (read from `.env`):
```
LLM_PROVIDER=local   # or "openrouter"
LOCAL_SLM_URL=http://localhost:11434/v1   # Ollama default endpoint
LOCAL_SLM_MODEL=llama3:8b                # model name as recognized by the server
OPENROUTER_API_KEY=your-key-here
```
"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local").lower()
LOCAL_SLM_URL = os.getenv("LOCAL_SLM_URL", "http://localhost:11434/v1")
LOCAL_SLM_MODEL = os.getenv("LOCAL_SLM_MODEL", "llama3:8b")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def get_llm():
    """Return an LLM client compatible with `llama_index.llms.openai.OpenAI`.

    - For ``local`` we point the OpenAI client at the local SLM endpoint.
    - For ``openrouter`` we use OpenRouter's base URL and API key.
    """
    from llama_index.llms.openai import OpenAI

    if LLM_PROVIDER == "local":
        return OpenAI(
            model=LOCAL_SLM_MODEL,
            base_url=LOCAL_SLM_URL,
            api_key="dummy",  # OpenAI client requires a key; dummy works for local servers
        )
    elif LLM_PROVIDER == "openrouter":
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is required when LLM_PROVIDER is 'openrouter'")
        return OpenAI(
            model="openrouter",  # placeholder; actual model chosen per request
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
