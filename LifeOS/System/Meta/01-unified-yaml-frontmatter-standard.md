---
{title: 01 Unified Yaml Frontmatter Standard, type: System, up: '[[System/Meta]]'}
---
# Unified YAML Frontmatter Standard

## Overview
This document outlines the standardized YAML frontmatter structure for all Markdown files in the LifeOS system.

## Required Fields
- `title`: The title of the document
- `subtitle`: A brief subtitle or description
- `type`: The type of document (e.g., index, project, area, resource)
- `category`: The category of the document (e.g., projects, areas, resources)
- `status`: The status of the document (e.g., Active, Completed, On Hold)
- `created`: The creation date in ISO 8601 format
- `last_modified`: The last modification date in ISO 8601 format
- `tags`: Relevant tags for the document
- `related_files`: List of related files or documents

## Optional Fields
- `related_areas`: List of related areas
- `related_projects`: List of related projects
- `next_action`: The next action or task related to the document

## Example
```yaml
---
title: "Example Document"
subtitle: "An example document"
type: "example"
category: "examples"
status: "Active"
created: "2025-11-11"
last_modified: "2025-11-11"
tags:
  - "example"
  - "document"
related_files:
  - "path/to/related/file.md"
---
```

## Guidelines
- All Markdown files should include the required fields.
- Use ISO 8601 format for dates.
- Keep the `tags` field relevant and concise.
- Update `last_modified` whenever the document is edited.

## Maintenance
This standard will be reviewed and updated quarterly to ensure it remains relevant and effective.