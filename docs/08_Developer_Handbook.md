Developer Handbook 
created Chat GPT (Perplexity assist) 2025-12-11
---

# 🛠️ **Developer Handbook for the PARA + GTD + Zettelkasten System**

A unified schema, workflow, and execution guide for building the “LifeOS” personal knowledge and productivity system, integrating **PARA**, **GTD**, **Zettelkasten**, and **Therapeutic Journaling**.

---

# 1. 🎯 **Purpose**

This document defines **all data models, operations, workflows, bridging logic, and expectations** required for an AI agent to:

* Parse user input
* Place it in the correct system layer (PARA/GTD/Zettelkasten/Therapeutic)
* Create/update the unified graph-based knowledge system
* Propose tasks, projects, zettels, reflections, and links
* Maintain long-term order and consistency

This *is* the “source of truth” for the AI developer.

---

# 2. 🧩 **Core Concepts**

### PARA

* **Projects:** multi-step outcomes with deadlines
* **Areas:** ongoing responsibilities
* **Resources:** reference materials, evergreen
* **Archives:** inactive items

### GTD

* **Tasks:** concrete, physical next actions
* **Contexts:** where/how tasks get done
* **Horizons:** purpose → vision → goals → areas → projects → tasks

### Zettelkasten

* **Zettels:** atomic notes
* **Links:** semantic relationships (bidirectional)
* **Reflections:** higher-level insights

### Therapeutic Graph (Coaching Module)

* **Journal Objects:** Entities representing emotional states
* **Nodes:** Emotion, Belief, Trigger, CopingMechanism, Episode
* **Flows:** Interactive coaching sessions (CBT, various frameworks)
* **GTD Dashboard:** Visual overview of tasks, contexts, and horizons for GTD workflow
* **Prism Clarity Studio:** AI‑powered decision‑making and training engine built on the knowledge base and a library of mental models

---

# 3. 📦 **Unified Data Models (Implementation-Ready Schemas)**

These should be treated as *JSON-like TypeScript interfaces*.

---

## 3.1 **Zettel**

```
{
  id: string,
  type: "zettel",
  title: string,
  body: string,
  created_at: timestamp,
  updated_at: timestamp,
  links: string[],            // zettel IDs or entity IDs
  tags: string[],
  horizon: "none" | "vision" | "goals" | "principles",
  contexts: string[]          // optional, GTD integration
}
```

---

## 3.2 **Project**

```
{
  id: string,
  type: "project",
  title: string,
  desired_outcome: string,
  why_it_matters: string,
  success_criteria: string[],
  next_actions: string[],        // task IDs
  status: "active" | "paused" | "done",
  area: string | null,           // area ID
  related_zettels: string[],
  horizon: "projects"
}
```

---

## 3.3 **Area**

```
{
  id: string,
  type: "area",
  title: string,
  description: string,
  health_metric: string,        // e.g. “Stable / Needs Attention”
  active_projects: string[],    // project IDs
  active_tasks: string[],
  related_resources: string[],
  related_zettels: string[],
  horizon: "areas"
}
```

---

## 3.4 **Resource**

```
{
  id: string,
  type: "resource",
  title: string,
  format: "link" | "file" | "zettel" | "mixed",
  body: string,
  tags: string[],
  related_zettels: string[],
  horizon: "resources"
}
```

---

## 3.5 **Task**

```
{
  id: string,
  type: "task",
  title: string,
  description: string,
  status: "next" | "waiting" | "scheduled" | "done",
  due: timestamp | null,
  context: string,
  project: string | null,
  area: string | null,
  related_zettels: string[],
  horizon: "actions"
}
```

---

## 3.6 **Goal**

```
{
  id: string,
  type: "goal",
  title: string,
  description: string,
  deadline: timestamp | null,
  success_criteria: string[],
  related_projects: string[],
  related_zettels: string[],
  horizon: "goals"
}
```

---

## 3.7 **Reflection**

```
{
  id: string,
  type: "reflection",
  body: string,
  insights: string[],            // textual insights
  generated_zettels: string[],   // IDs created during review
  related_areas: string[],
  related_projects: string[],
  created_at: timestamp
}
```

---

## 3.8 **Therapeutic Nodes (Coaching Module)**

These entities capture the emotional and psychological context of the user.

### **JournalEntry**
```
{
  id: string,
  type: "journal_entry",
  body: string,
  mood_rating: number, // 1-10
  emotions: string[],  // IDs of Emotion nodes
  beliefs: string[],   // IDs of Belief nodes
  created_at: timestamp
}
```

### **Emotion**
```
{
  id: string,
  type: "emotion",
  name: string,        // e.g. "Anxiety", "Joy"
  intensity: number,
  valence: "positive" | "negative" | "neutral",
  related_entries: string[]
}
```

### **Belief**
```
{
  id: string,
  type: "belief",
  statement: string,   // e.g. "I must be perfect"
  status: "limiting" | "empowering",
  related_entries: string[]
}
```

