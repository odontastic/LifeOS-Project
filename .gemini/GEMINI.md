# GEMINI.md — LifeOS Project-Specific Guide

This file provides **authoritative, project-specific instructions** for the Gemini coding agent working inside the LifeOS repository. It complements (and does not replace) `AGENTS.md` and the **LifeOS Agentic AI Coder Master Instructions**.

The following documents are authoritative, in order:

1. /docs/spec/LifeOS_Master_Specification_(v1.1).md
2. /docs/spec/LifeOS_Non_Functional_Invariants_(v1.1).md
3. AGENTS.md
4. This GEMINI.md `/.gemini/GEMINI.md`

---
AUTHORITY, SCOPE, CONSTRAINTS — Sections 1–4

## 1. Project Overview

**LifeOS** is a local-first, single-user, AI-enhanced personal system that functions as:

* A second brain
* A life coach
* A task and knowledge manager

It integrates ideas from PARA, GTD, and reflective journaling, with strong emphasis on:

* Personal growth
* Emotional intelligence
* Knowledge capture and retrieval

LifeOS is designed to be **commercially viable**, **permissively licensed**, and **fully user-owned**.

---

## 2. Operating Assumptions (Hard Context)

* Target mode: **single-user, local-first**
* Platform: **Linux** (CachyOS / Arch preferred, but not required)
* No multi-user SaaS assumptions
* No background analytics or telemetry

Do not introduce scale-oriented infrastructure unless explicitly instructed.

HARD CONSTRAINT:
All code, prompts, and logic MUST conform to:
1. MVP Product Specification
2. Supervisor Prompt
3. Supervisor Enforcement Pseudocode

If a conflict exists, Supervisor Enforcement Pseudocode takes precedence.
If unsure, STOP and ask for clarification.

AI agents may propose changes but have no authority to ratify:
- architectural decisions
- ethical boundaries
- scope expansions
- invariant modifications

All such changes require explicit human approval.

---

## 3. Prerequisites

### System Requirements

* Linux
* Python **3.11.x only**
* Node.js **LTS**
* SQLite
* Docker Engine (not Docker Desktop)

### Services (Local)

* Qdrant (vector store)
* ArangoDB (graph store)
* Ollama (optional, for local LLM inference)

All services must be runnable locally via Docker or system services.

---

## 4. Repository Layout (Expected)

```
lifeos/
├── apps/
│   ├── backend/
│   │   └── lifeos-rag-api/
│   └── frontend/
├── docs/
├── governance/
├── System/
│   └── AI-Context/
├── AGENTS.md
├── GEMINI.md
└── README.md
```

If the repository deviates, document the deviation.

---

WORKFLOW Sections — 5-9

## 5. Installation & Setup

### Clone Repository

```bash
git clone <repo-url> lifeos
cd lifeos
```

### Backend Setup

```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure:

* SQLite paths
* Qdrant URL
* ArangoDB credentials
* Model names (Ollama)

### Frontend Setup

```bash
cd apps/frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## 6. Development Workflow

### Authoritative Guides

* Primary architecture and rules: `docs/04_Agent_Guide.md`
* Current objective: `System/AI-Context/current_objective.md`
* Open questions: `System/AI-Context/open_questions.md`

### Task Tracking

* Use the `write_todos` tool
* Persist tasks in:

  * `System/AI-Context/session_tasks.md`

### Session Summaries

* Write a session summary to:

  * `System/AI-Context/current_session_summary.md`
* Frequency:

  * No more than once every 15 minutes
  * Always at end of a work session

### Session Archiving

* Append session summaries to:

  * `System/AI-Context/Archived-Conversation-Summaries.md`

### Version Control Discipline

* Commit no more than once every 30 minutes
* Commit when a logical unit of work completes
* Before final commit of a session:

  * Generate an **End-of-Day Report** using `git diff`

---

## 7. Build & Run Commands

### Backend (Docker)

```bash
docker-compose build
docker-compose up -d
docker-compose down
```

### Frontend

```bash
npm install
npm run dev
npm run build
```

---

## 8. Code Style & Quality

### General

* Prefer clarity over cleverness
* Avoid premature abstraction

### Python

* Format with **Black**
* Use type hints
* Docstrings must explain **what** and **why**

### TypeScript / JavaScript

* Format with **Prettier**
* Prefer explicit types

Public-facing functions and APIs must be documented.

---

## 9. Testing Expectations

Minimum required:

* Manual verification of new features
* Event creation and replay tests
* Index rebuild from raw data
* Degraded-mode tests (missing graph or vector store)

Frontend:

* Use Playwright for basic verification scripts

If a test cannot be written safely, document why.

---
SAFETY, ESCALATION, VALUES — Sections 10–14

## 10. Security & Safety

### Secrets Management

* Store secrets only in `.env`
* Never commit secrets
* `.env.example` is mandatory for new variables

### User Safety

* `safety.py` includes crisis-language detection
* Use it to:

  * Provide disclaimers
  * Suggest external help when appropriate

No medical, legal, or therapeutic claims.

---

## 11. Commit Message Guidelines

Follow **Conventional Commits**:

**Header**

* Imperative mood
* ≤ 50 characters

**Body**

* What changed and why

**Footer**

* Issue references if applicable

Example:

```
feat: add AI analysis for risk audit

Adds a backend endpoint for weekly risk audit analysis
and connects the frontend UI to the new endpoint.

Closes #123
```

---

## 12. Documentation Discipline

When making significant changes:

* Update README.md
* Update AGENTS.md if agent behavior changes
* Update GEMINI.md if workflow or tooling changes

Documentation drift is considered a bug.

---

## 13. Escalation Rules

Pause and escalate if:

* A new dependency is required
* A schema must change
* Licensing is unclear
* Constraints conflict with implementation reality

Do not silently improvise.

---

## 14. Final Reminder

LifeOS values:

* User ownership
* Reversibility
* Transparency

If forced to choose between speed and correctness, choose correctness.
