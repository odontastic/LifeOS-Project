---
title: "LifeOS Map of Content"
type: "MOC"
status: "Active"
created: "2025-12-11"
last_updated: "2025-12-11"
tags: ["moc", "entry-point", "documentation"]
---

# 🗺️ LifeOS Map of Content (MOC)

This document is the central hub for navigating the LifeOS project. It provides a high-level overview of the entire system, from core philosophy and architecture to the practical implementation of its components.

---

## 🏛️ **Core Project Documentation (`/docs`)**

This directory contains the foundational documents that define the LifeOS project.

-   **[01_LifeOS_Master_Plan.md](./docs/01_LifeOS_Master_Plan.md)**: The primary design document. It details the core philosophy (PARA + GTD), system architecture, key workflows, and the implementation roadmap. **This is the best place to start for a deep understanding of the system.**
-   **[02_Schema_and_Standards.md](./docs/02_Schema_and_Standards.md)**: The single source of truth for all data and file standards, including YAML frontmatter, file naming conventions, templates, and linking rules.
-   **[03_Architecture_Decisions.md](./docs/03_Architecture_Decisions.md)**: A record of the architectural review and the key decisions that shaped the current system structure. It explains the "why" behind the design.
-   **[04_Agent_Guide.md](./docs/04_Agent_Guide.md)**: A guide for AI agents working on the project, covering setup, build/test commands, and contribution guidelines.
-   **[05_Master_System_Prompt.md](./docs/05_Master_System_Prompt.md)**: The master system prompt that defines the core identity, function, and interaction style of the LifeOS AI assistant.
-   **[06_Personal_Growth_System.md](./docs/06_Personal_Growth_System.md)**: A detailed look at the framework for managing personal growth, habits, and self-improvement within LifeOS.

---

## 🚀 **The LifeOS System (`/knowledge_base`)**

This is the live implementation of the user's Personal Knowledge Management and Life OS.

### **Life Knowledge (BASB)**

The Tiago Forte PARA Method is an actionable system for organizing all types of digital information of your knowledge, responsibilities, and goals into four categories: Projects, Areas, Resources, and Archives. Its purpose is to reduce mental load, decision fatigue, and improve productivity by making information easily findable and actionable.

-   **[Projects/](./knowledge_base/Projects/)**: Goal-oriented endeavors with clear outcomes and deadlines.
-   **[Areas/](./knowledge_base/Areas/)**: Ongoing responsibilities and domains of life (e.g., Health, Family, Finance).
-   **[Resources/](./knowledge_base/Resources/)**: The knowledge bank, containing reference materials, notes, and assets.
-   **[Archives/](./knowledge_base/Archives/)**: A repository for inactive or completed items from the other three pillars.

### **The Action Engine (GTD)**

-   **[GTD-Tasks/](./knowledge_base/GTD-Tasks/)**: The central nervous system for all tasks and actions, organized by their workflow state.
    -   `0-Inbox/`: The universal capture location. Everything starts here.
    -   `1-Next-Actions/`: The list of tasks ready to be worked on now.
    -   `2-Waiting-For/`: Delegated tasks or items awaiting a response.
    -   `3-Someday-Maybe/`: Ideas and projects to consider in the future.
    -   `4-To-Read/`: The content consumption queue.
    -   `5-To-Think-About/`: Items that require deeper contemplation.
    -   `6-Needs-Processing/`: Raw notes and ideas that need to be refined.

---

## 💻 **Application Code (`/apps`)**

This section contains the source code for the web application that brings LifeOS to life.

-   **[frontend/LifeOS-Web/](./apps/frontend/LifeOS-Web/)**: The Next.js and React frontend that provides the user interface for the system.
-   **[backend/lifeos-rag-api/](./apps/backend/lifeos-rag-api/)**: The FastAPI backend that powers the Retrieval-Augmented Generation (RAG) and other AI capabilities.
