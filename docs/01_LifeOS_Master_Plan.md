---
title: "LifeOS Master Plan"
type: "Documentation"
status: "Active"
created: "2025-12-11"
last_updated: "2025-12-11"
tags: ["documentation", "master-plan", "architecture", "gtd", "para"]
---

# LifeOS Master Plan

**Goal**: Create a unified, AI-enhanced Personal Knowledge Management (PKM) and Life Coaching system ("LifeOS") that serves as a second brain, therapist, and executive assistant.

**Core Philosophy**: "Compassionate Firmness" – combining rigorous system management (GTD, PARA) with deep emotional and spiritual support. The system is supportive but steady, willing to tell the hard truth without sugar-coating difficult realities, while remaining empathetic to the user's context.

## Core Architectural Principles

### Principle 1: Separation of Concerns
**PARA organizes KNOWLEDGE. GTD organizes ACTIONS.**

- **PARA** (Projects, Areas, Resources, Archives) answers: *"What domain of life does this knowledge belong to?"*
- **GTD-Tasks** (Inbox → Next-Actions → Waiting-For, etc.) answers: *"What is the workflow state of this action?"*
- These are **orthogonal dimensions** - tasks link to Projects/Areas via metadata, not containment

### Principle 2: Single Source of Truth
- Tasks live in `GTD-Tasks/` directory structure
- Projects/Areas are **knowledge containers** that organize context, milestones, and goals
- Metadata creates bidirectional links (tasks point to projects, projects point to tasks)
- No duplication, no synchronization issues

### Principle 3: Metadata Over Hierarchy
- Content type, status, context, energy, priority → YAML frontmatter
- Enables powerful queries without rigid folder structures
- Future-proof: add new metadata without restructuring

### Principle 4: Processing States Are First-Class
Beyond binary "actionable/not actionable":
- `To-Read` for content consumption
- `To-Think-About` for contemplative work
- `Needs-Processing` for note elaboration/connection

---

## Directory Structure

```
LifeOS/
├── GTD-Tasks/                  # 🎯 ALL actionable items and processing states
│   ├── 0-Inbox/               # Unsorted capture (everything starts here)
│   ├── 1-Next-Actions/        # Ready to execute (the canonical action list)
│   ├── 2-Waiting-For/         # Delegated or blocked on others
│   ├── 3-Someday-Maybe/       # Not committed yet, future possibilities
│   ├── 4-To-Read/             # Books, articles, videos, podcasts to consume
│   ├── 5-To-Think-About/      # Needs contemplation before becoming action
│   └── 6-Needs-Processing/    # Raw notes needing elaboration/connection
│
├── Projects/                   # 📋 PARA: Outcomes with deadlines
│   ├── Active/
│   │   ├── Self-Improvement/
│   │   ├── Family-Projects/
│   │   ├── Home-Projects/
│   │   └── LifeOS-Development/
│   ├── Someday/               # Not active but defined
│   └── Completed/             # Archived completed projects
│
├── Areas/                      # 🏠 PARA: Ongoing responsibilities
│   ├── Family/
│   ├── Faith/
│   ├── Health/
│   ├── House/
│   ├── Homeschool/
│   └── Personal-Reflection/   # Daily/Weekly/Monthly journaling
│
├── Resources/                  # 📚 PARA: Reference material
│   ├── Zettelkasten/          # PKM: Atomic evergreen notes
│   │   ├── Fleeting/          # Quick captures, need processing
│   │   ├── Literature/        # Notes from sources
│   │   └── Permanent/         # Refined, connected concepts
│   ├── MOCs/                  # Maps of Content (index notes)
│   ├── People/                # Relationship notes (CRM-like)
│   ├── Books/                 # Book summaries and notes
│   ├── Articles/              # Article highlights
│   ├── Courses/               # Course materials
│   └── Templates/             # Reusable note templates
│
├── Archives/                   # 🗄️ PARA: Inactive content
│   └── Legacy-Plans/          # Old planning documents
│
└── System/                     # ⚙️ Meta: System documentation
    ├── Prompts/               # AI system prompts
    ├── Templates/             # Task, note, project templates
    ├── Queries/               # Saved query definitions
    └── Context-Definitions/   # GTD context documentation
```

---

## Key Workflows

### A. Capture → Process Workflow (GTD Core)

```
1. CAPTURE
   ↓
   Everything goes to GTD-Tasks/0-Inbox/
   (Voice notes, emails, thoughts, tasks, ideas)

2. PROCESS (Daily or as-needed)
   ↓
   For each item in Inbox, ask:
   
   "What is this?"
   ├─ Actionable?
   │  ├─ Yes → "Can I do it in <2 minutes?"
   │  │  ├─ Yes → Do it now ✓
   │  │  └─ No → Continue...
   │  │     "What's the very next physical action?"
   │  │     ├─ I must do it → Move to 1-Next-Actions/
   │  │     ├─ Someone else does it → Move to 2-Waiting-For/
   │  │     └─ Not ready to commit → Move to 3-Someday-Maybe/
   │  │
   │  └─ No → "What type of non-action is it?"
   │     ├─ Content to consume → Move to 4-To-Read/
   │     ├─ Needs thinking → Move to 5-To-Think-About/
   │     ├─ Raw notes → Move to 6-Needs-Processing/
   │     ├─ Reference → Move to Resources/
   │     └─ Trash → Delete
   │
   └─ Add metadata while processing:
      - Link to project/area if applicable
      - Tag with context (@Computer, @Home, etc.)
      - Estimate time/energy
      - Set priority

3. ORGANIZE
   Task now lives in appropriate GTD-Tasks/ folder with metadata

4. EXECUTE
   Work from 1-Next-Actions/ filtered by:
   - Context (What can I do here?)
   - Time available
   - Energy level
   - Priority
```

### Relationship Coaching (The "Heart")

**Source**: `system-blueprint.md` - Pursue-Withdraw Cycle Breaking

**Implementation**:
- Daily task: `GTD-Tasks/1-Next-Actions/evening-presence-with-wife.md`
  - Context: `@Home`
  - Time: `15min`
  - Energy: `Low` (can do when tired)
  - Linked: `[[Areas/Family/Marriage]]`

**First-Aid Kit Phrases** stored in: `Resources/Templates/first-aid-kit-phrases.md`

**Tracking**: Weekly journaling in `Areas/Personal-Reflection/Weekly/2025-W47.md`

### The ONE THING (Daily Priority)

**Morning Ritual** (7:00 AM):
1. AI prompts: *"What's your ONE THING for today?"*
2. User identifies the single most important task
3. Create or update task in `GTD-Tasks/1-Next-Actions/` with `priority: Critical`
4. Block time on calendar
5. Protect from distractions

**Evening Reflection** (6:00 PM):
1. AI prompts: *"Did you complete your ONE THING?"*
2. Journal entry in `Areas/Personal-Reflection/Daily/YYYY-MM-DD.md`
3. Celebrate or analyze obstacles

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

## Query Examples

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
