# Week 4 — Amazon Q + Ollama Equivalent Automations

This document describes how to replicate the Week 4 assignment automations using
**Amazon Q Developer (IDE)** and **Ollama (mistral-nemo:12b)** instead of Claude Code.

---

## Overview

| Claude Code Feature | Our Equivalent |
|---|---|
| `CLAUDE.md` guidance files | `.amazonq/rules/week4.md` — auto-loaded by Amazon Q |
| Custom slash commands (`.claude/commands/*.md`) | Saved prompts in `~/.aws/amazonq/prompts/` via `@prompt` |
| SubAgents (role-specialized) | Python script chaining Ollama calls with distinct system prompts |
| MCP servers | Ollama-backed MCP server (builds on week2/MyNotes MCP work) |

---

## Automation 1 — Amazon Q Workspace Rules (CLAUDE.md equivalent)

### Goal
Give Amazon Q persistent, project-specific context so every chat session
understands the week4 app structure, safe commands, and coding conventions —
without repeating yourself each time.

### How it works
Amazon Q automatically reads all `*.md` files under `.amazonq/rules/` at the
start of every chat and inline completion session.

### Setup

1. Create the rules directory at the repo root:
   ```bash
   mkdir -p /Users/stevengong/study/modern-software-dev-assignments/.amazonq/rules
   ```

2. Create `.amazonq/rules/week4.md` with the content below:

   ```markdown
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
   ```

3. Restart Amazon Q chat — the rules are now active for every session.

### Before vs. after
- Before: Manually explain app structure and conventions in every chat message.
- After: Amazon Q already knows the layout, safe commands, and workflow steps.

### Usage example
Open Amazon Q chat and ask:
> "Add a DELETE /notes/{id} endpoint"

Amazon Q will follow the workflow rule (test → implement → lint/test) automatically.

---

## Automation 2 — Ollama SubAgent Script (TestAgent + CodeAgent)

### Goal
Simulate Claude Code SubAgents using two sequential Ollama calls with distinct
system prompts: a **TestAgent** that writes a failing test, then a **CodeAgent**
that implements the code to pass it.

### How it works
A Python script calls `ollama` (via its REST API at `localhost:11434`) twice:
1. TestAgent receives the task + codebase context → outputs a pytest test.
2. CodeAgent receives the task + the generated test → outputs the implementation.

### Setup

1. Ensure Ollama is running:
   ```bash
   ollama serve
   # in another terminal, confirm model is available:
   ollama run mistral-nemo:12b
   ```

2. Install the `requests` library if not already present (it's in the project's
   Poetry env):
   ```bash
   conda activate cs146s
   poetry add requests  # or: pip install requests
   ```

3. Create `week4-amazon-q/subagents.py` (see **Automation 2 — Code** section below).

4. Run from the repo root:
   ```bash
   conda activate cs146s
   python week4-amazon-q/subagents.py "Add PUT /notes/{id} to edit a note's title and content"
   ```

### Code — `week4-amazon-q/subagents.py`

