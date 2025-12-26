# LifeOS – Human-Centered Operating System for Life
Modified: 12-24-25

**Status:** > ⚠️ ARCHIVED — This repository is frozen as a speculative platform experiment.  
    > Do not extend. Extract lessons only. See ARCHIVE.md.

**License:** (TBD – must allow commercial use, e.g., MIT or similar)  
LifeOS is a **single‑user, local‑first, AI‑enhanced life management system** that acts as a **second brain, reflective coach, and relational compass**. It integrates **BASB/PARA, GTD, and Zettelkasten** with evidence‑based psychology and emotional intelligence, while following strict **agentic AI and licensing constraints** so it can be commercially viable and understandable months or years from now.
***
## Document Authority Hierarchy

The following documents are authoritative, in order:

1. LifeOS_Master_Specification_(v1.1).md
2. LifeOS_Non_Functional_Invariants_(v1.1).md
3. AGENTS.md

All other documents (README, Design Rationale, ADRs) are explanatory or supportive.
If a conflict exists, higher-ranked documents override lower-ranked ones.

## A. Core Purpose

LifeOS exists to support a **cooperative journey toward virtue, connection, and clarity**—starting with one solo developer dad and extending to others. 

- Strengthen emotional intelligence and relational follow‑through (especially as spouse and father).  
- Unburden the mind from information overload and task anxiety.  
- Turn scattered notes, tasks, and feelings into an **integrated, humane life system** that runs locally and remains under the user’s control.

The system is **single‑user‑first and local‑first**, with the option to evolve into a hosted, multi‑user product later, without redesigning from scratch.

***

## B. Core Philosophy & Pillars

LifeOS rests on four pillars:

1. **Mental Frameworks**  
   - Uses PARA, GTD, Zettelkasten, C4‑style architecture thinking, and mental models to reduce complexity and improve decisions.

2. **Emotional & Spiritual Resilience**  
   - Inner Palette and Calm Compass support emotional granularity, regulation, and practices like daily examen, gratitude, and values alignment.

3. **Evidence‑Based Action**  
   - Draws on CBT/ACT, coaching, and behavioral science for prompts and workflows, not vague self‑help.

4. **Adaptive Mindsets**  
   - Designed to evolve with the user: progressive disclosure, modularity, and adjustable prompts that adapt to changing seasons of life and energy.

All development—human or AI‑driven—must respect a **human‑centered UX pact**: privacy, emotional safety, simplicity, and non‑coercive attention.

***

## C. Core Modules (Product Overview)

LifeOS is a set of cooperating services connected via an event log:

- **Inner Palette**  
  Frictionless emotion & somatic tracking (Plutchik wheel, valence/arousal, body sensations, context tags). Feeds state into other modules.

- **Calm Compass**  
  Grounding and crisis support. For high‑stress states, the interface collapses to simple choices (breathe, connect, reflect later) with science‑backed patterns.

- **Connection Engine**  
  A relationship CRM for real people (family, friends, support network). Tracks meaningful details, open loops, and suggested follow‑ups to support consistent, empathic connection.

- **Prism Clarity Studio**  
  Decision and reflection engine: bias detection, journaling analysis, mental models, and value‑alignment checks.

- **Engine Room (Tasks & Knowledge)**  
  PARA + GTD + Zettelkasten integration. Tasks, projects, and notes are linked to emotional state and relationships rather than isolated.

- **AI Insight Layer**  
  The AI Insight Layer may generate interpretations and recommendations, but must never initiate actions, modify state, or override user intent.
  Local LLM‑powered analysis (via Ollama) using LlamaIndex and LangChain within clear boundaries. Generates summaries, patterns, and recommendations grounded in the user’s own data.

Agent‑specific details (prompting, roles, constraints) live in `AGENTS.md` and `/docs/04_Agent_Guide.md`.

***

## D. Authoritative Technical Stack & Constraints

### Hard Non‑Negotiables

