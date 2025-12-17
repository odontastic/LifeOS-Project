# Architectural Recovery Log - LifeOS

This document tracks decisions, inconsistencies, and actions taken during the architectural recovery phase for LifeOS's data and event flow.

## Step 0: Preparation
- **Phase 1 Audit Confirmation:** Confirmed based on prior discussions on core purpose, boundaries, and data model/flow.
- **Backup Status:** User instructed to perform manual backup of databases and codebase. Confirmed by user.
- **Recovery Log Creation:** Document created.

---

## Step 1: Event Log Verification

**Objective:** Ensure the event log is correct and enforce append-only discipline.

**Actions Taken:**
- Confirmed `data/event_log.db` exists.
- Inspected `event_log` table schema in `data/event_log.db`, found it matches expected `event_id`, `event_type`, `timestamp`, `payload`, `schema_version`.
- Fixed missing `timezone` import in `apps/backend/lifeos-rag-api/src/database.py`.
- Reviewed `apps/backend/lifeos-rag-api/src/event_sourcing/event_store.py`.
- Reviewed `apps/backend/lifeos-rag-api/src/event_sourcing/event_processor.py`.
- Searched API endpoints (`apps/backend/lifeos-rag-api/src/routers/`) for direct writes to read models.
- Searched codebase (`apps/backend/lifeos-rag-api/`) for interactions with Qdrant and ArangoDB.

**Findings:**
- The `EventStore` class, specifically the `append_event` method, correctly implements an append-only mechanism using `db.add()` for `StoredEvent` objects. No `update` or `delete` operations are present in this class.
- Schema consistency for events is enforced at the point of event creation through the `StoredEvent` model and the `append_event` method parameters.
- The `EventProcessor` correctly implements event-driven updates for read models. It processes events from `event_store` and translates them into CUD operations on `ReadModel` tables.
- The `replay_events` function in `EventProcessor` provides a mechanism for rebuilding read models from the event log, reinforcing the single source of truth principle.
- **No direct writes to Read Models from API routers:** Searches confirmed that API router endpoints are correctly using `event_processor.get_read_model()` and `event_processor.get_all_read_models()` for reading data, and are not performing direct `db.add()`, `db.update()`, or `db.delete()` operations on `ReadModel` objects. This is a critical confirmation for event-sourcing.
- **Qdrant and ArangoDB Integration (Initial Audit):** Both Qdrant (vector store) and ArangoDB (graph store) are part of the system and configured. However, their updates were **NOT initially integrated with the `EventProcessor`**. They appeared to be handled by separate indexing/reconciliation scripts or were in placeholder stages.

**Inconsistencies / Gaps Identified (Initial Audit):**
- **Potential for malformed event payloads:** While `json.dumps` handles serialization, deserialization in `EventProcessor` (e.g., `payload = json.loads(event.payload)`) assumes a valid structure for `ReadModel` construction. Robust error handling for schema mismatches during event processing might be needed.
- **Derived Data Store Updates (Qdrant/ArangoDB):** This was a **MAJOR GAP** against the blueprint. The blueprint dictates that vector stores and graph stores are "derived data" and should be updated by the `EventProcessor` as a result of new events. The initial implementation did not reflect this.
- **Dual Data Models (`lifeos_core.db` and `*Model` classes):** The models `EmotionEntryModel`, `ContactProfileModel`, `TaskItemModel`, `KnowledgeNodeModel`, `SystemInsightModel` map to `lifeos_core.db`. While a direct search for `db.add/update/delete` on these models yielded no results within `apps/backend/lifeos-rag-api/`, their purpose and how they integrate with the event log require further clarification. If these are write targets, they would violate event sourcing.

**Checkpoint: Event log is the single source of truth; no data changes bypass it.**
- The first part of this checkpoint (event log is single source of truth for *read models*) is largely confirmed for the SQLite read models.
- However, the second part of the checkpoint (no data changes bypass it for *derived stores* like Qdrant and ArangoDB) was **NOT met** initially.

---

## **Recovery Action: Integrate Qdrant and ArangoDB Handlers into EventProcessor**

**Goal:** To establish event-driven updates for Qdrant (vector store) and ArangoDB (graph store) within the `EventProcessor`.

