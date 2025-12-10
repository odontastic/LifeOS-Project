# LifeOS: A Personal System for Growth and Self-Mastery

LifeOS is a comprehensive, AI-enhanced system designed to serve as a second brain, life coach, and personal assistant. It's a private and personalized tool for navigating life with intention, with a special focus on integrating productivity with deep emotional and spiritual growth.

## Core Philosophy: Compassionate Firmness

The guiding principle of LifeOS is "Compassionate Firmness." This means combining the rigorous, systematic approach of methodologies like GTD (Getting Things Done) and PARA (Projects, Areas, Resources, Archives) with the empathetic, insightful support of an AI life coach. The system is designed to be supportive yet steady, offering accountability and honest reflection to help you stay aligned with your deepest values.
## Core Architectural Principles

## System Architecture

LifeOS is built on a dual architecture: a conceptual framework for organizing your life and a technical stack for powering the AI and user interface.

### Conceptual Architecture

The core of LifeOS is a unique integration of two powerful organizational methodologies:

-   **PARA (Projects, Areas, Resources, Archives):** This system, developed by Tiago Forte, is used to organize your knowledge and information. It provides a clear and intuitive structure for everything you want to keep track of, from your personal projects to your long-term goals.
-   **GTD (Getting Things Done):** This renowned productivity method, created by David Allen, is used to manage your actions and tasks. It provides a clear and effective workflow for capturing, clarifying, and organizing everything you need to do.

By keeping these two systems separate but interconnected, LifeOS ensures a clear distinction between your knowledge and your actions, creating a powerful and flexible framework for managing your life.

### Technical Architecture
## Directory Structure

LifeOS is comprised of three main components:

1.  **`LifeOS/`:** This is the heart of your personal knowledge management system. It's a collection of markdown files organized according to the PARA method, where you'll store your notes, journal entries, project plans, and more.
2.  **`lifeos-rag-api/`:** This is the backend of the system, powered by a FastAPI application. It uses a RAG (Retrieval-Augmented Generation) architecture to provide a powerful, context-aware AI that can interact with your personal knowledge base. The backend is fully containerized with Docker and includes a Neo4j graph database, a Qdrant vector store, and the Open WebUI for a user-friendly interface.
3.  **`LifeOS-Web/`:** This is the frontend of the application, built with Next.js and React. It provides a clean and intuitive interface for interacting with the LifeOS system.

## Key Features

-   **AI-Powered Life Coaching:** Engage in insightful conversations with an AI that's aware of your personal context, helping you identify blind spots, understand your shortcomings, and develop strategies for growth.
-   **Integrated Knowledge Management:** Seamlessly combine the PARA method for organizing knowledge with the GTD system for managing tasks, creating a holistic view of your life.
-   **Personalized Workflows:** From daily check-ins and weekly reviews to specialized coaching for emotional intelligence, LifeOS is designed to support your unique goals and routines.
-   **RAG Architecture:** The powerful RAG-based backend allows the AI to retrieve relevant information from your personal notes, ensuring that its guidance is always grounded in your own experiences and reflections.
-   **Daily Journal:** A dedicated view to browse and review daily journal entries, which are composed of chat sessions. Includes the ability to navigate by date and export entries in various formats.
-   **Weekly Risk Audit:** An interactive grid to conduct a weekly audit across key life categories, with a scoring system and a placeholder for future AI analysis.

## Future Ideas

This project is a constantly evolving system. Here are some of the ideas for future development:

-   **Advanced AI Integration:** Enhance the AI's capabilities with smart suggestions, pattern recognition, and proactive habit tracking to provide even more personalized support.
-   **Voice-to-Text Capture:** Implement a seamless way to capture thoughts, ideas, and tasks on the go using voice notes that are automatically transcribed and integrated into the system.
-   **Automated Workflows:** Develop AI-driven assistance for daily and weekly reviews, helping to streamline the process and provide deeper insights.
-   **Deeper Relationship Coaching:** Expand the relationship coaching features with proactive suggestions, communication analysis, and personalized exercises for improving emotional intelligence.

## Getting Started

To get LifeOS up and running, you'll need to set up the backend and frontend services separately.
### Relationship Coaching (The "Heart")

### Backend Setup (`lifeos-rag-api/`)

1.  **Navigate to the `lifeos-rag-api` directory:**
    ```bash
    cd lifeos-rag-api
    ```
2.  **Create a `.env` file:**
    Copy the `.env.example` file to a new file named `.env` and fill in the required environment variables.
