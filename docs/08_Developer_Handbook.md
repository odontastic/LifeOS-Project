Developer Handbook 
created: Chat GPT (Perplexity assist) 2025-12-11
updated: 2025-12-14
---
Here is a merged and updated version of the LifeOS Developer Handbook, blending your original Developer Handbook with the most recent technical, architectural, and agentic coding guidance:

🛠️ LifeOS Developer Handbook (v2.0)
A unified schema, workflow, and execution guide for building the “LifeOS” personal knowledge, productivity, and emotional intelligence system, integrating PARA, GTD, Zettelkasten, Therapeutic Journaling, and Hybrid RAG AI.

1. 🎯 Purpose
This document defines all data models, operations, workflows, bridging logic, and expectations for AI agents and human developers to:

Parse user input

Place it in the correct system layer (PARA/GTD/Zettelkasten/Therapeutic)

Create/update the unified graph-based knowledge system

Propose tasks, projects, zettels, reflections, and links

Maintain long-term order and consistency

Orchestrate AI-driven insights, retrieval, and regulation (RAG, emotion logging, grounding)

This is the “source of truth” for the AI developer.

2. 🧩 Core Concepts
PARA
Projects: Multi-step outcomes with deadlines.

Areas: Ongoing responsibilities.

Resources: Reference materials, evergreen.

Archives: Inactive items.

GTD
Tasks: Concrete, physical next actions.

Contexts: Where/how tasks get done.

Horizons: Purpose → Vision → Goals → Areas → Projects → Tasks.

Zettelkasten
Zettels: Atomic notes.

Links: Semantic relationships (bidirectional).

Reflections: Higher-level insights.

Therapeutic Graph (Coaching Module)
Journal Objects: Entities representing emotional states.

Nodes: Emotion, Belief, Trigger, CopingMechanism, Episode.

Flows: Interactive coaching sessions (CBT, various frameworks).

GTD Dashboard: Visual overview of tasks, contexts, and horizons.

Prism Clarity Studio: AI-powered decision-making and training engine.

3. 📦 Unified Data Models (Implementation-Ready Schemas)
These should be treated as JSON-like TypeScript interfaces.

3.1 Zettel
json
{
  "id": "string",
  "type": "zettel",
  "title": "string",
  "body": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "links": ["string"], // zettel IDs or entity IDs
  "tags": ["string"],
  "horizon": "none|vision|goals|principles",
  "contexts": ["string"] // optional, GTD integration
}
3.2 Project
json
{
  "id": "string",
  "type": "project",
  "title": "string",
  "desired_outcome": "string",
  "why_it_matters": "string",
  "success_criteria": ["string"],
  "next_actions": ["string"], // task IDs
  "status": "active|paused|done",
  "area": "string|null",
  "related_zettels": ["string"],
  "horizon": "projects"
}
3.3 Area
json
{
  "id": "string",
  "type": "area",
  "title": "string",
  "description": "string",
  "health_metric": "Stable|Needs Attention",
  "active_projects": ["string"],
  "active_tasks": ["string"],
  "related_resources": ["string"],
  "related_zettels": ["string"],
  "horizon": "areas"
}
3.4 Resource
json
{
  "id": "string",
  "type": "resource",
  "title": "string",
  "format": "link|file|zettel|mixed",
  "body": "string",
  "tags": ["string"],
  "related_zettels": ["string"],
  "horizon": "resources"
}
3.5 Task
json
{
  "id": "string",
  "type": "task",
  "title": "string",
  "description": "string",
  "status": "next|waiting|scheduled|done",
  "due": "timestamp|null",
  "context": "string",
  "project": "string|null",
  "area": "string|null",
  "related_zettels": ["string"],
  "horizon": "actions"
}
3.6 Goal
json
{
  "id": "string",
  "type": "goal",
  "title": "string",
  "description": "string",
  "deadline": "timestamp|null",
  "success_criteria": ["string"],
  "related_projects": ["string"],
  "related_zettels": ["string"],
  "horizon": "goals"
}
3.7 Reflection
json
{
  "id": "string",
  "type": "reflection",
  "body": "string",
  "insights": ["string"],
  "generated_zettels": ["string"],
  "related_areas": ["string"],
  "related_projects": ["string"],
  "created_at": "timestamp"
}
3.8 Therapeutic Nodes (Coaching Module)
JournalEntry
json
{
  "id": "string",
  "type": "journal_entry",
  "body": "string",
  "mood_rating": "number", // 1–10
  "emotions": ["string"], // Emotion IDs
  "beliefs": ["string"], // Belief IDs
  "created_at": "timestamp"
}
Emotion
json
{
  "id": "string",
  "type": "emotion",
  "name": "string",
  "intensity": "number",
  "valence": "positive|negative|neutral",
  "related_entries": ["string"]
}
Belief
json
{
  "id": "string",
  "type": "belief",
  "statement": "string",
  "status": "limiting|empowering",
  "related_entries": ["string"]
}
Trigger
json
{
  "id": "string",
  "type": "trigger",
  "description": "string",
  "related_emotions": ["string"]
}
4. 🔗 Bridging Rules (Critical Execution Logic)
4.1 Zettel → Project Conversion
When a zettel expresses:

