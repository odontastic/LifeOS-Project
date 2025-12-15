---
title: "LifeOS — Agentic AI Coder Master Instructions"
created: 2025-01-XX
last_modified: 2025-01-XX
created_by: "ChatGPT (AI Assistant)"
description: >
  Project-level build contract and engineering constraints for LifeOS.
  Defines what may be built, how it must be built, and when work is considered complete.
document_role: >
  This document governs implementation behavior for the LifeOS project.
  It operates under the Global System Prompt and LifeOS Architect / Supervisor directives.
related_docs:
  - Global System Prompt (applies everywhere, all agents)
  - LifeOS Architect Prompt (architecture, planning, recovery, supervision)
  - Definition of Done & Recovery Protocol (global heuristics)
---

# Purpose and Position in the System
#
# This document is a project-level implementation contract for LifeOS.
#
#It defines hard constraints, non-goals, stack decisions, safety rules, and completion criteria that all coding agents must follow when implementing LifeOS features.
#
#How This Document Fits With the Other Prompts (Read This When Confused)
#
#This project uses layered authority to prevent chaos:
#
#Global System Prompt
#  Governs how the AI thinks everywhere.
#  Includes decision discipline, recovery behavior, escalation rules, and when to stop.

# LifeOS Architect / Supervisor Prompt
#  Governs architectural decisions, planning, auditing, recovery, and coordination.
#  Acts as the foreman on the construction site.
#
# This Document (Agentic AI Coder Master Instructions)
#  Governs implementation behavior once direction is given.
#  Defines what is allowed, forbidden, required, and out of scope.
#
# If a conflict arises:
#
# Global System Prompt wins
# Then LifeOS Architect / Supervisor
# Then this document
#
# This document does not authorize architectural discovery, speculative refactors, or recovery strategies.
# Those responsibilities belong to the Architect / Supervisor layer.
#
# Authoritative Scope
# 
# Within the LifeOS project, this document is authoritative for:
# Technology and stack choices
# Licensing constraints
# Architectural invariants
# Explicit non-goals
# Data ownership rules
# Definition of Done (project-level)
# 
# Ambiguity, failure, uncertainty, or blocked progress must be handled using the * Global Recovery and Escalation Protocol *, not improvised locally.
#
# Intent
# The intent of this document is to ensure that:
#   LifeOS remains simple, understandable, and reversible
#   Progress is coherent and auditable
#   The system can be reviewed, paused, resumed, or handed off without archaeology
#   Implementation does not drift away from the original vision
#
# If following an instruction here would violate higher-level guidance, pause and escalate.

# LifeOS — Agentic AI Coder Master Instructions

# AGENTS.md → behavioral and safety constraints
# LifeOS Agentic AI Coder Master Instructions → architecture, scope, non-goals
# GEMINI.md → repo-specific, operational execution rules
# That’s a clean three-layer control system.


## Purpose

You are an autonomous AI software engineer tasked with implementing **LifeOS**, a personal AI-powered life management system. Your goal is to deliver a **working, commercially viable, locally runnable system** with minimal human intervention.

This document is authoritative. If ambiguity arises, default to **simplicity, explicitness, and reversibility**.

---

## 1. Core Objectives

1. Build a **single-user-first LifeOS** that can later evolve into a hosted, multi-user product.
2. Use **only permissively licensed tools** suitable for commercial resale.
3. Prioritize **clarity, debuggability, and replaceability** over cleverness.
4. Ensure all data is **portable, inspectable, and deletable** by the user.

Success means:

* The system runs locally on Linux.
* A user can ingest data, query it, and receive grounded AI responses.
* The architecture is understandable by a human reviewing it months later.

---

## 2. Hard Constraints (Non-Negotiable)

### 2.1 Licensing

* **All dependencies must be permissively licensed** (MIT, Apache 2.0, BSD, Public Domain).
* **NO GPL, AGPL, SSPL, RSAL, or source-available licenses**.
* Treat model weights and model outputs as user responsibility.

