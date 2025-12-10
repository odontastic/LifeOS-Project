---
{title: Agents, type: Note, up: '[[Archives/Legacy-Plans]]'}
---
# AGENTS.md - Life OS Agent Documentation

## Essential Commands
### Development
```bash
# Start development server
npm run dev

# Build production assets
npm run build

# Start production server
npm run start

# Run linter
npm run lint

### Chat Interface

# Convert fleeting note to permanent note
[Process] Transform my fleeting note about "morning routine" into
a permanent concept note
# Create a new module
[Creation: Life Coaching] Draft a new life coaching framework with PARA method
integration

# Update project status
[Project: LifeOS Web] Progress update: Completed component A, next steps include
testing

## Codebase Structure

/home/austin/Documents/LifeOS/
├── 01-Projects/
   ├── Development/            # Web application
      ├── pages/              # Next.js pages
         ├── _app.js         # Layout root
         ├── journal.js      # Journal page
         └── risk-audit.js   # Risk audit page
      ├── app/                # Application logic
         └── pageActions.js  # Page routing logic
      └── lib/                # Type definitions
          ├── env.ts          # Environment variables
          └── baseSchemas.ts   # Data validation
├── .cursor/rules/life-operating-system.mdc  # Framework rules
├── .cursor/commands/start.md                # Initialization commands

## Naming Conventions

1. Files: Use descriptive kebab-case or snake_case with dates when relevant
•  2025-10-15_project_milestone.md 
•  module_b:module_desc.md 
2. Projects: Use active status folder structure
•  Active/project_name.md 
•  Completed/project_name.md 
•  Someday/project_name.md 
3. Verticals: Use domain-specific prefixes
•  proc_method_description.md 
•  ref_concept_keyword.md 
•  fct_statement_to_verify.md 


## Testing Approach

1. Unit Tests:
• Should be created for core components (currently missing)
• Use Jest with TypeScript configuration
• Focus on API endpoints and state management
2. E2E Testing:
• Next.js built-in testing framework
• Run with  npm test  command
• Cover main workflows like journaling and risk assessment


## Project-Specific Context

1. Spiritual Integration:
• All systems designed to operate in cooperation with divine guidance
• Virtue-based goal setting (e.g., faithfulness, perseverance)
2. Relationship Framework:
• Weekly relationship check-ins using Step 8 process
• Conflict resolution protocol aligned with Gottman method
3. Health System:
• Integrated across all life domains
• Customizable tracking templates for metrics
4. Technical Considerations:
• Environment variables require setup
• Claude API integration already implemented
• Requires  .env  file configuration


## Gotchas & Non-Obvious Patterns

1. Snowflake Elimination:
# Before
enum states { DRAFT, SUBMITTED, APPROVED }

# After
enum Status {
DRAFT = 1 0,
SUBMITTED = 1 1,
APPROVED = 1 2
}

2. Memory Management:
• Critical to implement LRU cache in data-heavy components
• Memory-intensive operations should use streaming architecture
3. Security:
• All JSON operations must use strict schema architecture
• AlI keys must be accessed through environment variables only
4. Performance:
• MC4 caching system requires 4 flags:
• F: Keep files
• C: Check cache
• R: Retry on failure
• A: Atomic writes

5. Cross-Platform Considerations:
• Maintain POSIX compatibility despite Windows development
• Use forward slashes in all path operations
• Validate encoding settings for multilingual support


## Recommended Next Steps

1. Complete test suite setup for core components
2. Implement environment variable encryption
3. Add dependency tracking for all modules
4. Establish CI/CD pipeline configuration
5. Create deployment documentation

This framework balances structure with flexibility to accommodate
your unique journey while maintaining strong foundations for future
growth.
