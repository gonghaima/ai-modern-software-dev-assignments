import sys
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral-nemo:12b"


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""


CONTEXT = {
    "models": read_file("week4-amazon-q/backend/app/models.py"),
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

    with open("week4-amazon-q/generated_test.py", "w") as f:
        f.write(test_code)
    with open("week4-amazon-q/generated_impl.py", "w") as f:
        f.write(impl_code)

    print("\nOutputs saved to week4-amazon-q/generated_test.py and generated_impl.py")
    print("Review, then manually integrate into the codebase and run: make test")
