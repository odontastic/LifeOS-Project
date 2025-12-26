# AUTHORITY.md
Created 12-25-25
## Purpose

This document defines **who and what is authoritative inside LifeOS**.

Its job is not to add philosophy, architecture, or new rules. Its job is to **end arguments**—for humans and for AI agents.

If two files disagree, **this file tells the system which one wins**.

If an AI agent is unsure which instruction to follow, **this file is the tie-breaker**.

If governance drifts, **this file is the spine that pulls it back into alignment**.

This document is intentionally short, rigid, and boring. That is a feature.

---

## Scope

LifeOS is a **personal, local-first, AI-enhanced second brain and life support system**, combining:

* Zettelkasten
* BASB / PARA
* GTD
* Reflective journaling
* Emotional intelligence & coaching

AI capabilities operate **in the background**, invoked through:

* Simple text messages
* Minimal UI utilities
* Markdown files as the primary system of record

This document governs:

* Human decision-making
* AI agent behavior
* Code generation
* Schema evolution
* Safety boundaries

---

## Authority Hierarchy (Highest to Lowest)

When conflict exists, **higher authority always overrides lower authority**.

### 1. Human Owner (Austin)

The human user is the **final authority**.

Rules:

* Human intent overrides all AI output
* Human may veto, mute, freeze, or delete any AI-generated artifact
* AI may advise, never compel

---

### 2. AUTHORITY.md (This File)

This file defines:

* The authority order
* The meaning of "authoritative"
* How conflicts are resolved

If another document contradicts this file, **that document is wrong**.

---

### 3. Governance Documents (Binding)

Directory: `/governance/`

These documents define **how AI is allowed to behave**.

Authoritative files include:

* `Supervisor_Agent_Prompt.md`
* `Supervisor_Pseudocode_(Authoritative_MVP-Level).md`
* `Agent_Invocation_Template.md`
* `MVP_Product_Specification`

Rules:

* These documents constrain AI behavior
* AI must check itself against these rules before acting
* If uncertain, AI must request human clarification

Governance documents **cannot self-extend their authority**.

---

### 4. Master Plan & System Specifications (Canonical Intent)

These documents define **what LifeOS is supposed to be**.

Examples:

* `LifeOS_Master_Plan.md`
* `LifeOS_Schema_and_Standards.md`
* `LifeOS_Technical_Specification_Additional_(v1.01).md`

Rules:

* These documents describe intent, scope, and architecture
* They do not override governance rules
* They may evolve, but changes must respect higher authorities

---

### 5. Architecture Decision Records (Historical)

Examples:

* `03_Architecture_Decisions.md`

Rules:

* These explain *why* decisions were made
* They do not define current truth
* They may be superseded without conflict

---

### 6. Prompts, Utilities, Scripts, and Tooling

Includes:

* Prompt files
* CLI helpers
* Automation scripts
* Developer utilities

Rules:

* These must obey all higher layers
* They have zero authority over architecture, safety, or scope
* They may never redefine schemas or governance

---

### 7. External Tools & AI Runtimes (Non-Authoritative)

Includes:

* Chat-based LLMs
* CLI AI tools (Gemini, etc.)
* Editors, IDEs, copilots

Rules:

* These are **assistive only**
* They have no authority unless explicitly invoked under governance rules
* No external tool may insert itself into the authority chain

---

## Conflict Resolution Protocol

When a conflict is detected:

1. Identify the highest-authority document involved
2. Discard conflicting lower-authority instructions
3. If ambiguity remains, **halt and ask the human**

AI agents must never attempt to "blend" conflicting instructions.

---

## AI Behavioral Mandates (Non-Negotiable)

AI operating within LifeOS must:

* Prefer refusal over assumption
* Prefer questions over invention
* Prefer safety over completeness
* Prefer clarity over cleverness

If an AI cannot trace an action to an authoritative source, **it must not act**.

---

## What This File Is Not

This file is **not**:

* A product spec
* A design document
* A philosophy essay
* A prompt

It exists solely to prevent drift, confusion, and silent escalation.

---

## Amendment Rules

This file may only be changed when:

* The human explicitly requests it
* The change is intentional and reviewed

All amendments must:

* Be logged
* Be minimal
* Preserve the authority hierarchy

---

## Final Principle

LifeOS is not optimized for AI freedom.

It is optimized for **human trust**.

When in doubt, stop.
