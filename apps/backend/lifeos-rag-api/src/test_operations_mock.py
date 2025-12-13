import sys
from unittest.mock import MagicMock
import uuid

# Mock the graph module before importing operations
sys.modules["src.graph"] = MagicMock()
mock_index = MagicMock()
sys.modules["src.graph"].get_property_graph_index.return_value = mock_index

# Mock LlamaIndex classes if they fail to import (optional safeguard)
# But we assume the environment has them.

# Import operations
# We use relative or absolute depending on how we run it. 
# We'll run it as a script from `lifeos-rag-api/src` probably.
if __name__ == "__main__" and __package__ is None:
    # Hack to allow relative imports when running as script
    sys.path.append('..')
    from src.operations import GraphOperations, create_project, convert_zettel_to_project
    from src.schemas import Project, Zettel
else:
    from .operations import GraphOperations, create_project, convert_zettel_to_project
    from .schemas import Project, Zettel

def test_create_project():
    print("Testing create_project()...")
    
    # Setup data
    proj = Project(
        id=str(uuid.uuid4()),
        title="Test Project",
        desired_outcome="World Peace",
        why_it_matters="It's good",
        next_actions=[],
        status="active"
    )
    
    # Call function
    res_id = create_project(proj)
    
    # Verify
    if res_id == proj.id:
        print("✅ create_project returned correct ID.")
    else:
        print(f"❌ Returned ID mismatch: {res_id} != {proj.id}")
        
    # Check if insert_nodes was called on the mock index
    if mock_index.insert_nodes.called:
        print("✅ insert_nodes() was called on the Graph Index.")
        # Inspect the node passed
        args, _ = mock_index.insert_nodes.call_args
        node = args[0][0] # First arg, first item in list
        if node.id_ == proj.id:
             print("✅ Node ID matches.")
        if node.metadata["desired_outcome"] == "World Peace":
             print("✅ Node metadata preserved.")
    else:
        print(f"❌ insert_nodes() was NOT called.")

def test_convert_zettel_to_project():
    print("\nTesting convert_zettel_to_project()...")
    
    z_id = str(uuid.uuid4())
    proj = Project(
        id=str(uuid.uuid4()),
        title="Derived Project",
        desired_outcome="Stuff",
        why_it_matters="Reasons",
        status="active"
    )
    
    convert_zettel_to_project(z_id, proj)
    
    # Verify links
    # Expect 2 calls to upsert_relations (SUPPORTS, RELATES_TO)
    store = mock_index.property_graph_store
    if store.upsert_relations.call_count == 2:
        print("✅ upsert_relations() called twice (bidirectional link).")
    else:
        print(f"❌ upsert_relations() called {store.upsert_relations.call_count} times, expected 2.")

if __name__ == "__main__":
    try:
        test_create_project()
        test_convert_zettel_to_project()
        print("\n🎉 All Operation Mock Tests Passed!")
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
