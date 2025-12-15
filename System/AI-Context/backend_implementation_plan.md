### LifeOS Backend Implementation Plan

**Phase 1: Foundation and Data Modeling**

1.  **Initialize Backend Application:**
    *   Verify and scaffold the FastAPI application structure inside `apps/backend/lifeos-rag-api/`.
    *   Establish dependency management with pinned versions in `requirements.txt` (FastAPI, Pydantic, Uvicorn, SQLAlchemy for SQLite, etc.).
    *   Set up configuration management using a `.env` file for settings like database paths.

2.  **Define Pydantic Models:**
    *   Create a `lifeos-rag-api/models` directory.
    *   For each schema in the `temp_schemas/` directory, create a corresponding Pydantic model (`zettel.py`, `project.py`, etc.). These models will define the data structures and enforce validation for all API interactions.

**Phase 2: Event-Sourcing Core**

3.  **Implement Event Bus:**
    *   Create a core module for the event-sourcing system.
    *   Define a generic `Event` model (Pydantic) with `event_id`, `event_type`, `timestamp`, `payload`, and `schema_version`.
    *   Implement a service that writes these events to a dedicated, append-only SQLite table (`event_log`), which will be the single source of truth.

**Phase 3: API Endpoint and Business Logic Implementation**

4.  **Build API Routers:**
    *   Create a `lifeos-rag-api/routers` directory.
    *   For each resource type (Zettel, Project, Area, etc.), create a dedicated router file (e.g., `routers/zettel.py`).
    *   Implement all CRUD endpoints (`POST`, `GET`, `PUT`, `DELETE`) as specified in `System/Documentation/Backend_Endpoints.md`.

5.  **Implement Command Logic:**
    *   The `POST`, `PUT`, and `DELETE` endpoints will function as **Commands**.
    *   They will validate input against the Pydantic models.
    *   Instead of modifying state directly, they will generate and log the appropriate event (e.g., `ProjectCreated`, `TaskStatusUpdated`) to the event bus.

6.  **Implement Query Logic (Read Models):**
    *   The `GET` endpoints will function as **Queries**.
    *   Create a state reconstruction service that reads the `event_log` from the beginning to build the current state of the application.
    *   For performance, this reconstructed state (a "read model") will be cached or stored in separate SQLite tables.
    *   `GET` endpoints will query these read-model tables, ensuring a clean separation from the write logic (CQRS).

**Phase 4: Security and Testing**

7.  **Implement Authentication:**
    *   Build the JWT-based local authentication system as mandated.
    *   Create endpoints for user registration and login.
    *   Secure all data-related endpoints, ensuring they are scoped to the authenticated user.

8.  **Develop Test Suite:**
    *   Set up a `tests/` directory.
    *   Write tests covering the critical requirements from the master instructions:
        *   Event creation and successful replay.
        *   Correct state reconstruction from the event log.
        *   API endpoint validation and security.
        *   Index rebuild and graceful degradation scenarios.

**Phase 5: Deployment and Documentation**

9.  **Containerize Application:**
    *   Create a `Dockerfile` and `docker-compose.yml` to run the FastAPI backend and its dependent services (ArangoDB, Qdrant) consistently.

10. **Finalize Documentation:**
    *   Ensure the FastAPI OpenAPI documentation is complete and accessible.
    *   Update the main project `README.md` with instructions on how to build, configure, and run the backend service.