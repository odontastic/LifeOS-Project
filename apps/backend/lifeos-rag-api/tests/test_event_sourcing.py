import unittest
from datetime import datetime, timedelta, timezone
import json
import tempfile
import os

from sqlalchemy import create_engine
from database import Base, StoredEvent, ZettelReadModel
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from models.zettel import Zettel

class TestEventSourcing(unittest.TestCase):

    def setUp(self):
        # Setup a temporary file-based SQLite database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.test_engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.test_engine) # Create all tables from the single Base

        self.event_store = EventStore(engine=self.test_engine)
        self.event_processor = EventProcessor(self.event_store, engine=self.test_engine)

    def tearDown(self):
        Base.metadata.drop_all(bind=self.test_engine)
        self.test_engine.dispose()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_event_creation_and_replay(self):
        # 1. Create a zettel event
        zettel_id = "test_zettel"
        initial_zettel_data = {
            "id": zettel_id,
            "type": "zettel",
            "title": "Test Zettel",
            "body": "This is a test zettel.",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "links": [],
            "tags": [],
            "horizon": "none",
            "contexts": [],
            "username": "testuser"
        }
        self.event_store.append_event(
            event_id="1",
            event_type="ZettelCreated",
            payload=initial_zettel_data,
            schema_version="1.0"
        )

        # 2. Create another event (update)
        updated_zettel_data = initial_zettel_data.copy()
        updated_zettel_data["title"] = "Updated Test Zettel"
        updated_zettel_data["updated_at"] = datetime.now(timezone.utc)
        self.event_store.append_event(
            event_id="2",
            event_type="ZettelUpdated",
            payload=updated_zettel_data,
            schema_version="1.0"
        )

        # 3. Create a delete event
        self.event_store.append_event(
            event_id="3",
            event_type="ZettelDeleted",
            payload={"id": zettel_id, "username": "testuser"},
            schema_version="1.0"
        )

        # 4. Replay ALL events
        self.event_processor.replay_events()

        # 5. Verify final read model state (should be deleted)
        deleted_read_model = self.event_processor.get_read_model(ZettelReadModel, zettel_id)
        self.assertIsNone(deleted_read_model)

if __name__ == '__main__':
    unittest.main()