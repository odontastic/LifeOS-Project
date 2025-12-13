description: v1.0 LifeOS **developer-ready System Architecture & Specification Document**. for **agentic coding AIs** (like Claude Engineer, Cursor, Aider, or Devin), with a balance between technical rigor and philosophical alignment — ensuring the resulting system remains *human-centered*.

Everything within this spec is modular, local-first, and philosophically consistent with your LifeOS vision: **Virtue → Connection → Clarity → Embodiment**.
created: 12-12-13
---
***

# **LifeOS Technical Specification Document (v1.0)**
*For Agentic AI Developers & Human Architects*
**Core Directive:** Build technologies that help humans flourish, not fragment.

***

## 1. System Overview

**Purpose:**
LifeOS is a local-first, human-centered Life Management Environment that unifies **emotion, cognition, relationships, and knowledge** into one reflective architecture.

**Primary Modules:**
1. **Inner Palette** – Emotion & somatic state tracking
2. **Calm Compass** – Regulation and grounding engine
3. **Connection Engine** – Relationship recall and empathy prosthesis
4. **Prism Clarity Studio** – Reflective logic, decision framing, bias detection
5. **Engine Room** – GTD / PARA / Zettelkasten task & knowledge integration
6. **Core AI Layer** – Contextual synthesis and personal insight generation

Each module exposes consistent API endpoints and event streams that interact via a common **EmotionContextBus**, ensuring emotional state feeds awareness across all modules.

***

## 2. Global Architecture & Principles

### 2.1 System Type
**Local-First Personal OS**
- Backend: Python (FastAPI) or Go (fiber/gRPC)
- Frontend: React + Tailwind + ShadcnUI
- Database: SQLite (encryption optional)
- Optional graph layer: Neo4j-lite (for relational insights)

### 2.2 Data Philosophy
- **All emotional data belongs to the user.**
- **Local storage by default.**
- **Interoperable through JSON-LD and Markdown.**
- AI agents run inside user’s environment, not the cloud.

### 2.3 Design Contract with Agentic AIs
When coding modules autonomously, the AI must:
1. Maintain **privacy and bounded autonomy** — no external calls for personal data.
2. Follow **module boundaries** — no cross-module mutation without event bus trigger.
3. Write **transparent logs** for interpretability.
4. Optimize for **frictionless use, emotional safety, and UI minimalism**.
5. Anchor output logic on the **Virtue–Connection–Clarity** triad (core design constraint).

***

## 3. Data Model: Master Schema Relationships

### 3.1 Entity Overview
The system revolves around five primary entities:

| Entity | Purpose | Primary Connections |
|---------|----------|---------------------|
| **EmotionEntry** | Captures emotional state data. | ContextTags, SomaticMarkers, ActionPrompts |
| **ContactProfile** | Represents a person or relationship. | EmotionEntry, InteractionNote, LoopStatus |
| **TaskItem** | Represents task/commitment. | LinkedEmotionEntries, Zettels, Resources |
| **KnowledgeNode** | Zettelkasten/Notes integration. | EmotionEntry, TagGraph, RelatedDecisions |
| **SystemInsight** | AI-generated reflection or recommendation. | Any entity as context anchor |

All entities share standard fields:
`id`, `created_at`, `updated_at`, `confidence_score`, `source_module`.

***

## 4. Detailed Schemas (Pydantic / JSON Schema Hybrid)

### 4.1 EmotionEntry
```python
class EmotionEntry(BaseModel):
    id: UUID
    timestamp: datetime
    primary_emotion: str  # 'anger', 'joy', etc.
    secondary_emotions: Optional[List[str]]
    valence: int  # 1–10
    arousal: int  # 1–10
    intensity: int  # composite metric
    somatic_markers: Optional[List[str]]  # e.g. 'tight_chest', 'warm_face'
    context_tags: Optional[List[str]]  # e.g. ['family','coding']
    notes: Optional[str]
    linked_contact_id: Optional[UUID]
    linked_task_id: Optional[UUID]
    action_prompt: Optional[str]  # AI-generated suggestion
    processed: bool = False
```

***

### 4.2 ContactProfile (Connection Engine)
```python
class ContactProfile(BaseModel):
    id: UUID
    name: str
    relationship_type: str  # spouse, friend, child
    importance_level: int  # 1–5
    last_interaction: Optional[datetime]
    open_loops: Optional[List[str]]  # e.g. ['tax stress','hip pain']
    sentiment_summary: Optional[str]
    next_follow_up: Optional[datetime]
    context_history: Optional[List[UUID]]  # linked EmotionEntry IDs
```

***