A desired outcome,

That requires multiple steps,

And describes effort over time,
THEN propose a Project and link bidirectionally.

4.2 Weekly Review Loop
For each Area:

Retrieve active projects, tasks, recent reflections.

Ask: “Any new changes in this Area?”

Generate new zettels for insights.

Propose new projects, task clean-ups, resource updates.

Create a Reflection capturing new insights.

4.3 Therapeutic Bridging (Journal → Insight)
When a JournalEntry reveals a recurring pattern or significant realization:

Extract Beliefs.

Create a Zettel for key beliefs/insights.

Propose a Task or Resource link for coping mechanisms.

5. 🧠 Session Expectations for the AI Agent
For every user query:

Identify involved system layers (PARA/GTD/Zettelkasten/Therapeutic/Prism).

Suggest data structure or state changes.

Generate prompts or pseudo-code for coding agents.

6. 🔧 Coding Agent Instructions (Junior-Level Ready)
Core Rules
Always validate input against the schemas.

Auto-detect content type (task, project, area, zettel, goal, reflection, GTD element, Prism request).

Follow bridging rules without exception.

Keep all links bidirectional.

Use timestamps automatically.

Never delete—only archive.

Produce consistent IDs (UUIDv4).

Every Project has at least one Next Action.

Every Zettel links to at least one other entity.

Weekly Review workflow must be a callable function.

7. ⚙️ System Operations API (Pseudo-API for AI Coder)
Zettel operations
create_zettel(data)

update_zettel(id, patch)

link_zettels(id1, id2)

Project operations
create_project(data)

add_task_to_project(project_id, task_id)

update_project_status(project_id, status)

Area operations
create_area(data)

assign_project_to_area(area_id, project_id)

Task operations
create_task(data)

update_task_status(id, status)

Reflection operations
create_reflection(data)

Weekly Review
run_weekly_review()

8. 📋 Checklist for the AI Coder
text
[ ] Validate all inputs using schema
[ ] Detect type: zettel/project/task/etc.
[ ] Apply bridging rules
[ ] Maintain bidirectional links
[ ] Update timestamps
[ ] Ensure each project has next actions
[ ] Archive only, never delete
[ ] Generate pseudo-code for all operations
[ ] Return both: state changes + reasoning
9. 📚 “Done-For-You” Prompts
Create a new entity
text
CreateEntity({
  type: "zettel",
  title: "...",
  body: "..."
})
Generate weekly review actions
text
RunWeeklyReview({ area_id: "..." })
Convert zettel → project
text
ConvertZettelToProject({ zettel_id: "..." })
10. 🧭 Final Note — How the AI Should Work
Think of the system as:

A graph (entities + links)

A workflow engine (bridging rules + weekly reviews)

A parser (interprets user text)

A consistent database (never messy)

Goal: Clarity, consistency, and long-term maintainability.
