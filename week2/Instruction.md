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
SELECT * FROM notes;

-- View all action items
SELECT * FROM action_items;

-- View action items with their associated notes
SELECT ai.id, ai.text, ai.done, n.content 
FROM action_items ai 
LEFT JOIN notes n ON ai.note_id = n.id;

-- Exit sqlite3
.quit
