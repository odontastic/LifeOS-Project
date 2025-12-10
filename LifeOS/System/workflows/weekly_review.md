---
description: Guide the user through a complete GTD Weekly Review
---

1. **Clear Inboxes**:
   - List all files in `GTD-Tasks/0-Inbox/`.
   - For each file:
     - Read content.
     - Ask user: "Actionable? (Next-Action, Waiting-For, Project, Reference, Trash)".
     - Move file to appropriate folder based on answer.
     - If "Next-Action", ask for Context tags (e.g., @Computer).

2. **Review Projects**:
   - List all folders in `Projects/Active/`.
   - For each project:
     - Ask: "Is this project still active? Any new next actions?"
     - If user provides actions, create new task files in `GTD-Tasks/1-Next-Actions/` linked to this project.

3. **Relationship Check**:
   - Ask: "How was your presence with your wife this week? Rate 1-10."
   - Ask: "What is one thing you can do to improve connection next week?"
   - Create a task for this improvement in `GTD-Tasks/1-Next-Actions/`.

4. **Plan Next Week**:
   - Ask: "What are the 'Big Rocks' for next week?"
   - Update `Dashboard.md` with these focus items.
