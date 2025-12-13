---
title: "LifeOS 2.0 Execution Plan"
type: "Plan"
status: "Active"
created: "2025-12-12"
last_updated: "2025-12-12"
tags: ["plan", "execution", "graph-rag", "lifeos-2.0"]
---

# 🚀 LifeOS 2.0 Execution Plan (Jules)

This document contains the merged, actionable instructions for implementing the therapist-grade, agentic GraphRAG system for LifeOS.

## Phase 1: Foundational Architecture & Infrastructure

1. **[ ] Create a dedicated Python repository**
   - Name: `lifeos-rag-api` (Done)
   - Purpose: All LlamaIndex and GraphRAG logic lives here.

2. **[ ] Define the Docker Compose stack**
   - Services:
     - `open-webui` (Frontend)
     - `backend-api` (Python RAG Service)
     - `neo4j` (Graph Database)
     - `qdrant` (Vector/Metadata Store)
   - Ensure all services are on the same Docker network.

3. **[ ] Configure volume mounts**
   - Mount `/Notes` (or equivalent) as read-only in `backend-api`.

4. **[ ] Implement the Ingestion API**
   - Create `/api/ingest` endpoint.

## Phase 2: Indexing, Schema, and Extraction

5. **[ ] Design the Therapeutic Schema**
   - **Nodes**: `JournalEntry`, `Emotion`, `Belief`, `Trigger`, `CopingMechanism`, `Goal`, `Episode`, `Pattern`, `SessionSummary`
   - **Relationships**: `AUTHORED_BY`, `RELATES_TO`, `TRIGGERED_BY`, `PRACTICED`, `PART_OF`, `MENTIONS`, `SUMMARIZES`
   - **Metadata**: `created_at`, `life_domain`, `life_stage`, `stability`, `confidence`

6. **[ ] Implement the Property Graph Index**
   - Use `PropertyGraphIndex` unifying Neo4j and Qdrant.
   - Use stable UUIDs as shared IDs.

7. **[ ] Build the Extraction Pipeline**
   - Use `SchemaLLMPathExtractor`.
   - Dual-store write logic (Neo4j + Qdrant).

8. **[ ] Implement Extraction Quality Control**
   - Confidence thresholds.

## Phase 3: Agentic & Generative Leap

9. **[ ] Implement Temporal Middleware**
   - Time reference parsing mapping to `created_at` filters.

10. **[ ] Build the Dual-Path Memory Coordinator**
    - `RouterQueryEngine` classification (Empathy vs. Fact vs. Analytics).

11. **[ ] Create the ResourceIndex**
    - Separate vector index for external knowledge.

12. **[ ] Implement the FrameworkSynthesizer**
    - JSON schema mental model output.

## Phase 4: UX, Safety, and Observability

13. **[ ] Ensure Source Transparency**
    - Render snippets with timestamps/tags.

14. **[ ] Implement Safety Guardrails**
    - Crisis language classifier.

15. **[ ] Design for Adaptive Learning**
    - Structured feedback logging.

16. **[ ] Plan for Coaching Flows**
    - Mode-based flows in Next.js.

## Additional Recommendations
- Top-k vectors from Qdrant -> fetch nodes from Neo4j.
- Single ingest pipeline (Dual-Store).
- Periodic reconciliation jobs.