3.  **Create a `notes` directory:**
    Create a new directory named `notes` in the `lifeos-rag-api` directory. This is where you will place all of your personal documents that you want the AI to be able to access.
4.  **Run the Docker containers:**
    ```bash
    docker-compose up -d
    ```
    This will start all the backend services in detached mode.

### Frontend Setup (`LifeOS-Web/`)

1.  **Navigate to the `LifeOS-Web` directory:**
    ```bash
    cd LifeOS-Web
    ```
2.  **Install the dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    This will start the Next.js development server, and you can access the application at `http://localhost:3000`.

## Directory Structure
### The ONE THING (Daily Priority)

Here's a high-level overview of the project's directory structure:

-   **`LifeOS/`**: Contains all your personal notes and documents, organized using the PARA method.
-   **`lifeos-rag-api/`**: The backend of the application, including the FastAPI service, Docker configuration, and related files.
-   **`LifeOS-Web/`**: The frontend of the application, built with Next.js.

This README provides a starting point for understanding and using LifeOS. For a more in-depth guide to the system's philosophy, structure, and workflows, please refer to the `MASTER_PLAN.md` in the `LifeOS/` directory.
### Weekly Review (Sunday Evening)

**Checklist** stored in: `System/Templates/weekly-review-checklist.md`

```markdown
# Weekly Review Checklist

## 1. Get Clear (30 min)
- [ ] Process all items in GTD-Tasks/0-Inbox/
- [ ] Review GTD-Tasks/2-Waiting-For/ (chase if needed)
- [ ] Review GTD-Tasks/6-Needs-Processing/ (process 2-3 notes)

## 2. Get Current (20 min)
- [ ] Review all Projects/Active/ (update status, add tasks)
- [ ] Review all Areas/ (anything needing attention?)
- [ ] Check calendar for next 2 weeks

## 3. Get Creative (10 min)
- [ ] Review GTD-Tasks/3-Someday-Maybe/ (anything ready to activate?)
- [ ] Review GTD-Tasks/5-To-Think-About/ (schedule thinking time?)
- [ ] Capture new ideas that emerged this week

## 4. Relationship Check (10 min)
- [ ] How was presence with wife this week?
- [ ] Any bids for connection missed?
- [ ] Plan one intentional connection for next week

## 5. Set ONE THING (5 min)
- [ ] What's the ONE THING for next week?
```

---

## Metadata Standards

### Task Template

```yaml
---
title: ""                    # Descriptive action
status: ""                   # Inbox | Next-Action | Waiting-For | Someday-Maybe | To-Read | To-Think-About | Needs-Processing
project: []                  # Link to Projects/Active/...
area: []                     # Link to Areas/...
context: []                  # [@Computer, @Home, @Calls, @Errands, @Shopping]
energy: ""                   # High | Medium | Low
time: ""                     # 5min | 15min | 30min | 1hr | 2hr+
priority: ""                 # Critical | High | Medium | Low
created: YYYY-MM-DD
due: ""                      # YYYY-MM-DD (optional)
completed: ""                # YYYY-MM-DD (when done)
---

# Title

## Action
[Specific next physical action]

## Why It Matters
[Connection to values/goals]

## Next Steps
1. 
2. 

## Related
- 
```

### Standard Contexts

Defined in `System/Context-Definitions/`:

- **@Computer** - Requires computer access (research, writing, coding)
- **@Home** - Can do anywhere at home (cleaning, organizing, thinking)
- **@Calls** - Phone calls to make
- **@Errands** - Outside the house (shopping, appointments)
- **@Shopping** - Specific purchases needed
- **@Cleaning** - Maintenance and cleaning tasks
- **@Organization** - Sorting, filing, system setup

---

## 7. Query Examples

### By Context
**Filename**: `System/Queries/computer-actions.md`

```markdown
# @Computer Actions

Show all tasks where:
- status = "Next-Action"
- context contains "@Computer"

Sort by: priority (Critical first), then time (shortest first)
```

### By Project
**Filename**: `System/Queries/college-prep-tasks.md`

```markdown
# All College Prep Tasks

Show all tasks where:
- project contains "College-Prep"

Group by: status
```

### Quick Wins
**Filename**: `System/Queries/quick-wins.md`

