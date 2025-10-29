# Contributing to UAB RC Documentation MCP Server

Thank you for your interest in contributing to the UAB Research Computing Documentation MCP Server! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding New Tools](#adding-new-tools)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Best Practices](#best-practices)

## Getting Started

Before contributing, please:

1. Familiarize yourself with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
2. Review the [UAB Research Computing documentation](https://docs.rc.uab.edu)
3. Read the [UAB RC documentation contributor guide](https://docs.rc.uab.edu/contributing/contributor_guide/)
4. Understand the current implementation by reviewing the code

## Development Setup

### Prerequisites

- Python 3.10 or higher
- `uv` package manager
- Git

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd uab-rc-docs-mcp-server
   ```

2. **Run the setup script:**
   
   **macOS/Linux:**
   ```bash
   ./setup.sh
   ```
   
   **Windows:**
   ```powershell
   .\setup.ps1
   ```

3. **Activate the virtual environment:**
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```
   
   **Windows:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Run tests to verify setup:**
   ```bash
   python test_server.py
   ```

## Project Structure

```
uab-rc-docs-mcp-server/
├── uab_docs_server.py         # Main MCP server implementation
├── test_server.py              # Test script for manual testing
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # User documentation
├── CONTRIBUTING.md             # This file
├── CLAUDE_DESKTOP_CONFIG.md    # Configuration examples
├── setup.sh                    # Setup script for macOS/Linux
├── setup.ps1                   # Setup script for Windows
├── .gitignore                  # Git ignore rules
└── .venv/                      # Virtual environment (not in repo)
```

## Adding New Tools

### Tool Structure

Tools are defined using the `@mcp.tool()` decorator. Here's the structure:

```python
@mcp.tool()
async def tool_name(param1: str, param2: int = 10) -> str:
    """
    Brief description of what the tool does (first line).
    
    Extended description providing more context about the tool's purpose,
    use cases, and any important information users should know.
    
    Args:
        param1: Description of the first parameter
        param2: Description of the second parameter (default: 10)
    
    Returns:
        Description of what the tool returns
    """
    # Implementation
    try:
        # Your logic here
        result = "..."
        return result
    except Exception as e:
        logger.error(f"Error in tool_name: {e}")
        return f"Error: {str(e)}"
```

### Tool Guidelines

1. **Naming:**
   - Use descriptive snake_case names
   - Follow the pattern: verb_noun (e.g., `search_documentation`, `get_page`)

2. **Documentation:**
   - First line: Brief, one-line description
   - Extended description: Provide context and use cases
   - Args: Document each parameter with type and description
   - Returns: Describe what is returned

3. **Type Hints:**
   - Always use type hints for parameters and return values
   - Use `str`, `int`, `float`, `bool`, `list`, `dict` as appropriate
   - Use `Optional[type]` for optional parameters

4. **Error Handling:**
   - Wrap logic in try-except blocks
   - Log errors to stderr using `logger.error()`
   - Return user-friendly error messages
   - Never use `print()` statements (STDIO servers)

5. **Return Format:**
   - Always return strings
   - Format output in a clear, readable way
   - Use markdown formatting for structure
   - Include relevant URLs and references

### Example: Adding a New Tool

Let's say we want to add a tool to check SLURM queue status:

```python
@mcp.tool()
async def get_slurm_queue_info() -> str:
    """
    Get information about SLURM job queues on Cheaha.
    
    This tool provides details about the available SLURM partitions,
    their configurations, and current status. Useful for understanding
    which queue to submit jobs to.
    
    Returns:
        Formatted information about SLURM queues including partition names,
        time limits, node counts, and submission guidelines
    """
    try:
        # Fetch information from documentation or API
        url = f"{DOCS_BASE_URL}/slurm/queues"
        content = await make_http_request(url)
        
        if content is None:
            return "Unable to fetch SLURM queue information. Please check the documentation directly."
        
        # Format and return the information
        result = f"""
# SLURM Queue Information

{content}

---
**Source:** {url}
**For real-time queue status:** Use `sinfo` command on Cheaha
"""
        return result
        
    except Exception as e:
        logger.error(f"Error fetching SLURM queue info: {e}")
        return f"Error: Unable to retrieve SLURM queue information. {str(e)}"
```

## Testing

### Manual Testing

Use the test script to verify your changes:

```bash
# Run all tests
python test_server.py

# Run interactive testing
python test_server.py interactive
```

### Testing in Claude Desktop

1. Configure the server in Claude Desktop (see README.md)
2. Restart Claude Desktop
3. Test your new tool by asking relevant questions
4. Verify the tool appears in the available tools list (🔌 icon)

### Test Checklist

Before submitting changes, ensure:

- [ ] The server starts without errors
- [ ] All existing tools still work
- [ ] New tools are properly documented
- [ ] Error handling is implemented
- [ ] No `print()` statements are used
- [ ] Logging uses `logger` to stderr
- [ ] The test script runs successfully
- [ ] The tool works in Claude Desktop

## Code Style

### General Guidelines

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Keep functions focused on a single responsibility
- Add comments for complex logic
- Use type hints throughout

### Formatting

- Use 4 spaces for indentation
- Maximum line length: 100 characters (flexible for readability)
- Use double quotes for strings
- Add blank lines between functions

### Imports

Organize imports in this order:
1. Standard library imports
2. Third-party imports
3. Local imports

```python
from typing import Any
import logging
import httpx
from mcp.server.fastmcp import FastMCP
```

## Submitting Changes

### Before Submitting

1. Test your changes thoroughly
2. Update documentation if needed
3. Ensure all tests pass
4. Check for any logging statements that go to stdout

### Commit Messages

Use clear, descriptive commit messages:

```
Add tool to fetch SLURM queue information

- Implements get_slurm_queue_info() tool
- Fetches and formats SLURM partition details
- Includes error handling and documentation
- Updates README with new tool description
```

### Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push to your fork
6. Open a pull request with:
   - Clear description of changes
   - Motivation for the changes
   - Testing performed
   - Screenshots (if UI changes)

## Best Practices

### MCP Server Development

1. **Never Write to stdout:**
   - STDIO transport uses stdout for JSON-RPC messages
   - Use `logger` for all logging (writes to stderr)
   - No `print()` statements

2. **Handle Errors Gracefully:**
   - Always catch exceptions
   - Return meaningful error messages
   - Log errors for debugging
   - Don't expose sensitive information

3. **Provide Rich Responses:**
   - Format responses with markdown
   - Include relevant links and references
   - Add context and explanations
   - Make responses actionable

4. **Optimize for AI Usage:**
   - Clear, structured output
   - Consistent formatting
   - Complete information
   - Helpful next steps

### UAB RC Documentation Integration

1. **Stay Current:**
   - Regularly check for documentation updates
   - Update tool descriptions to match documentation
   - Test against the live documentation site

2. **Respect the Documentation:**
   - Don't reproduce entire pages unnecessarily
   - Provide links to original content
   - Maintain attribution

3. **Support Multiple Use Cases:**
   - Consider different user levels (beginner to expert)
   - Provide paths for more information
   - Link related resources

## Questions or Issues?

- **For MCP Server issues:** Open an issue in this repository
- **For UAB RC documentation:** Contact UAB Research Computing support
- **For MCP protocol questions:** See [MCP documentation](https://modelcontextprotocol.io)

## License

By contributing to this project, you agree that your contributions will follow the same license terms as the project.

## Acknowledgments

Thank you for contributing to making UAB Research Computing resources more accessible through AI assistance!
