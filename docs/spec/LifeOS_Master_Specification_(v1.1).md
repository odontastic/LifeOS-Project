# LifeOS Master Specification v1.1
Created 12-24-25
## Status

Normative. Unified. Safety-locked.

## 0. Purpose & Scope

LifeOS is a local-first personal operating system designed to support human judgment, emotional regulation, relational fidelity, and deliberate action without delegating authority to automation or AI. This specification defines the invariant architecture, reasoning constraints, and lifecycle rules that govern all implementations.

This document supersedes all prior partial specifications (v1.0–v1.01). Where conflicts existed, safety, reversibility, and human authority prevailed.

---

## 1. Foundational Principles (Non-Negotiable)

1. **Human Authority**: No system component may assert truth, identity, or obligation.
2. **Cold–Warm Separation**: Analysis and synthesis never occur during emotional distress.
3. **Decay by Default**: All meaning degrades unless reaffirmed by a human.
4. **Local-First Sovereignty**: User data is local, inspectable, and portable.
5. **AI as Proposer Only**: AI suggests; humans ratify.

---

## 2. Canonical Architecture Layers

### 2.1 Capture Layer

Raw intake of text, emotion, events, or notes. No interpretation.

### 2.2 Distillation Layer

Structured questioning, classification, and atomization. May be AI-assisted but requires human ratification.

### 2.3 Reasoning Layer (Epistemic Distillation)

Pattern detection, aggregation proposals, and reflection prompts. Never prescriptive.

### 2.4 Action Layer

Tasks, reminders, and behaviors derived only from human-approved insights.

### 2.5 Memory & Decay Layer

Applies half-life rules, override enforcement, and dissolution logic.

---

## 3. Insight Model

### 3.1 Insight Atom

A time-bound, context-scoped observation ratified by a human.

**Required Fields**:

* id
* timestamp
* content
* context_tags
* emotional_state (optional)
* prompt_version
* invariant_version
* decay_profile

### 3.2 Warm Insight

Tentative synthesis of one or more atoms. Decays faster than atoms.

### 3.3 Aggregate Insight

Descriptive grouping of warm insights. Read-only by default. Cannot exist without live atoms.

---

## 4. Insight Aggregation Rules (Normative)

### Invariants

* Aggregation is descriptive, never explanatory.
* Aggregation does not increase authority.
* Aggregates dissolve automatically if supporting atoms decay.
* Cross-temporal aggregation requires explicit human confirmation.
* Aggregates are read-only unless edited by a human.

### Lifecycle

Detection → Proposal → Human Ratification → Warm Aggregate → Decay → Dissolution

---

## 5. Emotional Safety & Inner Palette Invariants

* Emotional logging must be executable in under 15 seconds.
* High arousal states block analysis and aggregation.
* During distress, system may only suggest grounding actions.
* No recursive questioning during emotional peaks.

---

## 6. Override Semantics (Absolute Authority)

### Override Types

* **Mute**: Suppress surfacing and aggregation. Silent decay continues.
* **Freeze**: Halt decay and aggregation. Requires explicit review.
* **Delete**: Permanent removal with cascade deletion.

### Invariants

* Overrides are absolute and irreversible by AI.
* Overrides require no justification.
* Muted or deleted data cannot influence future reasoning.

---

## 7. Decay & Temporal Logic

### Temporal Layers

* Immediate: hours–days
* Episodic: days–weeks
* Structural: weeks–months

### Tiered Decay Rules

* Immediate insights decay rapidly (half-life ~3–7 days).
* Episodic insights decay moderately (half-life ~14–21 days).
* Structural insights decay slowly but never become identity claims.

Decay is exponential and irreversible without human reaffirmation.

---

## 8. Prompt Governance & Versioning

### Rules

* Every insight stores prompt_version and invariant_version.
* New logic cannot reinterpret old insights.
* Legacy insights require re-ratification.
* Runtime compatibility checks are mandatory.
* Governance changes are user-visible and opt-in.

---

## 9. Connection Engine (Relational Integrity)

* Relationships are first-class entities.
* Tracks concerns, context, and follow-up loops.
* No sentiment scoring without user visibility.
* Prompts are suggestive, never obligatory.

---

## 10. Failure-Mode Design

### User Disengagement

* System enters dormancy.
* No escalation, no backlog pressure.
* On return: gentle recap, no judgment.

### Data Degradation

* Orphaned insights dissolve.
* Frozen insights require review.

---

## 11. Explicit Non-Goals

LifeOS will not:

* Diagnose mental health conditions
* Define user identity or personality
* Optimize productivity at the expense of well-being
* Perform covert behavioral shaping
* Centralize or monetize user data

---

## 12. Compliance & Auditability

All modules must:

* Declare invariant dependencies
* Fail closed on violation
* Expose logs for human inspection

---

## 13. Versioning

**LifeOS Master Specification v1.1**

* Unified, safety-locked baseline
* Future changes require explicit migration rules and review

---

End of Specification.