### 4.3 TaskItem
```python
class TaskItem(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    project_id: Optional[UUID]
    context_tags: Optional[List[str]]
    status: str  # 'open','in_progress','done'
    priority: int
    due_date: Optional[datetime]
    linked_emotion_ids: Optional[List[UUID]]
    linked_contact_ids: Optional[List[UUID]]
    energy_requirement: str  # 'low','medium','high'
```

***

### 4.4 KnowledgeNode (Zettelkasten / PARA)
```python
class KnowledgeNode(BaseModel):
    id: UUID
    title: str
    content: str
    tags: List[str]
    links: Optional[List[UUID]]  # bidirectional connections
    para_category: str  # project/area/resource/archive
    emotion_links: Optional[List[UUID]]
    last_reviewed: Optional[datetime]
```

***

### 4.5 SystemInsight (AI Layer)
```python
class SystemInsight(BaseModel):
    id: UUID
    insight_type: str  # 'pattern','recommendation','summary'
    generated_from: List[UUID]  # source objects
    model_version: str
    confidence: float
    message: str
    action_recommendations: Optional[List[str]]
```

***

## 5. Data Contracts & Inter-Module Event Bus

Each module communicates asynchronously through an **Internal Event Bus (EmotionContextBus)**.

### Event Payload Example

```json
{
  "event_type": "emotion_logged",
  "source_module": "inner_palette",
  "payload": {
    "emotion_id": "uuid-123",
    "primary_emotion": "anger",
    "valence": 2,
    "arousal": 8,
    "context_tags": ["family"]
  }
}
```

Downstream modules subscribe based on event type:

| Subscriber Module | Event Type | Reaction |
|--------------------|------------|----------|
| **Calm Compass** | emotion_logged | Evaluate regulation suggestion |
| **Connection Engine** | emotion_logged (with contact tag) | Update relationship dashboard |
| **Prism Clarity Studio** | emotion_logged | Queue reflection or bias analysis |
| **Engine Room** | emotion_logged | Update task filters (energy-level view) |

This ensures cross-domain emotional awareness.

***

## 6. Processing Workflow Overview

### 6.1 Inner Palette → Calm Compass → Insight Loop

1. User logs emotion via Inner Palette (fast capture).
2. The system calculates **valence-arousal composite score** and **performs context lookup.**
3. Based on emotional intensity and context, the **Calm Compass Algorithm** triggers the most relevant intervention type.
4. Once the user interacts (breathing, grounding, journaling), the system logs completion and AI generates a **SystemInsight** summarizing the learning pattern.
5. Insights sync with Connection Engine (if relational context) or Engine Room (if task-related) to suggest preventive or empathic actions.

***

## 7. Inner Palette → Calm Compass Algorithm

### 7.1 High-Level Logic Description

The feedback algorithm uses **dual-layer reasoning**:
- **Layer 1 (Reactive):** Provide immediate grounding or care protocol based on intensity/arousal.
- **Layer 2 (Reflective):** Suggest deeper insight or journaling once physiological state stabilizes.

### 7.2 Algorithm Flow in Pseudocode

```pseudocode
function process_emotion_entry(entry: EmotionEntry):

    # NORMALIZE INPUT
    V = entry.valence
    A = entry.arousal
    intensity = entry.intensity or average(V, A)

    context = get_context_tags(entry)

    # CLASSIFY STATE
    if A >= 8 and V <= 3:
        state = "High Stress"
    elif A <= 3 and V <= 3:
        state = "Low Mood"
    elif A >= 7 and V >= 7:
        state = "Excitement"
    else:
        state = "Stable"

    # ROUTE TO CALM COMPASS
    if state == "High Stress":
        recommendation = CalmCompassProtocol("grounding")
        message = "Take 3 slow breaths, focus on body sensations."

    elif state == "Low Mood":
        recommendation = CalmCompassProtocol("activation")
        message = "Try a small energizing task or call a friend."

    elif state == "Excitement":
        recommendation = CalmCompassProtocol("reflection")
        message = "Channel this into a creative task."

    else:
        recommendation = CalmCompassProtocol("maintain")
        message = "Log gratitude or journal insights."

    # Log feedback
    insight = SystemInsight(
        insight_type="pattern",
        generated_from=[entry.id],
        confidence=0.9,
        message=message,
        action_recommendations=[recommendation]
    )

    save_to_db(insight)

    # Optionally notify other modules
    EmotionContextBus.emit("calm_compass_action", {
        "state": state,
        "emotion_id": entry.id,
        "recommendation": recommendation
    })

    return insight
```

### 7.3 Feedback Reinforcement Learning
Over time, the system records which actions produced positive outcomes (self-rated calmness or follow-up valence improvement), adjusting probability weights for recommendations.

