import unittest
from datetime import datetime, timezone, timedelta
import json
import tempfile
import os
import time

from fastapi.testclient import TestClient
from main import app, get_event_store, get_event_processor, get_db
from auth import create_access_token, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, create_user, verify_password, get_user_by_username
from database import Base, StoredEvent, ZettelReadModel, User
from event_sourcing.event_store import EventStore
from event_sourcing.event_processor import EventProcessor
from schemas import ZettelCreate, ZettelUpdate # Import new schemas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestAPISecurity(unittest.TestCase):

    def setUp(self):
        # 1. Setup a temporary file-based SQLite database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.test_engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.test_engine) # Create all tables from the single Base
        self.TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.test_engine)

        from unittest.mock import MagicMock
        self.mock_qdrant = MagicMock()
        self.mock_arango = MagicMock()
        self.test_event_store = EventStore(engine=self.test_engine)
        self.test_event_processor = EventProcessor(
            self.test_event_store, 
            engine=self.test_engine,
            qdrant_client=self.mock_qdrant,
            arangodb_db=self.mock_arango
        )

        def override_get_event_store():
            return self.test_event_store

        def override_get_event_processor():
            return self.test_event_processor
        
        def override_get_db():
            db = self.TestSessionLocal()
            try:
                yield db
            finally:
                db.close()

        # Apply dependency overrides
        app.dependency_overrides[get_event_store] = override_get_event_store
        app.dependency_overrides[get_event_processor] = override_get_event_processor
        app.dependency_overrides[get_db] = override_get_db

        # Initialize TestClient AFTER dependency overrides
        self.client = TestClient(app)

        # Replay events to ensure clean state for EventProcessor (moved to individual tests where events are generated)
        # self.test_event_processor.replay_events()

        # Create a test user for authentication tests
        with self.TestSessionLocal() as db:
            create_user(db, "testuser", "testpassword")
    
    def tearDown(self):
        app.dependency_overrides.clear() # Clear overrides after each test
        # Drop tables and dispose engines after each test
        Base.metadata.drop_all(bind=self.test_engine)
        self.test_engine.dispose()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def get_token_for_user(self, username, password):
        # This will call the actual /token endpoint
        response = self.client.post(
            "/token",
            data={"username": username, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["access_token"]

    def test_unauthenticated_access_to_protected_endpoint(self):
        response = self.client.post("/zettel/", json={})
        self.assertEqual(response.status_code, 401)

    def test_invalid_token_access_to_protected_endpoint(self):
        headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.post("/zettel/", json={}, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_access_to_protected_endpoint(self):
        token = self.get_token_for_user("testuser", "testpassword")
        headers = {"Authorization": f"Bearer {token}"}
        valid_zettel_create_data = {
            "type": "zettel",
            "title": "Secure Zettel",
            "body": "This zettel is protected.",
            "links": [],
            "tags": [],
            "horizon": "vision",
            "contexts": []
        }
        response = self.client.post("/zettel/", json=valid_zettel_create_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json()["id"])
        self.assertEqual(response.json()["username"], "testuser")

    def test_user_data_scoping(self):
        # Create user1 and their zettel
        with self.TestSessionLocal() as db:
            create_user(db, "user1", "pass1")
        token1 = self.get_token_for_user("user1", "pass1")
        headers1 = {"Authorization": f"Bearer {token1}"}
        zettel_create_data1 = {
            "type": "zettel",
            "title": "User1's Zettel",
            "body": "Only user1 can see this.",
            "links": [], "tags": [], "horizon": "vision", "contexts": []
        }
        response = self.client.post("/zettel/", json=zettel_create_data1, headers=headers1)
        self.assertEqual(response.status_code, 201)
        user1_zettel_id = response.json()["id"]
        self.test_event_processor.replay_events() # Process the new event
    
    
        # Create user2 and try to access user1's zettel
        with self.TestSessionLocal() as db:
            create_user(db, "user2", "pass2")
        token2 = self.get_token_for_user("user2", "pass2")
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        response = self.client.get(f"/zettel/{user1_zettel_id}", headers=headers2)
        self.assertEqual(response.status_code, 404) # user2 should not find user1's zettel

        # user1 should be able to access their own zettel
        response = self.client.get(f"/zettel/{user1_zettel_id}", headers=headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], user1_zettel_id)
        self.assertEqual(response.json()["username"], "user1")
