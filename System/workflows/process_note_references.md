---
description: Extract and link important references when processing new notes
---

# Process Note References Workflow

Use this workflow when processing new notes (during intake or review) to identify and catalog important references.

## When to Use This Workflow

- When processing any new note that mentions authors, researchers, speakers, experts, books, movies, etc.
- During morning calibration when reviewing new notes
- During weekly review when processing accumulated notes
- Any time a note references a source that seems important to follow up on

## Workflow Steps

### 1. Scan the Note for References

Read through the note and identify mentions of:
- **Books** (titles or authors)
- **Movies, Documentaries, Shows** (titles or creators)
- **Researchers, Authors, Speakers** (names and their work)
- **Experts, Thought Leaders** (names and their domains)
- **Academic Papers or Articles** (titles or authors)
- **Podcasts or Podcast Episodes** (names/episodes)
- **Courses or Programs** (names or instructors)

### 2. Assess Importance

For each reference, determine if it's:
- **Critical**: Directly supports a Tier 1 or Life Project goal
- **High**: Aligns with Tier 2 goals or active areas of focus
- **Medium**: Related to general growth or interests
- **Low**: Tangentially mentioned, not worth cataloging

Only process items rated Medium or above.

### 3. Check for Duplicates

Before adding, search the existing `Resources/Lists/to_read_list.md` to see if the item is already listed.
- If it exists, create the link but don't duplicate the entry
- If it's new, proceed to step 4

### 4. Offer to Add to To Read/Watch List

For each new reference, ask the user:
> "I found a reference to **[ITEM]** by **[AUTHOR/CREATOR]** in this note. This seems [PRIORITY] priority because [REASON]. Would you like me to add it to your To Read/Watch list?"

Wait for user confirmation before proceeding.

### 5. Add to Appropriate List

Based on the type of reference, add it to the correct section:

**For Books/Articles** → Add to `Resources/Lists/to_read_list.md`
**For Movies/Shows/Videos** → Add to `Resources/Lists/favorite_movies_shows.md` (or create a new to_watch_list.md if needed)

Use this template format for `to_read_list.md`:

```markdown
### [Title or Topic]
**Source:** [Author/Creator]
**Category:** [Category 1, Category 2]
**Added:** [YYYY-MM-DD]
**Priority:** [Critical/High/Medium]
**Status:** Not Started

**Why:** [Brief explanation of why this is important, ideally linking to goals or projects]

**Key Topics:**
- [Topic 1]
- [Topic 2]

**Action After Reading:**
- [Specific action if known]
```

### 6. Create Bidirectional Links

In the **original note**, add a reference section at the bottom (if it doesn't exist):

```markdown
---

## References & Sources to Explore

- [[Resources/Lists/to_read_list#[Item Name]]] - [Brief reason why relevant]
```

In the **to_read_list.md entry**, add a backlink:

```markdown
**Referenced In:**
- [[Path/To/Original/Note|Note Title]] - [Context]
```

### 7. Create GTD Task if Needed

If the priority is **Critical** or **High**, offer to create a corresponding task in `GTD-Tasks/4-To-Read/` following the existing pattern:
- File: `GTD-Tasks/4-To-Read/read-[item-name].md`
- Link to the resource entry in `to_read_list.md`
- Add to appropriate project if applicable

### 8. Confirm Completion

Summarize what was added:
> "✓ Added [N] new references to your To Read/Watch list:
> - [Item 1] (Priority: [X])
> - [Item 2] (Priority: [Y])
> 
> Links have been created in both the original note and the resource list."

## Notes

- **Be selective**: Not every mention needs to be catalogued. Focus on sources that seem important for the user's goals.
- **Preserve context**: Always note WHY something is being added and how it relates to the user's life projects or goals.
- **Maintain consistency**: Use the existing formatting patterns in `to_read_list.md`.
- **Ask first**: Always confirm with the user before adding items—they may have already read it, may not be interested, or may have additional context.

## Integration Points

This workflow integrates with:
- `/morning_calibration` - Review new notes and process references
- `/weekly_review` - Batch process accumulated notes for references
- Daily note processing - Ad-hoc reference extraction as notes are created
