# UAB Research Computing Documentation MCP Server - Quick Start

## What You Have

A complete, ready-to-use MCP server that provides AI assistants (like Claude) with access to UAB Research Computing documentation.

## Files Included

1. **uab_docs_server.py** - The main MCP server implementation
2. **pyproject.toml** - Project configuration and dependencies
3. **README.md** - Complete user documentation
4. **CONTRIBUTING.md** - Developer guide for contributing
5. **CLAUDE_DESKTOP_CONFIG.md** - Configuration examples for Claude Desktop
6. **test_server.py** - Test script to verify functionality
7. **setup.sh** - Automated setup for macOS/Linux
8. **setup.ps1** - Automated setup for Windows
9. **.gitignore** - Git ignore configuration

## 5-Minute Setup Guide

### Option 1: Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

The script will:
- ✅ Verify Python 3.10+ is installed
- ✅ Install uv package manager if needed
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Run tests to verify everything works
- ✅ Show you the exact configuration for Claude Desktop

### Option 2: Manual Setup

1. **Install uv:**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Setup the project:**
   ```bash
   cd /path/to/uab-rc-docs-mcp-server
   uv venv
   source .venv/bin/activate  # macOS/Linux
   # OR
   .venv\Scripts\Activate.ps1  # Windows
   
   uv pip install -e .
   ```

3. **Test it:**
   ```bash
   python test_server.py
   ```

## Configure Claude Desktop

1. **Open Claude Desktop config file:**
   - macOS/Linux: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add this configuration:**
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
   
   **Important:** Replace `/ABSOLUTE/PATH/TO/uab-rc-docs-mcp-server` with the actual path!

3. **Restart Claude Desktop**

4. **Verify connection:**
   - Look for 🔌 icon in bottom right
   - Click it to see "uab-research-computing" server
   - Should show 5 available tools

## Available Tools

Once connected, the MCP server provides these tools:

### 1. search_documentation
Search UAB RC documentation for specific topics.

**Example queries:**
- "Search the UAB docs for SLURM tutorials"
- "Find information about GPU computing on Cheaha"
- "How do I submit a job?"

### 2. get_documentation_page
Retrieve the full content of a specific documentation page.

**Example queries:**
- "Get the page about storage systems"
- "Show me the quick start guide"

### 3. get_support_info
Get support contact information and office hours.

**Example queries:**
- "How do I get help from UAB Research Computing?"
- "What are the office hours?"

### 4. list_documentation_sections
List all main sections in the documentation.

**Example queries:**
- "What topics are covered in the UAB RC docs?"
- "Show me the documentation structure"

### 5. get_cheaha_quick_start
Get quick start information for Cheaha HPC cluster.

**Example queries:**
- "How do I get started with Cheaha?"
- "What is Cheaha?"

## Example Usage in Claude

After setup, you can ask Claude questions like:

- "Search the UAB Research Computing docs for information about Python"
- "How do I submit a SLURM job on Cheaha?"
- "What storage options are available at UAB RC?"
- "Show me the quick start guide for Cheaha"
- "What are the office hours for getting help?"
- "Find documentation about using GPUs"

## Troubleshooting

### Server doesn't appear in Claude Desktop
1. Check that the path is absolute (not relative)
2. Verify `uv` is installed: `which uv` (macOS/Linux) or `where uv` (Windows)
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

### "Command not found" error
- Use the full path to `uv` in the config
- Find it with: `which uv` (macOS/Linux) or `where uv` (Windows)

### Search returns no results
- GitHub API has rate limits (60 requests/hour without auth)
- Try searching with different terms
- Check that you have internet connectivity

### Tests fail
- Ensure Python 3.10+ is installed
- Verify all dependencies installed: `uv pip install -e .`
- Check for network connectivity

## Key Features

✅ **5 specialized tools** for UAB RC documentation
✅ **Search functionality** via GitHub API
✅ **Direct page retrieval** from documentation site
✅ **Support information** always up-to-date
✅ **Quick start guides** for new users
✅ **Comprehensive error handling**
✅ **Follows MCP best practices**
✅ **Easy to extend** with new tools

## Architecture

- **FastMCP framework** - Simplifies MCP server development
- **STDIO transport** - Standard communication with MCP clients
- **Async/await** - Efficient I/O operations
- **GitHub API** - Searches the documentation repository
- **HTTP fetching** - Retrieves page content directly

## Next Steps

1. **Run the setup script** to get started
2. **Configure Claude Desktop** with the absolute path
3. **Test the connection** by asking Claude about UAB RC
4. **Explore the documentation** through natural language queries
5. **Contribute improvements** using CONTRIBUTING.md

## Resources

- **UAB RC Documentation:** https://docs.rc.uab.edu
- **Cheaha Access:** https://rc.uab.edu
- **Model Context Protocol:** https://modelcontextprotocol.io
- **FastMCP:** https://github.com/jlowin/fastmcp

## Support

- **This MCP Server:** See README.md and CONTRIBUTING.md
- **UAB Research Computing:** https://docs.rc.uab.edu/help/support
- **MCP Protocol:** https://modelcontextprotocol.io

## Success Indicators

You'll know it's working when:
- ✅ Setup script completes without errors
- ✅ Tests pass successfully
- ✅ Server appears in Claude Desktop (🔌 icon)
- ✅ Claude can answer questions about UAB RC
- ✅ You see "uab-research-computing" with 5 tools

That's it! You're ready to make UAB Research Computing documentation accessible through AI assistance.

---

**Built for the UAB Research Computing community**
