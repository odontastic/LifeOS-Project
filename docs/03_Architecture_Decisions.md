---
title: "LifeOS Architecture Decisions"
type: "Documentation"
status: "Archived"
created: "2025-11-20"
last_updated: "2025-12-11"
tags: ["documentation", "architecture", "gtd", "para", "decision-record"]
---

# LifeOS Architecture Review & Decisions

**Date**: 2025-11-20  
**Reviewer**: System Architect  
**Scope**: Evaluate PARA-PKM-GTD integration for structure, simplicity, maintainability, and future adaptability.
**Note**: This document is an architectural decision record. It reflects the state of the architecture at the time of writing and the reasoning that led to the current `LifeOS Master Plan`.

---

## 🎯 Executive Summary

**Critical Finding**: The initial architectural proposal **mixed organizational paradigms with content types**, creating unnecessary complexity and missing core GTD components.

**Recommendation**: Adopt a **pure PARA structure** with GTD components added as peers, using metadata (tags/YAML) for content typing rather than directory structure. This recommendation was accepted and forms the basis of the current system architecture.

---

## 📊 Initial Proposal Analysis

### Proposed Structure (Now Deprecated)
```
00-Inbox/           # GTD capture
01-Projects/        # PARA Projects
02-Areas/           # PARA Areas  
03-Resources/       # PARA Resources
04-Archives/        # PARA Archives
05-Journal/         # PKM temporal notes
06-Knowledge/       # PKM Zettelkasten
07-People/          # CRM
99-System/          # Meta
```

### Evaluation Against Criteria

#### ❌ **Structure & Logic** (Score: 4/10)
**Problems**:
- PARA is designed as a complete system (Projects, Areas, Resources, Archives).
- Adding `05-Journal/`, `06-Knowledge/`, `07-People/` **breaks PARA's paradigm**.
- These are actually content types that should fit WITHIN PARA categories:
  - **Journal** → Area (ongoing responsibility to reflect)
  - **Knowledge** → Resources (reference material for thinking)
  - **People** → Resources (reference about relationships)

**Philosophy clash**: PARA asks "What is this FOR?" while the initial proposal asked "What TYPE is this?"

#### ❌ **Integration & Connectivity** (Score: 4/10)
**CRITICAL PROBLEMS**:
1. **No dedicated Next Actions location**: A core requirement of GTD. It was unclear where all `@Computer` tasks would be listed.
2. **No "Waiting For" tracking**: Another essential GTD component was missing.
3. **Unclear MOCs structure**: Maps of Content were mentioned but not implemented in the structure.
4. **Zettelkasten vs PARA tension**: The flat structure of a Zettelkasten conflicted with PARA's actionability-based hierarchy.

---

## 🏗️ Revised & Adopted Proposal: "PARA-Core + GTD Extensions"

### Philosophy
1. **Respect PARA** for what it does well (prioritization, actionability).
2. **Add GTD components** as peers (not forced into PARA).
3. **Use metadata** for content typing (not folders).
4. **Support multiple views** via queries/MOCs.

### Adopted Structure

```
LifeOS/
├── GTD-Tasks/                  # 🎯 GTD: ALL actionable items
│   ├── 0-Inbox/
│   ├── 1-Next-Actions/
│   ├── 2-Waiting-For/
│   ├── 3-Someday-Maybe/
│   ├── 4-To-Read/
│   ├── 5-To-Think-About/
│   └── 6-Needs-Processing/
│
├── Projects/                   # 📋 PARA: Outcomes with deadlines
│   ├── Active/
│   ├── Someday/
│   └── Completed/
│
├── Areas/                      # 🏠 PARA: Ongoing responsibilities
│   └── Personal-Reflection/   # ✅ Journal lives here
│
├── Resources/                  # 📚 PARA: Reference material
│   ├── Zettelkasten/         # ✅ PKM lives here
│   ├── MOCs/                  # ✅ MOCs live here
│   └── People/                # ✅ CRM lives here
│
├── Archives/                   # 🗄️ PARA: Inactive content
│
└── System/                     # ⚙️ Meta: System documentation
    ├── Prompts/
    ├── Templates/
    └── Context-Definitions/
```

### Key Changes & Rationale

#### 1. **Journal → `Areas/Personal-Reflection/`**
**Rationale**: Journaling is an ongoing responsibility (an Area), not a separate top-level category. This aligns perfectly with the PARA definition.

#### 2. **Knowledge → `Resources/Zettelkasten/`**
**Rationale**: Zettelkasten notes are reference material (Resources). This keeps the PARA structure clean and logically sound. Subfolders for `Fleeting/Literature/Permanent` notes can manage the note lifecycle.

#### 3. **People → `Resources/People/`**
**Rationale**: Notes about people are reference material about relationships, fitting naturally into Resources.

#### 4. **A Dedicated `GTD-Tasks/` Directory**
**Rationale**: To properly implement GTD, there must be a central place for all tasks, organized by their state (Next Action, Waiting For, etc.). This avoids scattering tasks across various project and area folders and allows for the creation of unified, context-based task lists (e.g., a single view of all `@Computer` tasks).

---

## ✅ Final Recommendations (Implemented)

1. **Adopted the proposed "PARA-Core + GTD Extensions" structure.**
2. **Use metadata extensively**: Content types, contexts, and status are all defined in YAML frontmatter, not by folder location.
3. **Build dynamic views**: The `GTD-Tasks` system allows for the generation of dynamic, context-based views (e.g., "Show me all low-energy tasks I can do in 15 minutes").
4. **AI-first approach**: The consistent structure and metadata make it easier for AI agents to file, query, and maintain the system.

This architectural review was pivotal in establishing the robust and logical structure that the LifeOS project currently uses.
