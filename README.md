# Salary Management API

Backend API for managing employees, computing net salary by country-specific deductions, and exposing simple salary metrics. Built as a Python assignment with a layered structure and test-driven development.

## Tech stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **pytest**

## Database choice

SQLite is used so the project runs with no external database server. The schema and layering (SQLAlchemy models, repositories, sessions) are straightforward to point at **MySQL** or **PostgreSQL** later by changing the connection URL and engine settings.

## Setup

1. Clone the repository.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   - macOS / Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the API locally (see commands below).
6. Run the test suite: `pytest`

## Scripts / commands

| Command | Purpose |
| -------- | -------- |
| `uvicorn app.main:app --reload` | Start the API with auto-reload |
| `pytest` | Run all tests |

On first startup, SQLite creates `salary_management.db` in the project root (unless you override `DATABASE_URL`). Tests use an in-memory database via `tests/conftest.py` for isolation.

## API endpoints (summary)

| Method | Path | Description |
| ------ | ---- | ----------- |
| `POST` | `/employees` | Create an employee |
| `GET` | `/employees/{id}` | Get an employee by id |
| `PUT` | `/employees/{id}` | Update an employee |
| `DELETE` | `/employees/{id}` | Delete an employee |
| `GET` | `/employees/{id}/salary` | Gross salary, deduction, and net salary for that employee |
| `GET` | `/metrics/country?name=India` | Min, max, and average salary for a country |
| `GET` | `/metrics/job?title=Backend%20Engineer` | Average salary for a job title |
| `GET` | `/health` | Health check |

## Salary rules (`GET /employees/{id}/salary`)

Deductions are applied to the employee’s stored **gross** salary based on **country**:

- **India** — 10% deduction  
- **United States** — 12% deduction  
- **All other countries** — no deduction  

**Net salary** = gross salary − deduction.

## Response format

Every endpoint returns the same JSON envelope:

```json
{
  "success": true,
  "message": "string",
  "statusCode": 200,
  "data": {}
}
```

- `success` — whether the operation succeeded from the client’s perspective  
- `message` — short human-readable text  
- `statusCode` — mirrors the HTTP status you would expect for that outcome  
- `data` — payload (object, array, or empty object as appropriate); validation and many errors use `data: {}`  

Validation and handler errors use the same shape with `success: false` and the matching HTTP status (e.g. 400, 404).

## Architecture overview

The code is split into **routes → services → repositories**, with **models** (SQLAlchemy) and **schemas** (Pydantic) defining persistence and API shapes.

- **Routes** — HTTP wiring, thin handlers  
- **Services** — business rules and orchestration  
- **Repositories** — database access  
- **Models / schemas** — ORM entities and request/response validation  

That separation keeps responsibilities obvious, makes behavior easier to test, and simplifies changes as the API grows.

## TDD approach

Development followed a strict test-first loop:

1. Write a failing integration test for the next behavior.  
2. Implement the smallest change that makes it pass.  
3. Refactor for clarity without changing behavior.  

Commits were kept small and aligned with that flow (red → green → refactor).

## AI usage

AI tools were used as a support system during development for:

- understanding and structuring test cases  
- improving commit messages and clarity  
- identifying potential edge cases  
- refining and optimizing parts of the implementation  
