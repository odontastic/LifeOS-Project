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
- **Qdrant and ArangoDB Integration:** Both Qdrant (vector store) and ArangoDB (graph store) are part of the system and configured. However, their updates are **NOT currently integrated with the `EventProcessor`**. They appear to be handled by separate indexing/reconciliation scripts or are in placeholder stages.

**Inconsistencies / Gaps Identified:**
- **Potential for malformed event payloads:** While `json.dumps` handles serialization, deserialization in `EventProcessor` (e.g., `payload = json.loads(event.payload)`) assumes a valid structure for `ReadModel` construction. Robust error handling for schema mismatches during event processing might be needed.
- **Derived Data Store Updates (Qdrant/ArangoDB):** This is a **MAJOR GAP** against the blueprint. The blueprint dictates that vector stores and graph stores are "derived data" and should be updated by the `EventProcessor` as a result of new events. The current implementation does not reflect this.
    -   Qdrant updates appear to be happening through `resource_indexer.py` and `reconciliation.py`, not via event processing.
    -   ArangoDB ingestion is primarily handled in `main.py` and `graph_db.py`, also seemingly separate from the `EventProcessor`'s event stream.
- **Dual Data Models (`lifeos_core.db` and `*Model` classes):** The models `EmotionEntryModel`, `ContactProfileModel`, `TaskItemModel`, `KnowledgeNodeModel`, `SystemInsightModel` map to `lifeos_core.db`. While a direct search for `db.add/update/delete` on these models yielded no results within `apps/backend/lifeos-rag-api/`, their purpose and how they integrate with the event log require further clarification. If these are write targets, they would violate event sourcing.

**Checkpoint: Event log is the single source of truth; no data changes bypass it.**
- The first part of this checkpoint (event log is single source of truth for *read models*) is largely confirmed for the SQLite read models.
- However, the second part of the checkpoint (no data changes bypass it for *derived stores* like Qdrant and ArangoDB) is **NOT met**. Data is being written to these stores outside the event processor, which violates the blueprint.

---

## **Audit Report: `lifeos_core.db` Usage**

**Action:** Searched the entire `apps/backend/lifeos-rag-api/` directory for `db.add()`, `db.update()`, `db.delete()` operations targeting `EmotionEntryModel`, `ContactProfileModel`, `TaskItemModel`, `KnowledgeNodeModel`, `SystemInsightModel`.

**Finding:** **No direct `db.add()`, `db.update()`, or `db.delete()` calls were found targeting these `*Model` classes within the `apps/backend/lifeos-rag-api/` application code.** This is a positive indication that direct SQLAlchemy write operations to `lifeos_core.db` models are not occurring within the `apps/backend/lifeos-rag-api/` application code, which aligns with the event-sourcing principle.

**Remaining Question:** The purpose and intended usage of `lifeos_core.db` and its `*Model` tables still need to be explicitly defined within the event-sourced architecture. If they are intended to be event-sourced, they should be converted to `ReadModel`s and explicitly managed by the `EventProcessor`. If they serve another purpose (e.g., configuration, user authentication details not handled by events), that needs to be clarified to ensure no violation of the core architectural principle.

---

**Next Action:**
- Address the **MAJOR GAP** regarding the integration of Qdrant and ArangoDB updates into the `EventProcessor` as outlined in the recovery action list.
    1.  Modify `EventProcessor` to include Qdrant client initialization and pass it to handler methods.
    2.  Modify `EventProcessor` to include ArangoDB client initialization and pass it to handler methods.
    3.  Create dedicated Qdrant service functions (e.g., `add_vector`, `update_vector`, `delete_vector`) to encapsulate Qdrant interaction logic.
    4.  Create dedicated ArangoDB service functions (e.g., `add_vertex`, `update_vertex`, `delete_vertex`, `add_edge`, `delete_edge`) to encapsulate ArangoDB interaction logic.
    5.  Implement new event handlers in `EventProcessor` that call the dedicated Qdrant service functions for relevant events.
    6.  Implement new event handlers in `EventProcessor` that call the dedicated ArangoDB service functions for relevant events.
    7.  Refactor existing direct Qdrant write/update logic (from `resource_indexer.py`, `graph_neo4j_deprecated.py`, `main.py`) to use the new event-driven approach.
    8.  Refactor existing direct ArangoDB write/update logic (from `graph_db.py`, `main.py`) to use the new event-driven approach.
    9.  Verify that all Qdrant and ArangoDB updates are exclusively event-driven via the `EventProcessor`.