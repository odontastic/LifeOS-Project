---
title: "LifeOS Architecture Decisions"
type: "Documentation"
status: "Archived"
created: "2025-11-20"
last_updated: "2025-12-12"
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
/ (Project Root)
├── knowledge_base/
│   ├── GTD-Tasks/                  # 🎯 GTD: ALL actionable items
│   │   ├── 0-Inbox/
│   │   └── ...
│   │
│   ├── Projects/                   # 📋 PARA: Outcomes with deadlines
│   │   ├── Active/
│   │   └── ...
│   │
│   ├── Areas/                      # 🏠 PARA: Ongoing responsibilities
│   │   └── Personal-Reflection/   # ✅ Journal lives here
│   │
│   ├── Resources/                  # 📚 PARA: Reference material
│   │   ├── Zettelkasten/         # ✅ PKM lives here
│   │   └── ...
│   │
│   └── Archives/                   # 🗄️ PARA: Inactive content
│
└── System/                     # ⚙️ Meta: System documentation
    ├── Prompts/
    ├── Templates/
    └── ...
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

## ✅ Final Recommendations (Implemented)

1.  **Adopted the proposed "PARA-Core + GTD Extensions" structure.**
2.  **Use metadata extensively**: Content types, contexts, and status are all defined in YAML frontmatter, not by folder location.
3.  **Build dynamic views**: The `GTD-Tasks` system allows for the generation of dynamic, context-based views (e.g., "Show me all low-energy tasks I can do in 15 minutes").
4.  **AI-first approach**: The consistent structure and metadata make it easier for AI agents to file, query, and maintain the system.

---

# Emotion Engine & Inner Palette Architecture (New Module)

**Date**: 2025-12-13
**Reviewer**: AI Agent
**Scope**: Integrate a robust emotional intelligence framework into LifeOS.

## 🎯 Executive Summary (New Module)

**Goal**: To seamlessly integrate advanced emotional intelligence capabilities into LifeOS, enabling users to track, understand, and cultivate their emotional states effectively. This involves two primary components: the **Inner Palette** (User Interface for emotional input) and the **Emotion Engine** (AI-driven backend for processing, analysis, and coaching).

**Rationale**: Emotional intelligence is a critical aspect of personal growth, self-mastery, and successful relationships, aligning perfectly with LifeOS's core philosophy of "Compassionate Firmness" and holistic well-being.

## 📊 Architectural Decisions

### 1. **Inner Palette (UI/Data Input Layer)**
*   **Role**: Serves as the primary, user-friendly interface for capturing emotional data.
*   **Multi-Modal Input**: Supports various input types (categorical, dimensional, somatic, narrative) to accommodate diverse user preferences and cognitive styles. This allows users to engage with emotions in the most comfortable and accurate way for them.
*   **Ubiquitous Access**: Designed to be quickly accessible from any page or card within the LifeOS UI, ensuring low friction for emotional logging.
*   **Metadata Integration**: Emotional entries will be tagged with relevant LifeOS metadata (e.g., linked to Projects, Areas, specific events from the calendar, or people), enriching contextual understanding.
*   **Privacy & Consent**: Built with explicit privacy controls, especially for features allowing the logging of others' emotional states.

### 2. **Emotion Engine (AI/Processing Layer)**
*   **Role**: The intelligent backend that processes, analyzes, and interprets emotional data from the Inner Palette, providing actionable insights and coaching.
*   **Core Principles**: Integrates neuropsychology (e.g., limbic system, PFC limits, dopamine loops, neuroplasticity), psychological theories, and evidence-based therapeutic techniques (CBT, DBT).
*   **Data Flow**: Receives emotional data from the Inner Palette, combines it with other contextual data from the LifeOS (journal entries, calendar, task status, etc.), and feeds it into AI models for analysis.
*   **Key Functions**:
    *   **Emotional Pattern Recognition**: Identifies recurring emotional triggers, responses, and long-term trends.
    *   **Personalized Coaching**: Generates context-aware prompts, "emotion recipes," and guides users through cognitive reappraisal, perspective-taking, and "tiny habits."
    *   **Emotional Blind Spot Detection**: Suggests new emotional vocabulary or challenges under-reported emotions.
    *   **Relationship & Empathy Support**: Utilizes data (potentially from logging others' emotions) to foster perspective-taking and improve relational dynamics.
    *   **"Neuro-Coaching"**: Interventions are designed to align with biological and neurological principles for sustainable change.
*   **Integration with Crisis Mode**: Provides emotional context upon activation of Crisis Mode and facilitates post-crisis reflection, helping identify triggers and refine coping mechanisms.
*   **Outputs**: Delivers insights, prompts, and recommendations back to the user via the UI, aiming to cultivate emotional awareness, regulation, and overall well-being.

## 🤝 Adherence to Existing Principles

*   **Metadata Over Hierarchy**: Emotional data will extensively use metadata (intensity, type, related context, linked entities) for flexible querying and AI analysis, rather than rigid folder structures.
*   **AI-Native Design**: The Emotion Engine is built from the ground up to leverage AI for pattern recognition, coaching, and personalized interventions.
*   **Spiritually Integrated**: The framework supports deeper self-reflection and personal growth, aligning with the "Compassionate Firmness" philosophy.

This architectural addition extends LifeOS's capabilities significantly into the domain of emotional intelligence, making it a more holistic and powerful tool for personal development.

