# Salary Management API

Python backend boilerplate for the Salary Management kata: **FastAPI**, **SQLAlchemy**, **SQLite**, **Pydantic**, and **pytest**.

## Layout

- `app/main.py` — application factory and lifespan (creates SQLite tables from models)
- `app/db/database.py` — engine, session, and declarative `Base`
- `app/core/` — unified API response helpers, domain exceptions, centralized error handlers
- `app/routes/` — HTTP routers
- `app/services/` — use-case layer
- `app/repositories/` — data access (empty placeholder for now)
- `app/models/` — SQLAlchemy ORM models (none yet)
- `app/schemas/` — Pydantic schemas (none yet)
- `tests/` — pytest + `TestClient`

All JSON responses use this envelope:

```json
{
  "success": true,
  "message": "string",
  "statusCode": 200,
  "data": {}
}
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

SQLite file: `salary_management.db` at the project root (created on first startup).
