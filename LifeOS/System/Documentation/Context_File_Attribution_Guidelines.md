---
{title: Context_File_Attribution_Guidelines, type: System, up: '[[System/Documentation]]'}
---
# Context File Attribution Guidelines

## The Problem
When building AI context files, it's easy to accidentally merge characteristics from multiple people (spouses, family members, colleagues) into a single profile, especially when source documents describe them.

## What Happened
In Austin's `context.md`, biographical details from Natalie (his wife) were incorrectly attributed to him:
- ❌ Vietnamese-American background (Natalie's)
- ❌ Surgeon career with 3 doctorates (Natalie's)
- ❌ 49+ countries traveled (Natalie's achievements)
- ❌ Income ~$500K/year (Natalie's)
- ❌ Real estate portfolio management (Natalie's)

## Prevention Strategy

### 1. **Clear File Ownership Declaration**
Every context file should start with:
```markdown
> **IMPORTANT:** This context file describes [PERSON NAME], not [other people].
> For [other person's] details, see [filename].
```

### 2. **Separate Files for Each Person**
- `context.md` → Austin only
- `natalies_wisdom.md` → Natalie only (already exists)
- Never mix biographical details

### 3. **Use Relationship Sections Carefully**
When describing family members in someone's context:
- ✅ "**Spouse:** Natalie - Surgeon, 3 doctorates" (in her section)
- ❌ "Vietnamese-American background" (without specifying it's hers)

### 4. **Third-Person References**
When in doubt, use explicit attribution:
- ✅ "Natalie has traveled to 49+ countries"
- ✅ "The family owns 8 properties (managed by Natalie)"
- ❌ "Owns 8 properties" (ambiguous whose)

### 5. **Regular Audits**
Before finalizing any context file, ask:
- "Is every statement in this file actually about [FILE OWNER]?"
- "Are there details that belong to someone else?"

## How to Fix When It Happens
1. Search for first-person statements that don't match the file owner
2. Check for professional/biographical details that belong to someone else
3. Move misattributed details to the correct section or file
4. Add explicit subject attribution ("Natalie...", "Austin...")
5. Update version number and changelog

## Applied to Austin's Context
**Fixed sections:**
- ✅ Age corrected: ~58 (not ~44)
- ✅ Living situation: "Dependent on Natalie's income" (not "income ~$500K")
- ✅ Travel: "Natalie loves extensive global travel; Austin participates" (not "world traveler")
- ✅ Real estate: "Family portfolio (managed primarily by Natalie)"
- ✅ Added warning at top directing to `natalies_wisdom.md` for her details

---

**Lesson:** When multiple people's information exists in the knowledge base, ruthlessly separate it by file ownership and use explicit attribution for any cross-references.
