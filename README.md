# UAB Research Computing Documentation MCP Server

An MCP (Model Context Protocol) server that provides AI assistants with access to the University of Alabama at Birmingham's Research Computing documentation.

## Overview

This MCP server allows AI applications like Claude to search and retrieve information from UAB's Research Computing documentation (https://docs.rc.uab.edu), including:

- **Cheaha HPC cluster documentation** - High-performance computing resources and usage guides
- **Getting support** - Office hours, contact information, and support channels
- **Software and tools** - Available applications, modules, and installation guides
- **Storage and data management** - Data storage systems, quotas, and best practices
- **Job scheduling (SLURM)** - Submitting and managing computational jobs
- **Contributing** - How to improve the documentation

## Features

The server provides the following tools:

### 1. `search_documentation`
Search the UAB Research Computing documentation for relevant content.

**Parameters:**
- `query` (string): Search term or phrase
- `max_results` (integer, optional): Maximum results to return (default: 5, max: 10)

**Example:**
```python
search_documentation("slurm tutorial")
search_documentation("gpu computing", max_results=10)
```

### 2. `get_documentation_page`
Retrieve the full content of a specific documentation page.

**Parameters:**
- `page_path` (string): Path to the page (e.g., "getting-started/intro") or full URL

**Example:**
```python
get_documentation_page("getting-started/intro")
get_documentation_page("https://docs.rc.uab.edu/storage/data-management")
```

### 3. `get_support_info`
Get comprehensive support information including office hours, contact methods, and support channels.

**Example:**
```python
get_support_info()
```

### 4. `list_documentation_sections`
List all main sections and categories in the documentation with descriptions.

**Example:**
```python
list_documentation_sections()
```

### 5. `get_cheaha_quick_start`
Get quick start information for accessing and using the Cheaha HPC cluster.

**Example:**
```python
get_cheaha_quick_start()
```

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended)

### Setup

1. **Install uv** (if not already installed):

   **macOS/Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **Windows:**
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Restart your terminal after installation.

2. **Clone or download this repository:**
   ```bash
   cd /path/to/uab-rc-docs-mcp-server
   ```

3. **Create virtual environment and install dependencies:**

   **macOS/Linux:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

   **Windows:**
   ```powershell
   uv venv
   .venv\Scripts\activate
   uv pip install -e .
   ```

## Usage

### Testing the Server Directly

Run the server directly to test it:

```bash
uv run uab_docs_server.py
```

The server will start and listen for MCP protocol messages on standard input/output.

### Using with Claude Desktop

1. **Install Claude Desktop** from https://claude.ai/download

2. **Configure Claude Desktop** to use this MCP server:

   **macOS/Linux:**
   Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "uab-research-computing": {
         "command": "uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/uab-rc-docs-mcp-server",
           "run",
           "uab_docs_server.py"
         ]
       }
     }
   }
   ```

   **Windows:**
   Edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "uab-research-computing": {
         "command": "uv",
         "args": [
           "--directory",
           "C:\\ABSOLUTE\\PATH\\TO\\uab-rc-docs-mcp-server",
           "run",
           "uab_docs_server.py"
         ]
       }
     }
   }
   ```

   **Important:** Replace `/ABSOLUTE/PATH/TO/uab-rc-docs-mcp-server` with the actual absolute path to this directory.

3. **Restart Claude Desktop** to load the new configuration.

4. **Verify the connection** in Claude Desktop:
   - Look for the 🔌 icon in the bottom right
   - Click it to see connected MCP servers
   - "uab-research-computing" should appear in the list

### Using with Other MCP Clients

This server follows the standard MCP protocol and can be used with any compatible MCP client. Refer to your client's documentation for configuration instructions.

Popular MCP clients include:
- Claude Desktop
- Continue (VS Code extension)
- Zed
- And many others (see https://modelcontextprotocol.io/clients)

## Example Queries

Once connected, you can ask Claude questions like:

- "Search the UAB Research Computing docs for information about GPU computing"
- "How do I submit a SLURM job on Cheaha?"
- "What storage systems are available at UAB Research Computing?"
- "Show me the quick start guide for Cheaha"
- "What are the office hours for UAB Research Computing support?"
- "Find documentation about using Python on Cheaha"

## Architecture

This MCP server:

1. **Uses FastMCP** - A Python framework that simplifies MCP server development
2. **Searches via GitHub API** - Searches the documentation repository on GitHub
3. **Fetches content via HTTP** - Retrieves documentation pages directly from the website
4. **Follows MCP best practices**:
   - Uses stderr for logging (not stdout, which would corrupt STDIO transport)
   - Provides clear tool descriptions and parameter documentation
   - Handles errors gracefully with informative messages

## Development

### Running Tests

```bash
uv run pytest
```

### Project Structure

```
uab-rc-docs-mcp-server/
├── uab_docs_server.py      # Main MCP server implementation
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # This file
└── .venv/                   # Virtual environment (created during setup)
```

### Adding New Tools

To add a new tool to the server:

1. Add a new function decorated with `@mcp.tool()`
2. Include a comprehensive docstring describing the tool's purpose
3. Use type hints for all parameters
4. Return formatted string results
5. Handle errors gracefully

Example:
```python
@mcp.tool()
async def my_new_tool(param1: str, param2: int = 10) -> str:
    """
    Description of what this tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        Description of what is returned
    """
    # Implementation here
    return "Result"
```

## Troubleshooting

### Server Not Appearing in Claude Desktop

1. Check that the path in `claude_desktop_config.json` is absolute and correct
2. Ensure `uv` is in your PATH (run `which uv` on macOS/Linux or `where uv` on Windows)
3. Restart Claude Desktop completely
4. Check Claude Desktop's logs for errors:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

### Connection Errors

1. Ensure all dependencies are installed: `uv pip install -e .`
2. Test the server directly: `uv run uab_docs_server.py`
3. Check for firewall or network restrictions

### Search Returns No Results

The search tool queries the GitHub API, which has rate limits:
- Unauthenticated: 60 requests per hour
- Authenticated: 5,000 requests per hour

For production use, consider adding GitHub API authentication.

## Resources

- **UAB Research Computing Documentation:** https://docs.rc.uab.edu
- **Cheaha Access Portal:** https://rc.uab.edu
- **Model Context Protocol:** https://modelcontextprotocol.io
- **FastMCP Documentation:** https://github.com/jlowin/fastmcp

## Contributing

To contribute to this MCP server:

1. Follow the UAB Research Computing documentation contributor guide: https://docs.rc.uab.edu/contributing/contributor_guide/
2. Submit issues or pull requests to the appropriate repository
3. Follow Python best practices and maintain compatibility with MCP standards

## License

This MCP server is provided for use with UAB Research Computing resources. Please refer to UAB's policies regarding research computing usage.

## Support

For questions about:
- **UAB Research Computing services:** Contact UAB Research Computing support through https://docs.rc.uab.edu/help/support
- **This MCP server:** Submit issues to the repository maintainers

## Acknowledgments

Built by the UAB Research Computing community to make research computing resources more accessible through AI assistance.
