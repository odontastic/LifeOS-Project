# LifeOS 2.0 Therapeutic Schema

This document outlines the therapeutic schema for the LifeOS 2.0 RAG API.

## Nodes

- **User**: The individual authoring the journal entries.
- **JournalEntry**: Represents a single journal entry.
- **Emotion**: A specific emotion mentioned or inferred.
- **Belief**: A core belief, assumption, or thought pattern.
- **Trigger**: An event, situation, or stimulus that causes a reaction.
- **CopingMechanism**: An action or thought process used to manage difficult emotions.
- **Goal**: A personal or professional goal.
- **Episode**: A significant life event or period (e.g., "Grad School," "First Job").
- **Pattern**: A recurring theme or pattern of behavior/thought.
- **SessionSummary**: A summary of a user's interaction with the system.

## Relationships

- **AUTHORED_BY**: `(JournalEntry)-[:AUTHORED_BY]->(User)`
- **RELATES_TO**: Connects various nodes that are related.
- **TRIGGERED_BY**: `(Emotion)-[:TRIGGERED_BY]->(Trigger)`
- **PRACTICED**: `(User)-[:PRACTICED]->(CopingMechanism)`
- **PART_OF**: `(JournalEntry)-[:PART_OF]->(Episode)`
- **MENTIONS**: `(JournalEntry)-[:MENTIONS]->(Belief)`
- **SUMMARIZES**: `(SessionSummary)-[:SUMMARIZES]->(JournalEntry)`

## Metadata (Properties on Nodes/Edges)

- **created_at**: Timestamp of the node's creation.
- **life_domain**: The area of life the node relates to (e.g., "Work," "Relationships").
- **life_stage**: The life stage associated with the node (e.g., "College," "Adulthood").
- **stability**: Whether the node is "Stable" or "Transient."
- **confidence**: The confidence score of the extraction (0.0 to 1.0).
