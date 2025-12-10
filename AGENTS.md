---
title: "AI Agent Guide"
type: Guide
status: Active
last_updated: 2024-07-25
tags: [guide, agents, development]
---

# AI Agent Guide

This document provides a comprehensive guide for AI agents working on the LifeOS project. It covers the project's overview, development commands, code style guidelines, testing instructions, and security considerations.

## Project Overview

LifeOS is a comprehensive, AI-enhanced system designed to serve as a second brain, life coach, and personal assistant. It's a private and personalized tool for navigating life with intention, with a special focus on integrating productivity with deep emotional and spiritual growth. The project is divided into three main components:

-   **`LifeOS/`**: A collection of markdown files organized according to the PARA method, where the user stores their notes, journal entries, project plans, and more.
-   **`lifeos-rag-api/`**: The backend of the system, powered by a FastAPI application. It uses a RAG (Retrieval-Augmented Generation) architecture to provide a powerful, context-aware AI that can interact with the user's personal knowledge base.
-   **`LifeOS-Web/`**: The frontend of the application, built with Next.js and React. It provides a clean and intuitive interface for interacting with the LifeOS system.

## Build and Test Commands

### Backend (`lifeos-rag-api/`)

-   **Build the Docker containers:**
    ```bash
    docker-compose build
    ```
-   **Start the backend services:**
    ```bash
    docker-compose up -d
    ```
-   **Stop the backend services:**
    ```bash
    docker-compose down
    ```

### Frontend (`LifeOS-Web/`)

-   **Install dependencies:**
    ```bash
    npm install
    ```
-   **Start the development server:**
    ```bash
    npm run dev
    ```
-   **Build the application for production:**
    ```bash
    npm run build
    ```

## Code Style Guidelines

Currently, there are no formal code style guidelines in place for this project. However, it is recommended to follow the standard conventions for Python and TypeScript/JavaScript.

## Testing Instructions

There are currently no automated tests in this project. All new features and bug fixes should be manually tested to ensure they are working correctly.

For frontend changes, it is recommended to use Playwright to write a verification script to test the changes in a headless browser. An example of a verification script can be found in the `AGENT_LOG.md` file.

## Security Considerations

-   **Secrets:** All secrets, such as API keys and database credentials, should be stored in a `.env` file in the `lifeos-rag-api` directory. A `.env.example` file is provided as a template.
-   **Crisis Language:** The `safety.py` module in the `lifeos-rag-api` service includes a function to detect crisis language in user input. This should be used to provide a disclaimer and a warning to the user when necessary.

## Commit Message Guidelines

Commit messages should follow the conventional commit format. Each commit message should consist of a header, a body, and a footer.

-   **Header:** The header is mandatory and should be a single line that contains a succinct description of the change. It should be no longer than 50 characters and should be written in the imperative mood.
-   **Body:** The body is optional and should be used to provide additional context about the change. It should be separated from the header by a blank line.
-   **Footer:** The footer is optional and should be used to reference any issues that the commit closes.

Example:

```
feat: Add AI analysis for risk audit

This commit introduces the AI analysis feature for the weekly risk audit
tool. It adds a new endpoint to the backend to handle the analysis of
risk audit data and connects the frontend to this endpoint.

Closes #123
```

## Current To-Do List

-   [ ] **Resolve Frontend Rendering Issue:** The `risk-audit` and `journal` pages in the `LifeOS-Web` application are currently throwing an "Internal Server Error" when rendered. This is preventing the Playwright verification script from running and needs to be resolved before the "AI Analysis" feature can be fully verified.
-   [ ] **Create `MASTER_SYSTEM_PROMPT.md`:** The `MASTER_PLAN.md` calls for a `MASTER_SYSTEM_PROMPT.md` to be created by merging `start.md` and `system-blueprint.md`. These files need to be located and the merge needs to be completed.
-   [ ] **Implement AI-Assisted Capture:** The `MASTER_PLAN.md` outlines a feature for "Intelligent Capture" that would allow the user to input natural language and have the AI suggest metadata and file it correctly in the GTD inbox.