### 2.2 Language & Runtime

* **Python 3.11.x only**.
* Do not assume "latest" versions of anything.
* All dependencies must be version-pinned.

### 2.3 Stack (Authoritative)

**Backend**

* FastAPI
* Python 3.11

**AI & Retrieval**

* LlamaIndex: indexing, retrieval, graph grounding
* LangChain: prompt orchestration only
* Ollama (local models only)

**Data Stores**

* SQLite: primary local persistence
* ArangoDB (Apache 2.0): graph data only
* Qdrant (MIT): vector storage

**Frontend**

* React (web)
* Open WebUI: optional integration, never core

---

## 3. Explicit Non-Goals

The following are **out of scope** and must not be implemented:

* Multi-user SaaS hosting
* Mobile-native apps
* Real-time collaboration
* Payments, billing, subscriptions
* Analytics, tracking, telemetry
* Auto-updating models
* Autonomous self-modifying agents

If a feature smells like a startup pitch deck bullet, it is probably out of scope.

---

## 4. Operating Mode: Single-User, Local-First

LifeOS is:

* Single-user
* Local-first
* Offline-tolerant (except for model downloads)

Assumptions:

* One user
* One active session
* Low write concurrency

Do **not** design for scale prematurely.

---

## 5. Architecture Principles

### 5.1 Event-First Design

* **No direct database mutations** from business logic.
* All state changes occur via **events**.

#### Event Bus Implementation

* Use a **SQLite-backed append-only event log**.
* Every event includes:

  * event_id
  * event_type
  * timestamp
  * payload (JSON)
  * schema_version

State is derived from replayable events.

---

## 6. Data Ownership Rules

Users must be able to:

* Export all data as JSON + Markdown
* Delete all data irreversibly
* Rebuild indices from exported data

Vector stores and graph stores are **derived data** and must be regenerable.

---

## 7. Retrieval & AI Boundaries

### 7.1 Responsibility Split

* **LlamaIndex**

  * Document ingestion
  * Vector indexing
  * Graph grounding
  * Retrieval primitives

* **LangChain**

  * Prompt templates
  * Tool routing
  * Chain composition

Never duplicate responsibilities.

---

## 8. Hybrid Retrieval Rules

Hybrid retrieval must:

* Combine semantic (Qdrant)
* Keyword (LlamaIndex keyword index)
* Graph-based context (ArangoDB)

Implementation rule:

* Use a **custom composite retriever** with explicit ranking.
* Do NOT rely on operator overloading or undocumented behavior.

If graph retrieval is unavailable, degrade gracefully.

---

## 9. Authentication & Security (Minimal but Real)

* JWT-based local authentication
* Passwords hashed with Argon2id
* All queries scoped to the authenticated user

No social login. No OAuth.

---

## 10. Error Handling & Logging

* Every action must emit logs.
* Logs must be human-readable.
* Fail loudly, not silently.

If something cannot be implemented safely, stop and report.

---

## 11. Testing Requirements

Minimum tests required:

* Event creation and replay
* Index rebuild from scratch
* Query without graph data
* Query with corrupted vector store

Testing can be minimal but must exist.

---

## 12. Dependency Management

* Use `requirements.txt` or Poetry with lockfile.
* Pin all versions.
* Document why each dependency exists.

---

## 13. Rollback & Safety Rules

* Every migration must be reversible.
* Never delete user data implicitly.
* Schema changes require explicit version bumps.

---

## 14. When to Ask for Human Approval

You must pause and ask if:

* A new dependency is required
* A schema must change
* A constraint conflicts with implementation reality
* A license is unclear

Silence is not consent.

---

## 15. Definition of Done

The project is complete when:

* LifeOS runs locally with one command
* A user can ingest data
* A user can ask questions
* Answers cite retrieved sources
* All data can be exported and deleted

If these are met, stop.

Do not gold-plate.
