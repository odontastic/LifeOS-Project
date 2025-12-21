import unittest
import logging
import sys
import os
from unittest.mock import MagicMock, patch
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from event_sourcing.event_processor import EventProcessor, logger
from database import ZettelReadModel

class TestPhase3Logging(unittest.TestCase):
    def setUp(self):
        self.mock_store = MagicMock()
        self.mock_engine = MagicMock()
        self.mock_qdrant = MagicMock()
        self.mock_arango = MagicMock()
        
        # Patch sessionmaker to avoid engine binding issues if any
        with patch('sqlalchemy.orm.sessionmaker') as mock_sessionmaker:
            self.processor = EventProcessor(
                event_store=self.mock_store,
                engine=self.mock_engine,
                qdrant_client=self.mock_qdrant,
                arangodb_db=self.mock_arango
            )
    
    def test_zettel_updated_success_log(self):
        """Verify success logs for REAL handler (Updated)"""
        mock_db = MagicMock()
        payload = {
            "id": "test_id_success",
            "title": "Updated Title",
            "updated_at": "2023-01-01T00:00:00"
        }
        
        with self.assertLogs('event_sourcing.event_processor', level='INFO') as cm:
            self.processor._handle_zettel_updated(mock_db, payload)
        
        # Check for specific structure
        # [Phase 3][REAL] ZettelUpdated - Updated ZettelReadModel for ID ... — processed
        found = False
        for log in cm.output:
            if "[Phase 3][REAL] ZettelUpdated" in log and "processed" in log:
                found = True
                break
        self.assertTrue(found, f"Expected success log not found. Logs: {cm.output}")

    def test_zettel_updated_failure_log(self):
        """Verify failure logs for REAL handler (Updated)"""
        mock_db = MagicMock()
        # Force an error
        mock_db.query.side_effect = Exception("Simulated DB Error")
        
        payload = {
            "id": "test_id_fail", 
            "title": "Fail Title",
            "updated_at": "2023-01-01T00:00:00"
        }
        
        with self.assertRaises(Exception):
            with self.assertLogs('event_sourcing.event_processor', level='ERROR') as cm:
                self.processor._handle_zettel_updated(mock_db, payload)
        
        # Check for specific structure
        # [Phase 3][REAL] ZettelUpdated error for ID ... — error: ...
        found = False
        for log in cm.output:
            if "[Phase 3][REAL] ZettelUpdated error" in log and "Simulated DB Error" in log:
                found = True
                break
        self.assertTrue(found, f"Expected failure log not found. Logs: {cm.output}")

    def test_zettel_deleted_success_log(self):
        """Verify success logs for REAL handler (Deleted)"""
        mock_db = MagicMock()
        payload = {"id": "test_id_del"}
        
        with self.assertLogs('event_sourcing.event_processor', level='INFO') as cm:
            self.processor._handle_zettel_deleted(mock_db, payload)
            
        found = False
        for log in cm.output:
            if "[Phase 3][REAL] ZettelDeleted" in log and "processed" in log:
                found = True
                break
        self.assertTrue(found, f"Expected success log not found. Logs: {cm.output}")

    def test_zettel_deleted_failure_log(self):
        """Verify failure logs for REAL handler (Deleted)"""
        mock_db = MagicMock()
        mock_db.query.side_effect = Exception("Delete Error")
        payload = {"id": "test_id_del_fail"}
        
        with self.assertRaises(Exception):
            with self.assertLogs('event_sourcing.event_processor', level='ERROR') as cm:
                self.processor._handle_zettel_deleted(mock_db, payload)
        
        found = False
        for log in cm.output:
            if "[Phase 3][REAL] ZettelDeleted error" in log and "Delete Error" in log:
                found = True
                break
        self.assertTrue(found, f"Expected failure log not found. Logs: {cm.output}")

    def test_missing_handler_warning(self):
        """Verify warning log for missing handler in _apply_event"""
        mock_event = MagicMock()
        mock_event.event_type = "UnknownType"
        mock_event.event_id = "evt_unknown"
        
        with self.assertLogs('event_sourcing.event_processor', level='WARNING') as cm:
            self.processor._apply_event(mock_event)
            
        found = False
        for log in cm.output:
            if "[Phase 3][N/A] No handler found" in log and "ignored" in log:
                found = True
                break
        self.assertTrue(found, f"Expected warning log not found. Logs: {cm.output}")

if __name__ == "__main__":
    unittest.main()
