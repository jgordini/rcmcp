# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides AI assistants with access to the University of Alabama at Birmingham's Research Computing documentation. The server is built with Python 3.10+ and FastMCP, using STDIO transport to communicate with MCP clients like Claude Desktop.

## Development Commands

### Environment Setup
```bash
# Install dependencies and set up virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Testing
```bash
# Run all automated tests
python test_server.py

# Run interactive testing mode
python test_server.py interactive

# Test the server directly
uv run uab_docs_server.py
```

### Running the Server
```bash
# Start the MCP server (for direct testing or development)
uv run uab_docs_server.py
```

Note: The server uses STDIO transport and is designed to be launched by MCP clients (like Claude Desktop). When running directly, it will wait for JSON-RPC messages on stdin.

## Code Architecture

### Core Design Principles

1. **STDIO Transport**: The server uses stdin/stdout for JSON-RPC communication. This means:
   - **NEVER** use `print()` statements - they corrupt the STDIO transport
   - All logging must go to stderr via the `logger` object
   - All output for MCP clients is returned as strings from tool functions

2. **Async-First**: All tools and HTTP requests use async/await patterns. The server uses `httpx.AsyncClient` for all network requests.

3. **Tool-Based Architecture**: Functionality is exposed through FastMCP tools decorated with `@mcp.tool()`. Each tool:
   - Has comprehensive docstrings (first line is brief description)
   - Uses type hints for all parameters and return values
   - Returns formatted strings (typically markdown)
   - Handles errors gracefully with try-except blocks

### File Structure

- `uab_docs_server.py` - Main MCP server with 5 tools
- `test_server.py` - Test harness for validating functionality
- `pyproject.toml` - Dependencies and project metadata
- Setup scripts (`setup.sh`, `setup.ps1`) - Automated installation

### Data Flow

```
MCP Client (Claude Desktop)
    ↓ (JSON-RPC over STDIO)
FastMCP Server (uab_docs_server.py)
    ↓ (Async HTTP requests)
External APIs:
    - GitHub API (code search)
    - docs.rc.uab.edu (documentation pages)
```

### Available Tools

1. `search_documentation` - Search docs via GitHub API
2. `get_documentation_page` - Fetch full page content
3. `get_support_info` - Get support contact information
4. `list_documentation_sections` - Show documentation structure
5. `get_cheaha_quick_start` - Quick start guide for Cheaha HPC

## Critical Development Rules

### Logging and Output
- **Always** use `logger.info()`, `logger.error()`, etc. for logging
- **Never** use `print()` statements in the server code
- Test scripts can use `print()` since they don't use STDIO transport

### Error Handling
- Wrap all tool implementations in try-except blocks
- Return user-friendly error messages as strings
- Log detailed errors to stderr using `logger.error()`
- Never expose sensitive information in error messages

### Adding New Tools
When adding a new tool to `uab_docs_server.py`:

```python
@mcp.tool()
async def tool_name(param: str, optional_param: int = 10) -> str:
    """
    Brief one-line description.
    
    Extended description explaining use cases and behavior.
    
    Args:
        param: Description of parameter
        optional_param: Description with default value
    
    Returns:
        Description of return value
    """
    try:
        # Implementation using async HTTP calls
        result = await make_http_request(url)
        return formatted_string_result
    except Exception as e:
        logger.error(f"Error in tool_name: {e}")
        return f"Error: {str(e)}"
```

### HTTP Requests
- Use `make_http_request()` helper function for consistency
- Always set `User-Agent` header
- Use 30-second timeout
- Enable `follow_redirects=True`
- Handle both JSON and text responses

## Configuration for MCP Clients

### Claude Desktop Configuration
The server is configured in `claude_desktop_config.json`:

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/rcmcp",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

Must restart Claude Desktop after configuration changes.

## External Resources

### Documentation Sources
- UAB RC Docs: https://docs.rc.uab.edu
- Cheaha Portal: https://rc.uab.edu
- GitHub Repo: https://github.com/uabrc/uabrc.github.io

### API Endpoints
- GitHub Code Search: `https://api.github.com/search/code`
- Rate Limits: 60 requests/hour (unauthenticated), 5000/hour (authenticated)

### MCP Protocol
- Homepage: https://modelcontextprotocol.io
- FastMCP: https://github.com/jlowin/fastmcp

## Troubleshooting

### Server Issues
- Check that Python 3.10+ is installed: `python --version`
- Verify `uv` is available: `which uv` or `where uv`
- Test server directly: `uv run uab_docs_server.py`
- Check Claude Desktop logs:
  - macOS: `~/Library/Logs/Claude/`
  - Windows: `%APPDATA%\Claude\logs\`

### Common Pitfalls
1. Using `print()` in server code breaks STDIO transport
2. Forgetting to use absolute paths in Claude Desktop config
3. Not restarting Claude Desktop after config changes
4. GitHub API rate limits (60/hour without authentication)
5. Mixing sync and async code patterns

## Dependencies

Core dependencies (from `pyproject.toml`):
- `mcp[cli]>=1.2.0` - FastMCP framework
- `httpx>=0.25.0` - Async HTTP client

Dev dependencies:
- `pytest>=7.0.0`
- `pytest-asyncio>=0.21.0`

## Code Style

- Follow PEP 8 conventions
- Use type hints for all function parameters and returns
- Maximum line length: 100 characters (flexible)
- Use double quotes for strings
- Document all functions with comprehensive docstrings
- Organize imports: standard library → third-party → local
