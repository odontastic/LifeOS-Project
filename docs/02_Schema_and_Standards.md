---
title: "LifeOS Schema and Standards"
type: "Documentation"
status: "Active"
created: "2025-12-11"
last_updated: "2025-12-11"
tags: ["documentation", "schema", "standards", "frontmatter", "gtd", "para"]
---

# LifeOS Project Schema Standards 
# created: 2025-12-10

## Overview
This document comprehensively documents all schema standards used throughout the LifeOS project. These standards ensure consistency, maintainability, and effective knowledge management across the entire system.

---

## 1. YAML Frontmatter Standards

### Required Fields
- `title`: The title of the document (string)
- `type`: The type of document (e.g., "Note", "Project", "Area", "Resource", "System", "Template", "Journal")
- `status`: Current status (e.g., "Active", "Completed", "On Hold", "Inbox", "Next Action", "Waiting For", "Someday Maybe", "To Read", "To Think About", "Needs Processing")
- `created`: Creation date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- `tags`: Array of relevant tags for categorization and searching

### Optional Fields
- `subtitle`: Brief description or subtitle
- `category`: Document category (e.g., "projects", "areas", "resources", "system", "archives")
- `last_modified`: Last modification date in ISO 8601 format
- `project`: Related project reference using [[link]] format
- `area`: Related area reference using [[link]] format
- `context`: Context tag for tasks (e.g., "@Computer", "@Home", "@Calls", "@Errands", "@Shopping", "@Cleaning", "@Organization")
- `priority`: Priority level (e.g., "Critical", "High", "Medium", "Low")
- `energy`: Energy required (e.g., "High", "Medium", "Low")
- `time`: Estimated time required (e.g., "5min", "15min", "30min", "1h", "2h+")
- `due`: Due date in ISO 8601 format
- `completed`: Completion date in ISO 8601 format
- `related_files`: Array of related file paths
- `related_areas`: Array of related area references
- `related_projects`: Array of related project references
- `next_action`: Next action description

### Special Frontmatter Structure for Templates
Templates use a special dual frontmatter structure:
```yaml
---
{title: Template Name, type: System, up: '[[System/Templates]]'}
---
---
title: "Dynamic Title {{date}}"
type: DynamicType
date: {{date}}
tags: [tag1, tag2]
---
```

### Validation
- All markdown files must have proper YAML frontmatter
- Frontmatter must start and end with `---`
- Use ISO 8601 date format consistently
- Update `last_modified` whenever document is edited
- Run validation with: `python check_frontmatter.py`

---

## 2. File Organization and Naming Conventions

### Directory Structure
```
Project Root/
├── knowledge_base/
│   ├── Projects/           # Active and completed projects
│   ├── Areas/             # Life areas and responsibilities
│   ├── Resources/         # Knowledge assets, references, guides
│   ├── GTD-Tasks/         # Task management by priority
│   ├── Journal/           # Personal reflections and daily notes
│   ├── Archives/          # Completed and historical content
│   └── Inbox.md          # Catch-all for unprocessed items
│
└── System/               # System documentation, templates, standards
```

### File Naming Standards
- Use camel snake case for all file names
- Prefix with numbers for ordering (e.g., `01-note-template.md`, `02-area-template.md`)
- Use dates in YYYY-MM-DD format for time-sensitive files
- Include descriptive names that reflect content type

### Prefix Ordering System
- `00-` for master indexes and foundational files
- `01-` for primary templates and core files
- `02-`, `03-` for secondary and tertiary files
- Numbers followed by descriptive names

---

## 3. Template Standards

### Note Template (Enhanced)
```yaml
---
title: "Note Title"
type: Note
status: Active
created: YYYY-MM-DD
tags: [note, topic]
related_files: [[related-file]]
related_areas: [[Areas/Area-Name]]
related_projects: [[Projects/Active/Project-Name]]
---
```

### Project Template
```yaml
---
title: "Project Name"
type: Project
status: Active  # Active | On Hold | Completed
created: YYYY-MM-DD
tags: [project, category]
area: [[Areas/Area-Name]]
---
```

### Area Template
```yaml
---
title: "Area Name"
type: Area
status: Active
created: YYYY-MM-DD
tags: [area, life-domain]
description: |
  Comprehensive description of the life area
  including scope and responsibilities.
```

