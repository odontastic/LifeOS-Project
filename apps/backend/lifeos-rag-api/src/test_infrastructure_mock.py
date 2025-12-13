import sys
import json
import asyncio
from unittest.mock import MagicMock

# Mock Redis
mock_redis_module = MagicMock()
sys.modules["redis"] = mock_redis_module
mock_redis_instance = MagicMock()
mock_redis_module.Redis.return_value = mock_redis_instance

# Mock LlamaIndex & Qdrant to avoid import errors or connections
sys.modules["llama_index.core"] = MagicMock()
sys.modules["llama_index.vector_stores.qdrant"] = MagicMock()
sys.modules["qdrant_client"] = MagicMock()
sys.modules["src.graph"] = MagicMock()
sys.modules["src.extractor"] = MagicMock()
sys.modules["src.deduplication"] = MagicMock()
sys.modules["src.temporal"] = MagicMock()
sys.modules["src.router"] = MagicMock()
sys.modules["src.synthesizer"] = MagicMock()

# Import main (requires relative imports to work, so run as module)
if __name__ == "__main__" and __package__ is None:
    # Hack for script execution
    import os
    # We prefer running with -m src.test_infrastructure_mock
    pass

from .main import health_check, start_flow, advance_flow, StartFlowRequest, AdvanceFlowRequest

def run_async(coro):
    return asyncio.run(coro)

def test_health_check():
    print("Testing /health endpoint...")
    # Mock Redis ping
    mock_redis_instance.ping.return_value = True
    
    # Run
    res = run_async(health_check())
    
    print(f"Health Status: {res}")
    if res["services"]["redis"] == "up":
        print("✅ Redis check passed.")
    else:
        print("❌ Redis check failed.")

def test_flow_persistence():
    print("\nTesting Flow Persistence (Redis)...")
    
    # 1. Start Flow
    req = StartFlowRequest(flow_type="daily_coaching")
    res = run_async(start_flow(req))
    
    flow_id = res["flow_id"]
    print(f"Started Flow ID: {flow_id}")
    
    # Verify Redis SET was called
    mock_redis_instance.set.assert_called()
    args, kwargs = mock_redis_instance.set.call_args
    # args[0] is key, args[1] is value
    if args[0] == f"flow:{flow_id}":
        print("✅ Redis SET called with correct Key.")
    
    saved_state = json.loads(args[1])
    if saved_state["current_step"] == "step_1_greeting":
         print("✅ Redis SET called with correct Initial State.")

    # 2. Advance Flow
    # Mock Redis GET to return the state we just "saved"
    mock_redis_instance.get.return_value = json.dumps(saved_state)
    
    adv_req = AdvanceFlowRequest(
        flow_id=flow_id,
        current_step="step_1_greeting",
        response="Anxious"
    )
    
    res_adv = run_async(advance_flow(adv_req))
    
    print(f"Advanced to: {res_adv['current_step']}")
    
    # Verify Redis SET called again with updated state
    # method calls list: set, get, set
    # check last call
    last_call_args = mock_redis_instance.set.call_args
    updated_state = json.loads(last_call_args[0][1])
    
    if updated_state["current_step"] == "step_2_explore_emotion":
        print("✅ Redis updated with new step.")
    if updated_state["context"]["emotion"] == "Anxious":
        print("✅ Redis stored user context (emotion).")

if __name__ == "__main__":
    try:
        test_health_check()
        test_flow_persistence()
        print("\n🎉 Infrastructure Mock Tests Passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