- **Licensing:**  
  - All dependencies must be **permissively licensed** (MIT, Apache‑2.0, BSD, Public Domain).  
  - **No** GPL, AGPL, SSPL, RSAL, or restrictive source‑available licenses.  
  - Model weights and outputs are treated as **user responsibility**.

- **Runtime & Language:**  
  - **Python 3.11.x only** for backend.  
  - Do not rely on “latest” anything; all versions must be pinned.

### Stack (Authoritative)

- **Backend**  
  - Python 3.11  
  - FastAPI

- **AI & Retrieval**  
  - **LlamaIndex** – document ingestion, indexing, retrieval, graph grounding  
  - **LangChain** – prompt templates and chain orchestration only  
  - **Ollama** – local models only (no cloud AI is required for core operation)

- **Data Stores**  
  - **SQLite** – primary local persistence and append‑only event log  
  - **ArangoDB** (Apache 2.0) – graph data only  
  - **Qdrant** (MIT) – vector storage

- **Frontend**  
  - React (web)  
  - Open WebUI (optional, never a core dependency)

### Explicit Non‑Goals

The following are **out of scope** and must not be implemented in this project:

- Multi‑user SaaS hosting  
- Mobile‑native apps (iOS / Android)  
- Mobile-native apps are intentionally out of scope to preserve:
    - local data control
    - low notification pressure
    - deep work over ambient engagement
- Real‑time collaboration  
- Payments, billing, subscriptions  
- Analytics, tracking, telemetry  
- Auto‑updating models  
- Autonomous self‑modifying agents

If it feels like a pitch‑deck bullet, it probably does not belong in v1.

***

## E. System Architecture (High‑Level)

### Operating Mode

- **Single user**  
- **Local‑first**, Linux‑first  
- Offline‑tolerant (only model downloads and optional remote APIs require network)  
- One user, one active session, low write concurrency  
- No premature scaling.
- LifeOS must remain usable and meaningful with zero historical data ("cold start"), without requiring prior journaling, tagging, or model training.


### Event‑First Design

- No business logic writes directly to “tables of record.”  
- All state changes are represented as **events** in a SQLite‑backed **append‑only event log**.  
- Each event has:
  - `event_id`  
  - `event_type`  
  - `timestamp`  
  - `payload` (JSON)  
  - `schema_version`
- Read models and indices are derived by replaying events.  
- Vector stores (Qdrant) and graph (ArangoDB) are **derived data** and must be regenerable from the event log + exported documents.

### Context & Containers

- **Context / Integrations (optional):**  
  - Filesystem (Markdown, configs, exports)  
  - Email / Calendar (if configured)  
  - Local LLM runtime (Ollama)

- **Core Containers:**  
  - `emotion_service` – Inner Palette, Calm Compass, emotion event handling  
  - `relationship_service` – Connection Engine  
  - `reflection_service` – Prism Clarity Studio  
  - `task_knowledge_service` – Engine Room (PARA, GTD, Zettelkasten)  
  - `ai_insight_service` – LlamaIndex/LangChain orchestration

***

## F. Data Ownership & Export

Users must always be able to:

- Export all data as **JSON + Markdown**.  
- Delete all data **irreversibly** on demand.  
- Rebuild indices (vector, graph) from exported data and/or event log.  

Vector stores and graph stores are **derived** and must be fully reconstructable.

***

## G. Retrieval & AI Boundaries

**Responsibility Split:**

- **LlamaIndex**  
  - Document ingestion  
  - Vector indexing  
  - Graph grounding  
  - Retrieval primitives

- **LangChain**  
  - Prompt templates  
  - Tool routing  
  - Chain composition

Do **not** duplicate responsibilities between these libraries.

**Hybrid Retrieval Rules:**

- Combine:  
  - Semantic search via **Qdrant**  
  - Keyword search via LlamaIndex keyword index  
  - Graph‑based context via **ArangoDB**
