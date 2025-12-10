---
{title: Lifeos_Ai_Integration_Guide, type: System, up: '[[System]]'}
---
# LifeOS AI Starter Kit for Austin's LifeOS AI Integration Guide
**Purpose:** A starter kit for integrating AI into your daily LifeOS routines.
**Goal:** Use AI to augment your spiritual, relational, and executive functions, key prompts, and automation workflows.

---

## 🌅 MORNING KICKOFF ROUTINE

### **The Sacred Start** (Daily, 5-10 minutes)

**Prompt Chain:**
```
1. [Catholic Spiritual Grounding]
2. [Day Preview & Prioritization]
3. [Gentle Accountability Set]
```

#### Step 1: Spiritual Grounding (context.md + custom prompt)

**Prompt Name:** `morning_spiritual_kickoff`

**Template:**
```markdown
Today is [DATE - DAY OF WEEK].

**Liturgical Calendar:**
[Fetch from Catholic API or manual entry: Today's saint, readings, or feast]

**Morning Reflection:**
Based on Austin's current life situation (marriage crisis, unemployment, family needs), what ONE insight from today's Gospel reading or the saint of the day offers practical wisdom?

Keep it brief (2-3 sentences), non-preachy, and actionable.

**Prayer Intention:**
Suggest one specific prayer intention for today based on his Tier 1 goals.
```

**Example Output:**
> **St. Cecilia (Patroness of Musicians) - Nov 22**  
> Today's reading: "Martha, Martha, you are anxious about many things" (Luke 10:41). Like Martha, you're drowning in tasks—but Jesus calls you to presence, not productivity Olympics. One conversation with Natalie where you're fully present beats 10 "efficient" interactions.  
> **Prayer Intention:** Ask St. Joseph (model of quiet strength) for the grace to listen to Natalie without planning your response.

---

#### Step 2: Day Preview & Prioritization

**Prompt Name:** `day_preview_with_priorities`

**Input:** Your calendar + task list (from LifeOS)

**Processing:**
```markdown
Austin's Top 3 for Today:
1. [Most important task aligned with Tier 1 goals]
2. [Second priority]
3. [Third priority]

Time Blocks:
- Morning (9am-12pm): [Suggested focus]
- Afternoon (1pm-4pm): [Suggested focus]
- Evening (5pm-8pm): [Family time - protect this]

Relationship Check:
- When will you connect with Natalie today? (Suggest specific time for intentional conversation)
```

---

#### Step 3: Gentle Accountability Set

**Prompt Name:** `daemon_nudge_scheduler`

**Output:**
```markdown
I'll check in with you at:
- **11:30 AM** - "How's focus? Still on Priority #1?"
- **2:30 PM** - "Energy check. Time for a walk or prayer break?"
- **7:00 PM** - "Evening reflection ready. 5 minutes?"

Your word for today: [JOY / PRESENCE / FOCUS / COURAGE]
(One word to anchor your intention. Changes daily based on needs.)
```

---

## ⚡ PRODUCTIVITY NUDGES (Throughout Day)

### Nudge Template

**Format:**
> **[TIME] - Gentle Reminder**  
> [Observation based on activity]  
> [Suggestion]  
> [Encouragement]

**Examples:**

**11:30 AM - Mid-Morning Check**
> You've been deep in LifeOS documentation for 2 hours. Great focus.  
> Suggestion: Stand up, stretch, pray one Our Father.  
> Remember: You're building this system to serve your family, not escape them. ❤️

**2:30 PM - Afternoon Slump**
> Energy dip detected. This is normal.  
> Suggestion: 10-minute walk outside OR switch to a lighter task (email triage?).  
> Quote to carry: "The glory of God is man fully alive." —St. Irenaeus

**7:00 PM - Evening Transition**
> Work day is ending. Time to shift into husband/dad mode.  
> Suggestion: Close all work tabs. Ask Natalie: "What was the best part of your day?"  
> No fixing. Just listen.

---

## 💌 EMAIL MANAGEMENT SYSTEM

### Phase 1: Unsubscribe Blitz (One-Time Setup)

**Prompt Name:** `email_unsubscribe_candidates`

**Input:** Export list of senders from last 3 months

**Output:**
```markdown
Quick Wins (Unsubscribe immediately):
- [List of promotional emails, newsletters you never read]

Maybe Keep (Review):
- [Newsletters that occasionally have value - create digest instead]

VIPs (Whitelist):
- [Important personal/business contacts]
```

---

### Phase 2: Daily Digest System

**Prompt Name:** `email_daily_digest`

**Automation:** Run every morning at 8 AM

**Process:**
1. Scan inbox from past 24 hours
2. Categorize:
   - **Urgent/Personal** (Natalie, family, critical)
   - **Action Required** (bills, appointments, decisions)
   - **FYI/Newsletters** (aggregate into digest)
   - **Spam/Junk** (auto-archive)

**Output Format:**
```markdown
🔴 URGENT (Reply Today):
- [Sender]: [1-line summary] - [Suggested action]

🟡 ACTION NEEDED (This Week):
- [Task]: [Deadline] - [Context]

📰 FYI DIGEST (Read if time):
**Today's Themes:** [Common topics across newsletters]
- [Article 1 title]: Key takeaway in 1 sentence
- [Article 2 title]: Key takeaway in 1 sentence

📧 EMAIL DRAFTS READY:
I've drafted replies to 3 emails. Review & send? [Link to drafts]
```

---

## 💔 RELATIONSHIP PROCESSING SYSTEM

### **After-Argument Protocol**

