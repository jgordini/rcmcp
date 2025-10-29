# Setup Checklist - UAB Research Computing MCP Server

Use this checklist to ensure a successful installation and configuration.

## 📋 Pre-Installation Checklist

- [ ] Python 3.10+ is installed
  - Check with: `python3 --version` or `python --version`
  - Download from: https://www.python.org/downloads/

- [ ] Internet connection is available
  - Needed for downloading dependencies
  - Needed for accessing documentation

- [ ] Have write access to installation directory
  - Can create files and folders
  - Can install packages

- [ ] Claude Desktop is installed (for usage)
  - Download from: https://claude.ai/download
  - Can be installed later

## 📥 Installation Checklist

### Option 1: Automated Setup (Recommended)

- [ ] Navigate to package directory
- [ ] Run setup script
  - macOS/Linux: `./setup.sh`
  - Windows: `.\setup.ps1`
- [ ] Setup completes without errors
- [ ] See green checkmarks (✅) for all steps
- [ ] Tests pass successfully
- [ ] Note the configuration shown at the end

### Option 2: Manual Setup

- [ ] Install uv package manager
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- [ ] Restart terminal after uv installation
- [ ] Verify uv: `uv --version`
- [ ] Create virtual environment: `uv venv`
- [ ] Activate virtual environment
  - macOS/Linux: `source .venv/bin/activate`
  - Windows: `.venv\Scripts\Activate.ps1`
- [ ] See `(.venv)` in terminal prompt
- [ ] Install dependencies: `uv pip install -e .`
- [ ] Run tests: `python test_server.py`
- [ ] All tests pass

## 📝 Configuration Checklist

### Getting Required Paths

- [ ] Find uv executable path
  - macOS/Linux: `which uv`
  - Windows: `where uv`
  - Write it down: ___________________

- [ ] Find absolute path to server directory
  - Navigate to directory
  - macOS/Linux: `pwd`
  - Windows: `cd` (Command Prompt) or `Get-Location` (PowerShell)
  - Write it down: ___________________

### Configuring Claude Desktop

- [ ] Locate config file
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

- [ ] Open config file in text editor

- [ ] Add server configuration:
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "/full/path/to/uv",
      "args": [
        "--directory",
        "/full/path/to/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

- [ ] Replace `/full/path/to/uv` with actual uv path
- [ ] Replace `/full/path/to/uab-rc-docs-mcp-server` with actual directory path
- [ ] Verify JSON syntax is valid (no trailing commas)
- [ ] Save the file

### Windows-Specific Configuration Checks

- [ ] Paths use double backslashes: `C:\\Users\\...`
  - Or forward slashes: `C:/Users/...`
- [ ] No single backslashes in paths
- [ ] File extension included: `.exe` for uv.exe

## ✅ Verification Checklist

### Starting Claude Desktop

- [ ] Completely quit Claude Desktop (if running)
- [ ] Start Claude Desktop fresh
- [ ] Look for 🔌 icon in bottom right corner
- [ ] Click 🔌 icon

### Checking Server Connection

- [ ] "uab-research-computing" appears in server list
- [ ] Shows "5 tools" or similar indicator
- [ ] No error messages
- [ ] Status shows connected/active

### Testing Functionality

- [ ] Start a new conversation in Claude
- [ ] Ask: "What tools are available from UAB Research Computing?"
- [ ] Claude lists 5 tools:
  - [ ] search_documentation
  - [ ] get_documentation_page
  - [ ] get_support_info
  - [ ] list_documentation_sections
  - [ ] get_cheaha_quick_start

### Testing Real Queries

Test each of these:

- [ ] "Search the UAB Research Computing docs for SLURM tutorials"
  - Returns search results with links
  
- [ ] "How do I get support from UAB Research Computing?"
  - Returns support information
  
- [ ] "What topics are covered in the UAB RC documentation?"
  - Lists documentation sections
  
- [ ] "Show me the Cheaha quick start guide"
  - Returns quick start information
  
- [ ] "Find information about GPU computing at UAB"
  - Searches and returns relevant information

## 🐛 Troubleshooting Checklist

### If Server Doesn't Appear

- [ ] Config file path is correct
- [ ] JSON syntax is valid
- [ ] Paths are absolute (not relative)
- [ ] uv path is correct
- [ ] Server directory path is correct
- [ ] Claude Desktop was restarted (not just closed)
- [ ] No typos in configuration

### If Tools Don't Work

- [ ] Virtual environment is created
- [ ] Dependencies are installed
- [ ] Test script passes: `python test_server.py`
- [ ] Internet connection is working
- [ ] No firewall blocking connections

### If Searches Return Nothing

- [ ] Internet connection is working
- [ ] GitHub API is accessible
- [ ] Not hitting rate limit (60 requests/hour)
- [ ] Search terms are reasonable
- [ ] Try different search terms

## 📊 Success Indicators

You know everything is working when:

- [x] Setup script completed without errors
- [x] Tests pass successfully
- [x] Server appears in Claude Desktop 🔌 menu
- [x] Shows 5 tools
- [x] Can list available tools
- [x] Search queries return results
- [x] Support info is retrieved
- [x] Documentation sections are listed
- [x] Quick start guide appears
- [x] Claude can answer UAB RC questions

## 🎯 Final Checklist

- [ ] All installation steps completed
- [ ] Configuration is correct
- [ ] Server is connected
- [ ] All tools work
- [ ] Can perform searches
- [ ] Can get documentation
- [ ] Can get support info
- [ ] Ready to use in daily work!

## 📚 Resources Used

Check off as you reference them:

- [ ] START_HERE.md - Initial orientation
- [ ] QUICK_START.md - Fast setup guide
- [ ] INSTALLATION_GUIDE.md - Detailed instructions
- [ ] README.md - Full documentation
- [ ] CLAUDE_DESKTOP_CONFIG.md - Configuration help
- [ ] ARCHITECTURE.md - Understanding how it works
- [ ] CONTRIBUTING.md - Adding features (if needed)

## 🎉 Completion

Date completed: _______________

Time taken: _______________

Notes:
_________________________________
_________________________________
_________________________________

## 🔄 Post-Installation

Things to do after successful installation:

- [ ] Bookmark https://docs.rc.uab.edu for reference
- [ ] Familiarize yourself with available tools
- [ ] Try various types of queries
- [ ] Share with colleagues (if appropriate)
- [ ] Consider contributing improvements
- [ ] Keep documentation handy for troubleshooting

## 🆘 If You Need Help

Before asking for help, verify you've:

- [ ] Read QUICK_START.md
- [ ] Read INSTALLATION_GUIDE.md
- [ ] Checked troubleshooting sections
- [ ] Verified all paths are correct
- [ ] Confirmed JSON syntax is valid
- [ ] Restarted Claude Desktop
- [ ] Tested with `python test_server.py`

If still having issues:

- Review INSTALLATION_GUIDE.md troubleshooting
- Check Claude Desktop logs
- Verify all checklist items above
- Re-run setup script

---

**Remember:** The most common issues are:
1. Using relative paths instead of absolute paths
2. Not restarting Claude Desktop after configuration
3. Invalid JSON syntax (trailing commas, missing quotes)
4. Wrong path to uv or server directory

**Tip:** If in doubt, re-run the setup script - it will show you the exact configuration to use!

---

**Good luck! You've got this!** 🚀
