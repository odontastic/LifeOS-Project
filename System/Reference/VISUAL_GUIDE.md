---
{title: Visual_Guide, type: Note}
---
# LifeOS Visual Guide
**Quick Reference for System Structure and Workflows**

---

## System Architecture Overview

```mermaid
graph TB
    subgraph "GTD-Tasks (ACTIONS)"
        I[0-Inbox<br/>Capture Everything]
        NA[1-Next-Actions<br/>Ready to Execute]
        WF[2-Waiting-For<br/>Delegated/Blocked]
        SM[3-Someday-Maybe<br/>Future Possibilities]
        TR[4-To-Read<br/>Content to Consume]
        TT[5-To-Think-About<br/>Needs Contemplation]
        NP[6-Needs-Processing<br/>Raw Notes]
    end
    
    subgraph "PARA (KNOWLEDGE)"
        P[Projects<br/>Outcomes + Deadlines]
        A[Areas<br/>Ongoing Responsibilities]
        R[Resources<br/>Reference Material]
        AR[Archives<br/>Inactive]
    end
    
    I --> NA
    I --> WF
    I --> SM
    I --> TR
    I --> TT
    I --> NP
    
    NA -.metadata links.-> P
    NA -.metadata links.-> A
    WF -.metadata links.-> P
    SM -.metadata links.-> P
    
    P -.contains links.-> NA
    P -.contains links.-> WF
    A -.contains links.-> NA
    
    style I fill:#ff9999
    style NA fill:#99ff99
    style P fill:#9999ff
    style A fill:#ffff99
```

---

## Capture → Process Workflow

```mermaid
flowchart TD
    Start([Thought/Email/Idea]) --> Inbox[Capture to<br/>0-Inbox/]
    
    Inbox --> Q1{Actionable?}
    
    Q1 -->|Yes| Q2{Can do in<br/>2 minutes?}
    Q1 -->|No| Q3{What type?}
    
    Q2 -->|Yes| DoNow[Do It Now ✓]
    Q2 -->|No| Q4{Who does it?}
    
    Q4 -->|Me| NA[1-Next-Actions/]
    Q4 -->|Others| WF[2-Waiting-For/]
    Q4 -->|Not ready| SM[3-Someday-Maybe/]
    
    Q3 -->|Content| TR[4-To-Read/]
    Q3 -->|Thinking| TT[5-To-Think-About/]
    Q3 -->|Notes| NP[6-Needs-Processing/]
    Q3 -->|Reference| Res[Resources/]
    Q3 -->|Trash| Del[Delete]
    
    NA --> Meta[Add Metadata:<br/>context, energy,<br/>time, project]
    WF --> Meta
    TR --> Meta
    
    style Inbox fill:#ff9999
    style NA fill:#99ff99
    style DoNow fill:#99ff99
```

---

## Task Metadata Structure

```mermaid
graph LR
    Task[Task File] --> Status[Status<br/>Next-Action, Waiting, etc.]
    Task --> Project[Project Link<br/>What outcome?]
    Task --> Area[Area Link<br/>What responsibility?]
    Task --> Context[Context Tags<br/>@Computer, @Home]
    Task --> Energy[Energy Level<br/>High, Medium, Low]
    Task --> Time[Time Required<br/>5min to 2hr+]
    Task --> Priority[Priority<br/>Critical to Low]
    
    style Task fill:#ffff99
    style Project fill:#9999ff
    style Area fill:#99ff99
```

---

## How Projects and Tasks Connect

```mermaid
graph TB
    subgraph "Project (Knowledge Container)"
        P1["Projects/Active/<br/>College-Prep.md"]
        P1 --> Obj[Objective:<br/>Get son into college]
        P1 --> Miles[Milestones:<br/>FAFSA, Visits, Apps]
        P1 --> Links[Task Links:<br/>Points to GTD-Tasks/]
    end
    
    subgraph "Tasks (Actions)"
        T1["GTD-Tasks/1-Next-Actions/<br/>research-financial-aid.md"]
        T2["GTD-Tasks/1-Next-Actions/<br/>schedule-campus-visits.md"]
        T3["GTD-Tasks/2-Waiting-For/<br/>recommendation-letter.md"]
    end
    
    Links -.links to.-> T1
    Links -.links to.-> T2
    Links -.links to.-> T3
    
    T1 -.metadata<br/>points back.-> P1
    T2 -.metadata<br/>points back.-> P1
    T3 -.metadata<br/>points back.-> P1
    
    style P1 fill:#9999ff
    style T1 fill:#99ff99
    style T2 fill:#99ff99
    style T3 fill:#ffcc99
```

---

## Weekly Review Flow

```mermaid
flowchart TD
    Start([Sunday Evening]) --> Step1[Process Inbox to Zero]
    
    Step1 --> Step2[Review Waiting-For<br/>Chase if needed]
    
    Step2 --> Step3[Review All Projects<br/>Each has ≥1 Next Action?]
    
    Step3 --> Step4[Review All Areas<br/>Anything needs attention?]
    
    Step4 --> Step5[Check Calendar<br/>Next 2 weeks]
    
    Step5 --> Step6[Review Someday-Maybe<br/>Activate anything?]
    
    Step6 --> Step7[Relationship Check<br/>Presence with wife?]
    
    Step7 --> Step8[Set ONE THING<br/>for next week]
    
    Step8 --> Done([Ready for New Week])
    
    style Start fill:#ffff99
    style Done fill:#99ff99
```

---

## Daily ONE THING Practice