```python
import sys
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral-nemo:12b"

# Read relevant source files to give agents context
def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""

CONTEXT = {
    "models":  read_file("week4-amazon-q/backend/app/models.py"),
    "schemas": read_file("week4-amazon-q/backend/app/schemas.py"),
    "notes_router": read_file("week4-amazon-q/backend/app/routers/notes.py"),
    "test_notes": read_file("week4-amazon-q/backend/tests/test_notes.py"),
}

def ollama_call(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": f"SYSTEM: {system_prompt}\n\nUSER: {user_prompt}",
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["response"]

def test_agent(task: str) -> str:
    system = (
        "You are TestAgent. Given a task and existing code, write ONLY a pytest test "
        "function for the described feature. Output only the Python test code, no explanation."
    )
    user = f"""Task: {task}

Existing models:
{CONTEXT['models']}

Existing schemas:
{CONTEXT['schemas']}

Existing test file:
{CONTEXT['test_notes']}

Write a new pytest test function for this task."""
    return ollama_call(system, user)

def code_agent(task: str, test_code: str) -> str:
    system = (
        "You are CodeAgent. Given a task, a failing test, and existing code, implement "
        "ONLY the minimal code changes needed to make the test pass. "
        "Output only the Python implementation code, no explanation."
    )
    user = f"""Task: {task}

Failing test to satisfy:
{test_code}

Existing router:
{CONTEXT['notes_router']}

Existing models:
{CONTEXT['models']}

Existing schemas:
{CONTEXT['schemas']}

Write the implementation."""
    return ollama_call(system, user)

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or "Add PUT /notes/{id} to edit a note"

    print("=" * 60)
    print(f"TASK: {task}")
    print("=" * 60)

    print("\n[TestAgent] Generating test...\n")
    test_code = test_agent(task)
    print(test_code)

    print("\n[CodeAgent] Generating implementation...\n")
    impl_code = code_agent(task, test_code)
    print(impl_code)

    # Optionally write outputs to files for review
    with open("week4-amazon-q/generated_test.py", "w") as f:
        f.write(test_code)
    with open("week4-amazon-q/generated_impl.py", "w") as f:
        f.write(impl_code)

    print("\nOutputs saved to week4-amazon-q/generated_test.py and generated_impl.py")
    print("Review, then manually integrate into the codebase and run: make test")
```

### Expected output
```
============================================================
TASK: Add PUT /notes/{id} to edit a note's title and content
============================================================

[TestAgent] Generating test...
def test_update_note(client):
    ...

[CodeAgent] Generating implementation...
@router.put("/notes/{note_id}", response_model=NoteOut)
def update_note(...):
    ...

Outputs saved to week4-amazon-q/generated_test.py and generated_impl.py
```

### Before vs. after
- Before: Manually write test, then manually write implementation, then run tests.
- After: Run one command → get both test and implementation scaffolded → review and integrate.

### Rollback / safety notes
- The script only **reads** source files and **writes** to `week4-amazon-q/generated_*.py`.
- It never modifies the actual app files — you review and copy in manually.
- Always run `make test` after integrating generated code.

---

## Automation 3 (Bonus) — Saved Prompts as Reusable Slash Commands

### Goal
Replicate Claude Code's `.claude/commands/*.md` slash commands using Amazon Q
saved prompts, accessible via `@prompt` in any chat session.

### Setup

1. Create the prompts directory:
   ```bash
   mkdir -p ~/.aws/amazonq/prompts
   ```

2. Create `~/.aws/amazonq/prompts/docs-sync.md`:
   ```markdown
   Read the current OpenAPI spec from http://localhost:8000/openapi.json and compare
   it against week4-amazon-q/docs/TASKS.md. List any endpoints that exist in the API but are
   not documented, and any documented tasks that are not yet implemented. Output a
   concise diff-style summary with TODOs.
   ```

3. Create `~/.aws/amazonq/prompts/run-tests.md`:
   ```markdown
   Run `make test` from the week4-amazon-q/ directory. If tests pass, also run `make lint`.
   Summarize any failures with the failing test name, error message, and a suggested
   fix. If all pass, confirm with a green summary.
   ```

### Usage
In Amazon Q chat, type:
```
@docs-sync
@run-tests
```

### Before vs. after
- Before: Type out the full instruction every time you want a docs check or test run.
- After: Reference a saved prompt with `@prompt-name` in one keystroke.

---

## Applying the Automations to the Week 4 TASKS

Here's how to use the automations above to work through `week4-amazon-q/docs/TASKS.md`:

| Task | Automation to use |
|---|---|
| Task 2: Add search endpoint | Run `subagents.py "Add GET /notes/search?q=... endpoint"` → review → integrate |
| Task 3: Complete action item flow | Run `subagents.py "Implement PUT /action-items/{id}/complete"` |
| Task 4: Improve extraction logic | Run `subagents.py "Extend extract.py to parse #tags from note content"` |
| Task 5: Notes CRUD enhancements | Run `subagents.py "Add PUT /notes/{id} and DELETE /notes/{id}"` |
| Task 7: Docs drift check | Use `@docs-sync` prompt in Amazon Q chat |

After each integration step, always run:
```bash
cd week4-amazon-q
make format && make lint && make test
```
