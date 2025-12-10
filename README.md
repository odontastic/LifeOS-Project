# LifeOS: A Personal System for Growth and Self-Mastery

LifeOS is a comprehensive, AI-enhanced system designed to serve as a second brain, life coach, and personal assistant. It's a private and personalized tool for navigating life with intention, with a special focus on integrating productivity with deep emotional and spiritual growth.

## Core Philosophy: Compassionate Firmness

The guiding principle of LifeOS is "Compassionate Firmness." This means combining the rigorous, systematic approach of methodologies like GTD (Getting Things Done) and PARA (Projects, Areas, Resources, Archives) with the empathetic, insightful support of an AI life coach. The system is designed to be supportive yet steady, offering accountability and honest reflection to help you stay aligned with your deepest values.

## System Architecture

LifeOS is built on a dual architecture: a conceptual framework for organizing your life and a technical stack for powering the AI and user interface.

### Conceptual Architecture

The core of LifeOS is a unique integration of two powerful organizational methodologies:

-   **PARA (Projects, Areas, Resources, Archives):** This system, developed by Tiago Forte, is used to organize your knowledge and information. It provides a clear and intuitive structure for everything you want to keep track of, from your personal projects to your long-term goals.
-   **GTD (Getting Things Done):** This renowned productivity method, created by David Allen, is used to manage your actions and tasks. It provides a clear and effective workflow for capturing, clarifying, and organizing everything you need to do.

By keeping these two systems separate but interconnected, LifeOS ensures a clear distinction between your knowledge and your actions, creating a powerful and flexible framework for managing your life.

### Technical Architecture

LifeOS is comprised of three main components:

1.  **`LifeOS/`:** This is the heart of your personal knowledge management system. It's a collection of markdown files organized according to the PARA method, where you'll store your notes, journal entries, project plans, and more.
2.  **`lifeos-rag-api/`:** This is the backend of the system, powered by a FastAPI application. It uses a RAG (Retrieval-Augmented Generation) architecture to provide a powerful, context-aware AI that can interact with your personal knowledge base. The backend is fully containerized with Docker and includes a Neo4j graph database, a Qdrant vector store, and the Open WebUI for a user-friendly interface.
3.  **`LifeOS-Web/`:** This is the frontend of the application, built with Next.js and React. It provides a clean and intuitive interface for interacting with the LifeOS system.

## Key Features

-   **AI-Powered Life Coaching:** Engage in insightful conversations with an AI that's aware of your personal context, helping you identify blind spots, understand your shortcomings, and develop strategies for growth.
-   **Integrated Knowledge Management:** Seamlessly combine the PARA method for organizing knowledge with the GTD system for managing tasks, creating a holistic view of your life.
-   **Personalized Workflows:** From daily check-ins and weekly reviews to specialized coaching for emotional intelligence, LifeOS is designed to support your unique goals and routines.
-   **RAG Architecture:** The powerful RAG-based backend allows the AI to retrieve relevant information from your personal notes, ensuring that its guidance is always grounded in your own experiences and reflections.

## Future Ideas

This project is a constantly evolving system. Here are some of the ideas for future development:

-   **Advanced AI Integration:** Enhance the AI's capabilities with smart suggestions, pattern recognition, and proactive habit tracking to provide even more personalized support.
-   **Voice-to-Text Capture:** Implement a seamless way to capture thoughts, ideas, and tasks on the go using voice notes that are automatically transcribed and integrated into the system.
-   **Automated Workflows:** Develop AI-driven assistance for daily and weekly reviews, helping to streamline the process and provide deeper insights.
-   **Deeper Relationship Coaching:** Expand the relationship coaching features with proactive suggestions, communication analysis, and personalized exercises for improving emotional intelligence.

## Getting Started

To get LifeOS up and running, you'll need to set up the backend and frontend services separately.

### Backend Setup (`lifeos-rag-api/`)

1.  **Navigate to the `lifeos-rag-api` directory:**
    ```bash
    cd lifeos-rag-api
    ```
2.  **Create a `.env` file:**
    Copy the `.env.example` file to a new file named `.env` and fill in the required environment variables.
3.  **Create a `notes` directory:**
    Create a new directory named `notes` in the `lifeos-rag-api` directory. This is where you will place all of your personal documents that you want the AI to be able to access.
4.  **Run the Docker containers:**
    ```bash
    docker-compose up -d
    ```
    This will start all the backend services in detached mode.

### Frontend Setup (`LifeOS-Web/`)

1.  **Navigate to the `LifeOS-Web` directory:**
    ```bash
    cd LifeOS-Web
    ```
2.  **Install the dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    This will start the Next.js development server, and you can access the application at `http://localhost:3000`.

## Directory Structure

Here's a high-level overview of the project's directory structure:

-   **`LifeOS/`**: Contains all your personal notes and documents, organized using the PARA method.
-   **`lifeos-rag-api/`**: The backend of the application, including the FastAPI service, Docker configuration, and related files.
-   **`LifeOS-Web/`**: The frontend of the application, built with Next.js.

This README provides a starting point for understanding and using LifeOS. For a more in-depth guide to the system's philosophy, structure, and workflows, please refer to the `MASTER_PLAN.md` in the `LifeOS/` directory.
