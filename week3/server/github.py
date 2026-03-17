import os
from pathlib import Path
from dotenv import load_dotenv
import httpx

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

GITHUB_API = "https://api.github.com"
TIMEOUT = 10.0


def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _check_rate_limit(response: httpx.Response) -> None:
    remaining = response.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) == 0:
        raise RuntimeError("GitHub API rate limit exceeded. Please wait before retrying.")


def list_issues(owner: str, repo: str, state: str = "open") -> list[dict]:
    with httpx.Client(timeout=TIMEOUT) as client:
        response = client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_headers(),
            params={"state": state, "per_page": 30},
        )
        _check_rate_limit(response)
        response.raise_for_status()
        return response.json()


def create_issue(owner: str, repo: str, title: str, body: str = "") -> dict:
    with httpx.Client(timeout=TIMEOUT) as client:
        response = client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_headers(),
            json={"title": title, "body": body},
        )
        _check_rate_limit(response)
        response.raise_for_status()
        return response.json()