- Use an explicit composite retriever with clear ranking and fallbacks.  
- If graph retrieval is unavailable, degrade gracefully to vector + keyword.

***

## H. Project Structure

A one‑level view (subject to evolution):

- `/apps` – Application source  
  - `/backend` – FastAPI app, event log, services  
  - `/frontend` – React UI  
- `/knowledge_base` – PARA/GTD system, Zettelkasten, user content  
- `/docs` – Extended documentation  
  - `01_LifeOS_Master_Plan.md` – Vision, philosophy, product spec  
  - `02_Schema_and_Standards.md` – Data models, file and event schemas  
  - `03_Architecture_Decisions.md` – ADRs (Architecture Decision Records)  
  - `04_Agent_Guide.md` – How to work with AI agents safely  
- `/prompts` – Master prompts (coder, reflection, summarization, etc.)  
- `/data` – Local DB files, config, backups (**never committed**)  
- `/tests` – Unit, integration, and resilience tests  
- `AGENTS.md` – High‑level instructions, roles, and constraints for agentic coders

For a conceptual map, see **[LifeOS Map of Content (LIFOS_MOC.md)](./LIFOS_MOC.md)**, which links to all key documents.

***

## I. Installation & Setup (Dev)

**Prerequisites** (example; see docs for final versions):

- Linux (CachyOS / Arch preferred)  
- Python 3.11.x  
- Node.js (LTS)  
- SQLite  
- Qdrant + ArangoDB (local containers/services)  
- Optional: Ollama for local LLMs

**Clone & Setup:**

```bash
git clone <repo-url> lifeos
cd lifeos
```

Backend example:

```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # configure DB paths, model names, etc.
```

Frontend example:

```bash
cd apps/frontend
npm install
cp .env.example .env.local
npm run dev
```

Exact commands will be documented in `/docs` as the implementation stabilizes.

***

## J. Development Flow & Quality

### Testing Requirements

Minimum required tests:

- Event creation and replay  
- Index rebuild from scratch  
- Query without graph data  
- Query with corrupted vector store (graceful fallback)

Integration tests focus on **critical pipelines** (e.g., emotion_logged → Calm Compass → AI Insight → visible task filtering).

### Linting & Style

- **Python:** Black, isort, and a linter like flake8 or Ruff  
- **JS/TS:** ESLint + Prettier  
- All dependencies must be version‑pinned (requirements.txt / Poetry lockfile).  
- For each dependency, document why it exists in a short comment or doc.

### Error Handling & Logging

- Every meaningful action should emit **human‑readable logs**.  
- Fail loudly and clearly, never silently.  
- If something cannot be implemented safely (license, security, ambiguity), code should stop and surface an explicit message.

### Schema & Migration Safety

- Every migration must be reversible.  
- Never delete user data implicitly.  
- Schema changes must bump schema version and be recorded in ADRs.

***

## K. Human‑Centered Design & UX Pact

Core UX principles:

- **Frictionless when stressed, deep when calm**  
  - 1–2 click capture for emotions and quick notes.  
  - Advanced tools available but never forced.

- **Non‑coercive attention**  
  - No streaks, manipulative gamification, or guilt‑based nudges.

- **Emotional safety**  
  - Supportive, non‑judgmental language.  
  - Clear boundaries: LifeOS is a tool, not a therapist.

- **Privacy‑first**  
  - No analytics or telemetry.  
  - No hidden remote calls with emotional or relational data.

***

## L. When AI Agents Must Ask for Human Approval

Agentic coders must **pause and request approval** (via issue, TODO, or explicit prompt) if:

- A new dependency is required.  
- A schema or event type must change.  
- A license is unclear or borderline.  
- A constraint (runtime, stack, non‑goal) conflicts with reality.

Silence is **not** consent. When in doubt, stop and ask.

***

## M. Definition of Done (v1)

The project is “functionally complete” when:

