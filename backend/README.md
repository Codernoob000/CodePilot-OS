# CodePilot OS Backend

The backend is a FastAPI modular-monolith foundation aligned with the product architecture. It exposes only a process health endpoint today; domain, database, agent, and worker packages are intentionally empty boundaries for subsequent phases.

## Run locally

1. Copy `.env.example` to `.env` and set only local development values.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Start the API: `python -m uvicorn app.main:app --reload --port 8000`
4. Call `GET http://localhost:8000/api/v1/health`.

## Verification

Run `python -m pytest` from this directory. The health check is asynchronous and returns a request correlation ID in both the response header and body.

## Architectural decisions

- The application factory keeps configuration explicit and makes isolated tests possible.
- FastAPI routes remain thin; future business logic belongs in `app/services`.
- Typed Pydantic settings use environment variables; credentials are never hardcoded.
- The health endpoint is process-level. Database/Redis readiness checks will be added only when their lifecycle is implemented.
- `app/db`, `app/models`, `app/agents`, and `app/services` are preserved as small, intentional boundaries from the architecture document.
