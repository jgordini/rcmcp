# Example Claude Desktop Configuration

This file shows example configurations for connecting the UAB Research Computing
Documentation MCP server to Claude Desktop.

## macOS/Linux Configuration

File location: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/your-username/path/to/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

## Windows Configuration

File location: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\path\\to\\uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

## Configuration with Full Path to uv

If `uv` is not in your PATH, use the full path to the uv executable:

### macOS/Linux
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "/Users/your-username/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/your-username/path/to/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

### Windows
```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "C:\\Users\\YourUsername\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\path\\to\\uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    }
  }
}
```

## Multiple MCP Servers

You can configure multiple MCP servers in the same configuration file:

```json
{
  "mcpServers": {
    "uab-research-computing": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/uab-rc-docs-mcp-server",
        "run",
        "uab_docs_server.py"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/your-username/Documents"
      ]
    }
  }
}
```

## Troubleshooting

### Finding the uv executable path

**macOS/Linux:**
```bash
which uv
```

**Windows (Command Prompt):**
```cmd
where uv
```

**Windows (PowerShell):**
```powershell
Get-Command uv | Select-Object -ExpandProperty Source
```

### Finding the absolute path to the server directory

**macOS/Linux:**
```bash
cd /path/to/uab-rc-docs-mcp-server
pwd
```

**Windows (Command Prompt):**
```cmd
cd C:\path\to\uab-rc-docs-mcp-server
cd
```

**Windows (PowerShell):**
```powershell
cd C:\path\to\uab-rc-docs-mcp-server
Get-Location
```

### Common Issues

1. **Server doesn't appear in Claude Desktop:**
   - Verify the JSON syntax is valid (no trailing commas, proper quotes)
   - Ensure the path is absolute, not relative
   - Restart Claude Desktop completely (not just close the window)

2. **"Command not found" error:**
   - Use the full path to the `uv` executable
   - Ensure uv is installed and accessible

3. **Path on Windows:**
   - Use double backslashes (`\\`) or forward slashes (`/`) in JSON
   - Avoid single backslashes as they are escape characters in JSON

## Verifying the Configuration

After configuring Claude Desktop:

1. Restart Claude Desktop
2. Start a new conversation
3. Look for the 🔌 icon in the bottom right corner
4. Click it to see the list of connected MCP servers
5. "uab-research-computing" should appear with 5 available tools
6. Try asking: "What tools are available from UAB Research Computing?"
