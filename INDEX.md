# UAB Research Computing Documentation MCP Server - Complete Package

## 📦 Package Contents

This package contains everything you need to set up an MCP (Model Context Protocol) server for UAB Research Computing documentation.

### Core Files

| File | Size | Purpose |
|------|------|---------|
| **uab_docs_server.py** | 13 KB | Main MCP server implementation with 5 tools |
| **pyproject.toml** | 493 B | Project dependencies and configuration |
| **test_server.py** | 4.1 KB | Test script to verify functionality |

### Documentation Files

| File | Size | Purpose |
|------|------|---------|
| **README.md** | 8.5 KB | Complete user guide and documentation |
| **QUICK_START.md** | 6.3 KB | 5-minute setup guide |
| **CONTRIBUTING.md** | 9.1 KB | Developer guide for contributors |
| **CLAUDE_DESKTOP_CONFIG.md** | 3.5 KB | Configuration examples for Claude Desktop |

### Setup Scripts

| File | Size | Purpose |
|------|------|---------|
| **setup.sh** | 3.2 KB | Automated setup for macOS/Linux |
| **setup.ps1** | 4.8 KB | Automated setup for Windows |

### Configuration

| File | Size | Purpose |
|------|------|---------|
| **.gitignore** | - | Git ignore rules for the project |

---

## 🚀 Getting Started

**New to MCP?** Start with [QUICK_START.md](QUICK_START.md)

**Ready to install?** Run the setup script:
- macOS/Linux: `./setup.sh`
- Windows: `.\setup.ps1`

**Need help?** See [README.md](README.md) for detailed instructions

**Want to contribute?** Read [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🛠️ What This MCP Server Does

Provides AI assistants (like Claude) with 5 specialized tools to access UAB Research Computing documentation:

### 1. 🔍 search_documentation
Search the documentation for specific topics
- Example: "Find information about SLURM job submission"

### 2. 📄 get_documentation_page
Retrieve complete content from a specific page
- Example: "Get the storage systems page"

### 3. 💬 get_support_info
Get contact information and office hours
- Example: "How do I get support?"

### 4. 📋 list_documentation_sections
View the documentation structure
- Example: "What topics are covered?"

### 5. ⚡ get_cheaha_quick_start
Get Cheaha HPC quick start information
- Example: "How do I start using Cheaha?"

---

## 📊 Technical Details

**Language:** Python 3.10+
**Framework:** FastMCP (MCP SDK)
**Transport:** STDIO
**Dependencies:** httpx for HTTP requests
**API:** GitHub API for search, direct HTTP for pages

**Architecture:**
```
User → Claude Desktop → MCP Server → UAB RC Docs
                ↓
        5 specialized tools
                ↓
        GitHub API + HTTP
```

---

## 📝 File Descriptions

### uab_docs_server.py
The main server implementation featuring:
- 5 MCP tools for documentation access
- Async HTTP request handling
- Error handling and logging
- GitHub API integration
- Clean, documented code following MCP best practices

### test_server.py
Testing utilities including:
- Automated test suite for all tools
- Interactive testing mode
- Verification of functionality
- Usage examples

### setup.sh / setup.ps1
Automated setup scripts that:
- Check Python version (3.10+ required)
- Install uv package manager if needed
- Create virtual environment
- Install dependencies
- Run tests
- Show Claude Desktop configuration

### README.md
Comprehensive documentation covering:
- Installation instructions
- Usage examples
- Tool descriptions
- Troubleshooting guide
- Architecture overview

### QUICK_START.md
Fast-track guide with:
- 5-minute setup process
- Essential configuration steps
- Quick troubleshooting
- Example queries

### CONTRIBUTING.md
Developer guide including:
- Development setup
- How to add new tools
- Code style guidelines
- Testing procedures
- Contribution process

### CLAUDE_DESKTOP_CONFIG.md
Configuration examples for:
- macOS/Linux setup
- Windows setup
- Multiple MCP servers
- Troubleshooting tips

---

## 🎯 Use Cases

**For Researchers:**
- Quick access to HPC documentation
- Find answers about Cheaha cluster
- Learn about available software
- Understand storage options
- Get support information

**For System Administrators:**
- Help users find documentation
- Provide instant answers to common questions
- Reduce support ticket volume
- Improve documentation accessibility

**For Developers:**
- Extend with new tools
- Integrate with other systems
- Build custom workflows
- Learn MCP server development

---

## ✅ Requirements

**System Requirements:**
- Python 3.10 or higher
- Internet connection
- 50 MB disk space

**For Claude Desktop:**
- Claude Desktop app installed
- Configuration file access
- Restart permission

**For Development:**
- Git (for version control)
- Text editor or IDE
- Basic Python knowledge

---

## 🔗 Important Links

**UAB Research Computing:**
- Documentation: https://docs.rc.uab.edu
- Cheaha Portal: https://rc.uab.edu
- GitHub Repo: https://github.com/uabrc/uabrc.github.io

**Model Context Protocol:**
- Official Site: https://modelcontextprotocol.io
- Documentation: https://modelcontextprotocol.io/docs
- Client List: https://modelcontextprotocol.io/clients

**Tools & Frameworks:**
- FastMCP: https://github.com/jlowin/fastmcp
- uv: https://github.com/astral-sh/uv
- Claude Desktop: https://claude.ai/download

---

## 📈 Version History

**v1.0.0** (Current)
- Initial release
- 5 core tools implemented
- Full documentation
- Automated setup scripts
- Comprehensive error handling

---

## 🤝 Support & Community

**For this MCP Server:**
- Read the documentation files
- Check troubleshooting sections
- Review example configurations

**For UAB Research Computing:**
- Visit: https://docs.rc.uab.edu/help/support
- Office Hours: Check documentation
- Email support: Via support portal

**For MCP Protocol:**
- Official Docs: https://modelcontextprotocol.io
- Community: Various MCP client communities

---

## 📄 License

This MCP server is provided for use with UAB Research Computing resources.

---

## 🎉 Ready to Start?

1. **Choose your path:**
   - Quick: Run setup script → Follow prompts
   - Detailed: Read README.md → Manual setup
   
2. **Configure Claude Desktop:**
   - See CLAUDE_DESKTOP_CONFIG.md
   - Use absolute path to server directory
   
3. **Test it out:**
   - Ask Claude about UAB Research Computing
   - Try: "Search the UAB docs for SLURM tutorials"
   
4. **Enjoy AI-powered documentation access!** 🚀

---

**Questions?** Start with QUICK_START.md or README.md

**Want to help?** See CONTRIBUTING.md

**Need support?** Check the troubleshooting sections in the docs

---

Built with ❤️ for the UAB Research Computing community