**Actions Taken:**
1.  **Modified `EventProcessor` constructor:** `apps/backend/lifeos-rag-api/src/event_sourcing/event_processor.py` was updated to accept `QdrantClient` and `StandardDatabase` instances, and instantiate `QdrantService` and `ArangoDBService`.
2.  **Reorganized imports:** Imports in `event_processor.py` were cleaned up and sorted.
3.  **Added `QdrantService` (`src/services/qdrant_service.py`):** Created a dedicated service to encapsulate Qdrant interaction logic (upsert/delete vectors, create collections).
4.  **Added `ArangoDBService` (`src/services/arangodb_service.py`):** Created a dedicated service to encapsulate ArangoDB interaction logic (upsert/delete vertices/edges, create collections).
5.  **Updated `event_handlers` dictionary:** The `self.event_handlers` dictionary in `EventProcessor.__init__` was updated to map relevant CUD events for `Zettel`, `Resource`, `Project`, `Area`, `Task`, `Goal`, `Reflection`, `JournalEntry`, `Emotion`, `Belief`, and `Trigger` to new combined ReadModel and derived store handlers.
6.  **Implemented combined Qdrant/ReadModel handlers:** New asynchronous methods (`_handle_*_qdrant_and_readmodel`) were added to `EventProcessor` for `Zettel` and `Resource` CUD events. These handlers first update the ReadModel and then call the corresponding `qdrant_service` methods.
7.  **Implemented combined ArangoDB/ReadModel handlers:** New asynchronous methods (`_handle_*_arangodb_and_readmodel`) were added to `EventProcessor` for `Project`, `Area`, `Task`, `Goal`, `Reflection`, `JournalEntry`, `Emotion`, `Belief`, and `Trigger` CUD events. These handlers first update the ReadModel and then call the corresponding `arangodb_service` methods for vertex management (with initial edge handling for Task-Project).
8.  **Removed old ReadModel-only handlers:** The original ReadModel-only handlers for `Zettel`, `Resource`, `Project`, `Area`, `Task`, `Goal`, `Reflection`, `JournalEntry`, `Emotion`, `Belief`, and `Trigger` were removed from `EventProcessor` via manual intervention.
9.  **Handled `AsyncGenerator`:** Added `AsyncGenerator` to imports and updated `_get_db`, `_apply_event`, `replay_events` to be `async` to accommodate asynchronous service calls.
10. **Refactored direct Qdrant write/update logic (from `resource_indexer.py`, `graph_neo4j_deprecated.py`, `main.py`):**
    *   `src/resource_indexer.py`: Refactored to emit `ResourceCreated` events instead of direct Qdrant writes.
    *   `src/graph_neo4j_deprecated.py`: Deleted as it was deprecated and used Neo4j.
    *   `src/main.py`: Verified that no direct Qdrant writes exist; Qdrant client usage is for health checks or read-only queries.
11. **Refactored direct ArangoDB write/update logic (from `graph_db.py`, `main.py`):**
    *   `src/graph_db.py`: `insert_vertex` and `insert_edge` functions deleted as their functionality is now handled by `ArangoDBService`.
    *   `src/main.py`: Imports for `insert_vertex` and `insert_edge` removed, and direct calls to these functions within the `/ingest` endpoint have been commented out.
12. **Verified all Qdrant and ArangoDB updates are exclusively event-driven via the `EventProcessor`:** Confirmed through review and broad codebase search that all known direct write/update operations have been eliminated or replaced with event-driven mechanisms.
13. **Implemented explicit Pydantic model validation of event payloads:** The `_apply_event` method in `event_sourcing/event_processor.py` was modified to use `self.event_payload_schemas` to validate incoming event payloads with their corresponding Pydantic models. Error handling for `ValidationError` and `json.JSONDecodeError` was added.

**Current Status:**
- The `EventProcessor` is now structured to process CUD events for multiple entities and update both the SQLite ReadModels and the Qdrant/ArangoDB derived stores in an event-driven manner.
- The code in `event_sourcing/event_processor.py` is in the desired state for handler integration.
- Direct Qdrant and ArangoDB write logic has been refactored or removed from `resource_indexer.py`, `graph_neo4j_deprecated.py`, `graph_db.py`, and `main.py`.
- The system is now significantly more aligned with the event-sourced architecture for derived data stores.
- Explicit Pydantic model validation of event payloads has been integrated into the `EventProcessor`.

**Remaining Actions (from original recovery action list):**
- **Address remaining inconsistencies/gaps:**
    - Clarify usage of `lifeos_core.db` and its `*Model` classes.
    - Clarify Pydantic Model Usage (further, beyond event payloads).
    - Implement Schema Versioning Logic.
    - Enhance Event Processor Error Handling (further, for dead-letter queues or error events).

---

**Next Action:**
- Clarify usage of `lifeos_core.db` and its `*Model` classes. This involves determining whether these models should be fully event-sourced, deprecated, or if they serve a distinct, non-event-sourced purpose within the architecture.