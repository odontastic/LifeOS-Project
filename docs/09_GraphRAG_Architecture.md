---
title: "LifeOS GraphRAG Architecture and Implementation Plan"
type: "Documentation"
status: "Plan"
created: "2025-12-12"
last_updated: "2025-12-12"
tags: ["documentation", "architecture", "rag", "graph-rag", "plan"]
---

# LifeOS GraphRAG Architecture and Implementation Plan

This document outlines the architecture and implementation plan for "Jules," the AI agent within the LifeOS, specifically focusing on a therapist-grade, agentic GraphRAG system.

## 1. Core Architecture Overview
The system implements a **Hybrid Agentic GraphRAG** approach with a **Dual-Store Pattern**, treating Neo4j and Qdrant as synchronized views of the same entities.

### Key Components
-   **Graph Store (Neo4j)**: Source of truth for structure and semantics.
-   **Vector Store (Qdrant)**: Source of truth for similarity search.
-   **Shared Identity**: All entities use a stable UUID present in both stores.
-   **Single Ingest Pipeline**: One function handles writes to both stores to ensure consistency.
-   **Strategic Router**: Dynamically routes queries to specialized pipelines.

## 2. Graph Schema Design
The schema is designed to model the user's life, emotional state, and productivity system. All entities inherit from `BaseNode`.

### 2.1 Core Entities (Nodes)
*   **Person**: The user and key people in their life.
*   **Note**: A generic note or journal entry (`AUTHORED_BY` User).
*   **JournalEntry**: Specific temporal reflection (`PART_OF` Episode).
*   **Project**: A PARA project (`RELATES_TO` Goal).
*   **Task**: An actionable item (`PART_OF` Project).
*   **Resource**: Reference material (`SUPPORTS` Project).
*   **Concept/Topic**: Abstract ideas (`MENTIONED_IN` Note).
*   **Event/Episode**: Significant temporal events (`HAPPENED_AT` Time).
*   **Emotion**: Emotional states (`FELT_BY` User, `TRIGGERED_BY` Event).
*   **Belief**: Core beliefs or patterns (`HELDS_BY` User).

### 2.2 Core Relationships (Edges)
*   **AUTHORED_BY**: Documents $\to$ User.
*   **RELATES_TO**: Generic semantic connection.
*   **PART_OF**: Hierarchical connection (Task $\to$ Project, Entry $\to$ Episode).
*   **SUPPORTS**: Resource $\to$ Project/Goal.
*   **MENTIONS**: content $\to$ Person/Concept.
*   **TRIGGERED_BY**: Emotion $\to$ Event/Trigger.
*   **PRECEDES / FOLLOWS**: Temporal sequencing of events.

## 3. Data Synchronization Strategy (Dual-Store Pattern)
To maintain consistency between Neo4j and Qdrant:
1.  **Shared IDs**: Every entity is assigned a UUID (`node.id`) which serves as the Neo4j Node ID and Qdrant Point ID.
2.  **Field Ownership**:
    -   **Neo4j** stores graph structure, semantics, and high-level properties.
    -   **Qdrant** stores embeddings and essential filterable metadata (`type`, `created_at`, `domain`).
3.  **Ingest Pipeline**:
    -   Generate UUID.
    -   Write Node + Relationships to Neo4j (Transaction).
    -   Compute Embedding.
    -   Upsert Vector + Payload to Qdrant.

## 4. Advanced Features

### 4.1 Temporal Metadata & Filtering
All nodes and edges will feature rich temporal metadata to support "time-travel" queries:
*   `created_at`: Creation timestamp.
*   `valid_from` / `valid_to`: For beliefs or life stages.
*   **Filtering**: Support for recency windows ("last 2 weeks") and life periods ("college years").

### 3.2 Dynamic Routing (Agentic RAG)
A classifier will analyze incoming queries and route them to sub-pipelines:
*   **Empathy Pipeline**: For emotional support, validation, and reflection (accesses Journals, Emotions, Beliefs).
*   **Analytics Pipeline**: For quantifying data (e.g., "How many days did I track habits?").
*   **Fact/Recall Pipeline**: For retrieving specific notes or resources.
*   **Advice/Coaching Pipeline**: For synthesizing mentorship based on established frameworks (Therapeutic Module).

### 3.3 Structure-Augmented Retrieval
Data will be indexed in separate but accessible indices to optimize retrieval precision:
*   **Journal Index**: Private, emotion-heavy reflections.
*   **Goals/Habits Index**: Structured progress data.
*   **Resources Index**: External knowledge and references.
*   **Combined Search**: The Agent can query across indices using metadata filters.

## 4. Safety & Transparency

### 4.1 Transparency
*   **Source Citations**: The UI must render snippets of retrieved nodes/documents.
*   **Explainability**: The agent should be able to explain *why* it retrieved certain memories ("I recalled this because you mentioned feeling anxious about work...").

### 4.2 Safety Guardrails
*   **Crisis Detection**: Real-time scanning for self-harm or high-distress language (`safety.py`).
*   **Escalation**: Pre-defined protocols for handling detected crises (disclaimer, resource links).

## 5. Adaptive Learning
*   **Feedback Loop**: Users can rate interaction helpfulness.
*   **Logging**: Structured logging of query $\to$ retrieved context $\to$ response $\to$ feedback for future fine-tuning or prompt optimization.

## 6. Implementation Roadmap

1.  **Schema Definition**: Formalize the Schema in code (`schemas.py`).
2.  **Extraction Logic**: Update `extractor.py` to populate new entities/relationships.
3.  **Pipeline Implementation**: Build the Router and Sub-pipelines.
4.  **UI Integration**: Update Frontend to display source nodes and timestamps.
5.  **Refinement**: Implement identifying specific "Life Stages" and temporal logic.
