# LifeOS 2.0 - Coaching Flows API Design

This document outlines the proposed API structure for implementing multi-step, interactive "Coaching Flows" in the LifeOS 2.0 system.

## 1. Core Concepts

**Coaching Flow:** A predefined, multi-step interaction designed to guide the user through a specific therapeutic process (e.g., a daily check-in, debriefing a stressful event).

**Flow State:** A server-side object that maintains the user's progress through a flow, including the current step, context, and any collected information.

## 2. Proposed API Endpoints

### 2.1. Start a New Flow

-   **Endpoint:** `POST /api/flows/start`
-   **Purpose:** Initializes a new coaching flow for a user.
-   **Request Body:**
    ```json
    {
        "flow_type": "daily_check_in" // or "debrief_trigger", etc.
    }
    ```
-   **Response Body:**
    ```json
    {
        "flow_id": "unique_flow_id_123",
        "current_step": "step_1_greeting",
        "message": "Welcome to your daily check-in. How are you feeling right now?"
    }
    ```

### 2.2. Advance a Flow

-   **Endpoint:** `POST /api/flows/advance`
-   **Purpose:** Submits a user's response and advances the flow to the next step.
-   **Request Body:**
    ```json
    {
        "flow_id": "unique_flow_id_123",
        "current_step": "step_1_greeting",
        "response": "I'm feeling a bit anxious today."
    }
    ```
-   **Response Body (Example: Moving to the next step):**
    ```json
    {
        "flow_id": "unique_flow_id_123",
        "current_step": "step_2_explore_emotion",
        "message": "I understand you're feeling anxious. Can you tell me more about what's on your mind?"
    }
    ```
-   **Response Body (Example: Flow completion):**
    ```json
    {
        "flow_id": "unique_flow_id_123",
        "current_step": "step_final_summary",
        "message": "Thank you for sharing. It's important to acknowledge these feelings. Remember to be kind to yourself today.",
        "is_complete": true
    }
    ```

## 3. Data Structures

### 3.1. Flow State Object (Server-Side)

This object would be stored in memory or a database on the server, keyed by `flow_id`.

```json
{
    "flow_id": "unique_flow_id_123",
    "user_id": "user_abc",
    "flow_type": "daily_check_in",
    "current_step": "step_2_explore_emotion",
    "context": {
        "emotion": "anxious",
        "log": [
            { "step": "step_1_greeting", "response": "I'm feeling a bit anxious today." }
        ]
    },
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:01:00Z"
}
```

## 4. Example Flow: "Daily Check-in"

-   **Step 1: Greeting**
    -   **System:** "Welcome to your daily check-in. How are you feeling right now?"
    -   **User:** (Provides emotion)
-   **Step 2: Explore Emotion**
    -   **System:** "I understand you're feeling [emotion]. Can you tell me more about what's on your mind?"
    -   **User:** (Provides context)
-   **Step 3: Acknowledge and Reframe**
    -   **System:** (Retrieves a relevant CBT technique from the `ResourceIndex`) "It's common to feel that way when [context]. A technique that might help is Cognitive Restructuring. Have you heard of it?"
    -   **User:** (Responds)
-   **Step 4: Summary and Conclusion**
    -   **System:** "Thank you for sharing. Remember to be kind to yourself. I've logged this check-in for you."

This API design provides a clear and scalable structure for building interactive and therapeutic coaching flows, forming a strong foundation for the next stage of development.