### Daily Journal Template
```yaml
---
title: "Daily Reflection - {{date}}"
type: Journal
date: {{date}}
tags: [journal, daily]
---
```

### Task Template
```yaml
---
title: "Task Title"
status: Inbox  # Inbox | Next-Action | Waiting-For | Someday-Maybe | To-Read | To-Think-About | Needs-Processing
project: []    # [[Projects/Active/Project-Name]]
area: []       # [[Areas/Area-Name]]
context: []    # [@Computer, @Home, @Calls, @Errands, @Shopping, @Cleaning, @Organization]
energy: Medium # High | Medium | Low
time: 15min    # 5min | 15min | 30min | 1hr | 2hr+
priority: Medium # Critical | High | Medium | Low
created: {{date}}
due: ""        # YYYY-MM-DD
completed: ""  # YYYY-MM-DD
---
```

---

## 4. Linking and Relationship Standards

### Bi-directional Linking
- Use `[[target-file]]` format for internal links
- Include `up` field in frontmatter to establish parent-child relationships
- Link to relevant areas, projects, and resources from content

### Context Definitions
- Use `@` prefix for context tags (e.g., "@Computer", "@Home", "@Calls")
- Contexts represent locations or tools needed for tasks

### Relationship Fields
- `up`: Parent file relationship (e.g., `'[[System/Templates]]'`)
- `related_files`: Array of related file paths
- `related_areas`: Array of area references
- `related_projects`: Array of project references

---

## 5. Tagging Standards

### Tag Format
- Use `#tag-name` format within content
- Include `tags` array in frontmatter for categorization
- Use kebab-case for multi-word tags
- Keep tags relevant and concise

### Common Tag Categories
- **Type tags**: `note`, `project`, `area`, `resource`, `system`, `template`, `journal`, `daily`
- **Status tags**: `active`, `completed`, `archived`, `in-progress`
- **Domain tags**: `productivity`, `health`, `relationships`, `finance`, `education`
- **Priority tags**: `high-priority`, `medium-priority`, `low-priority`

### Tag Management
- Use Tags MOC (`System/MOCs/Tags_MOC.md`) for tag overview
- Avoid creating too many specific tags
- Use existing tags when possible
- Review and clean tags quarterly

---

## 6. GTD Task Management Standards

### GTD Directory Structure
```
GTD-Tasks/
├── 0-Inbox/          # Unprocessed tasks and ideas
├── 1-Next-Actions/   # Immediate next actions
├── 2-Waiting-For/    # Items delegated to others
├── 3-Someday-Maybe/  # Future possibilities
├── 4-To-Read/        # Reading list
├── 5-To-Think-About/  # Items requiring consideration
└── 6-Needs-Processing/ # Items requiring clarification
```

### Task Status Values
- `Inbox`: Unprocessed tasks
- `Next Action`: Immediate next action
- `Waiting For`: Delegated items
- `Someday Maybe`: Future possibilities
- `To Read`: Reading list items
- `To Think About`: Items requiring consideration
- `Needs Processing`: Items requiring clarification

### Task Metadata
- `context`: Where/with what the action can be performed
- `priority`: Critical, High, Medium, Low
- `energy`: Energy level required
- `time`: Estimated time required
- `project`: Related project
- `area`: Related life area

---

## 7. Project/Area/Resource Organization (PARA)

### PARA Methodology
- **Projects**: Goal-oriented with a clear outcome
- **Areas**: Ongoing responsibilities and life domains
- **Resources**: Knowledge assets and reference materials
- **Archives**: Completed or inactive content

### Project Organization
```
Projects/
├── 00-project-master-index.md
├── Active/
│   ├── project-name/
│   └── project-name.md
├── Completed/
└── Someday/
```

### Area Organization
```
Areas/
├── 00-area-master-index.md
├── Area-Name/
│   ├── sub-area/
│   └── area-file.md
└── Personal-Reflection/
```

### Resource Organization
```
Resources/
├── Knowledge/          # Knowledge assets and guides
├── Lists/             # Collections and lists
├── People/           # Contact information
├── Courses/          # Learning materials
├── Books/            # Book references
├── Articles/         # Article references
└── Guides/           # How-to guides
```

---

## 8. Archive Standards

### Archive Categories
- **Projects Completed**: Successfully finished projects
- **Areas Deprecated**: Restructured or irrelevant areas
- **Resources Obsolete**: Superseded or outdated materials
- **Historical**: Version history and development records

