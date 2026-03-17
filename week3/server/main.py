import logging
import sys
import httpx
from mcp.server.fastmcp import FastMCP
from github import list_issues, create_issue

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("github-mcp")


@mcp.tool()
def list_github_issues(owner: str, repo: str, state: str = "open") -> str:
    """List issues for a GitHub repository."""
    try:
        issues = list_issues(owner, repo, state)
        if not issues:
            return f"No {state} issues found in {owner}/{repo}."
        lines = [f"#{i['number']}: {i['title']} ({i['state']})" for i in issues]
        return "\n".join(lines)
    except RuntimeError as e:
        return str(e)
    except httpx.TimeoutException:
        return "Request timed out. Please try again."
    except httpx.HTTPStatusError as e:
        logger.exception("GitHub API error")
        return f"GitHub API error: {e.response.status_code} {e.response.text}"
    except Exception:
        logger.exception("Unexpected error in list_github_issues")
        return "An unexpected error occurred."


@mcp.tool()
def create_github_issue(owner: str, repo: str, title: str, body: str = "") -> str:
    """Create a new issue in a GitHub repository."""
    try:
        issue = create_issue(owner, repo, title, body)
        return f"Created issue #{issue['number']}: {issue['title']}\n{issue['html_url']}"
    except RuntimeError as e:
        return str(e)
    except httpx.TimeoutException:
        return "Request timed out. Please try again."
    except httpx.HTTPStatusError as e:
        logger.exception("GitHub API error")
        return f"GitHub API error: {e.response.status_code} {e.response.text}"
    except Exception:
        logger.exception("Unexpected error in create_github_issue")
        return "An unexpected error occurred."


if __name__ == "__main__":
    mcp.run(transport="stdio")
