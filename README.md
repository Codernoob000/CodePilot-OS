# CodePilot OS

A production-grade, asynchronous AI Engineering Operating System backend built with FastAPI, SQLAlchemy 2.0, PostgreSQL, and Docker.

---

# Overview

**CodePilot OS** is a modular, high-performance backend platform designed to power an autonomous AI Engineering Operating System. It serves as the foundation for managing code repositories, workspace projects, user authentication, and eventual multi-agent AI execution workflows.

### Why It Exists
Modern software development requires seamless orchestration between developer workflows, repository management, and autonomous AI agents. CodePilot OS bridges this gap by offering a enterprise-ready API architecture with strict domain boundaries, asynchronous data access, request tracing, and scalable persistence layers.

### Problem Solved
- **Monolithic Bottlenecks:** Replaces tightly coupled codebases with a modular monolith architecture that can evolve into distributed microservices.
- **Synchronous I/O Latency:** Utilizes native Python `async`/`await` primitives with `asyncpg` and SQLAlchemy 2.0 for high-throughput, non-blocking I/O operations.
- **Security & Multi-Tenancy:** Enforces robust JWT authentication and strict resource ownership verification across workspace projects.
- **Observability Gaps:** Embeds structured JSON logging and end-to-end request correlation IDs (`X-Request-ID`) into every HTTP cycle.

### High-Level Architecture
The project follows a clean, layered **Modular Monolith** pattern:
```
Client Request
      │
      ▼
┌──────────────┐
│ Router Layer │  (FastAPI APIRouters, Pydantic Validation, OpenAPI Specs)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Service Layer │  (Business Logic, Domain Authorization, Password Hashing)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Repository  │  (Data Access Layer, SQLAlchemy 2.0 AsyncSession Queries)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Database    │  (PostgreSQL 16 Relational Engine)
└──────────────┘
```

---

# Features

CodePilot OS includes the following implemented features:

- 🔐 **JWT Authentication System:** Secure registration and login flow issuing signed JWT access tokens (HS256) with configurable expiration (`access_token_expire_minutes`).
- 🔑 **Authorization & Resource Protection:** OAuth2 Password Bearer flow with user ownership enforcement on project management endpoints.
- 👤 **User Management:** Complete user domain persistence with `bcrypt` password hashing (`passlib`), unique email/username constraints, and profile retrieval (`/auth/me`).
- 📁 **Project Management CRUD:** Full lifecycle management (Create, Read, List, Update, Delete) for user-owned workspace projects with cascade deletion rules.
- 📦 **Repository Management CRUD:** Source-code repository tracking with pagination parameters (`offset`, `limit`), GitHub URL metadata, and local path mapping.
- ⚡ **Asynchronous ORM & Database Access:** Built on SQLAlchemy 2.0 `AsyncSession` with PostgreSQL connections managed by `asyncpg` connection pooling.
- 🔄 **Database Migrations:** Automated schema versioning and migration management using Alembic.
- 🛡️ **Validation & Data Contracts:** Pydantic v2 schemas for strict input validation, response serialization, and uniform error envelopes (`ErrorResponse`).
- 💉 **Dependency Injection:** Reusable FastAPI `Depends` injection for request-scoped database sessions, repositories, services, and security contexts.
- 📊 **Structured Logging & Tracing:** JSON-formatted application logging with `X-Request-ID` correlation middleware for request tracking.
- 🐳 **Containerization:** Container environment featuring a multi-stage `Dockerfile` and `docker-compose.yml` for PostgreSQL 16 and backend services.

---

# Tech Stack