### Archive Management
- Use `Archives/00-archive-master-index.md` for catalog
- Implement retention policy:
  - Completed projects: Indefinite retention
  - Deprecated areas: 2 years then evaluate
  - Obsolete resources: 1 year unless historically significant
  - Historical data: Permanent retention
- Maintain broken link prevention
- Preserve historical context in metadata

### Archive Status
- Use `status: archived` in frontmatter
- Include `archived_date: YYYY-MM-DD`
- Keep tags for searchability
- Maintain cross-references to active content

---

## 9. Journal and Daily Note Standards

### Daily Journal Structure
```yaml
---
title: "Daily Reflection - YYYY-MM-DD"
type: Journal
date: YYYY-MM-DD
tags: [journal, daily]
---
```

### Daily Journal Sections
- **Morning Calibration** (7:00 AM):
  - Emotional state assessment
  - Wife's state assessment
  - ONE THING focus
  - Virtue focus

- **Evening Review** (6:00 PM):
  - ONE THING completion check
  - Relationship check (presence, connection, conflict)
  - Wins & gratitude (3 items)
  - Tomorrow's priority

### Daily Note Format
- Use ISO 8601 timestamps
- Include relevant tags for categorization
- Link to related projects and areas
- Document activities, thoughts, and observations
- Include future action items

---

## 10. Automation and Validation Scripts

### Frontmatter Validation
- **Script**: `check_frontmatter.py`
- **Purpose**: Validates all markdown files have proper YAML frontmatter
- **Usage**: `python check_frontmatter.py`
- **Validation**:
  - Checks for proper `---` delimiters
  - Verifies content exists after frontmatter
  - Reports files with missing or malformed frontmatter

### Contextual Guardian
- **Script**: `contextual_guardian.py`
- **Purpose**: Emergency emotional regulation tool
- **Usage**: `python contextual_guardian.py`
- **Features**:
  - Breathing exercises (4-7-8 technique)
  - Active listening guidance
  - Relationship repair prompts

### Empathy Engine
- **Script**: `empathy_engine.py`
- **Purpose**: AI-powered empathy and relationship analysis
- **Usage**: `python empathy_engine.py --dry-run`
- **Features**:
  - Analyzes communication patterns
  - Provides relationship insights
  - Suggests improvement strategies

### Python Script Standards
- Use shebang: `#!/usr/bin/env python3`
- Include docstrings with purpose and usage
- Handle exceptions gracefully
- Provide clear output and error messages
- Include dry-run mode for safe testing

---

## 11. Web Application Standards

### Technology Stack
- **Framework**: Next.js with TypeScript
- **Styling**: Tailwind CSS
- **Package Manager**: npm
- **Development**: `npm run dev`
- **Build**: `npm run build`
- **Start**: `npm start`

### API Routes
- Location: `app/api/`
- Structure: RESTful endpoints
- Error handling: Try-catch blocks with proper HTTP status codes
- Environment variables: Use `.env` files for sensitive data

### Chat Interface
- **Route**: `/api/chat/route.ts`
- **Purpose**: AI conversation endpoint
- **Security**: Environment variable protection
-- **Mock Response**: Development placeholder for testing

### Web Application Standards
- Use TypeScript for type safety
- Follow Next.js app router conventions
- Implement proper error handling
- Use environment variables for configuration
- Include development and production modes

---

## 12. RAG API Schema Standards

### Node Types
- **User**: Individual authoring journal entries
- **JournalEntry**: Single journal entry
- **Emotion**: Specific emotion mentioned or inferred
- **Belief**: Core belief or thought pattern
- **Trigger**: Event causing emotional reaction
- **CopingMechanism**: Action or thought process for managing emotions
- **Goal**: Personal or professional goal
- **Episode**: Significant life event or period
- **Pattern**: Recurring theme or behavior
- **SessionSummary**: Summary of user interaction

### Relationship Types
- **AUTHORED_BY**: `(JournalEntry)-[:AUTHORED_BY]->(User)`
- **RELATES_TO**: Connects related nodes
- **TRIGGERED_BY**: `(Emotion)-[:TRIGGERED_BY]->(Trigger)`
- **PRACTICED**: `(User)-[:PRACTICED]->(CopingMechanism)`
- **PART_OF**: `(JournalEntry)-[:PART_OF]->(Episode)`
- **MENTIONS**: `(JournalEntry)-[:MENTIONS]->(Belief)`
- **SUMMARIZES**: `(SessionSummary)-[:SUMMARIZES]->(JournalEntry)`

