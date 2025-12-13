# Session Tasks (2025‑12‑12)

- [x] **Review emotional awareness, relationship dynamics, and PKM content** – completed (summary doc & index created).
- [ ] **Document GTD Dashboard module** – placeholder file to be created (`docs/09_GTD_Dashboard.md`).
- [ ] **Document Prism Clarity Studio module** – placeholder file to be created (`docs/10_Prism_Clarity_Studio.md`).
- [x] **Update `docs/08_Developer_Handbook.md`** – already added references to GTD Dashboard and Prism Clarity Studio.
- [ ] **Add cross‑links from therapeutic sections to new emotional overview** (`docs/11_Emotional_Awareness_and_Relationships.md`).
- [ ] **Run front‑matter validation** (`python knowledge_base/check_frontmatter.py`).
- [x] **Fix broken link in `AGENTS.md`**.
- [x] **Backend Optimizations**: Implemented Redis, centralized config, added health checks, and updated `main.py` flow logic.
- [x] **Resolve Frontend Rendering Issue**: Fixed hydration mismatch in `JournalView` component. Build passed.

- [x] **Security and Privacy Audit**: Completed. No hardcoded occurrences of `OPENROUTER_API_KEY` found (only placeholders/examples). `Life_OS_UI_prototype` is a safe instructional text file.
- [ ] **GraphRAG Dual-Store Ingest**: Implement `ingest_service.py` with single-pipeline transaction logic for Neo4j+Qdrant syncing.
- [x] **GraphRAG Schema**: `schemas.py` updated with `BaseNode` (UUID) and full Therapeutic entity set.
- [ ] **GraphRAG Extractor**: Update `extractor.py` to auto-extract these relationships.
- [ ] **Router Pipeline**: Implement dynamic routing (Empathy vs Fact) in `router.py`.
- [x] **Cleanup**: Deleted `Life_OS_UI_prototype` (safe instructional text file).

*These tasks will be tracked in the GTD‑Tasks inbox and moved to the appropriate areas as work progresses.*
