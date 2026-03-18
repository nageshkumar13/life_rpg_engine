# LIFE RPG ENGINE Backend

Rules-based FastAPI backend for a gamified habit and task execution engine.

## Stack

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic Settings
- Pytest

## Quick Start

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment file:

```bash
cp .env.example .env
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start the app:

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest app/tests -q
```

## Architecture

- `app/api`: thin HTTP layer
- `app/services`: business rules and orchestration
- `app/repositories`: data access
- `app/models`: SQLAlchemy ORM models
- `app/schemas`: request and response contracts
- `app/workers`: nightly review and scheduler stubs

