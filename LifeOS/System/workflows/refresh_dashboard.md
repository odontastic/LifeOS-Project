---
description: Regenerate the Dashboard.md with live data from the system
// turbo-all
---

1. **Gather Data**:
   - **Date**: Get current date.
   - **Focus**: Read the latest file in `Areas/Personal-Reflection/Journal/` to find the "ONE THING" and "Emotion".
   - **Inboxes**: Count files in `GTD-Tasks/0-Inbox/` and `GTD-Tasks/6-Needs-Processing/`.
   - **Active Workflows**: Read `Projects/Active/` to list top 3 active projects.

2. **Generate Content**:
   - Construct a new markdown string for `Dashboard.md` following the standard layout:
     - Header: Date & Focus
     - Section 1: Daily Focus (One Thing, Virtue, Emotion)
     - Section 2: Inboxes (with counts)
     - Section 3: Quick Actions (Links to Queries)
     - Section 4: Active Workflows (Summary of active projects)
     - Section 5: Navigation & Help

3. **Update File**:
   - Overwrite `/home/austin/Documents/LifeOS/Dashboard.md` with the generated content.
   - Notify user: "Dashboard refreshed."
