# UAB Research Computing Documentation MCP Server - Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Claude Desktop App                     │  │
│  │                                                           │  │
│  │  User asks: "How do I submit a SLURM job on Cheaha?"    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ MCP Protocol (STDIO)
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     MCP SERVER (This Package)                   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         uab_docs_server.py (FastMCP Server)           │    │
│  │                                                        │    │
│  │  Tool 1: search_documentation()                       │    │
│  │  Tool 2: get_documentation_page()                     │    │
│  │  Tool 3: get_support_info()                           │    │
│  │  Tool 4: list_documentation_sections()                │    │
│  │  Tool 5: get_cheaha_quick_start()                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         HTTP Client (httpx + async)                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌────────────────────────────┐
│    GitHub API (Search)    │   │   UAB RC Docs Website      │
│                           │   │                            │
│  api.github.com/          │   │  https://docs.rc.uab.edu   │
│  search/code              │   │                            │
│                           │   │  Direct HTTP requests      │
│  Returns:                 │   │  for page content          │
│  - File paths             │   │                            │
│  - Snippets               │   │  Returns:                  │
│  - Repository links       │   │  - Full page content       │
└───────────────────────────┘   │  - Markdown format         │
                                └────────────────────────────┘
```

## Component Flow

### 1. User Interaction
```
User → Claude Desktop → Natural language query
Example: "How do I use SLURM on Cheaha?"
```

### 2. MCP Protocol Communication
```
Claude Desktop → MCP Server (STDIO)
- Sends tool request via JSON-RPC
- Includes query parameters
- Waits for response
```

### 3. Tool Execution
```
MCP Server → Appropriate tool function
- Parses parameters
- Validates input
- Executes async logic
```

### 4. Data Retrieval
```
Tool → External API/Website
- GitHub API for search
- Direct HTTP for pages
- Async requests
- Error handling
```

### 5. Response Formatting
```
Tool → Formatted response
- Markdown structure
- Relevant links
- Clear information
- Error messages if needed
```

### 6. Result Delivery
```
MCP Server → Claude Desktop → User
- Returns formatted string
- Claude processes and displays
- User sees natural language response
```

## Data Flow Example

### Example: Searching for SLURM Documentation

```
1. User Query
   │
   └─→ "Search for SLURM tutorials"
       │
2. Claude Desktop
   │
   └─→ MCP Request: search_documentation("SLURM tutorials")
       │
3. MCP Server
   │
   ├─→ Parse query
   ├─→ Build GitHub API request
   └─→ Execute async HTTP call
       │
4. GitHub API
   │
   ├─→ Search: "SLURM tutorials repo:uabrc/uabrc.github.io"
   └─→ Return matching files
       │
5. MCP Server
   │
   ├─→ Parse results
   ├─→ Format as markdown
   └─→ Return to Claude
       │
6. Claude Desktop
   │
   └─→ Present to user in natural language
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Application Layer             │
│                                         │
│  • Claude Desktop (Client)              │
│  • User Interface                       │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│          Protocol Layer (MCP)           │
│                                         │
│  • JSON-RPC over STDIO                  │
│  • Tool definitions                     │
│  • Request/Response handling            │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Server Implementation           │
│                                         │
│  • Python 3.10+                         │
│  • FastMCP framework                    │
│  • Async/await patterns                 │
│  • Type hints                           │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Network Layer                   │
│                                         │
│  • httpx (HTTP client)                  │
│  • Async I/O                            │
│  • Connection pooling                   │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         External Services               │
│                                         │
│  • GitHub API (search)                  │
│  • UAB RC Docs (content)                │
│  • Rate limiting                        │
└─────────────────────────────────────────┘
```

## Security & Best Practices

```
┌──────────────────────────────────┐
│      Security Measures           │
├──────────────────────────────────┤
│ • HTTPS for all requests         │
│ • User-Agent headers             │
│ • Error message sanitization    │
│ • No sensitive data in logs      │
│ • Rate limit handling            │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│      Logging (stderr only)       │
├──────────────────────────────────┤
│ • Application events             │
│ • Error tracking                 │
│ • Debug information              │
│ • Performance metrics            │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│      Error Handling              │
├──────────────────────────────────┤
│ • Try-catch blocks               │
│ • Graceful degradation           │
│ • User-friendly messages         │
│ • Automatic retry logic          │
└──────────────────────────────────┘
```

## Deployment Architecture

```
Development Environment:
┌────────────────────────┐
│  Local Machine         │
│  ├─ Python 3.10+       │
│  ├─ Virtual env (.venv)│
│  ├─ MCP Server code    │
│  └─ Claude Desktop     │
└────────────────────────┘

Production/User Environment:
┌────────────────────────┐
│  User Machine          │
│  ├─ Python 3.10+       │
│  ├─ Virtual env        │
│  ├─ MCP Server         │
│  └─ Claude Desktop     │
│     (Configured)       │
└────────────────────────┘
           │
           ▼ Internet
┌────────────────────────┐
│  External Services     │
│  ├─ GitHub API         │
│  └─ docs.rc.uab.edu    │
└────────────────────────┘
```

## Tool Architecture

Each tool follows this pattern:

```
@mcp.tool() decorator
    │
    ├─→ Function definition with type hints
    │   └─→ Parameters with descriptions
    │
    ├─→ Docstring (triple-quoted)
    │   ├─→ Brief description
    │   ├─→ Detailed explanation
    │   ├─→ Args documentation
    │   └─→ Returns documentation
    │
    ├─→ Implementation
    │   ├─→ Input validation
    │   ├─→ Async HTTP calls
    │   ├─→ Error handling
    │   └─→ Response formatting
    │
    └─→ Return formatted string
```

## Configuration Flow

```
1. Installation
   ├─ Run setup.sh/setup.ps1
   ├─ Install dependencies
   └─ Create virtual environment

2. Configuration
   ├─ Edit claude_desktop_config.json
   ├─ Add server definition
   └─ Specify absolute paths

3. Activation
   ├─ Restart Claude Desktop
   ├─ Server auto-starts
   └─ Tools become available

4. Usage
   ├─ User asks question
   ├─ Claude selects appropriate tool
   ├─ Tool executes
   └─ Response delivered
```

## Performance Characteristics

```
┌─────────────────────────────────────┐
│  Response Times                     │
├─────────────────────────────────────┤
│  • Tool invocation: <100ms          │
│  • GitHub search: 500-2000ms        │
│  • Page fetch: 300-1500ms           │
│  • Total (typical): 1-3 seconds     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Rate Limits                        │
├─────────────────────────────────────┤
│  • GitHub API: 60 req/hour (unauth) │
│  • Direct HTTP: No limit            │
│  • MCP calls: No server limit       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Resource Usage                     │
├─────────────────────────────────────┤
│  • Memory: ~50-100 MB               │
│  • CPU: Minimal (async I/O)         │
│  • Disk: ~50 MB (with deps)         │
│  • Network: Per request basis       │
└─────────────────────────────────────┘
```

---

This architecture provides:
✅ Scalable tool-based access to documentation
✅ Clean separation of concerns
✅ Robust error handling
✅ Async performance
✅ Easy extensibility

For implementation details, see the source code in uab_docs_server.py
