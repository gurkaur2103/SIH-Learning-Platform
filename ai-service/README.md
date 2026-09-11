# Learning Platform AI Service

Modular FastAPI service for SIH26101. It provides document parsing, professional
profile extraction, explainable competency-gap analysis, course recommendations,
adaptive roadmaps, grounded quiz generation, RAG tutoring and mastery analytics.

## Run locally

1. Create a virtual environment: `python -m venv .venv`
2. Activate it and run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add a Gemini API key.
4. Run `uvicorn app.main:app --reload --port 8001`
5. Open `http://localhost:8001/docs`

The service works without a Gemini key using transparent demo responses. File
ingestion is held in memory for the local MVP; the main backend owns durable
PostgreSQL storage.

## API workflow

1. `POST /api/v1/profile/extract` — extract a CV or service profile.
2. `POST /api/v1/competencies/gaps` — rank competency gaps.
3. `POST /api/v1/recommendations` — rank the iGOT-ready course catalogue.
4. `POST /api/v1/roadmaps` — create the time-constrained plan.
5. `POST /api/v1/quizzes/documents` — upload training material.
6. `POST /api/v1/quizzes/generate` — generate and validate grounded MCQs.
7. `POST /api/v1/tutor/chat` — retrieve sources and answer.
8. `POST /api/v1/analytics/mastery` — calculate mastery and next action.

## Production replacement points

- Replace `InMemoryRAG` with PostgreSQL/pgvector.
- Replace `courses.json` with an authorized iGOT API adapter.
- Put the service behind the authenticated main backend; do not expose it
  directly to untrusted clients.