```markdown
# Quick Wins (Low Energy, Short Time)

Show all tasks where:
- status = "Next-Action"
- energy = "Low"
- time <= "15min"

Use when: Tired but want to make progress
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [x] ~~Create MASTER_PLAN.md~~
- [x] ~~Architectural review~~
- [x] Create GTD-Tasks/ directory structure
- [x] Create Projects/, Areas/, Resources/, Archives/ structure
- [x] Move existing content to new locations:
  - `03-Contexts/` → `System/Context-Definitions/`
  - Old planning docs → `Archives/Legacy-Plans/`

### Phase 2: Templates & Standards (Week 2)
- [x] Create task template (`System/Templates/task-template.md`)
- [x] Create project template
- [x] Create area template
- [x] Create daily journal template
- [x] Document all metadata standards
- [ ] Create context definition files

### Phase 3: Content Migration (Week 3)
- [ ] Identify existing tasks scattered in current structure
- [ ] Migrate to appropriate GTD-Tasks/ folders
- [ ] Add metadata to all tasks
- [ ] Create initial Projects/Active/ entries
- [ ] Set up Areas/ structure

### Phase 4: Workflow Setup (Week 4)
- [ ] Create weekly review checklist
- [ ] Set up daily prompts (ONE THING morning/evening)
- [ ] Create query files in System/Queries/
- [ ] Test capture → process workflow
- [ ] Run first complete weekly review

### Phase 5: AI Integration (Week 5+)
- [ ] Create MASTER_SYSTEM_PROMPT.md (merge `start.md` + `system-blueprint.md`)
- [ ] Set up AI capture assistance (voice → Inbox)
- [ ] Build query automation (generate @Computer view on demand)
- [ ] Implement smart suggestions (context-aware task recommendations)
- [ ] Add relationship coaching prompts

---

## AI Agent Configuration

### Core Capabilities

**1. Intelligent Capture**
- Accept natural language input
- Auto-file to GTD-Tasks/0-Inbox/
- Suggest metadata based on context
- Extract action items from rambling thoughts

**2. Smart Processing**
- Guide user through Inbox processing
- Suggest appropriate GTD-Tasks/ category
- Recommend context, energy, time estimates
- Identify related projects/areas

**3. Dynamic Queries**
- Generate context views on demand ("Show me @Computer tasks")
- Create custom filters ("Low energy tasks under 15min")
- Project dashboards ("All College Prep tasks by status")

**4. Coaching & Accountability**
- Daily ONE THING check-in
- Weekly review facilitation
- Relationship pattern recognition
- Habit tracking and encouragement

**5. Knowledge Management**
- Connect tasks to relevant Resources/
- Suggest Zettelkasten note creation
- Identify orphaned notes (no connections)
- Recommend MOC updates

---

## Success Metrics

### System Health (Weekly)
- **Inbox Zero**: GTD-Tasks/0-Inbox/ processed to empty
- **Next Actions Count**: 10-30 (not empty, not overwhelming)
- **Project Health**: All active projects have ≥1 next action
- **Waiting For**: All items have follow-up dates

### Relationship Health (Weekly)
- **Presence Hours**: Device-free time with wife
- **First-Aid Kit Usage**: Times phrases prevented withdrawal
- **Bids Responded**: % of connection bids turned toward

### Personal Growth (Monthly)
- **ONE THING Completion**: % of days completed
- **Weekly Reviews**: Completed on time
- **Note Processing**: Fleeting → Permanent conversion rate
- **Habit Adherence**: Target habit streak lengths

---

## What Makes This System Different

### 1. True Separation of Concerns
Most systems mix "where it goes" with "what to do with it."  
LifeOS: **PARA organizes knowledge. GTD-Tasks organize actions.**

### 2. Rich Processing States
Beyond "actionable/not actionable":
- Content to consume (`To-Read`)
- Ideas needing contemplation (`To-Think-About`)
- Notes needing elaboration (`Needs-Processing`)

### 3. Metadata-Driven Flexibility
Add new frameworks without restructuring folders.  
Want to add "Energy Management" or "Eisenhower Matrix"? → Add metadata properties.

### 4. AI-Native Design
Built for AI assistance from day one:
- Consistent metadata for query/analysis
- Natural language capture
- Dynamic view generation
- Pattern recognition for coaching

### 5. Spiritually Integrated
Not just productivity—character formation:
- Values embedded in project definitions
- Virtue tracking in journaling
- Relationship primacy in daily prompts
- Ignatian examen in evening reflections

---

## Next Steps

**Immediate** (Today):
1. Review and approve this Master Plan
2. Create GTD-Tasks/ directory structure
3. Move first 5 items to Inbox for practice

**This Week**:
1. Complete all Phase 1 tasks
2. Create essential templates
3. Run first Inbox processing session

**This Month**:
1. Complete Phases 1-4
2. Migrate existing content
3. Run first full weekly review
4. Begin AI integration

---

**Status**: Ready for implementation. Awaiting user approval to proceed with Phase 1.
