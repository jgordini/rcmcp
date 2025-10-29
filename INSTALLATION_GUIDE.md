# UAB Research Computing MCP Server - Complete Installation & Usage Guide

## 📖 Table of Contents

1. [Overview](#overview)
2. [What's Included](#whats-included)
3. [Prerequisites](#prerequisites)
4. [Installation Methods](#installation-methods)
5. [Configuration](#configuration)
6. [Testing & Verification](#testing--verification)
7. [Using the Server](#using-the-server)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Topics](#advanced-topics)

---

## Overview

This MCP server enables AI assistants like Claude to access and search the University of Alabama at Birmingham's Research Computing documentation. It provides 5 specialized tools that allow natural language queries about Cheaha HPC cluster, SLURM job submission, storage systems, and more.

**Key Benefits:**
- ✅ Instant access to UAB RC documentation through conversation
- ✅ No need to manually search through documentation
- ✅ Context-aware responses based on actual documentation
- ✅ Always up-to-date with the latest documentation
- ✅ Natural language interface for technical information

---

## What's Included

### 11 Files in This Package

**Core Implementation (3 files):**
1. `uab_docs_server.py` - Main server with 5 MCP tools
2. `pyproject.toml` - Dependencies and project config
3. `test_server.py` - Testing and verification scripts

**Documentation (5 files):**
4. `README.md` - Complete user documentation
5. `QUICK_START.md` - 5-minute setup guide
6. `INDEX.md` - Package overview and file guide
7. `ARCHITECTURE.md` - Technical architecture details
8. `CONTRIBUTING.md` - Developer guide
9. `CLAUDE_DESKTOP_CONFIG.md` - Configuration examples

**Setup Scripts (2 files):**
10. `setup.sh` - Automated setup for macOS/Linux
11. `setup.ps1` - Automated setup for Windows

**Configuration:**
12. `.gitignore` - Git configuration

---

## Prerequisites

### System Requirements

**Required:**
- **Python 3.10 or higher** - Check with: `python3 --version`
- **Internet connection** - For accessing documentation and GitHub API
- **50 MB disk space** - For virtual environment and dependencies

**For Claude Desktop Integration:**
- **Claude Desktop app** - Download from https://claude.ai/download
- **File system access** - To edit configuration file
- **Admin rights** - May be needed to restart Claude Desktop

### Check Your Python Version

```bash
# macOS/Linux
python3 --version

# Windows
python --version
```

You should see: `Python 3.10.x` or higher

### Install Python (if needed)

**macOS:**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11
```

**Windows:**
Download from https://www.python.org/downloads/

---

## Installation Methods

### Method 1: Automated Setup (Recommended) ⭐

The easiest way to get started.

#### macOS/Linux

```bash
# Navigate to the package directory
cd /path/to/uab-rc-docs-mcp-server

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

#### Windows (PowerShell)

```powershell
# Navigate to the package directory
cd C:\path\to\uab-rc-docs-mcp-server

# Run setup (you may need to allow script execution)
.\setup.ps1
```

**What the script does:**
1. ✅ Checks Python version
2. ✅ Installs `uv` package manager
3. ✅ Creates virtual environment
4. ✅ Installs all dependencies
5. ✅ Runs tests
6. ✅ Shows configuration for Claude Desktop

**If successful, you'll see:**
- Green checkmarks (✅) for each step
- Test results showing all tools work
- The exact configuration to use in Claude Desktop

### Method 2: Manual Setup

If you prefer manual control or the automated script fails.

#### Step 1: Install uv Package Manager

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Important:** After installing uv, restart your terminal!

#### Step 2: Verify uv Installation

```bash
# Should show version number
uv --version
```

If not found, check:
- macOS/Linux: Add `~/.local/bin` to PATH
- Windows: Add `%USERPROFILE%\.local\bin` to PATH

#### Step 3: Create Virtual Environment

```bash
# Navigate to package directory
cd /path/to/uab-rc-docs-mcp-server

# Create virtual environment
uv venv
```

#### Step 4: Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your prompt.

#### Step 5: Install Dependencies

```bash
uv pip install -e .
```

This installs:
- `mcp[cli]` - MCP SDK and FastMCP framework
- `httpx` - Async HTTP client

#### Step 6: Verify Installation

```bash
python test_server.py
```

If successful, you'll see test results for all 5 tools.

---

## Configuration

### Finding Paths

Before configuring, you need two paths:

**1. Path to uv executable:**

```bash
# macOS/Linux
which uv

# Windows (Command Prompt)
where uv

# Windows (PowerShell)
Get-Command uv | Select-Object -ExpandProperty Source
```

Example outputs:
- macOS: `/Users/username/.local/bin/uv`
- Linux: `/home/username/.local/bin/uv`
- Windows: `C:\Users\Username\.local\bin\uv.exe`

**2. Absolute path to server directory:**

```bash
# macOS/Linux
cd /path/to/uab-rc-docs-mcp-server
pwd

# Windows (Command Prompt)
cd C:\path\to\uab-rc-docs-mcp-server
cd

# Windows (PowerShell)
cd C:\path\to\uab-rc-docs-mcp-server
Get-Location
```

Write these down - you'll need them!

### Configure Claude Desktop

#### Step 1: Find Config File

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
Claude Desktop is not officially available yet.

#### Step 2: Open Config File

**macOS/Linux (using VS Code):**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows (using VS Code):**
```powershell
code $env:APPDATA\Claude\claude_desktop_config.json
```

**Or use any text editor:**
- macOS: TextEdit
- Windows: Notepad
- Any: VS Code, Sublime Text, etc.

#### Step 3: Add Server Configuration

If the file is empty or doesn't exist, create it with:

```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "/FULL/PATH/TO/uv",
      "args": [
        "--directory",
        "/FULL/PATH/TO/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

If the file already has content, add the `uab-research-computing` entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "uab-research-computing": {
      "command": "/FULL/PATH/TO/uv",
      "args": [
        "--directory",
        "/FULL/PATH/TO/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

**Example Configurations:**

**macOS:**
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "/Users/johndoe/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/johndoe/Documents/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "C:\\Users\\JohnDoe\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\JohnDoe\\Documents\\uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

**Important Notes:**
- ⚠️ Use **absolute paths** (full paths), not relative
- ⚠️ Windows: Use double backslashes (`\\`) or forward slashes (`/`)
- ⚠️ Ensure JSON is valid (no trailing commas, proper quotes)

#### Step 4: Save and Restart

1. Save the configuration file
2. **Completely quit** Claude Desktop (not just close the window)
3. Restart Claude Desktop

---

## Testing & Verification

### Verify Server Connection

1. **Open Claude Desktop**
2. **Start a new conversation**
3. **Look for the 🔌 icon** in the bottom right corner
4. **Click the icon** to see connected servers
5. **Check for "uab-research-computing"** with "5 tools"

If you see this, congratulations! 🎉 The server is connected.

### Test the Tools

Try asking Claude:

```
"What tools are available from UAB Research Computing?"
```

Claude should list 5 tools:
1. search_documentation
2. get_documentation_page
3. get_support_info
4. list_documentation_sections
5. get_cheaha_quick_start

### Test Actual Functionality

Try these example queries:

```
"Search the UAB Research Computing docs for SLURM tutorials"

"How do I submit a job on Cheaha?"

"What storage systems are available?"

"Show me the Cheaha quick start guide"

"What are the office hours for getting help?"
```

If Claude can answer these using the MCP server, everything is working! ✅

---

## Using the Server

### Example Queries

**Getting Started:**
- "How do I get started with Cheaha?"
- "What is Cheaha?"
- "Show me the quick start guide"

**Searching Documentation:**
- "Search for information about GPU computing"
- "Find docs about Python on Cheaha"
- "Search for SLURM array jobs"

**Specific Topics:**
- "How do I submit a SLURM job?"
- "What storage options are available?"
- "How do I load software modules?"
- "What's the process for requesting a GPU?"

**Getting Help:**
- "How do I get support from UAB Research Computing?"
- "What are the office hours?"
- "How do I contact support?"

**Exploring Documentation:**
- "What topics are covered in the documentation?"
- "Show me the documentation structure"
- "What sections are available?"

### Understanding Responses

When you ask a question, Claude will:

1. **Select the appropriate tool** - Based on your query
2. **Call the MCP server** - Execute the tool
3. **Receive structured data** - From the documentation
4. **Synthesize a response** - In natural language
5. **Provide sources** - Links to documentation

### Best Practices

✅ **DO:**
- Ask specific questions
- Request searches for topics you need
- Ask for explanations of concepts
- Request quick start guides
- Ask about support options

❌ **DON'T:**
- Expect real-time cluster status (server provides documentation only)
- Ask for personal account information
- Expect the server to execute jobs
- Request sensitive or privileged information

---

## Troubleshooting

### Server Not Appearing

**Issue:** Server doesn't show up in Claude Desktop's 🔌 icon.

**Solutions:**
1. Check path is absolute (use `pwd` or `cd`)
2. Verify `uv` path is correct (`which uv`)
3. Ensure JSON syntax is valid
4. Restart Claude Desktop completely
5. Check Claude Desktop logs

**Finding Logs:**
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

### Command Not Found

**Issue:** Error about `uv` not found.

**Solutions:**
1. Use full path to `uv` in config
2. Verify `uv` is installed: `uv --version`
3. Reinstall `uv` if needed
4. Check PATH environment variable

### Connection Errors

**Issue:** Server shows but tools fail.

**Solutions:**
1. Run `python test_server.py` to verify
2. Check dependencies: `uv pip list`
3. Reinstall: `uv pip install -e .`
4. Check internet connectivity
5. Verify GitHub API is accessible

### Search Returns Nothing

**Issue:** Searches return no results.

**Solutions:**
1. Try different search terms
2. Check internet connection
3. GitHub API may be rate limited (60 req/hour)
4. Wait a few minutes and try again

### Path Issues on Windows

**Issue:** Paths not recognized in config.

**Solutions:**
1. Use double backslashes: `C:\\Users\\...`
2. Or use forward slashes: `C:/Users/...`
3. Ensure no single backslashes
4. Verify path exists

---

## Advanced Topics

### Adding GitHub API Authentication

To increase rate limits from 60 to 5,000 requests/hour:

1. Create a GitHub personal access token
2. Modify `uab_docs_server.py`:

```python
GITHUB_TOKEN = "your_token_here"

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}
```

### Adding New Tools

See `CONTRIBUTING.md` for detailed instructions on adding new tools.

Basic pattern:
```python
@mcp.tool()
async def my_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

### Using with Other MCP Clients

This server works with any MCP-compatible client:
- Continue (VS Code)
- Zed
- Various other clients

See their documentation for configuration.

### Debugging

Enable debug logging:

```python
# In uab_docs_server.py
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG
    ...
)
```

View logs in Claude Desktop's log directory.

---

## Quick Reference

### Common Commands

```bash
# Test server
python test_server.py

# Interactive testing
python test_server.py interactive

# Find uv path
which uv                    # macOS/Linux
where uv                    # Windows

# Find current directory
pwd                         # macOS/Linux
cd                          # Windows

# Activate virtual environment
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
uv pip install -e .
```

### Important Files

```
uab_docs_server.py          - Main server
test_server.py              - Testing
claude_desktop_config.json  - Configuration
README.md                   - Full documentation
QUICK_START.md              - Fast setup
```

### Key URLs

- **UAB RC Docs:** https://docs.rc.uab.edu
- **Cheaha Portal:** https://rc.uab.edu
- **Claude Desktop:** https://claude.ai/download
- **MCP Docs:** https://modelcontextprotocol.io

---

## Getting Help

**For This MCP Server:**
- Check `README.md` for detailed docs
- See `TROUBLESHOOTING` section above
- Review `CONTRIBUTING.md` for development

**For UAB Research Computing:**
- Visit: https://docs.rc.uab.edu/help/support
- Check office hours
- Submit support ticket

**For MCP Protocol:**
- Official docs: https://modelcontextprotocol.io
- Client-specific documentation

---

## Success Checklist

Use this to verify your installation:

- [ ] Python 3.10+ installed
- [ ] uv package manager installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Tests pass successfully
- [ ] Configuration file updated
- [ ] Absolute paths used
- [ ] Claude Desktop restarted
- [ ] Server appears in 🔌 menu
- [ ] Shows 5 tools
- [ ] Test query works
- [ ] Can search documentation
- [ ] Can get support info

If all items are checked, you're ready to go! 🚀

---

**Questions?** Start with the relevant documentation file or troubleshooting section.

**Ready to contribute?** See `CONTRIBUTING.md`.

**Enjoying the tool?** Share it with other UAB researchers!

---

Built with ❤️ for the UAB Research Computing community