| Category | Technology | Description / Usage |
| :--- | :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) `v0.139+` | Asynchronous web framework for high-performance REST APIs |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) `v0.51+` | Production ASGI server implementation |
| **Database** | [PostgreSQL](https://www.postgresql.org/) `16` | Relational database engine |
| **Async Database Driver** | [asyncpg](https://github.com/MagicStack/asyncpg) `v0.31+` | Asynchronous PostgreSQL database client |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) `v2.0+` | Asynchronous Object Relational Mapper & query builder |
| **Database Migrations** | [Alembic](https://alembic.sqlalchemy.org/) `v1.18+` | Database migration and revision management tool |
| **Data Validation & Settings** | [Pydantic](https://docs.pydantic.dev/) `v2.13+` | Data parsing, validation, and environment configuration |
| **Authentication & Hashing** | PyJWT / `python-jose` & `passlib[bcrypt]` | JWT token creation/decoding & bcrypt password hashing |
| **Containerization** | [Docker](https://www.docker.com/) & Docker Compose | Service containerization and environment orchestration |
| **Structured Logging** | `python-json-logger` `v3.3+` | JSON-formatted logs with request correlation fields |
| **Testing & Linting** | `pytest`, `pytest-asyncio`, `ruff` | Automated test suite and high-speed Python linter |
| **Python Version** | Python `3.12` | Runtime language environment |

---

# Architecture

The application implements a decoupled 5-tier architecture:

```
Client
  │
  ▼
Router Layer (FastAPI APIRouter)
  │
  ▼
Service Layer (Business Rules & Domain Validation)
  │
  ▼
Repository Layer (SQLAlchemy Async Data Access)
  │
  ▼
Database (PostgreSQL 16)
```

### Layer Responsibilities

1. **Client**
   - Sends HTTP requests carrying JSON payloads and optional `Authorization: Bearer <JWT>` tokens.
   - Receives standardized HTTP status codes and structured JSON response envelopes.

2. **Router Layer (`app/api`)**
   - Declares API endpoints using FastAPI `APIRouter`.
   - Handles HTTP route mapping, query parameter parsing, request body validation via Pydantic, and OpenAPI documentation generation.
   - Injects dependencies (database sessions, repositories, services, authenticated user context) using FastAPI `Depends`.

3. **Service Layer (`app/services`)**
   - Implements business logic and domain validation rules.
   - Performs domain security checks (e.g., verifying that a project belongs to the requesting `owner_id`).
   - Hashes raw passwords and checks user credential validity.
   - Raises domain-specific exceptions (`ProjectNotFoundError`, `UnauthorizedProjectAccessError`, `EmailAlreadyExistsError`).

4. **Repository Layer (`app/repositories`)**
   - Encapsulates database interactions and hides ORM details from domain logic.
   - Executes async database queries using SQLAlchemy `AsyncSession` (`select`, `add`, `commit`, `refresh`, `delete`).
   - Supports paginated listings and filtered single-record lookups.

5. **Database Layer**
   - PostgreSQL 16 relational database engine storing tables (`users`, `projects`, `repositories`).
   - Enforces Foreign Key constraints, unique indexes (`username`, `email`), cascade deletion rules, and timezone-aware timestamps.

---

# Project Structure

```
CodePilot-OS/
├── .env.example              # Template for root environment configuration
├── .gitignore                # Git exclusion rules
├── docker-compose.yml        # Docker Compose configuration for API and PostgreSQL
├── requirements.txt          # Root Python dependencies list
├── README.md                 # Project documentation
├── agents.md                 # Agent architecture guidelines
│
├── 00_Project_Management/    # Product requirements and development strategy
│   ├── DevelopmentPlan.md    # Multi-phase roadmap and task breakdown
│   └── PRD.md                # Product Requirements Document
│
├── 03_Docs/                  # Architectural documentation
│   └── Architecture.md       # Full architecture specification document
│
├── backend/                  # FastAPI Application Root
│   ├── Dockerfile            # Container image build manifest (Python 3.12-slim)
│   ├── README.md             # Backend-specific instructions
│   ├── alembic.ini           # Alembic migration configuration
│   ├── requirements.txt      # Backend Python dependencies
│   │
│   ├── alembic/              # Database migration scripts
│   │   ├── env.py            # Alembic async migration environment
│   │   └── versions/         # Alembic migration revision scripts
│   │       ├── d9aa3026f02f_initial_schema.py        # Repositories table
│   │       ├── 07d5b8723f7f_add_user_model.py        # Users table
│   │       └── 952f424450a7_create_projects_table.py # Projects table
│   │
│   ├── app/                  # Application core source code
│   │   ├── main.py           # FastAPI application factory and entrypoint
│   │   │
│   │   ├── api/              # HTTP routers and dependency injections
│   │   │   ├── dependencies.py                  # FastAPI Depends helpers
│   │   │   ├── repositories.py                  # Repository HTTP routes
│   │   │   └── v1/
│   │   │       ├── router.py                    # V1 router aggregation
│   │   │       ├── auth.py                      # Auth & user routes
│   │   │       ├── projects.py                  # Project management routes
│   │   │       └── endpoints/
│   │   │           └── health.py                # Health check endpoint
│   │   │
│   │   ├── core/             # Application configuration & security
│   │   │   ├── config.py                        # Pydantic Settings instance
│   │   │   ├── logging.py                       # JSON structured logger
│   │   │   ├── middleware.py                    # Request correlation ID middleware
│   │   │   └── security.py                      # Password hashing & JWT helpers
│   │   │
│   │   ├── db/               # Database setup and sessions
│   │   │   ├── base.py                          # SQLAlchemy DeclarativeBase
│   │   │   └── session.py                       # Async engine & sessionmaker
│   │   │
│   │   ├── models/           # SQLAlchemy ORM database models
│   │   │   ├── user.py                          # User ORM model
│   │   │   ├── project.py                       # Project ORM model
│   │   │   └── repository.py                    # Repository ORM model
│   │   │
│   │   ├── repositories/     # Data access repositories
│   │   │   ├── user.py                          # User data access
│   │   │   └── project_repository.py            # Project data access
│   │   │
│   │   ├── schemas/          # Pydantic data contracts
│   │   │   ├── errors.py                        # Standard error payload contract
│   │   │   ├── health.py                        # Health check status contract
│   │   │   ├── user.py                          # User input/output contracts
│   │   │   ├── project.py                       # Project input/output contracts
│   │   │   └── repository.py                    # Repository input/output contracts
│   │   │
│   │   ├── services/         # Business domain services
│   │   │   ├── user.py                          # User business service
│   │   │   ├── project_service.py               # Project business service
│   │   │   └── repository_service.py            # Repository business service
│   │   │
│   │   ├── agents/           # Domain boundary for future AI agents
│   │   └── utils/            # Shared utility functions
│   │
│   └── tests/                # Async automated test suite
│       ├── conftest.py       # Test fixtures and TestClient instantiation
│       └── test_health.py    # Health endpoint verification tests
│
├── database/                 # Additional database artifacts and SQL scripts
│   ├── schema.sql            # Core SQL schema reference
│   ├── migrations/           # Raw migration scripts directory
│   └── seed/                 # Seed data files directory
│
├── frontend/                 # Frontend application boundary (Next.js scaffold)
├── configs/                  # Environment configuration files
├── prompts/                  # System prompt templates and specifications
└── scripts/                  # Automation and utility scripts
```

---

# Database Models

SQLAlchemy models defined in `app/models/`:

| Model | Table Name | Purpose | Relationships & Constraints |
| :--- | :--- | :--- | :--- |
| **`User`** | `users` | Stores system user credentials, active status, and audit timestamps. | **One-to-Many** with `Project` (`User.projects` ↔ `Project.owner`, `cascade="all, delete-orphan"`). Unique indexes on `username` and `email`. |
| **`Project`** | `projects` | Represents workspace projects owned by registered users. | **Many-to-One** with `User` (`Project.owner_id` Foreign Key → `users.id` with `ON DELETE CASCADE`). |
| **`Repository`** | `repositories` | Represents source-code repository metadata registered in CodePilot OS. | Standalone entity with attributes for `github_url`, `local_path`, `default_branch`, and `language`. |

---

# API Endpoints

### System Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/health` | Returns application health, environment status, and correlation ID | No |

### Authentication & Users (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate user credentials and return JWT Bearer token | No |
| `GET` | `/api/v1/auth/me` | Retrieve the authenticated user's profile | Yes (Bearer Token) |

### Workspace Projects (`/api/v1/projects`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/projects` | Create a new project owned by the current user | Yes (Bearer Token) |
| `GET` | `/api/v1/projects` | List all projects owned by the current user | Yes (Bearer Token) |
| `GET` | `/api/v1/projects/{project_id}` | Get detailed project information by UUID | Yes (Bearer Token) |
| `PATCH` | `/api/v1/projects/{project_id}` | Partially update project details (owner only) | Yes (Bearer Token) |
| `DELETE` | `/api/v1/projects/{project_id}` | Delete a project and its associated data (owner only) | Yes (Bearer Token) |

### Source Code Repositories (`/api/v1/repositories`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/repositories` | Create a new repository metadata record | No |
| `GET` | `/api/v1/repositories` | List repositories with pagination (`offset`, `limit`) | No |
| `GET` | `/api/v1/repositories/{repository_id}` | Get repository details by UUID | No |
| `PATCH` | `/api/v1/repositories/{repository_id}` | Apply partial updates to a repository record | No |
| `DELETE` | `/api/v1/repositories/{repository_id}` | Delete a repository record by UUID | No |

---

# Authentication

CodePilot OS utilizes standard **OAuth2 with Password Flow** and **JWT Access Tokens**.

```
Client                     FastAPI API                     Database
  │                             │                             │
  ├─── POST /auth/register ────►│── Save hashed pass (bcrypt)─►│
  │    (username, email, pass)  │                             │
  │                             │                             │
  ├─── POST /auth/login ───────►│── Verify credentials ──────►│
  │    (form_data: username,pass)│                             │
  │◄── Returns JWT token ───────┤                             │
  │    (access_token, bearer)   │                             │
  │                             │                             │
  ├─── GET /projects ──────────►│                             │
  │    (Header: Bearer <JWT>)   │── Extract sub UUID ────────►│
  │◄── Returns User Data ───────│                             │
```

1. **Password Hashing:** Passwords are hashed using `passlib` with `bcrypt`. Raw passwords are never stored.
2. **Token Generation:** Upon successful authentication (`POST /api/v1/auth/login`), the system creates a JWT containing the user's UUID in the `sub` claim and an expiration timestamp (`exp`). The token is signed using `jwt_secret_key` and algorithm `HS256`.
3. **Protected Routes:** Endpoint functions enforce security by declaring `current_user: User = Depends(get_current_user)`.
4. **Token Validation:** `get_current_user` extracts the HTTP `Authorization: Bearer <token>` header, decodes the JWT using `python-jose`, fetches the user record from PostgreSQL, and confirms active account status.

---

# Database

The database architecture uses an asynchronous PostgreSQL infrastructure managed through SQLAlchemy 2.0 and Alembic.

- **PostgreSQL 16:** Relational database engine running in containerized setups or on host servers.
- **SQLAlchemy 2.0 Async:** Database interaction is handled asynchronously using `create_async_engine` with `postgresql+asyncpg://`. Connection pooling is configured with `pool_size=10`, `max_overflow=20`, and `pool_recycle=1800`.
- **Async Sessions:** Request-scoped sessions are yielded by `get_db()`, ensuring proper commit/rollback boundaries and deterministic cleanup per HTTP transaction.
- **Alembic Versioning:** Database migrations are defined under `backend/alembic/versions/`:
  - `d9aa3026f02f`: Initial schema creating the `repositories` table.
  - `07d5b8723f7f`: Schema update creating the `users` table with indexes on `username` and `email`.
  - `952f424450a7`: Schema update creating the `projects` table with foreign key reference to `users.id`.

---

# Installation

### Prerequisites

- **Python:** Version `3.12` or higher
- **PostgreSQL:** Version `16` (or Docker)
- **Git:** Installed on host system

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Codernoob000/CodePilot-OS.git
   cd CodePilot-OS
   ```

2. **Create and Activate a Virtual Environment**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install Dependencies**
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

5. **Start PostgreSQL & Apply Alembic Migrations**
   If using local PostgreSQL, ensure the database `codepilot` exists, then run:
   ```bash
   alembic upgrade head
   ```

6. **Run with Docker Compose (Alternative)**
   To spin up both the backend API and containerized PostgreSQL in one command:
   ```bash
   docker-compose up --build
   ```

---

# Environment Variables

Create a `backend/.env` file with your environment configurations:

```env
# Application Settings
APP_NAME="CodePilot OS API"
APP_VERSION="0.1.0"
ENVIRONMENT="local"
LOG_LEVEL="INFO"
API_V1_PREFIX="/api/v1"
DOCS_ENABLED=true
CORS_ORIGINS=["http://localhost:3000"]

# Security & Authentication
JWT_SECRET_KEY="your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Connection (Async Driver)
DATABASE_URL="postgresql+asyncpg://codepilot:codepilot123@localhost:5432/codepilot"

# Cache & Storage
REDIS_URL="redis://localhost:6379/0"
OBJECT_STORAGE_BUCKET=""

# External Integrations (Optional)
OPENAI_API_KEY=""
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
```

---

# Running the Project

### Running via Docker Compose

Start backend and PostgreSQL containers:
```bash
docker-compose up -d
```
Check running logs:
```bash
docker-compose logs -f backend
```
Stop container environment:
```bash
docker-compose down
```

### Local Development (without Docker)

1. Ensure PostgreSQL is running locally on port `5432`.
2. Apply database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```
3. Start the FastAPI application with Uvicorn auto-reload:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Running Alembic Migrations

- **Apply all pending migrations:**
  ```bash
  alembic upgrade head
  ```
- **Revert last migration:**
  ```bash
  alembic downgrade -1
  ```
- **Generate a new migration script:**
  ```bash
  alembic revision --autogenerate -m "describe_schema_changes"
  ```

---

# API Documentation

When the application is running (`DOCS_ENABLED=true`), interactive API documentation is automatically accessible at:

- **Swagger UI:** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **OpenAPI JSON Spec:** [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

# Current Progress

- [x] **Core System Architecture:** FastAPI application factory, settings management, and structured logging.
- [x] **Async Database Engine:** SQLAlchemy 2.0 `AsyncSession` setup with PostgreSQL connection pooling (`asyncpg`).
- [x] **Database Migrations:** Alembic configuration with active migration history.
- [x] **User Management & Auth:** Password hashing (`bcrypt`), JWT authentication, and user profile resolution (`/auth/me`).
- [x] **Project Management Module:** Complete CRUD functionality for workspace projects with user ownership controls.
- [x] **Repository Management Module:** Repository persistence service, CRUD routes, and paginated queries.
- [x] **Container Infrastructure:** Multi-stage `Dockerfile` and Docker Compose setup for local development.
- [🔄] **Automated Testing Suite:** Pytest setup with health check assertion tests.
- [ ] **GitHub OAuth & API Integration:** Syncing remote repositories via GitHub OAuth.
- [ ] **AI Agent Orchestration:** Background agent workers and LLM task execution pipeline.
- [ ] **Frontend Dashboard:** Next.js user interface for workspace visualization.

---

# Future Roadmap

Based on the established architecture, upcoming development will focus on the following modules:

1. **GitHub Integration Module:** OAuth2 authentication with GitHub, webhooks handling, and remote repository cloning.
2. **AI Analysis & Agent Orchestration:** Multi-agent framework (`app/agents`) powered by OpenAI/Gemini for automated code review, refactoring, and bug detection.
3. **Task Queue & Background Processing:** Celery/Redis background task distribution for repository indexing and LLM embeddings generation.
4. **Vector Search & Code Graph:** Vector database integration for code semantics search and context retrieval.
5. **Frontend Web Interface:** Next.js frontend with Tailwind CSS and real-time WebSocket updates.

---

# Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your Changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
4. **Run Tests & Linter**
   ```bash
   pytest
   ruff check .
   ```
5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

---

# License

This project is licensed under the [MIT License](LICENSE).

---

# Author

**CodePilot OS Team**
- GitHub: [@Codernoob000](https://github.com/Codernoob000)
- Repository: [https://github.com/Codernoob000/CodePilot-OS](https://github.com/Codernoob000/CodePilot-OS)
