# Sprint 1 — Data Layer

**Date:** 2026-06-18
**Status:** Complete

## What We Built

- **Docker Compose** environment running Postgres 16 + FastAPI, fully launchable with `docker-compose up`
- **4 SQLAlchemy models**: `User`, `MasterProfile`, `Application`, `TailoredDocument` — with JSONB columns for flexible profile data and UUID primary keys throughout
- **Full JWT auth flow**: register, login, `GET /auth/me`, and `PUT /auth/api-key` for BYOK key storage
- **MasterProfile CRUD**: upsert endpoint that creates or fully replaces a user's work history, education, and skills
- **Application CRUD**: full `GET / POST / PATCH / DELETE` for job tracking with Kanban-ready `status` enum (`saved → applied → interviewing → rejected → offer`)

## Architecture Decisions & Why

**Fernet encryption for API keys** — Each user's Anthropic API key is encrypted at rest using symmetric Fernet encryption before being written to Postgres. The plaintext key is never stored or logged. Only the last 4 characters are saved as a display hint.

**JSONB for MasterProfile arrays** — `experience`, `education`, and `skills` are stored as JSONB rather than normalized tables. This allows flexible, schema-free profile structures that map directly to what the AI pipeline consumes in Sprint 2, without requiring a migration every time a resume field changes.

**Environment-aware CORS** — CORS origins are toggled via the `ENVIRONMENT` env var (`dev` → localhost:3000, `prod` → your domain). This means zero code changes when deploying to AWS.

**`create_all` over Alembic for Sprint 1** — Using `Base.metadata.create_all()` on startup keeps the dev loop fast. Alembic migrations will be introduced before the AWS production deploy.

## Challenges & How We Solved Them

**Model import ordering for `create_all`** — SQLAlchemy's `create_all` only creates tables for models it knows about at call time. Solved by importing `app.models` explicitly in `main.py` before the `create_all` call, ensuring all four models are registered.

## Testing

A `pytest` integration suite was added in `backend/tests/` covering all 21 Sprint 1 endpoints. Tests run against a live Postgres container (started via `docker-compose up -d db`) using FastAPI's `TestClient` with the `get_db` dependency overridden per test. Tables are dropped and recreated before each test to guarantee clean state.

**To run:**
```bash
pip install -r backend/requirements-test.txt
docker-compose up -d db
cd backend && python -m pytest -v
```

**Coverage breakdown:**

| Module | Tests |
|---|---|
| Auth | register, duplicate email rejection, login, wrong password, unknown email, `GET /auth/me` (auth + unauth), API key hint storage |
| Profile | 404 before creation, upsert creates, upsert updates in place, `GET` after upsert, unauth rejection |
| Applications | empty list, create, get by ID, 404, PATCH status, delete → verify gone, user isolation, full Kanban status cycle |

**Why SQLite was not used** — The models use `postgresql.UUID` and `postgresql.JSONB` dialect types that are incompatible with SQLite. Tests require a real Postgres instance; the existing dev Docker container satisfies this with no extra setup.

**Known warnings** — `datetime.utcnow()` deprecation notices from `auth_service.py` and `python-jose`. These are non-breaking and will be resolved before the AWS production deploy by switching to `datetime.now(datetime.UTC)`.

## Sprint 2 Preview — AI Pipeline

Next sprint wires in the multi-agent LLM pipeline:
1. **Extractor** — parses a raw job description into structured skills and requirements
2. **Matcher** — compares extracted requirements against the user's `MasterProfile`
3. **Generator** — rewrites resume bullet points to highlight matched skills without hallucinating new experience
4. **Scorer** — returns a 0–100 ATS match score with a breakdown by category

The pipeline will use the user's own Anthropic API key (decrypted at request time) and return a `TailoredDocument` JSON object linked to the job `Application`.
