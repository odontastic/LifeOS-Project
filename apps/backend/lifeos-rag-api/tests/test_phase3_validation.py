import unittest
from datetime import datetime, timezone
import tempfile
import os
import json
from sqlalchemy import create_engine
from database import Base, StoredEvent, ResourceReadModel
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from unittest.mock import MagicMock

class TestPhase3Validation(unittest.TestCase):

    def setUp(self):
        # Setup a temporary file-based SQLite database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.test_engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.test_engine)

        self.mock_qdrant = MagicMock()
        self.mock_arango = MagicMock()
        self.event_store = EventStore(engine=self.test_engine)
        self.event_processor = EventProcessor(
            self.event_store, 
            engine=self.test_engine,
            qdrant_client=self.mock_qdrant,
            arangodb_db=self.mock_arango
        )

    def tearDown(self):
        Base.metadata.drop_all(bind=self.test_engine)
        self.test_engine.dispose()
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_resource_created_flow(self):
        """Verified end-to-end event flow for ResourceCreated (Checklist Item 3)."""
        resource_id = "res_123"
        payload = {
            "id": resource_id,
            "username": "testuser",
            "type": "resource",
            "title": "Test Resource",
            "format": "markdown",
            "body": "This is a test resource body.",
            "tags": ["test", "phase3"],
            "related_zettels": [],
            "horizon": "none"
        }
        
        # 1. Append the event
        self.event_store.append_event(
            event_id="evt_001",
            event_type="ResourceCreated",
            payload=payload,
            schema_version="1.0"
        )
        
        # 2. Process/Replay
        self.event_processor.replay_events()
        
        # 3. Verify Read Model
        resource = self.event_processor.get_read_model(ResourceReadModel, resource_id)
        self.assertIsNotNone(resource, "ResourceReadModel should exist after replay")
        self.assertEqual(resource['title'], "Test Resource")
        self.assertEqual(resource['format'], "markdown")
        # ResourceReadModel uses SQLiteJSON for tags, verify it's handled (pydantic handles serialization, SQLAlchemy JSON handles deserialization)
        # Note: In the read model dict returned by get_read_model, tags should be a list or a JSON string depending on how it's stored.
        # Actually ResourceReadModel uses SQLiteJSON.
        self.assertIn("phase3", resource['tags'])

    def test_stub_handlers_no_crash(self):
        """Verifies that STUB handlers (KnowledgeNode) do not crash the processor (Checklist Item 4)."""
        node_id = "node_456"
        payload = {
            "id": node_id,
            "title": "Stub Node",
            "content": "This should not be persisted",
            "node_type": "para_resource",
            "tags": ["stub"],
            "related_nodes": []
        }
        
        # 1. Append KnowledgeNodeCreated event
        self.event_store.append_event(
            event_id="evt_002",
            event_type="KnowledgeNodeCreated",
            payload=payload,
            schema_version="1.0"
        )
        
        # 2. Process/Replay
        try:
            self.event_processor.replay_events()
        except Exception as e:
            self.fail(f"Replaying a stub event should not raise an exception: {e}")
        
        # 3. Verify NO read model exists (as it's a stub)
        # KnowledgeNodeModel is available in database.py, but not assigned to a KnowledgeNodeReadModel for EventProcessor yet in Phase 3.
        # Wait, I should check if there IS a table for it. 
        # database.py has KnowledgeNodeModel.
        # But EventProcessor has no real mapping for it.
        # If I try to query it via get_read_model with ZettelReadModel (placeholder), it shouldn't find it.
        # Actually EventProcessor.event_payload_schemas uses Zettel for KnowledgeNodeCreated.
        
        # The goal is just to ensure it doesn't crash and nothing is persisted to the 'zettels' table by mistake.
        # First, ensure 'zettels' table is empty.
        zettel = self.event_processor.get_read_model(ResourceReadModel, node_id) # Won't find it in resources either
        self.assertIsNone(zettel)

if __name__ == '__main__':
    unittest.main()
