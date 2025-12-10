---
{title: Metadata Standards, type: System, up: '[[System]]'}
---
# LifeOS Metadata Standards

## Overview
Consistent metadata allows the system to filter, sort, and query information effectively. All markdown files should include a YAML frontmatter block at the top.

## 1. Task Metadata
Used for files in `GTD-Tasks/`

```yaml
---
title: "Action Verb + Object"
status: Next-Action      # Options: Inbox, Next-Action, Waiting-For, Someday-Maybe, To-Read, To-Think-About, Needs-Processing
project: []              # Wiki-link: [[Projects/Active/Project-Name]]
area: []                 # Wiki-link: [[Areas/Area-Name]]
context: []              # Tags: @Computer, @Home, @Calls, @Errands, @Shopping, @Cleaning, @Organization
energy: Medium           # Options: High, Medium, Low
time: 15min              # Options: 5min, 15min, 30min, 1hr, 2hr+
priority: Medium         # Options: Critical, High, Medium, Low
created: YYYY-MM-DD
last_updated: YYYY-MM-DD # When file was last modified
due: YYYY-MM-DD          # Optional
completed: YYYY-MM-DD    # When status changes to Done
---
```

### Field Definitions
- **status**: The current workflow state.
- **project**: The outcome this task supports.
- **area**: The ongoing responsibility this task falls under.
- **context**: The physical location or tool needed.
- **energy**: Mental/physical effort required.
- **time**: Estimated duration.
- **priority**:
  - **Critical**: Must be done today / ONE THING.
  - **High**: Important, do soon.
  - **Medium**: Standard task.
  - **Low**: Do when possible.

## 2. Project Metadata
Used for files in `Projects/`

```yaml
---
title: "Project Name"
type: Project
status: Active           # Options: Active, Someday, Completed
area: []                 # Wiki-link: [[Areas/Area-Name]]
created: YYYY-MM-DD
deadline: YYYY-MM-DD     # Optional
completed: YYYY-MM-DD    # When status changes to Completed
tags: [project, topic]
---
```

## 3. Area Metadata
Used for files in `Areas/`

```yaml
---
title: "Area Name"
type: Area
owner: Austin
created: YYYY-MM-DD
tags: [area]
---
```

## 4. Resource/Note Metadata
Used for files in `Resources/`

```yaml
---
title: "Note Title"
type: Concept            # Options: Concept, Fact, Person, Book, Article, Template
status: Permanent        # Options: Fleeting, Literature, Permanent
tags: [topic, theme]
created: YYYY-MM-DD
source: ""               # URL or Citation
---
```

## 5. Journal Metadata
Used for files in `Areas/Personal-Reflection/`

```yaml
---
title: "Daily Reflection - YYYY-MM-DD"
type: Journal
date: YYYY-MM-DD
tags: [journal, daily/weekly/monthly]
---
```
