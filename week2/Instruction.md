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

check code in the following folder
/Users/stevengong/study/modern-software-dev-assignments/week2/app

/Users/stevengong/study/modern-software-dev-assignments/week2/frontend

and "TODO 2: Add Unit Tests" section in /Users/stevengong/study/modern-software-dev-assignments/week2/assignment.md

Don't change anything, but suggest what to do, is current code already contains required feature?