### Node Properties
- **created_at**: Timestamp of node creation
- **life_domain**: Area of life (e.g., "Work", "Relationships")
- **life_stage**: Life stage (e.g., "College", "Adulthood")
- **stability**: "Stable" or "Transient"
- **confidence**: Confidence score (0.0 to 1.0)

### API Endpoints
- **POST /api/ingest**: Process new text and extract entities
- **POST /api/query**: Query the knowledge graph
- **POST /api/flows/start**: Initialize coaching flow
- **POST /api/flows/advance**: Advance coaching flow
- **POST /api/feedback**: Log user feedback
- **GET /**: Health check

### Safety Features
- Crisis language detection
- Emergency disclaimers
- Safe content processing
- User protection mechanisms

---

## 13. Command and Workflow Standards

### Command Menu System
- **Location**: `System/COMMAND_MENU.md`
- **Purpose**: Comprehensive command reference
- **Structure**: Categorized commands with descriptions and usage

### Workflows
- **Location**: `System/workflows/`
- **Types**: Content intake, crisis support, morning calibration, weekly review
- **Structure**: Step-by-step processes with clear actions
- **Documentation**: Each workflow includes purpose, steps, and examples

### Command Standards
- Use clear, action-oriented names
- Include purpose and usage instructions
- Provide examples when helpful
- Organize by category and priority
- Update regularly as system evolves

---

## 14. Maintenance and Quality Assurance

### Regular Maintenance Tasks
- **Weekly**: Process GTD inboxes, review active projects, relationship check
- **Monthly**: Archive completed items, clean up tags, review system health
- **Quarterly**: Review and update standards, major system cleanup
- **Annually**: Comprehensive system review and strategic planning

### Quality Assurance
- Run frontmatter validation regularly
- Check for broken links
- Review archive organization
- Update templates as needed
- Validate automation scripts

### System Health Indicators
- All markdown files have proper frontmatter
- Broken link percentage remains low
- Archive size is manageable
- Templates are up-to-date
- Automation scripts function correctly

---

## 15. Integration and Interoperability

### AI Integration
- **Prompt Templates**: Located in `System/Prompts/`
- **AI Agents**: Contextual guardian, empathy engine, pattern hunter
- **Coaching Frameworks**: Integrated therapeutic approaches
- **Safety Protocols**: Crisis detection and response

### Version Control
- **Git Integration**: Standard git workflow with meaningful commits
- **Branch Strategy**: Main branch for stable releases, feature branches for development
- **Commit Messages**: Clear, descriptive messages following conventional commits
- **Tagging**: Version tags for major releases

### Cross-Reference System
- **File References**: Consistent use of `[[file-path]]` format
- **Area-Project Links**: Projects link to relevant areas
- **Resource Integration**: Knowledge assets referenced in relevant contexts
- **Template Usage**: Templates consistently used for content creation

---

## Implementation Guidelines

### New Content Creation
1. **Choose Template**: Select appropriate template from `System/Templates/`
2. **Fill Frontmatter**: Complete all required fields, optional as needed
3. **Use Links**: Link to related areas, projects, and resources
4. **Add Tags**: Include relevant tags for categorization
5. **Follow Structure**: Use standard section hierarchy
6. **Review Quality**: Ensure content meets system standards

### System Evolution
1. **Document Changes**: Update standards when adding new features
2. **Maintain Backward Compatibility**: Ensure existing content remains functional
3. **Test New Features**: Validate changes in development environment
4. **Gradual Rollout**: Implement changes systematically
5. **Gather Feedback**: Collect user input on improvements

### Training and Onboarding
1. **Start Here**: Use `00-Start-Here.md` for system introduction
2. **Template Guide**: Reference `System/Getting_Started/01_Using_Templates.md`
3. **Connection Guide**: Use `System/Getting_Started/02_Creating_Connections.md`
4. **AI Integration**: Review `System/Getting_Started/03_Working_With_AI.md`
5. **Workflow Training**: Study `System/Getting_Started/05_Maintenance_and_Workflow.md`

---

This comprehensive schema standard document ensures consistency, maintainability, and effective knowledge management across the entire LifeOS project. Regular review and updates will keep the system optimized for its intended purpose.
