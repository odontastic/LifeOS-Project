# Backend API Startup Incident Report

**Date:** December 14, 2025

**Summary:**
The `backend-api` service (`lifeos-rag-api`) failed to start after recent code restructuring, exhibiting a series of Python errors upon Docker container initialization. Extensive debugging efforts were made to resolve these issues, often requiring full Docker rebuilds.

**Chronology of Errors Encountered:**

1.  **`NameError: name 'get_db' is not defined` (in `auth.py`)**:
    *   **Root Cause:** Circular dependency and incorrect module-level import of `get_db` in `auth.py` within FastAPI's dependency injection context.
    *   **Resolution Attempts:**
        *   Moving `get_db` import inside `get_current_user` function.
        *   Removing `Depends(get_db)` from `get_current_user` signature and attempting manual session creation.
        *   Ensuring `get_db` was imported at the module level in `auth.py`.
    *   **Current State:** Resolved by refactoring `get_current_user` in `auth.py` to *only* verify the token and return the username, deferring the DB session and user lookup to the FastAPI routes in `main.py`. This broke the direct dependency.

2.  **`NameError: name 'oauth2_scheme' is not defined` (in `auth.py`)**:
    *   **Root Cause:** `OAuth2PasswordBearer` instance `oauth2_scheme` was used before its definition in `auth.py`.
    *   **Resolution:** Added `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")` at the module level in `auth.py`.

3.  **`IndentationError: unexpected indent` (in `schemas.py` at line 1)**:
    *   **Root Cause:** Malformed `schemas.py` file starting with an indented line (e.g., `interaction_date` field was at module level).
    *   **Resolution:** Recreated `schemas.py` with correct Python syntax, ensuring Pydantic models (like `RelationLogRequest`) were properly defined within `class` blocks and all necessary imports were present.

4.  **`ModuleNotFoundError: No module named 'src'` (when importing `src.main` from `debug_main.py`)**:
    *   **Root Cause:** Python's import system within the Docker container was not correctly resolving `src` as a package, even with `WORKDIR /app` and `COPY ./src ./src`. This was exacerbated by `python src/debug_main.py` execution, where `src` was treated as a top-level script directory, not a package.
    *   **Resolution Attempts:**
        *   Added `ENV PYTHONPATH=/app` to `Dockerfile`.
        *   Modified `debug_main.py` to print `sys.path`.
        *   Modified `debug_main.py` to attempt `from src.main import app`.
    *   **Current State:** Unclear if truly resolved or bypassed by subsequent fixes.

5.  **`NameError: name 'Optional' is not defined` (in `event_bus.py`)**:
    *   **Root Cause:** `Optional` type hint used without being imported from `typing`.
    *   **Resolution:** Added `from typing import Optional` to `event_bus.py`.

6.  **`SyntaxError: 'return' outside function` (in `calm_compass.py` at line 1)**:
    *   **Root Cause:** A `return` statement at the module level in `calm_compass.py`, likely intended for a function.
    *   **Resolution:** Wrapped the module-level `return` statement within the `process_emotion_entry_for_calm_compass` function and added necessary imports (`logging`, `UUID`, `Session`, `EmotionEntry`, `SystemInsight`).

7.  **`TypeError: RateLimiter.__call__() missing 1 required positional argument: 'response'` (in `main.py`)**:
    *   **Root Cause:** Incorrect usage of `RateLimiter` decorator from `fastapi-limiter`. It was used as `@RateLimiter(...)` directly, but it should be passed to `Depends()` as `Depends(RateLimiter(...))`.
    *   **Resolution:** Modified usage to `Depends(RateLimiter(times=5, seconds=60))`.

8.  **`AttributeError: 'FastAPI' object has no attribute 'on_startup'` (in `main.py`)**:
    *   **Root Cause:** Deprecated usage of `@app.on_startup` decorator; FastAPI now prefers `@app.on_event("startup")` or the `lifespan` context manager.
    *   **Resolution:** Changed `@app.on_startup` to `@app.on_event("startup")` in `main.py`.

**Next Steps & Learning:**
The repeated cycle of fixing one error only to encounter another highlights a fragile initial setup or significant breaking changes across library versions. Going forward, a more systematic approach to environment setup and dependency management is crucial. This incident underscores the importance of:
*   **Comprehensive initial environment validation.**
*   **Clearer error reporting and logging mechanisms.**
*   **Careful review of library documentation for version-specific changes.**
*   **Using minimal reproducible examples to isolate complex startup issues.**
