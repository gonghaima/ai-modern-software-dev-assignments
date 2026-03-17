"""
MCP client: uses Ollama (mistral-nemo) to decide tool calls,
dispatches them to the GitHub MCP STDIO server.

Usage:
    python3 client.py "List open issues in microsoft/vscode"
"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ollama

MODEL = "mistral-nemo:12b"
_here = __import__("pathlib").Path(__file__).resolve().parent
SERVER_PYTHON = str(_here.parent / ".venv/bin/python3")
SERVER_SCRIPT = str(_here / "server/main.py")


async def run(user_query: str) -> None:
    server_params = StdioServerParameters(
        command=SERVER_PYTHON,
        args=[SERVER_SCRIPT],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Fetch tools from MCP server and convert to Ollama format
            tools_result = await session.list_tools()
            ollama_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    },
                }
                for t in tools_result.tools
            ]

            messages = [{"role": "user", "content": user_query}]

            # Agentic loop: keep going until model stops calling tools
            while True:
                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )
                msg = response.message
                messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

                if not msg.tool_calls:
                    print(msg.content)
                    break

                # Dispatch each tool call to the MCP server
                for tc in msg.tool_calls:
                    tool_name = tc.function.name
                    tool_args = tc.function.arguments
                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)

                    print(f"[calling tool: {tool_name}({tool_args})]", file=sys.stderr)
                    result = await session.call_tool(tool_name, tool_args)
                    tool_output = result.content[0].text if result.content else ""

                    messages.append({"role": "tool", "content": tool_output})


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "List open issues in microsoft/vscode"
    asyncio.run(run(query))
