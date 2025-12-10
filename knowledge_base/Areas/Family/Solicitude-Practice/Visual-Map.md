---
title: "Solicitude System Map"
type: Resource
status: Active
tags: [visualization, mermaid, solicitude]
up: [[00-Program-Overview]]
created: 2025-12-05
---

# 🗺️ The Architecture of Care

This map visualizes how the components of the **Engineering of Empathy** program interact to generate the virtue of Solicitude.

```mermaid
graph TD
    %% Core Nodes
    User((Austin))
    Wife((Wife))
    Virtue[Solicitude / Active Care]

    %% Modules
    M1[Module 1: Theology]
    M2[Module 2: Psychology]
    M3[Module 3: Habits]
    Log[Daily Log]

    %% Concepts
    OS[Original Solitude]
    ATTUNE[ATTUNE Framework]
    Anchors[Cognitive Anchors]

    %% Relationships
    User -->|Possesses| OS
    OS -->|Reframed as Asset| M1
    M1 -->|Provides Motivation| Virtue

    User -->|Learns| ATTUNE
    ATTUNE -->|Provides Skill| M2
    M2 -->|Enables Connection| Wife

    User -->|Executes| Anchors
    Anchors -->|Automates| M3
    M3 -->|Generates| Virtue

    Virtue -->|Directed Towards| Wife
    User -->|Tracks| Log
    Log -->|Feedback Loop| Virtue

    %% Styling
    classDef core fill:#f9f,stroke:#333,stroke-width:4px;
    classDef module fill:#bbf,stroke:#333,stroke-width:2px;
    classDef concept fill:#dfd,stroke:#333,stroke-width:2px;

    class User,Wife,Virtue core;
    class M1,M2,M3,Log module;
    class OS,ATTUNE,Anchors concept;
```

## 🔗 Key Connections
- **Original Solitude** is the *Input Source* (Your capacity for depth).
- **Solicitude** is the *Output Signal* (Directed attention).
- **Habits** are the *Transmission Lines* (Ensuring the signal reaches the receiver).
