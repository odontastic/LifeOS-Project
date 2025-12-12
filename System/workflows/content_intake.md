---
description: Process conversations, notes, and content into LifeOS
---

# Content Intake Processing Workflow

Use this workflow to systematically process **conversations, notes, web articles, videos, and other content** into your LifeOS. This is separate from PARA-GTD task triage (use `QUICK_TRIAGE_GUIDE.md` for that).

## When to Use This Workflow

- After meaningful AI conversations that contain insights, decisions, or ideas
- When processing meeting notes, podcast notes, or article highlights
- After consuming educational content (courses, videos, books)
- When capturing creative ideas or reflections
- During weekly review when processing accumulated notes

---

## Step 1: Identify Content Type

Determine what you're processing:

### 🗣️ **Conversation/Dialogue**
- AI coaching sessions
- Meeting notes
- Phone call summaries
- Meaningful text exchanges

### 📝 **Note/Reflection**
- Personal thoughts
- Journal entries
- Ideas or insights
- Prayers or spiritual reflections

### 📚 **Learning Content**
- Article highlights
- Book notes
- Course content
- Video/podcast summaries

### 🎨 **Creative/Reference Material**
- Design ideas
- Quote collections
- Recipes or how-tos
- Lists or collections

---

## Step 2: Extract Core Value

Ask yourself: **What's the essence of this content?**

1. **Is there a decision made?** → Create a decision log entry
2. **Is there a commitment or promise?** → Create a GTD task
3. **Is there a principle or insight?** → Add to knowledge base
4. **Are there references to follow up on?** → Run `/process_note_references`
5. **Is it purely archival?** → File in appropriate Area or Resource

---

## Step 3: Determine Destination

Use this decision tree:

### 📋 If it's ACTIONABLE:
- **Use PARA-GTD Triage**: Follow `QUICK_TRIAGE_GUIDE.md`
- Create tasks in `GTD-Tasks/`
- Add to active projects in `Projects/Active/`

### 📚 If it's KNOWLEDGE/REFERENCE:
Save to `Resources/Knowledge/`:

**Categorize by type:**
- **Guides** → `Resources/Knowledge/Guides/`
- **Mental Models** → `Resources/Knowledge/Mental_Models.md` or new file
- **How-To** → `Resources/Knowledge/Guides/`
- **Philosophy/Worldview** → `Resources/Knowledge/`
- **Theology/Spiritual** → `Resources/Knowledge/Theology/`
- **Interests** → `Resources/Knowledge/Interests/`

**Naming Convention:**
- Use descriptive names: `Topic-Subtopic-Type.md`
- Example: `Personal-Mantras-Collection.md`
- Example: `Stoic-Philosophy-Core-Principles.md`

### 🏔️ If it's AREA-RELATED (ongoing responsibility):
Save to relevant Area in `Areas/`:
- **Family** → `Areas/Family/`
- **Faith** → `Areas/Faith/`
- **Health** → `Areas/Health/`
- **Personal Development** → `Areas/Personal-Reflection/`
- **Tech** → `Areas/Tech/`

### 🗃️ If it's ARCHIVAL:
- **Completed projects** → `Archives/Projects/`
- **Old versions** → `Archives/`
- **Historical reference** → `Archives/`

---

## Step 4: Create the Document

### Standard Header Format

For knowledge resources, use:

```markdown
# [Title]

**Created:** YYYY-MM-DD  
**Category:** [Primary Category, Secondary Category]  
**Status:** [Active Reference / Draft / Archive]

---

## Overview

[Brief description of what this document contains and why it matters]

**Context:** [How this was created, source, or conversation origin]

---

[Main content sections]

---

## Related Resources

- [[Path/To/Related/Doc|Link Title]]

---

**Next Steps:**
- [ ] [Any follow-up actions]
```

### Conversation Processing Template

For AI conversations specifically:

```markdown
# [Topic] - Conversation Summary

**Date:** YYYY-MM-DD  
**Context:** [What prompted this conversation]  
**Outcome:** [Key decisions or insights]

---

## Key Insights

1. [Major insight #1]
2. [Major insight #2]

---

## Decisions Made

- [Decision 1] → [Action/Task created]
- [Decision 2] → [No action needed]

---

## Content Created

- [[Path/To/New/Document|Document Name]] - [Purpose]

---

## References to Follow Up

- [Author/Book/Resource] - Priority: [High/Medium/Low]
  - Task created: [[GTD-Tasks/path/to/task|Task Name]]

---

## Related

- [[Path/To/Related|Related Topic]]
```

---

## Step 5: Create Bidirectional Links

Ensure discoverability by linking:

1. **From the new document** → Related areas, projects, or resources
2. **To the new document** → Update relevant dashboards or index files

### Key Index Files to Update:

- `00-Start-Here.md` - If it's a major system addition
- Relevant Area index (e.g., `Areas/Family/00-Family-Hub.md`)
- `Resources/Knowledge/` index files if they exist
- Related project files

---

## Step 6: Extract Actionable Items

Run through the content and ask:

### Are there tasks?
- Create in appropriate GTD folder
- Link to the source document

### Are there references?
- Run `/process_note_references` workflow
- Add to `Resources/Lists/to_read_list.md`

### Are there people mentioned?
- Add to `Resources/People/` if significant
- Create contact entries if needed

### Are there commitments?
- Add to calendar if time-specific
- Add to GTD Next Actions if ASAP
- Add to Waiting For if delegated

---

## Step 7: Tag for Future Discovery

Add relevant tags in the frontmatter:

```yaml
---
tags: [category, theme, project-name, person-name]
up: [[Parent/Document|Parent Name]]
---
```

Common tags:
- `transformation`, `growth`, `coaching`
- `theology`, `philosophy`, `spirituality`
- `family`, `marriage`, `parenting`
- `tech`, `automation`, `ai`
- `creative`, `reflection`, `planning`

---

## Step 8: Confirm Completion

Provide a summary:

> ✓ **Intake Complete**  
> 
> **Created:**  
> - [Document Name] in [Location]
> 
> **Linked to:**  
> - [Related Document 1]
> - [Related Document 2]
> 
> **Extracted:**  
> - [N] tasks created
> - [N] references added
> - [N] links established

---

## Quick Reference Decision Matrix

| Content Type | Destination | Action |
|-------------|-------------|---------|
| Personal reflection | `Areas/Personal-Reflection/` | Save & tag |
| General knowledge | `Resources/Knowledge/` | Save & link |
| How-to guide | `Resources/Knowledge/Guides/` | Save & index |
| Spiritual insight | `Resources/Knowledge/Theology/` | Save & link to Area |
| Family-related | `Areas/Family/` | Save & link to Area |
| Task/commitment | `GTD-Tasks/` | Use PARA-GTD triage |
| Reference source | `Resources/Lists/to_read_list.md` | Use reference workflow |
| Creative collection | `Resources/Knowledge/` | Save with descriptive name |

---

## Integration with Other Workflows

- **Task Creation** → Use `QUICK_TRIAGE_GUIDE.md`
- **Reference Extraction** → Use `/process_note_references`
- **Morning Review** → Use `/morning_calibration`
- **Weekly Review** → Use `/weekly_review`

---

## Notes

- **Be selective**: Not everything needs to be saved. Focus on content that has lasting value.
- **Add context**: Always explain WHY something was created and HOW it relates to your goals.
- **Create connections**: The power of this system is in the links between ideas.
- **Review regularly**: During weekly reviews, check if saved content is still relevant.
