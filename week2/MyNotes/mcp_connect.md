# MCP Server Setup and Usage

## Prerequisites
- Ollama installed with mistral-nemo:12b model
- Python virtual environment with required packages

## Setup Instructions

1. **Activate virtual environment:**
   ```bash
   cd /Users/stevengong/study/modern-software-dev-assignments
   source venv/bin/activate
   ```

2. **Navigate to MyNotes directory:**
   ```bash
   cd week2/MyNotes
   ```

3. **Run the MCP client:**
   ```bash
   python mcp_client.py
   ```

## Available MCP Tools

The client automatically connects to `simple_mcp.py` server and provides three tools:

### 1. List Files Tool
**Trigger prompts:**
- "list files in the current directory"
- "list files"

### 2. Read File Tool  
**Trigger prompts:**
- "Read the contents of simple_mcp.py"
- "read file simple_mcp.py"
- "read contents of filename.txt"

### 3. Edit File Tool
**Trigger prompts:**
- "edit file" or "create file"
- Will prompt for: file path, old string, new string

## Usage Examples

```
You: list files in the current directory
Files: [list of files and directories]

You: Read the contents of simple_mcp.py  
File content: [full file content]

You: edit file
Enter file path: test.txt
Enter old string (empty for new file): 
Enter new string: Hello World
Result: {'path': '/path/to/test.txt', 'action': 'created_file'}
```

## Exit
Type `quit` to exit the client.