import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ollama

async def main():
    # Start MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["simple_mcp.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Example: Use the MCP tools with Ollama
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                # Simple keyword-based tool calling
                if "list files" in user_input.lower():
                    result = await session.call_tool("list_files_tool", {"path": "."})
                    print("Files:", result.content)
                elif "read" in user_input.lower() and ("content" in user_input.lower() or "file" in user_input.lower()):
                    # Extract filename from the prompt or ask for it
                    words = user_input.split()
                    filename = None
                    for word in words:
                        if "." in word:  # Simple check for filename with extension
                            filename = word
                            break
                    if not filename:
                        filename = input("Enter filename: ")
                    result = await session.call_tool("read_file_tool", {"filename": filename})
                    print("File content:", result.content)
                elif "edit" in user_input.lower() or "create" in user_input.lower():
                    path = input("Enter file path: ")
                    old_str = input("Enter old string (empty for new file): ")
                    new_str = input("Enter new string: ")
                    result = await session.call_tool("edit_file_tool", {"path": path, "old_str": old_str, "new_str": new_str})
                    print("Result:", result.content)
                else:
                    # Send to Ollama for general chat
                    response = ollama.chat(
                        model='mistral-nemo:12b',
                        messages=[{'role': 'user', 'content': user_input}]
                    )
                    print("Assistant:", response['message']['content'])

if __name__ == "__main__":
    asyncio.run(main())