### **Trigger**
```
{
  id: string,
  type: "trigger",
  description: string,
  related_emotions: string[]
}
```

---

# 4. 🔗 **Bridging Rules (Critical Execution Logic)**

These rules *must* be executed automatically by the AI agent whenever interpreting user content.

---

## 4.1 **Zettel → Project Conversion Rule**

When a zettel expresses:

* a **desired outcome**,
* that requires **multiple steps**,
* and describes **effort over time**,

THEN the AI must propose a Project:

```
{
  desired_outcome,
  why_it_matters,
  success_criteria: [],
  next_actions: []
}
```

And link:

* zettel → project
* project → zettel

---

## 4.2 **Weekly Review Loop**

For each **Area**:

1. Retrieve:

   * active projects
   * active tasks
   * recent reflections

2. Ask:

   * “Any new changes in this Area?”
   * “Any new problems, insights, or emerging outcomes?”

3. Generate new zettels for insights.

4. Propose:

   * new projects
   * task clean-ups
   * resource updates

5. Create a **Reflection** capturing:

   * new insights
   * created zettels
   * project status adjustments

---

## 4.3 **Therapeutic Bridging (Journal → Insight)**

When a **JournalEntry** reveals a recurring pattern or significant realization:

1. **Extract Beliefs**: Identify core beliefs underlying the entry.
2. **Create Zettel**: If a belief is identified as a "limiting belief" or "key insight", create a Zettel to formally track it in the Zettelkasten.
3. **Propose Action**: If a **CopingMechanism** is identified, propose it as a potential **Task** or **Resource** link.

**Example Logic:**
> IF `JournalEntry` mentions "I feel overwhelmed by Project X" 
> AND `Project X` exists 
> THEN Link `JournalEntry` -> `Project X`
> AND Suggest `Task`: "Break down Project X into smaller steps"

---

# 5. 🧠 **Session Expectations for the AI Agent**

For **every** user query:

### 1️⃣ Identify Layers Involved

Label which system layers are relevant:

* PARA
* GTD
* Zettelkasten
* Therapeutic
* GTD Dashboard
* Prism Clarity Studio

### 2️⃣ Suggest Data Structure or State Changes

Specify exactly which entities would be created/updated.

### 3️⃣ Generate Prompts or Pseudo-Code

Provide output in a format the coding agent can execute, such as:

* JSON patches
* database operations
* create/update/delete instructions
* schema validation warnings

This turns ChatGPT into a structured *design + architecture companion*.

---

# 6. 🔧 **Coding Agent Instructions (Junior-Level Ready)**

Give these directly to your AI developer:

---

## “AI Coder Instructions — Core Rules”

1. Always validate input against the schemas.

2. Auto-detect whether user content is a:

   * task
   * project
   * area update
   * zettel
   * goal
   * reflection
   * GTD dashboard element
   * Prism Clarity Studio request

3. Follow the bridging rules without exception.

4. Keep all links **bidirectional**.

5. Use timestamps automatically.

6. Never delete data — only archive.

7. Produce consistent IDs (UUIDv4).

8. Ensure every Project has at least one Next Action.

9. Every Zettel must link to at least one other entity.

10. Weekly Review workflow must be able to run as a function.

---

# 7. ⚙️ **System Operations API (Pseudo-API for the AI Coder)**

Expose these as callable actions:

### Zettel operations

* `create_zettel(data)`
* `update_zettel(id, patch)`
* `link_zettels(id1, id2)`

### Project operations

* `create_project(data)`
* `add_task_to_project(project_id, task_id)`
* `update_project_status(project_id, status)`

### Area operations

* `create_area(data)`
* `assign_project_to_area(area_id, project_id)`

### Task operations

* `create_task(data)`
* `update_task_status(id, status)`

### Reflection operations

* `create_reflection(data)`

### Weekly Review

* `run_weekly_review()`

---

# 8. 📋 Checklist for the AI Coder (Copy-Paste Ready)

```
[ ] Validate all inputs using schema
[ ] Detect type: zettel/project/task/etc.
[ ] Apply bridging rules
[ ] Maintain bidirectional links
[ ] Update timestamps
[ ] Ensure each project has next actions
[ ] Archive only, never delete
[ ] Generate pseudo-code for all operations
[ ] Return both: state changes + reasoning
```

---

# 9. 📚 “Done-For-You” Prompts the Coder Can Run

## Create a new entity:

```
CreateEntity({
  type: "zettel",
  title: "...",
  body: "..."
})
```

## Generate weekly review actions:

```
RunWeeklyReview({ area_id: "..." })
```

## Convert zettel → project:

```
ConvertZettelToProject({ zettel_id: "..." })
```

---

# 10. 🧭 Final Note — How the AI Should Work

The coder should think of the entire system as:

* **A graph** (entities + links)
* **A workflow engine** (bridging rules + weekly reviews)
* **A parser** (interprets user text)
* **A consistent database** (never messy)

The goal is clarity, consistency, and long-term maintainability.

---
