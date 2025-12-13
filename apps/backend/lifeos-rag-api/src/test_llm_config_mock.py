import os
import sys
from unittest.mock import MagicMock
import importlib

# Mock LlamaIndex OpenAI class BEFORE importing anything else
mock_openai_class = MagicMock()
sys.modules["llama_index.llms.openai"] = MagicMock()
sys.modules["llama_index.llms.openai"].OpenAI = mock_openai_class

# Helper to get the module for reloading
def get_config_module():
    if __package__:
        from . import llm_config
        return llm_config
    else:
        import llm_config
        return llm_config

# Import configuration for the first time
if __name__ == "__main__" and __package__ is None:
    # Set environment variables for testing
    os.environ["LLM_PROVIDER"] = "local"
    # ... other vars
    from llm_config import get_llm
else:
    from .llm_config import get_llm

def test_local_provider_config():
    print("Testing 'local' provider configuration...")
    mock_openai_class.reset_mock()
    
    # Reload config to pick up new env vars
    config_module = get_config_module()
    
    os.environ["LLM_PROVIDER"] = "local"
    os.environ["LOCAL_SLM_URL"] = "http://test-local:1234/v1"
    os.environ["LOCAL_SLM_MODEL"] = "test-model"
    
    importlib.reload(config_module)
    
    # Call the function from the reloaded module
    llm = config_module.get_llm()
    
    # Verify OpenAI was initialized with correct params
    mock_openai_class.assert_called_with(
        model="test-model",
        base_url="http://test-local:1234/v1",
        api_key="dummy"
    )
    print("✅ Local provider configured correctly.")

def test_openrouter_provider_config():
    print("Testing 'openrouter' provider configuration...")
    mock_openai_class.reset_mock()
    
    config_module = get_config_module()
    
    os.environ["LLM_PROVIDER"] = "openrouter"
    os.environ["OPENROUTER_API_KEY"] = "sk-test-key"
    
    importlib.reload(config_module)
    
    llm = config_module.get_llm()
    
    mock_openai_class.assert_called_with(
        model="openrouter",
        base_url="https://openrouter.ai/api/v1",
        api_key="sk-test-key"
    )
    print("✅ OpenRouter provider configured correctly.")

if __name__ == "__main__":
    try:
        test_local_provider_config()
        test_openrouter_provider_config()
        print("\n🎉 All LLM Config Tests Passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