```mermaid
sequenceDiagram
    participant User
    participant AI as AI Assistant
    participant Tasks as GTD-Tasks/
    participant Journal as Daily Journal
    
    Note over User,Journal: 7:00 AM - Morning
    AI->>User: What's your ONE THING today?
    User->>AI: Practice presence at breakfast
    AI->>Tasks: Create/update in 1-Next-Actions/
    AI->>User: I'll check in at 6 PM
    
    Note over User,Journal: 6:00 PM - Evening
    AI->>User: Did you complete your ONE THING?
    User->>AI: Yes, asked about her day
    AI->>Journal: Create entry with reflection
    AI->>User: Celebrate! What did you learn?
```

---

## Context Filtering

```mermaid
graph TB
    All[All Next Actions] --> Q{Filter by...}
    
    Q -->|Context| C1[@Computer<br/>Research, writing]
    Q -->|Context| C2[@Home<br/>Cleaning, organizing]
    Q -->|Context| C3[@Calls<br/>Phone calls]
    Q -->|Context| C4[@Errands<br/>Outside tasks]
    
    Q -->|Energy| E1[High Energy<br/>Deep work]
    Q -->|Energy| E2[Medium Energy<br/>Admin work]
    Q -->|Energy| E3[Low Energy<br/>Quick wins]
    
    Q -->|Time| T1[5-15 min<br/>Quick tasks]
    Q -->|Time| T2[30-60 min<br/>Focused work]
    Q -->|Time| T3[2+ hours<br/>Deep projects]
    
    style All fill:#ffff99
    style C1 fill:#99ccff
    style E1 fill:#ffcc99
    style T1 fill:#cc99ff
```

---

## Information Flow

```mermaid
flowchart LR
    subgraph "Capture"
        Voice[Voice Notes]
        Email[Emails]
        Thoughts[Random Thoughts]
        Web[Web Clips]
    end
    
    subgraph "Process"
        Inbox[0-Inbox/]
        Decision{Clarify}
    end
    
    subgraph "Organize"
        GTD[GTD-Tasks/<br/>various folders]
        PARA[PARA<br/>Projects/Areas/Resources]
    end
    
    subgraph "Execute"
        Context[Filter by Context]
        Do[Take Action]
    end
    
    Voice --> Inbox
    Email --> Inbox
    Thoughts --> Inbox
    Web --> Inbox
    
    Inbox --> Decision
    Decision --> GTD
    Decision --> PARA
    
    GTD --> Context
    Context --> Do
    
    style Inbox fill:#ff9999
    style GTD fill:#99ff99
    style Do fill:#9999ff
```

---

## Zettelkasten Lifecycle

```mermaid
flowchart TD
    Fleeting[Resources/Zettelkasten/<br/>Fleeting/<br/>Quick capture] 
    
    Fleeting --> Process{Process<br/>Weekly}
    
    Process -->|From source| Lit[Literature/<br/>Notes from books/articles]
    Process -->|Original thought| Perm[Permanent/<br/>Refined concepts]
    Process -->|Not valuable| Trash[Delete]
    
    Lit --> Connect{Add<br/>Connections}
    Perm --> Connect
    
    Connect --> MOC[MOCs/<br/>Maps of Content<br/>Index notes]
    
    Connect --> Link[Link to other<br/>Permanent notes]
    
    style Fleeting fill:#ffff99
    style Perm fill:#99ff99
    style MOC fill:#9999ff
```

---

## Priority Integration

```mermaid
graph TB
    subgraph "Value Level"
        Faith[Faith<br/>Catholic values]
        Family[Family<br/>Wife, Sons]
    end
    
    subgraph "Area Level"
        A1[Areas/Faith/]
        A2[Areas/Family/]
    end
    
    subgraph "Project Level"
        P1[Projects/Active/<br/>Spiritual-Growth/]
        P2[Projects/Active/<br/>Family-Projects/]
    end
    
    subgraph "Task Level"
        T1[GTD-Tasks/1-Next-Actions/<br/>morning-prayer.md]
        T2[GTD-Tasks/1-Next-Actions/<br/>evening-presence-wife.md]
    end
    
    Faith -.informs.-> A1
    Family -.informs.-> A2
    
    A1 -.guides.-> P1
    A2 -.guides.-> P2
    
    P1 -.generates.-> T1
    P2 -.generates.-> T2
    
    T1 -.supports.-> P1
    T2 -.supports.-> P2
    
    style Faith fill:#ffcccc
    style Family fill:#ffcccc
    style T1 fill:#99ff99
    style T2 fill:#99ff99
```

---

## Quick Reference: When to Use What

| Situation | Destination | Why |
|-----------|-------------|-----|
| Random thought during day | `GTD-Tasks/0-Inbox/` | Capture first, clarify later |
| Clear next action identified | `GTD-Tasks/1-Next-Actions/` | Ready to execute |
| Waiting on someone | `GTD-Tasks/2-Waiting-For/` | Track delegation |
| Interesting but not now | `GTD-Tasks/3-Someday-Maybe/` | Future review |
| Book to read | `GTD-Tasks/4-To-Read/` | Content queue |
| Philosophical question | `GTD-Tasks/5-To-Think-About/` | Contemplation needed |
| Raw meeting notes | `GTD-Tasks/6-Needs-Processing/` | Needs elaboration |
| Multi-step outcome | `Projects/Active/` | Knowledge container |
| Ongoing responsibility | `Areas/` | Maintenance standard |
| Reference material | `Resources/` | Future lookup |
| Daily reflection | `Areas/Personal-Reflection/Daily/` | Journaling home |

---

**Remember**: PARA organizes KNOWLEDGE. GTD-Tasks organize ACTIONS.
