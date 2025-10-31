# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that provides AI assistants with access to the University of Alabama at Birmingham's Research Computing documentation. The server allows Claude and other AI applications to search and retrieve information from UAB's Research Computing docs (https://docs.rc.uab.edu).

## Development Commands

### Environment Setup
```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Or use the automated setup script
./setup.sh    # macOS/Linux
./setup.ps1   # Windows
```

### Running and Testing
```bash
# Run the MCP server directly
uv run uab_docs_server.py

# Run tests
python test_server.py

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests with pytest (if using dev dependencies)
uv run pytest
```

### Lint and Code Quality
The project uses Python type hints and follows standard Python conventions. No specific linting commands are configured, but follow PEP 8 standards.

## Architecture

### Core Components

1. **Main Server (`uab_docs_server.py`)**: FastMCP-based server that implements the MCP protocol
2. **Tools**: Five main MCP tools for documentation access:
   - `search_documentation`: Search docs via GitHub API
   - `get_documentation_page`: Retrieve full page content
   - `get_support_info`: UAB RC support information
   - `list_documentation_sections`: Documentation structure overview
   - `get_cheaha_quick_start`: Quick start guide for Cheaha HPC

3. **Prompts**: Pre-defined prompts to help users interact with the server effectively

### Key Technical Details

- **Transport**: Uses stdio transport for MCP communication
- **HTTP Client**: `httpx` for async HTTP requests to GitHub API and raw content
- **GitHub Integration**: Searches the `uabrc/uabrc.github.io` repository
- **URL Handling**: Converts GitHub repository paths to docs.rc.uab.edu URLs
- **Error Handling**: Graceful handling of HTTP errors, rate limits, and missing content
- **Logging**: Uses stderr for logging (required for stdio MCP servers)

### Data Flow

1. Search requests go to GitHub API (`api.github.com/search/code`)
2. Content retrieval uses raw GitHub content (`raw.githubusercontent.com`)
3. URLs are transformed from repository structure to documentation site structure
4. Results are formatted as markdown with metadata

## Configuration Files

- **`pyproject.toml`**: Project metadata, dependencies, and build configuration
- **`setup.sh`/`setup.ps1`**: Platform-specific setup scripts
- **`smithery.json`/`smithery.yaml`**: Smithery MCP registry configuration
- **`Dockerfile`**: Container configuration for deployment

## Environment Variables

- **`GITHUB_TOKEN`** (optional): GitHub API token for higher rate limits (5000/hour vs 60/hour)

## Claude Desktop Integration

The server is designed to integrate with Claude Desktop via MCP. Configuration goes in:
- **macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Example config:
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/repo", "run", "uab_docs_server.py"]
    }
  }
}
```

## Development Guidelines

### Adding New Tools
1. Use `@mcp.tool()` decorator with annotations
2. Include comprehensive docstrings
3. Use async functions for HTTP operations
4. Return formatted strings (markdown preferred)
5. Handle errors gracefully with informative messages

### Error Handling Patterns
- Use structured error messages that identify the failure point
- Log errors to stderr, not stdout (stdio transport requirement)
- Provide fallback options when possible (e.g., try different GitHub branches)
- Include rate limit guidance for GitHub API errors

### URL Path Handling
The server converts between different URL formats:
- Repository paths: `docs/cheaha/slurm/tutorial.md`
- Documentation URLs: `https://docs.rc.uab.edu/cheaha/slurm/tutorial`
- Raw content URLs: `https://raw.githubusercontent.com/uabrc/uabrc.github.io/main/docs/cheaha/slurm/tutorial.md`

## Dependencies

### Core Dependencies
- `mcp[cli]>=1.2.0`: MCP protocol implementation
- `httpx>=0.25.0`: Async HTTP client

### Development Dependencies
- `pytest>=7.0.0`: Testing framework
- `pytest-asyncio>=0.21.0`: Async test support

## File Structure

- **Server files**: `uab_docs_server*.py` (main and variants)
- **Test files**: `test_server.py`
- **Setup scripts**: `setup.sh`, `setup.ps1`
- **Config**: `pyproject.toml`, `smithery.*`, `Dockerfile`
- **Documentation**: `README.md`, `Bak/` directory with additional docs