# Future Ideas and Automation Todo List

This document captures ideas for future development, including automation with cron jobs and other enhancements for the LifeOS project.

## Automation Ideas (Cron Jobs)

-   **Automate Neo4j Backups:** Schedule regular backups of the Neo4j database using `neo4j-admin dump` and a cron job. This should include storing backups in a secure, remote location and implementing a retention policy.
    -   *Reference:* `docs/11_Backup_and_Recovery.md`
-   **Automate Qdrant Backups:** Schedule regular backups of Qdrant collections using `qdrant-cli backup` (or `docker exec` commands to create snapshots) and a cron job. This should also include remote storage and a retention policy.
    -   *Reference:* `docs/11_Backup_and_Recovery.md`
-   **Automate Data Reconciliation:** Schedule the `DataReconciler` (`src/reconciliation.py`) to run periodically to identify and resolve discrepancies between Neo4j and Qdrant data. This can include automatic re-ingestion of missing items or deletion of dangling entries.
    -   *Reference:* `src/reconciliation.py`

## Other Future Enhancements

-   **Inner Palette & Emotion Engine Vision:** This integrated module is a core, ongoing development initiative for emotional intelligence. Its full vision includes Neuro-Coaching, advanced feedback loops, deep integration with Crisis Mode, and sophisticated pattern recognition for emotional growth.
-   **Resolving Licensing Conflicts:** High-priority consideration for replacing non-permissive components like Neo4j (GPLv3) and newer Redis versions (RSALv2/SSPLv1) with permissively licensed alternatives (e.g., ArangoDB, KeyDB, older Redis versions).
-   **Full Android Native App Development:** Plan for a dedicated native or cross-platform (Flutter/React Native) mobile application to provide a superior user experience, leveraging the FastAPI backend.
-   **Enhanced Database Security:** Beyond current authentication, implement robust authentication, encryption (in-transit and at-rest), and strict network access controls for all databases (Qdrant, Redis/alternative, Graph DB alternative).
-   **JSON Schema Registry & AI Safety Layer Implementation:** Develop the `/schemas/registry.json` and individual schema files, and enforce the "Ethical Contract Layer" and "Engineering Conduct Rules" for AI agents to ensure schema invariance, module purity, and predictable, aligned behavior.
-   **Self-Feedback Loop & Autonomous Framework Learning:** Implement adaptive learning mechanisms where the system uses user feedback (e.g., on `SystemInsight` effectiveness) to adjust model weights and improve the accuracy and relevance of AI-generated recommendations and insights.

-   **Temporal Middleware Semantic Filtering Enhancement:**
    -   **Current State:** `extract_semantic_filters_with_llm` in `src/temporal.py` uses a basic LLM call for semantic extraction (e.g., `life_stage`, `episode`).
    -   **Enhancement:** Improve the LLM's prompt and/or integrate a more sophisticated parsing mechanism to more accurately extract and map diverse semantic terms from user queries into filterable properties. This will directly support the "Contextual Dashboard Generator" workflow.
-   **Dual-Path Memory Coordinator Refinement:**
    -   **Current State:** `src/router.py` uses a `RouterQueryEngine` with two tools (graph and resources) and `PydanticSingleSelector` for routing.
    -   **Enhancement:** Refine the intent classification for routing into the four granular categories (Empathy/Session, Pattern Recognition/Analytics, Fact Lookup, Advice/Psychoeducation). This might involve:
        -   More detailed and specific descriptions for `QueryEngineTool`s.
        -   Implementing custom selectors or a multi-step routing mechanism for complex queries.
-   **Observability - Structured Logging:**
    -   **Current State:** Basic Python logging is used.
    -   **Enhancement:** Integrate a structured logging library (e.g., `python-json-logger`) to output logs in JSON format, making them easier to parse, filter, and analyze by monitoring tools.
-   **Observability - Advanced Metrics Endpoints:**
    -   **Current State:** `/api/metrics` provides basic node/point counts.
    -   **Enhancement:** Expand the `/api/metrics` endpoint to expose more detailed operational metrics, such as:
        -   Database connection pool statistics (Neo4j, Qdrant, Redis).
        -   LLM call counts and token usage per endpoint/model.
        -   Cache hit/miss rates for Redis.
        -   Latency breakdowns for internal operations within `ingest` and `query` endpoints.
-   **Feedback Loop for Adaptive Learning (PEFT/LoRA):**
    -   **Current State:** User feedback is logged to `feedback.csv`.
    -   **Enhancement:** Develop a system to leverage the logged user feedback for fine-tuning the LLM using techniques like PEFT (Parameter-Efficient Fine-Tuning) or LoRA (Low-Rank Adaptation) to improve performance and personalization. This directly supports the "Adaptive Learning" aspect of the plan.
-   **Coaching Flows Expansion:**
    -   **Current State:** Basic `start_flow` and `advance_flow` endpoints exist with Redis for state management.
    -   **Enhancement:** Implement more sophisticated, multi-step coaching flows within the backend. This would involve defining flow schemas, dynamic branching logic, and deeper integration with the `FrameworkSynthesizer` and specific knowledge resources to provide personalized guidance.
-   **Prompt/Schema Versioning System:**
    -   **Current State:** Schema and prompt versions are hardcoded variables in Python files.
    -   **Enhancement:** Develop a system for dynamic loading and management of different versions of prompts and schemas, potentially from external configuration files (e.g., JSON, YAML). This would allow for easier A/B testing, rapid iteration, and tracking of historical prompt/schema performance.
-   **"Next-Gen" AI Workflows Implementation:** Systematically work through the five "Next-Gen" AI Workflows outlined in `System/AI-Context/Next-Gen_AI_Workflows.md`, building out the necessary backend logic and API endpoints to support them.
    -   *Serendipity Engine*
    -   *Pre-Mortem Simulator*
    -   *Socratic Mirror*
    -   *Progressive Summarization Agent*
    -   *Contextual Dashboard Generator*