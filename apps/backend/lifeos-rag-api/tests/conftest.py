import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Fallback mock for dateparser/llama_index if missing (environment issues)
try:
    import dateparser
except ImportError:
    from unittest.mock import MagicMock
    sys.modules["dateparser"] = MagicMock()
    sys.modules["dateparser.search"] = MagicMock()

try:
    import llama_index
except ImportError:
    from unittest.mock import MagicMock
    sys.modules["llama_index"] = MagicMock()
    sys.modules["llama_index.core"] = MagicMock()
    sys.modules["llama_index.core.llms"] = MagicMock()
    sys.modules["llama_index.vector_stores"] = MagicMock()
    sys.modules["llama_index.vector_stores.qdrant"] = MagicMock()

try:
    import redis
except ImportError:
    from unittest.mock import MagicMock
    sys.modules["redis"] = MagicMock()
    sys.modules["redis.asyncio"] = MagicMock()

try:
    import argon2
except ImportError:
    from unittest.mock import MagicMock
    sys.modules["argon2"] = MagicMock()
    sys.modules["argon2id"] = MagicMock()