1. LifeOS runs locally on Linux with a single, documented command (or short sequence).  
2. A user can ingest data (notes/documents and basic events).  
3. A user can ask questions about their data and receive **grounded, cited** responses.  
4. Emotional events can be logged and routed to Calm Compass and other modules.  
5. All user data can be exported and deleted.  
6. Indexes (vector and graph) can be rebuilt from exported data/event log.

Once these are met, v1 should prioritize stability, documentation, and small refinements over feature creep.

***

## N. Where to Go Next

- **Read:** `LIFOS_MOC.md` for the full map of content.  
- **Understand:** `/docs/01_LifeOS_Master_Plan.md` for philosophy and product vision.  
- **Implement:** Follow `/docs/02_Schema_and_Standards.md` and `AGENTS.md` for concrete schemas and agent instructions.  
- **Record Decisions:** Use `/docs/03_Architecture_Decisions.md` when making any structural change.

The guiding question for any change—human or AI—is:

> Does this help a real human live with more **virtue, connection, clarity, and peace**, without sacrificing their autonomy or privacy?

***

Here’s the updated **README.md** with a new section describing the **agent guidelines overview** as requested, plus a check for any other essential or helpful sections that could be included. The section is written in a way that communicates the convergence, clarity, and safety principles of your agent policy, while fitting naturally into the existing document structure.

***

## O. Agent Guidelines Overview

LifeOS is designed to be developed and extended by **agentic AI coders**, but only within strict, clearly defined boundaries. 

### Why This Matters

- **Forces Convergence:**  
- **Eliminates Ambiguity:** 80% of future arguments are avoided by:
  - Pinning Python 3.11.x and all dependencies.  
  - Declaring single-user, local-first scope.  
  - Making derived data (vector/graph stores) disposable and regenerable.  
  - Making the event bus and data contracts concrete and explicit.  
- **Provides an Escape Hatch:** If something breaks or a constraint conflicts with implementation reality, the agent must **stop and ask for human approval**—not invent a workaround or “helpful” extension.

### Natural Extensions (Future-Proofing)

If the project evolves, the next logical steps are:
- A **“Hosted Mode Delta”** document (what changes when moving from SQLite to a hosted, multi-user backend).  
- A **Canonical Event Schema appendix** (pure JSON, zero prose).  
- A **Prompting Constitution for LifeOS** (separate from the coder’s instructions).

***

## P. Essential & Helpful Sections Checklist

Here’s a quick checklist of sections that are **essential or highly recommended** for a robust, maintainable, and collaborative LifeOS project:

| Section | Included? | Notes |
|--------|-----------|-------|
| Project Title & Status | ✅ | Clear visibility |
| Core Purpose & Philosophy | ✅ | Connects tech to human goals |
| Core Modules & Architecture | ✅ | Modular, event-first design |
| Technology Stack & Constraints | ✅ | Licensing, runtime, stack |
| Project Structure | ✅ | Folder layout, doc links |
| Installation & Setup | ✅ | Dev environment steps |
| Development Flow & Quality | ✅ | Testing, linting, style |
| Human-Centered UX Pact | ✅ | Frictionless, safe, privacy-first |
| Agent Guidelines Overview | ✅ | Convergence, escape hatch, future-proofing |
| Definition of Done | ✅ | v1 success criteria |
| Where to Go Next | ✅ | Doc map, next steps |

### Additional Helpful Sections (Optional)

| Section | Consider Adding? | Notes |
|--------|------------------|-------|
| Security & Privacy Policy | ⚠️ | Especially for SaaS evolution |
| Changelog / Release Notes | ⚠️ | For version tracking |
| Community & Contribution Guidelines | ⚠️ | If opening to collaborators |
| Troubleshooting & FAQ | ⚠️ | For new users or agents |
| Glossary of Terms | ⚠️ | For clarity on jargon |

All essential sections are included in the current README.md. Optional sections can be added as the project grows or opens to collaborators.

***

