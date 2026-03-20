# Week 4 Project Rules

## App entry points
- Backend: `week4-amazon-q/backend/app/main.py`
- Routers: `week4-amazon-q/backend/app/routers/`
- Services: `week4-amazon-q/backend/app/services/`
- Tests: `week4-amazon-q/backend/tests/`
- Frontend: `week4-amazon-q/frontend/`
- DB seed: `week4-amazon-q/data/seed.sql`

## Run commands (from week4-amazon-q/ directory)
- Start app: `make run`
- Run tests: `make test`
- Format: `make format`
- Lint: `make lint`
- Seed DB: `make seed`

## Coding conventions
- Formatter: black
- Linter: ruff
- ORM: SQLAlchemy (not raw SQL)
- Schemas: Pydantic v2
- Always run `make lint` and `make test` after any backend change

## Workflow: adding a new endpoint
1. Write a failing test in `week4-amazon-q/backend/tests/`
2. Implement the route in `week4-amazon-q/backend/app/routers/`
3. Run `make format && make lint && make test`
4. Update `week4-amazon-q/docs/TASKS.md` if the task is complete

## Commands to avoid
- Do NOT drop or recreate the database directly; use `make seed`
- Do NOT commit without passing lint and tests
