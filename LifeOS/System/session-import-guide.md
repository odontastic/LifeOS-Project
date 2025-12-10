---
{title: Session Import Guide, type: System, up: '[[System]]'}
---
# Session Import Guide
**Purpose**: Guidelines for importing past LLM conversations into LifeOS for continuity and pattern analysis

---

## Recommended Import Structure

### Option 1: Chronological Session Files (RECOMMENDED)
Store each conversation as a dated session file in the Assessments directory:

```
Areas/Personal-Reflection/Assessments/
├── 2025-11-20_Initial_Assessment.md (already created)
├── Sessions/
│   ├── 2025-11-15_ChatGPT_Session.md
│   ├── 2025-11-10_Claude_Session.md
│   ├── 2025-11-05_Gemini_Session.md
│   └── README.md (index of all sessions)
```

**Naming Convention**: `YYYY-MM-DD_[LLM-Name]_Session.md`

### Option 2: Thematic Organization
Group by topic rather than date:

```
Areas/Personal-Reflection/Assessments/
├── Marriage-Coaching/
│   ├── 2025-11-15_Session.md
│   ├── 2025-11-10_Session.md
├── EQ-Development/
│   ├── 2025-11-12_Session.md
├── System-Design/
│   ├── 2025-11-08_Session.md
```

---

## Import Methods

### Method 1: Direct Copy-Paste (Simplest)
1. Copy the conversation from the other LLM
2. Create new file: `Areas/Personal-Reflection/Assessments/Sessions/YYYY-MM-DD_[LLM]_Session.md`
3. Add YAML frontmatter:
```yaml
---
title: "Session with [LLM Name] - [Topic]"
date: YYYY-MM-DD
llm: ChatGPT | Claude | Gemini | Other
type: Session
tags: [session, topic1, topic2]
---
```
4. Paste conversation below frontmatter
5. Add a brief summary at the top

### Method 2: Structured Import (Better for Analysis)
Use this template for each imported session:

```markdown
---
title: "Session: [Topic]"
date: YYYY-MM-DD
llm: [LLM Name]
type: Session
tags: [session, topic]
---

# Session Summary

**Date**: YYYY-MM-DD  
**LLM**: [Name]  
**Focus**: [Main topic/question]  
**Key Insights**: [1-2 sentence summary]

---

## My Questions/Prompts

1. [First question]
2. [Second question]

## Key Insights from LLM

- [Insight 1]
- [Insight 2]

## Action Items Identified

- [ ] [Action 1]
- [ ] [Action 2]

## Related Notes

- [[Link to related project]]
- [[Link to related resource]]

---

## Full Conversation

[Paste full conversation here]
```

### Method 3: File Upload (If Available)
If you have conversation exports as files:
1. Place them in `Areas/Personal-Reflection/Assessments/Sessions/Raw/`
2. I can help you process and structure them

---

## Best Practices

### 1. Add Metadata
Always include:
- Date of conversation
- LLM used (ChatGPT, Claude, Gemini, etc.)
- Main topic/focus
- Tags for searchability

### 2. Extract Key Insights
Don't just archive—synthesize:
- What did you learn?
- What patterns emerged?
- What actions were suggested?
- What questions remain?

### 3. Link to Projects/Areas
Connect sessions to active work:
```markdown
## Related
- Project: [[Projects/Active/Personal-Growth/Emotional-Intelligence-Mastery]]
- Area: [[System/MOCs/Family]]
- Resource: [[Resources/Knowledge/Guides/Wife-Translator]]
```

### 4. Track Action Items
If the session suggested actions:
```markdown
## Actions from This Session
- [ ] Read "Hold Me Tight" (Chapter 3)
- [ ] Practice perception checking 3x this week
- [ ] Schedule couples therapy consultation
```

---

## How I Can Help

Once you import sessions, I can:

1. **Pattern Analysis**: Identify recurring themes across conversations
2. **Consolidation**: Merge insights from multiple sessions into MOCs
3. **Action Extraction**: Pull out all suggested actions into a master task list
4. **Progress Tracking**: Compare early vs. recent sessions to show growth
5. **Question Synthesis**: Identify unanswered questions that need follow-up

---

## Recommended Workflow

### For Each Import:

1. **Create the file** (I can do this for you)
2. **Paste the conversation**
3. **Add summary at top** (I can help)
4. **Tag appropriately**
5. **Extract action items** → move to `GTD-Tasks/`
6. **Link to related notes**

### After Multiple Imports:

1. **Create Session Index MOC**: `Areas/Personal-Reflection/Assessments/Sessions/README.md`
2. **Pattern Analysis**: I'll review all sessions and create `Session-Patterns.md`
3. **Consolidated Insights**: Create `Key-Learnings-MOC.md`

---

## Example Session Index (README.md)

```markdown
# Coaching Session Index

## 2025-11 Sessions

| Date | LLM | Topic | Key Insight | Status |
|------|-----|-------|-------------|--------|
| 2025-11-20 | LifeOS AI | Initial Assessment | EQ baseline 3-4/10, shame-withdrawal pattern | ✓ Processed |
| 2025-11-15 | ChatGPT | Marriage Conflict | Kitchen = trust signal | ⏳ Actions pending |
| 2025-11-10 | Claude | INTP Analysis | Fe blindspot is core issue | ✓ Integrated |

## By Theme

### Marriage/Relationship
- [2025-11-15_ChatGPT_Session.md](./2025-11-15_ChatGPT_Session.md)
- [2025-11-20_Initial_Assessment.md](../2025-11-20_Initial_Assessment.md)

### Emotional Intelligence
- [2025-11-12_Gemini_Session.md](./2025-11-12_Gemini_Session.md)
```

---

## Quick Start

**To import your first session:**

1. Tell me: "Import session from [date] with [LLM] about [topic]"
2. Paste the conversation
3. I'll create the structured file with metadata
4. I'll extract key insights and action items
5. I'll link it to relevant projects/areas

**Ready to import? Just paste the conversation and tell me:**
- Date (if you remember)
- Which LLM (ChatGPT, Claude, Gemini, etc.)
- Main topic

I'll handle the rest!
