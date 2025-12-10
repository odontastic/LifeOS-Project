---
{title: Automation_Setup_Guide, type: System, up: '[[System/Documentation]]'}
---
# 🤖 LifeOS AI Automation Setup Guide

This guide helps you wire your LifeOS LifeOS AI into your actual digital life using Gmail Filters and Google Calendar.

---

## 📧 PART 1: EMAIL TRIAGE (Gmail)

**Goal:** Auto-label emails so your `email_daily_digest` prompt knows what to ignore and what to highlight.

### Step 1: Create Labels
Create these 3 labels in Gmail (nested under a parent label `LifeOS AI` if you like):
1.  `@LifeOS AI/Urgent` (Red color)
2.  `@LifeOS AI/Newsletters` (Blue color)
3.  `@LifeOS AI/Receipts` (Gray color)

### Step 2: Create Filters
Go to **Settings > Filters and Blocked Addresses > Create a new filter**.

**Filter A: The VIPs (Urgent)**
*   **From:** `natalie@example.com` OR `school@example.com` OR `bank@example.com` (Add your key contacts)
*   **Action:** Apply label `@LifeOS AI/Urgent`, Star it, "Never send to Spam".

**Filter B: The Noise (Newsletters)**
*   **Has the words:** `unsubscribe` OR `view in browser`
*   **From:** `-(natalie@example.com)` (Exclude VIPs to be safe)
*   **Action:** Apply label `@LifeOS AI/Newsletters`, Skip Inbox (Archive it).
    *   *Note:* This is scary at first! But remember, your AI Digest will read these for you.

**Filter C: The Paper Trail (Receipts)**
*   **Subject:** `receipt` OR `order confirmation` OR `invoice`
*   **Action:** Apply label `@LifeOS AI/Receipts`, Skip Inbox.

### Step 3: The Workflow
1.  **Daily:** Open your `@LifeOS AI/Urgent` label first. Handle these.
2.  **Daily:** Select all unread emails in `@LifeOS AI/Newsletters`.
3.  **Action:** Copy the text (or use a tool to export) -> Run `email_daily_digest` prompt.
4.  **Result:** Read the 1-page summary. Ignore the rest.

---

## 📅 PART 2: CALENDAR REMINDERS (Google Calendar)

**Goal:** Trigger your "Human" brain to run the "AI" prompts at the right times.

### Event 1: Morning Kickoff
*   **Time:** 8:00 AM (Daily)
*   **Title:** 🌅 LifeOS AI Kickoff
*   **Description:**
    ```
    1. Open LifeOS.
    2. Run prompt: morning_spiritual_kickoff
    3. Review output & pray.
    ```
*   **Notification:** 10 minutes before.

### Event 2: The Mid-Day Nudge
*   **Time:** 1:30 PM (Daily)
*   **Title:** ⚡ Energy Check
*   **Description:**
    ```
    Run prompt: daemon_productivity_nudge
    Input: "Feeling [Low/Med/High], Working on [Task]"
    ```

### Event 3: Evening Examen
*   **Time:** 8:30 PM (Daily)
*   **Title:** 🌙 Daily Examen
*   **Description:**
    ```
    1. Stop all screens.
    2. Run prompt: evening_examen_reflection
    3. Input: Highs/Lows of the day.
    4. Sleep.
    ```

---

## 🧪 PART 3: TESTING WEEK (The "Beta" Phase)

Don't try to be perfect. Just try to be consistent for 7 days.

**Day 1-3: Manual Mode**
- [ ] Manually copy/paste email text into the prompt.
- [ ] Manually run the morning/evening prompts.
- [ ] **Goal:** Tweak the `context.md` if the AI sounds "off" or too preachy.

**Day 4-7: Refinement**
- [ ] Did the email digest miss something important? (Adjust Gmail filters).
- [ ] Is the morning prompt too long? (Edit `system.md` to say "Be briefer").
- [ ] **Goal:** Trust the system enough to actually archive newsletters without reading them.

---

## 🛠️ ADVANCED: SCRIPTING (Future Step)
Once you are comfortable, we can write a Python script to:
1.  Connect to Gmail API.
2.  Fetch `@LifeOS AI/Newsletters`.
3.  Send to OpenAI/Claude with the prompt.
4.  Email you the summary automatically every morning.

*Let's stick to Manual Mode for Week 1 to ensure quality control.*