**Prompt Name:** `process_marital_conflict`

**When to Use:** After any difficult conversation with Natalie

**Input Template:**
```markdown
What happened: [Brief description of the argument]
What was said (your words): [Key things you said]
What was said (her words): [Key things she said]
How you felt: [Your emotions during/after]
What you think she felt: [Attempt to name her emotions]
What triggered it: [Proximate cause]
```

**AI Processing (Using Gottman + Catholic framework):**

**Output:**
```markdown
🔍 ANALYSIS:
Four Horsemen Check:
- [ ] Criticism detected in your response? [Yes/No + example]
- [ ] Contempt (eye-rolling, sarcasm)? [Yes/No]
- [ ] Defensiveness? [Yes/No + where]
- [ ] Stonewalling (shutting down)? [Yes/No]

Her Four Horsemen:
- [Same check for Natalie's behaviors]

🎯 WHAT SHE WAS REALLY SAYING:
Beneath the words "[her quote]", she was likely expressing:
- [Unmet need]: She needs to feel [valued/heard/supported/etc.]
- [Fear]: She's afraid that [deeper fear]

💡 REPAIR ATTEMPT:
Script for next conversation (adapt to your voice):
"Natalie, I've been thinking about [specific moment]. I realize when I said [your words], you might have felt [her emotion]. That wasn't fair. What I should have said is [better version]. Can we talk about this?"

🙏 SPIRITUAL LENS:
Catholic marriage theology reminder:
[Brief quote from John Paul II's "Theology of the Body" or similar relevant teaching]

Your vocation isn't to win arguments. It's to lay down your life in love, one conversation at a time.

📖 RECOMMENDED READING:
From your TBR list: [Specific chapter from Gottman's "Seven Principles" that applies]
```

---

### **Weekly Marriage Check-In**

**Prompt Name:** `weekly_marriage_health_check`

**Frequency:** Every Sunday evening

**Input:**
- How many meaningful conversations did you have with Natalie this week? (>15 min, no distractions)
- How many times did you offer appreciation without being asked?
- How many times did you "turn toward" her bids for connection?

**AI Response:**
```markdown
This Week's Marriage Stats:
- Meaningful conversations: [Your count] (Goal: 5+)
- Unprompted appreciation: [Your count] (Goal: 7+, one per day)
- Turned toward: [Your count]

Grade: [A/B/C/D/F] + [Brief encouragement or correction]

Next Week's Focus:
[One specific behavior to improve, based on Gottman research]

Example: "This week, practice the 'I Feel' formula: 'I feel [emotion] when [situation] because [reason]. I need [request].'"
```

---

## 🌙 EVENING REFLECTION ROUTINE

### **The Daily Examen** (Catholic + Productivity)

**Prompt Name:** `evening_examen_reflection`

**When:** 7-8 PM, after family time

**Process:**

**AI Prompt:**
```markdown
Reflect on your day (5 minutes):

1. **Gratitude:** What are you grateful for today? (3 things)
   - [Item 1]
   - [Item 2]
   - [Item 3]

2. **Where did you feel God's presence?**
   - [Moment of grace, beauty, connection]

3. **Where did you feel most alive today?**
   - [When were you in "flow"?]

4. **Where did you fall short?**
   - [One specific failure or sin - no shame, just honesty]

5. **What needs repair tomorrow?**
   - [One relationship or task to address]

6. **Tomorrow's ONE THING:**
   - [The single most important thing to accomplish]
```

**AI Response:**
```markdown
Austin, based on your reflection:

**Celebrate:**
[Specific affirmation based on what went well]

**Forgive:**
[Gentle reframe of failure - "You're human. Tomorrow is new."]

**Prepare:**
To make tomorrow's ONE THING happen, you'll need to:
- [Practical step 1]
- [Practical step 2]

**Pray:**
[Suggested short prayer for the night - could be traditional Catholic or simple personal]

Example:
"Lord, thank you for [specific grace from today]. Forgive me for [specific shortcoming]. Help me tomorrow to [specific need]. Amen."

**Sleep well. Tomorrow, we try again.**
```

---

## 🔧 AUTOMATION SETUP

### Tools You'll Need
1. **Task Scheduler** (cron job or similar) for timed prompts
2. **Email API** (Gmail filters + Google Apps Script)
3. **Calendar Integration** (Google Calendar API)
4. **Optional:** Voice assistant integration (for always-on listening - future goal)

### Quick Wins to Implement First
1. ✅ **Morning Kickoff** - Manual for now (set phone alarm for 8 AM, run prompt)
2. ✅ **Email Digest** - Set up Gmail filters to auto-label, run digest prompt once daily
3. ✅ **Evening Examen** - Calendar reminder at 7 PM
4. ⏳ **Relationship Processing** - Use as-needed after conflicts
5. ⏳ **Productivity Nudges** - Manual for first week, then explore automation

---

## 📦 FABRIC PROMPTS TO CREATE

Some of these don't exist yet in your library. You'll need to create custom prompts:

### New Prompts Needed:
1. **`morning_spiritual_kickoff`** - Catholic + day planning hybrid
2. **`process_marital_conflict`** - Gottman + Catholic marriage theology
3. **`daemon_productivity_nudge`** - Gentle accountability check-ins
4. **`email_daily_digest`** - Aggregate and summarize inbox
5. **`evening_examen_reflection`** - Catholic daily examen + productivity review

Would you like me to generate the actual `system.md` files for these custom prompts next?

---

**Last Updated:** 2025-11-21  
**Status:** Draft v1.0 - Ready for User Feedback
