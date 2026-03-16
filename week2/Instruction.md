## Run ai

ollama serve
or
ollama run mistral-nemo:12b

## Run app

cd /Users/stevengong/study/modern-software-dev-assignments/week2

```
uvicorn app.main:app --reload
```

## Inspect db data

cd /Users/stevengong/study/modern-software-dev-assignments/week2
sqlite3 data/app.db

-- View all notes
SELECT \* FROM notes;

-- View all action items
SELECT \* FROM action_items;

-- View action items with their associated notes
SELECT ai.id, ai.text, ai.done, n.content
FROM action_items ai
LEFT JOIN notes n ON ai.note_id = n.id;

-- Exit sqlite3
.quit

## Run unit test

```
pytest week2/tests/test_extract.py
```

## Change log

Week2 TODO 2:
changed

Added Pydantic schemas and wired response_model + request models in routers.
Updated db.py to return plain dicts instead of sqlite3.Row.
Moved init_db() into FastAPI lifespan.
Replaced manual validation with Pydantic validation (whitespace-trimming + empty checks).
Centralized config in config.py (DB paths + model name).
Swapped print for logging.exception and removed unused imports.

check code in the following folder
/Users/stevengong/study/modern-software-dev-assignments/week2/app

/Users/stevengong/study/modern-software-dev-assignments/week2/frontend

and "TODO 3: Refactor Existing Code for Clarity" section in /Users/stevengong/study/modern-software-dev-assignments/week2/assignment.md

Don't change anything, but suggest what to do, is current code already contains required feature?
