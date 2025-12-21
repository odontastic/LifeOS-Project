---
title: "AI Agent Entry Point"
type: "Entry Point"
status: "Active"
created: "2025-12-12"
last_updated: "2025-12-14"
tags: ["agent", "entry-point"]
---

***

# AGENTS.md — LifeOS Agent Development Kit

## 1. Purpose

This document defines the **rules, boundaries, and safety protocols** for all agentic AI coders working on LifeOS. Its goal is to ensure that agents contribute to a **stable, human-centered, and philosophically aligned system**—not a runaway feature factory, dependency salad, or accidental SaaS startup.

***

## 2. Guardrail Policy

### 2.1 Hard Constraints

- **Licensing:**  
  - Only use permissively licensed tools (MIT, Apache 2.0, BSD, Public Domain).  
  - No GPL, AGPL, SSPL, RSAL, or restrictive source-available licenses.  
  - Model weights and outputs are treated as user responsibility.

- **Scope:**  
  - Only implement features within the **single-user, local-first, Linux-first** scope.  
  - No multi-user, real-time collaboration, or SaaS hosting unless explicitly approved.

- **Dependencies:**  
  - Pin all dependency versions.  
  - Document why each dependency is needed.

- **Architecture:**  
  - All state changes must occur via the **event bus**.  
  - Never write directly to “tables of record.”  
  - Vector stores and graph stores are **derived data** and must be regenerable.

***

## 3. Agent Behavior Rules

### 3.1 Convergence & Escape Hatch

- **Convergence:**  
  - There is exactly one acceptable interpretation of success.  
  - If ambiguity arises, default to simplicity, explicitness, and reversibility.

- **Escape Hatch:**  
  - If something breaks, the agent must **stop and ask for human approval**.  
  - Never invent a workaround or “helpful” extension without explicit permission.

### 3.2 No Improvisation

- **Architecture:**  
  - No improvisation in architecture, licensing, or scope.  
  - Follow the authoritative stack and event-first design.

- **Scope:**  
  - No feature creep. If a feature smells like a startup pitch deck bullet, it is probably out of scope.

***

## 4. Examples of Protection

### 4.1 Example: Dependency Addition

- **Scenario:**  
  - An agent wants to add a new library for advanced graph analysis.

- **Protection:**  
  - The agent must:
    1. Check the license (must be permissive).
    2. Document why the library is needed.
    3. Ask for human approval before adding it.

### 4.2 Example: Schema Change

- **Scenario:**  
  - An agent wants to change the event schema to support a new feature.

- **Protection:**  
  - The agent must:
    1. Record the change in the event schema version.
    2. Ask for human approval before merging.
    3. Ensure the migration is reversible.

### 4.3 Example: Feature Implementation

- **Scenario:**  
  - An agent wants to implement a new module for real-time collaboration.

- **Protection:**  
  - The agent must:
    1. Check the scope (single-user, local-first).
    2. Recognize that real-time collaboration is out of scope.
    3. Stop and ask for human approval before proceeding.

***

## 5. Explicit Permission Levels

- **Allowed Actions:**  
  - Code generation, documentation, testing, and routine updates.

- **Requires Human Approval:**  
  - Schema changes, new dependencies, major architectural shifts, or any action that affects licensing, security, or scope.

***

## 6. Communication Protocol

- **Escalation:**  
  - If an agent encounters a blocker or has a question, escalate through the appropriate channels (issues, comments, or specific communication channels).

- **Reporting:**  
  - All significant changes, decisions, or issues must be documented in the project’s issue tracker or communication platform.

***

## 7. Error and Exception Handling

- **Error Handling:**  
  - If an agent encounters an error or unexpected behavior, stop and ask for human approval.

- **Exception Handling:**  
  - If an agent receives ambiguous instructions, stop and clarify with a human.

***

## 8. Data Privacy and Security Reminders

- **Data Privacy:**  
  - Never expose or transmit sensitive user data without explicit permission.

- **Security:**  
  - Follow all security best practices and document any security-related changes.

***

## 9. Documentation Updates

- **Updates:**  
  - Agents must update relevant documentation (README, AGENTS.md, GEMINI.md and all /governance files) whenever making significant changes or adding new features.

- **Version Control:**  
  - Ensure all documentation changes are committed and versioned.

***

## 10. Summary

- **Convergence:**  
  - There is exactly one acceptable interpretation of success.

- **Escape Hatch:**  
  - If something breaks, the agent must stop and ask, not invent.

- **No Improvisation:**  
  - Follow the authoritative stack and event-first design.

This document ensures that LifeOS remains **bold, bounded, and survivable**—a human-centered, locally-run system, not a runaway SaaS startup, research project, or dependency salad.

***
