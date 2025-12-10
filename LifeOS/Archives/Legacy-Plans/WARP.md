---
{title: Warp, type: Note, up: '[[Archives/Legacy-Plans]]'}
---
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is a markdown-based knowledge management system (Second Brain) designed to work with AI assistants. It uses a structured directory system to organize personal knowledge, projects, notes, and resources. The system is primarily text-based with some Python/Bash utilities and a React/Electron UI component.

## Directory Structure Architecture

The repository uses a hybrid knowledge organization approach inspired by PARA, Zettelkasten, and other methodologies:

**Core Knowledge Directories:**
- `Knowledge/` - Structured factual information (Concepts/Core, Concepts/Derived, Facts/Verified, Facts/Unverified, Procedures, References)
- `Notes/` - Capturing system (Fleeting, Permanent, Literature)
- `Projects/` - Task-oriented work (Active, Completed)
- `Journal/` - Time-based reflections (Daily, Weekly, Monthly)
- `Resources/` - Learning materials (Books, Articles, Videos, Courses, Templates, Screenshots)
- `People/` - Contact information (Personal, Professional)

**Specialized Directories:**
- `Interests/`, `Personal/`, `Lifestyle/`, `Media/`, `Professional/`, `Creativity/`, `Collections/`, `Niche Topics/`, `Areas/`, `Learning/`
- `Tags/` - Cross-referencing system
- `Metadata/` - System information
- `Archives/` - Inactive content
- `Commands/` - Scripts and documentation for system interaction

**UI Component:**
- `SecondBrainUI/` - React/Electron desktop application

## Key Commands

### Screenshot Processing
```bash
# Process screenshot with OCR and create fleeting note
Commands/screenshot.sh /path/to/screenshot.png [--title "Optional Title"]
```

**Prerequisites:**
- Python 3.6+
- Tesseract OCR (`brew install tesseract` on macOS, `sudo apt-get install tesseract-ocr` on Linux)
- Python packages: pytesseract, Pillow (auto-installed by script)

### Directory Structure Setup
```bash
# Create the full directory structure from scratch
./create_directory_structure.sh
```

### SecondBrainUI Development
```bash
cd SecondBrainUI

# Start React development server
npm start

# Run Electron app in dev mode
npm run electron-dev

# Build production version
npm run build

# Package as desktop app
npm run dist
```

**Available platforms:** macOS (dmg), Windows (nsis), Linux (AppImage)

## AI Agent Integration Patterns

This repository is designed to be managed by AI assistants. The system uses:

1. **Command Prefixes** - Structured prefixes like `[Daily]`, `[Thought]`, `[Project: Name]` to categorize content
2. **Natural Language Understanding** - AI should interpret intent even without exact command formats
3. **Automatic File Organization** - AI creates/updates markdown files in appropriate directories
4. **Metadata Management** - Consistent YAML frontmatter and markdown metadata blocks

### Key AI Interaction Files
- `AI_Interaction_Guide.md` - General AI interaction guidance
- `Commands/Comprehensive_Command_Reference.md` - Complete list of 50+ command prefixes
- `Commands/Natural_Language_Understanding.md` - Natural language processing guidelines
- `Commands/AI_Agent_Optimization.md` - Agent optimization strategies

### Content Creation Workflow
When AI creates/updates notes, it should:
1. Use descriptive filenames (snake_case or kebab-case)
2. Include metadata (created/modified dates, tags, related notes)
3. Write in first-person as if the user wrote it
4. Add "Questions to Explore" and "Possible Next Steps" sections for fleeting notes
5. Cross-reference related notes using `[[wiki-style-links]]`

## File Naming Conventions

- Use descriptive names: `quantum_computing_basics.md` not `qc1.md`
- Include dates when relevant: `2023-10-15_project_milestone.md`
- Use kebab-case or snake_case consistently
- Add prefixes for categories: `ref_Einstein_relativity.md`, `proc_making_sourdough.md`

## Testing

This is primarily a documentation/knowledge repository. There are no traditional unit tests. Validation involves:
- Ensuring markdown files are properly formatted
- Verifying directory structure exists
- Testing screenshot OCR functionality with sample images
- Testing SecondBrainUI React app: `cd SecondBrainUI && npm test`

## Important Notes

### Content Philosophy
- All notes should be written in first-person perspective as if the user wrote them
- AI acts as an intelligent extension of the user's thinking process
- Focus on capturing, organizing, and connecting knowledge
- Maintain consistent metadata across all notes

### Processing Pipeline
Fleeting notes (raw thoughts) → Permanent notes (refined knowledge) → Archived (completed/inactive)

### Git Workflow
- Empty directories contain `.gitkeep` files for version control tracking
- `.gitignore` excludes macOS system files, node_modules, IDE configs, and environment variables
- Do not commit sensitive information (API keys, personal details)

### Screenshot System
The screenshot processing system:
1. Extracts text using Tesseract OCR
2. Saves screenshot copy to `Resources/Screenshots/`
3. Creates fleeting note with extracted text in `Notes/Fleeting/`
4. Links the screenshot in the note for reference

### Cross-Platform Considerations
- Bash scripts use `#!/bin/bash` shebang
- Python scripts require Python 3.6+
- React app uses standard Node.js tooling (npm/yarn)
- Electron app supports macOS, Windows, and Linux

## Command Reference Summary

**Most Common Operations:**
- `[Daily] <content>` - Create daily journal entry
- `[Thought] <idea>` - Capture quick idea
- `[Project: Name] <update>` - Update project
- `Find notes about <topic>` - Search knowledge base
- `Summarize my notes on <topic>` - Get summary
- `[Process]` - Convert fleeting to permanent note

**Developer-Specific:**
- `[Code: Language] <snippet>` - Document code
- `[Architecture] <design>` - Document system design
- `[Debug: Issue] <solution>` - Track debugging insights

See `Commands/Comprehensive_Command_Reference.md` for complete list of 50+ commands across all domains (personal, professional, creative, lifestyle, media, etc.).

## Architecture Insights

### Hybrid Knowledge System
Combines multiple proven methodologies:
- **PARA** (Projects, Areas, Resources, Archives) for organization
- **Zettelkasten** principles for atomic notes and connections
- **Building a Second Brain** capture/organize/distill/express workflow
- **Progressive summarization** through fleeting → permanent note progression

### AI-First Design
Unlike traditional note systems, this is optimized for AI interaction:
- Structured command prefixes for easy parsing
- Consistent metadata for context building
- Natural language fallbacks when commands aren't used
- First-person voice maintained by AI to feel authentic
- Connection suggestions and relationship discovery

### Separation of Concerns
- **Knowledge layer** (`Knowledge/`, `Notes/`) - Pure information
- **Temporal layer** (`Journal/`) - Time-based organization
- **Action layer** (`Projects/`) - Goal-oriented work
- **Input layer** (`Resources/`) - External materials
- **Social layer** (`People/`) - Relationship management
- **Personal layers** (`Interests/`, `Lifestyle/`, `Media/`, etc.) - Life aspects
- **Inbox layer** ('Inbox/') - GTD Brain dump, to-do, to think about, needs processing

This design allows content to exist in multiple conceptual spaces simultaneously through tagging and cross-references while maintaining clear physical organization.
