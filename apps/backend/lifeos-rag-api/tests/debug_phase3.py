#!/usr/bin/env python
"""Debug script to test the Phase 3 ResourceCreated flow."""
import tempfile
import os
from sqlalchemy import create_engine
from database import Base, StoredEvent, ResourceReadModel
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from unittest.mock import MagicMock
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup temp DB
db_fd, db_path = tempfile.mkstemp()
print(f"Created temp DB at: {db_path}")
test_engine = create_engine(f'sqlite:///{db_path}', echo=True)
Base.metadata.create_all(test_engine)

mock_qdrant = MagicMock()
mock_arango = MagicMock()
event_store = EventStore(engine=test_engine)
event_processor = EventProcessor(
    event_store, 
    engine=test_engine,
    qdrant_client=mock_qdrant,
    arangodb_db=mock_arango
)

# Append event
resource_id = 'res_123'
payload = {
    'id': resource_id,
    'username': 'testuser',
    'type': 'resource',
    'title': 'Test Resource',
    'format': 'markdown',
    'body': 'This is a test resource body.',
    'tags': ['test', 'phase3'],
    'related_zettels': [],
    'horizon': 'none'
}

print("\n=== Appending event ===")
stored = event_store.append_event(
    event_id='evt_001',
    event_type='ResourceCreated',
    payload=payload,
    schema_version='1.0'
)
print(f'Appended event: {stored}')

# Get all events
events = event_store.get_all_events()
print(f'\n=== Events in store: {len(events)} ===')
for e in events:
    print(f'  - {e.event_type}: {e.payload[:50]}...')

# Replay
print('\n=== Replaying events... ===')
event_processor.replay_events()

# Query resource
print('\n=== Querying resource... ===')
resource = event_processor.get_read_model(ResourceReadModel, resource_id)
print(f'Resource result: {resource}')

if resource:
    print("SUCCESS: Resource was found!")
else:
    print("FAILURE: Resource was not found!")

# Cleanup
os.close(db_fd)
os.unlink(db_path)
print("\nCleanup complete.")
