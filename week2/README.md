# Action Item Extractor

A FastAPI + SQLite web app that converts free-form notes into enumerated action items, with both regex-based and LLM-powered extraction.

## Setup

1. Activate your Conda environment and install dependencies from the repo root:
   ```bash
   conda activate cs146s
   poetry install --no-interaction
   ```

2. (Optional) Set the Ollama model via environment variable (defaults to `mistral-nemo:12b`):
   ```bash
   export OLLAMA_MODEL=mistral-nemo:12b
   ```
   Pull the model with Ollama before using LLM extraction:
   ```bash
   ollama pull mistral-nemo:12b
   ```

## Running the App

From the repo root:
```bash
poetry run uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the frontend HTML |
| `POST` | `/action-items/extract` | Extract action items using regex heuristics |
| `POST` | `/action-items/extract-llm` | Extract action items using an Ollama LLM |
| `GET` | `/action-items` | List all action items (optional `?note_id=` filter) |
| `POST` | `/action-items/{id}/done` | Mark an action item done/undone |
| `POST` | `/notes` | Create and save a note |
| `GET` | `/notes` | List all saved notes |
| `GET` | `/notes/{note_id}` | Get a single note by ID |

### Request / Response examples

**POST `/action-items/extract`**
```json
// Request
{ "text": "- [ ] Set up database\n- Write tests", "save_note": true }

// Response
{ "note_id": 1, "items": [{ "id": 1, "text": "Set up database" }, { "id": 2, "text": "Write tests" }] }
```

**POST `/action-items/{id}/done`**
```json
// Request
{ "done": true }

// Response
{ "id": 1, "done": true }
```

## Running Tests

```bash
poetry run pytest week2/tests/
```
