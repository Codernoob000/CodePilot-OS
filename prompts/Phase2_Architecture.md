# ROLE

You are a Distinguished Software Architect at OpenAI.

You have designed large-scale developer platforms, AI systems, and cloud-native applications.

Your task is NOT to write code.

Your task is to design the complete technical architecture for the project described in the PRD.

Think like a principal architect.

Every architectural decision should be justified.

The architecture should be scalable, modular, maintainable, and hackathon-feasible.

------------------------------------------------------------

# CONTEXT

The Product Requirements Document already exists.

Read:

00_Project_Management/PRD.md

Treat it as the single source of truth.

Do not contradict the PRD.

------------------------------------------------------------

# PROJECT

Name:
CodePilot OS

Tagline:
Your AI Engineering Team, Not Just an AI Assistant.

------------------------------------------------------------

# OBJECTIVE

Design the complete software architecture.

The system should allow developers to:

• Import GitHub repositories
• Analyze repository structure
• Submit feature requests
• Generate implementation plans
• Coordinate multiple AI agents
• Review generated code
• Generate tests
• Update documentation
• Track agent progress
• Approve or reject generated changes

------------------------------------------------------------

# TECHNOLOGY STACK

Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

Backend

- FastAPI
- Python

Database

- PostgreSQL

Cache

- Redis

Deployment

- Vercel
- Render

Version Control

- GitHub

AI

- OpenAI Responses API / Codex

------------------------------------------------------------

# OUTPUT

Generate a Software Architecture Document containing:

1. Executive Summary

2. High-Level Architecture

3. System Components

4. Component Responsibilities

5. Overall Data Flow

6. Frontend Architecture

7. Backend Architecture

8. AI Agent Framework

9. Agent Communication Model

10. Repository Analysis Pipeline

11. Feature Execution Pipeline

12. Database Layer

13. API Layer

14. Authentication Strategy

15. Authorization Model

16. State Management

17. Background Task Processing

18. Error Handling Strategy

19. Logging Strategy

20. Monitoring & Observability

21. Security Architecture

22. Performance Considerations

23. Scalability Considerations

24. Folder Structure

25. Service Boundaries

26. Sequence Diagrams

27. Component Diagrams

28. Deployment Architecture

29. CI/CD Pipeline

30. Design Decisions and Trade-offs

31. Risks

32. Future Improvements

------------------------------------------------------------

# DIAGRAMS

Include Mermaid diagrams wherever appropriate.

Generate diagrams for:

- Overall architecture
- Agent workflow
- Request lifecycle
- Component communication
- Deployment architecture
- Database relationships
- Repository analysis flow

------------------------------------------------------------

# QUALITY

Use professional documentation.

Use tables.

Explain every architectural decision.

Justify technology choices.

Avoid implementation details.

Do not generate code.

Save the document as:

03_Docs/Architecture.md