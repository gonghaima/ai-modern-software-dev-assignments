# Week 3 Implementation Plan: Custom MCP Server

## What we're building
A local STDIO MCP server wrapping the GitHub API, discoverable by Claude Desktop.

## API: GitHub REST API
- `GET /repos/{owner}/{repo}/issues` — list issues
- `POST /repos/{owner}/{repo}/issues` — create an issue

## Folder structure
```
week3/
├── server/
│   ├── main.py        # MCP server entrypoint
│   └── github.py      # GitHub API client wrapper
├── README.md
└── implementationPlan.md
```

## Steps

### 1. Add dependencies
Add `mcp[cli]` and `httpx` to the root `pyproject.toml`.

### 2. `github.py` — GitHub API client
Thin wrapper with:
- `list_issues(owner, repo, state)` — fetch issues from a repo
- `create_issue(owner, repo, title, body)` — open a new issue
- Timeout handling and HTTP error raising
- Rate-limit detection via `X-RateLimit-Remaining` header
- `GITHUB_TOKEN` read from environment

### 3. `main.py` — MCP server
Two tools exposed via MCP:
- `list_github_issues` — params: `owner`, `repo`, `state` (open/closed/all)
- `create_github_issue` — params: `owner`, `repo`, `title`, `body`

Rules:
- Graceful error messages returned to client (no raw tracebacks)
- All logging goes to stderr (required for STDIO transport)
- Token loaded from `GITHUB_TOKEN` env var

### 4. `README.md`
- Prerequisites and environment setup (`GITHUB_TOKEN`)
- Run instructions (local STDIO)
- Claude Desktop config snippet
- Tool reference: names, parameters, example inputs/outputs

## Rubric coverage
| Criteria | How |
|---|---|
| Functionality (35pts) | 2 tools + real GitHub API integration |
| Reliability (20pts) | Timeouts, HTTP errors, rate-limit warning |
| Dev experience (20pts) | README with Claude Desktop config |
| Code quality (15pts) | Type hints, minimal code, descriptive names |
