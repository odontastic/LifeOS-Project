---
title: "Event-Driven Testing Protocol"
type: "Documentation"
status: "Draft"
created: "2025-12-13"
last_updated: "2025-12-13"
tags: ["testing", "event-driven", "ci", "EmotionContextBus", "protocol"]
---

# Event-Driven Testing Protocol

This protocol simulates cross-module event flow for CI validation, ensuring modules interact correctly via the EmotionContextBus.

## Test Event Sequence (Example: Emotion Logged → Calm Compass → Insight)

**Trigger:** `POST /emotion/log` with sample `EmotionEntry` (high arousal, low valence).

**Expect:** Bus emits `emotion_logged` event.

**Calm Compass:** Receives event, classifies state, displays grounding protocol, emits `calm_compass_action`.

**Prism Clarity Studio:** Receives `emotion_logged`, queues bias detection, emits `insight_created`.

**Connection Engine:** If contact tag present, updates relationship dashboard, emits `contact_updated`.

**Engine Room:** Filters tasks by energy requirement, emits `task_state_changed`.

**AI Insight Layer:** Aggregates data, generates digest, emits `insight_summary_generated`.

## CI Validation Script (Pseudocode)

```python
function run_event_flow_test():
    # Step 1: Log emotion
    emotion_entry = create_sample_emotion_entry(valence=2, arousal=8, context_tags=["family"])
    response = POST /emotion/log emotion_entry

    # Step 2: Validate event bus
    assert event_emitted("emotion_logged", emotion_entry.id)

    # Step 3: Calm Compass response
    assert module_receives("Calm Compass", "emotion_logged")
    assert UI_shows("grounding", "Breathe/Connect/Reflect")
    assert event_emitted("calm_compass_action", emotion_entry.id)

    # Step 4: Prism Clarity response
    assert module_receives("Prism Clarity Studio", "emotion_logged")
    assert event_emitted("insight_created", emotion_entry.id)

    # Step 5: Connection Engine response
    assert module_receives("Connection Engine", "emotion_logged")
    assert dashboard_updated("family", "open_loop: tax_stress")

    # Step 6: Engine Room response
    assert module_receives("Engine Room", "emotion_logged")
    assert task_filter_shows("low-energy")

    # Step 7: AI Insight Layer response
    assert module_receives("AI Insight Layer", "insight_created")
    assert digest_generated("family stress ↑ this week")

    log("All event-driven flows validated.")
```
Agents should run this test on every build to ensure cross-module consistency and correct event propagation.
