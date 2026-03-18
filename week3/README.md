# Week 3: Custom MCP Server for GitHub API

This project implements a local STDIO MCP server that wraps the GitHub REST API, providing tools to list and create issues in GitHub repositories. The server is discoverable by MCP clients like Claude Desktop.

## Prerequisites

- Python 3.10 or higher
- A GitHub Personal Access Token with `repo` scope (for private repos) or `public_repo` scope (for public repos)
- Dependencies installed via Poetry (from root `pyproject.toml`)

## Environment Setup

1. Create a `.env` file in the root directory of the project (next to `pyproject.toml`):
   ```
   GITHUB_TOKEN=your_github_personal_access_token_here
   ```
   Replace `your_github_personal_access_token_here` with your actual GitHub token.

2. Install dependencies:
   ```bash
   poetry install
   ```

## Run Instructions (Local STDIO)

To run the MCP server locally:

```bash
cd week3/server
python main.py
```

The server will start and listen for STDIO input/output, ready to be used by an MCP client.

## Claude Desktop Configuration

To integrate with Claude Desktop:

1. Open Claude Desktop settings
2. Go to the "Developer" section
3. Add a new MCP server with the following configuration:

```json
{
  "mcpServers": {
    "github-mcp": {
      "command": "python",
      "args": ["/path/to/week3/server/main.py"],
      "env": {
        "GITHUB_TOKEN": "your_github_personal_access_token_here"
      }
    }
  }
}
```

Replace `/path/to/week3/server/main.py` with the absolute path to the `main.py` file on your system.

## Tool Reference

### list_github_issues

Lists issues from a GitHub repository.

**Parameters:**
- `owner` (string, required): The GitHub username or organization name
- `repo` (string, required): The repository name
- `state` (string, optional): Issue state filter - "open", "closed", or "all" (default: "open")

**Example Input:**
```
owner: "octocat"
repo: "Hello-World"
state: "open"
```

**Example Output:**
```
#1: Found a bug (open)
#2: Feature request (open)
```

**Expected Behaviors:**
- Returns a list of issues with their numbers, titles, and states
- Handles rate limits gracefully with a user-friendly message
- Returns appropriate messages for empty results or errors

### create_github_issue

Creates a new issue in a GitHub repository.

**Parameters:**
- `owner` (string, required): The GitHub username or organization name
- `repo` (string, required): The repository name
- `title` (string, required): The issue title
- `body` (string, optional): The issue body/description (default: empty)

**Example Input:**
```
owner: "octocat"
repo: "Hello-World"
title: "New feature request"
body: "Please add support for dark mode."
```

**Example Output:**
```
Created issue #3: New feature request
https://github.com/octocat/Hello-World/issues/3
```

**Expected Behaviors:**
- Creates the issue and returns the issue number and URL
- Handles authentication errors and rate limits
- Provides clear error messages for invalid repositories or permissions