```pseudocode
on user_feedback_received(insight_id, rating):
    update_model_weights(insight_id, rating)
    retrain local reinforcement bandit
```

***

## 8. AI-Enhanced Insights: Next-Generation Capabilities

### 8.1 Contextual Reflection (Local LLM)
- Uses local LLM (Llama3 / Mistral) via **Ollama** to analyze notes + emotion logs.
- Generates **digest reports** summarizing weekly states:
  - Emotion trends
  - Recurring relational patterns
  - Bias language frequency
  - Personalized coping strategies

### 8.2 Latent Semantic Graph (Neo4j-lite)
- Emotions, contacts, and notes connected into a **relational knowledge graph**.
- Enables queries like:
  “When I feel anxious during work, which task tags or people are most correlated?”

Algorithm concept:
```pseudocode
MATCH (e:EmotionEntry)-[:TAGGED_WITH]->(t:ContextTag)
RETURN t, COUNT(e) ORDER BY COUNT(e) DESC
```

### 8.3 Insight Synthesis
AI agents synthesize correlations into clear, compassionate language:
> “Most stress occurs around ‘Work’ and ‘Evenings’. Consider scheduling light activity after 5 PM.”

***

## 9. AI Safety & Constraint Layer

**Guardrails:**
- Agents must use only *predefined schema fields.* No dynamic schema morphing.
- Emotional suggestions must reference **validated CBT/ACT** techniques from whitelisted library.
- No self-writing of goal-setting prompts without explicit user approval.
- Limit external API exposure strictly to: calendar / local sensors (optional).

***

## 10. UI Interaction Protocols

### 10.1 Emotion Capture Shortcuts
```yaml
Shortcut: CTRL + E
trigger: open("InnerPaletteModal")
```

### 10.2 Calm Compass UI Config
```json
{
  "state": "High Stress",
  "display_mode": "focus",
  "buttons": [
    {"label": "Breathe", "path": "/calm/breath"},
    {"label": "Connect", "path": "/calm/connect"},
    {"label": "Reflect Later", "path": "/calm/defer"}
  ],
  "theme_color": "#6DA9E4"
}
```

***

## 11. Module Interfaces Summary

| Module | Primary API Endpoints | Subscribed Events | Published Events |
|---------|----------------------|-------------------|------------------|
| Inner Palette | `/emotion/log`, `/emotion/retrieve`, `/emotion/analyze` | — | `emotion_logged` |
| Calm Compass | `/calm/recommend`, `/calm/feedback` | `emotion_logged` | `calm_compass_action` |
| Connection Engine | `/relation/log`, `/relation/prompts` | `emotion_logged`, `calm_compass_action` | `contact_updated` |
| Prism Clarity Studio | `/reflection/analyze`, `/bias/detect` | `emotion_logged` | `insight_created` |
| Engine Room | `/task/sync`, `/para/update` | `emotion_logged`, `insight_created` | `task_state_changed` |
| AI Insight Layer | `/insight/generate`, `/insight/train` | all | `insight_summary_generated` |

***

## 12. Security, Privacy, and Scaling

| Concern | Implementation |
|----------|----------------|
| **Data privacy** | SQLite local store + optional AES encryption. |
| **Syncing** | Encrypted file export/import, no cloud dependency. |
| **AI sandboxing** | Local inference only, deterministic outputs. |
| **Fail-safe** | If AI models unavailable, fallback to static CBT-guided content. |

***

## 13. Meta-Development Guardrails for Agents

1. Each AI coding unit (e.g., Cursor agent) builds **only one module per session.**
2. Cross-module links use event bus contracts only.
3. All code must pass local integrity audits (`lifos lint --contract-check`).
4. LLM agents must be given schema context before generating code:
   ```
   You are bound to LifeOS v1.0 spec.
   Maintain schema consistency and do not introduce new data fields.
   Respect emotion safety and privacy rule #3.
   ```

***

## 14. Summary:
### The Human-to-System Feedback Loop

**1. Awareness** – Emotion captured through Inner Palette.
**2. Regulation** – Calm Compass provides immediate grounding.
**3. Reflection** – Prism Clarity reframes meaning and intent.
**4. Integration** – Connection Engine and Engine Room align relationships and tasks.
**5. Insight Generation** – Local AI synthesizes learnings into clarity and foresight.

LifeOS learns from patterns, recommends compassionate adjustments, and helps the user embody wisdom daily — all without leaving their local system.

***

## Other document for coding agents to directly import during build execution:

**Flow Sequence Diagram (PlantUML-style)** and **JSON schema registry index**

***
