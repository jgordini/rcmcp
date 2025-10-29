# CORRECTED SOLUTION - Based on Official Smithery Docs

## What the Documentation Shows

For **Custom Container** deployments, Smithery should automatically:
1. Read `configSchema` from `smithery.yaml`
2. Generate a configuration UI
3. Pass config as URL parameters to your server

## Your Current Setup is Correct!

Your `smithery.yaml` already has the correct configuration:

```yaml
runtime: "container"
startCommand:
  type: "http"
  configSchema:
    type: object
    properties:
      githubToken:
        type: string
        title: "GitHub Token"
        description: "Optional GitHub Personal Access Token"
        default: ""
```

This is **exactly right** according to the docs!

## The Real Problem

The timeout issue is because your server isn't compatible with Smithery's streamable HTTP protocol. The "No test config found" is a **secondary issue** - Smithery can't even connect to test the config.

## Two Solutions

### Solution 1: Use Smithery SDK (Recommended)

This is what `uab_docs_server_smithery.py` does - it's the **correct** approach.

**Files needed:**
1. ✅ `smithery.yaml` (you have this)
2. ✅ `Dockerfile` (updated to install `smithery`)
3. ✅ `uab_docs_server_smithery.py` (uses Smithery SDK)
4. ❌ `smithery.json` (NOT needed for custom containers!)

**Why smithery.json wasn't working:**
- `smithery.json` is for **external/stdio** servers
- **Custom container** servers get config from URL parameters
- Your server needs to parse URL parameters, not read a file

### Solution 2: Manual URL Parameter Parsing

If you don't want to use Smithery SDK, you need to manually parse config from URL parameters:

```python
# Your server receives requests like:
# GET /mcp?githubToken=xxx

# You need to parse query parameters:
from urllib.parse import parse_qs

def handle_request(query_string):
    params = parse_qs(query_string)
    github_token = params.get('githubToken', [''])[0]
```

## Why It's Timing Out

Your server currently uses FastMCP's SSE, which sends responses like:

```
event: message
data: {"jsonrpc":"2.0",...}
```

But Smithery expects **streamable HTTP** format (different SSE structure).

The Smithery SDK handles this translation automatically.

## Correct Deployment Steps

### Option A: Use Smithery SDK Version (Recommended)

```bash
# 1. Make sure you have these files:
ls -la
# Should see:
# - smithery.yaml ✅
# - Dockerfile ✅ (with smithery package)
# - uab_docs_server_smithery.py ✅
# - pyproject.toml ✅

# 2. Push to GitHub
git add .
git commit -m "Use Smithery SDK for compatibility"
git push

# 3. Deploy on Smithery
# Scanner should now work!
```

### Option B: Add Well-Known Endpoint

Add a `/.well-known/mcp-config` endpoint to your server that returns:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://your-server.com/.well-known/mcp-config",
  "title": "UAB RC Docs MCP Configuration",
  "type": "object",
  "properties": {
    "githubToken": {
      "type": "string",
      "title": "GitHub Token",
      "description": "Optional GitHub Personal Access Token",
      "default": ""
    }
  }
}
```

This is optional but helps Smithery understand your config better.

## What About smithery.json?

Based on the official docs:

**For Custom Container:**
- ❌ Don't need `smithery.json`
- ✅ Config comes from URL parameters
- ✅ Schema defined in `smithery.yaml`

**For External/Stdio Servers:**
- ✅ May need `smithery.json` for local testing
- ✅ Used by Smithery CLI tools

Since you're using **Custom Container**, you don't need `smithery.json`.

## The Real Fix

**The issue isn't missing smithery.json - it's that FastMCP's SSE isn't compatible with Smithery.**

Use the Smithery SDK version (`uab_docs_server_smithery.py`) which:
1. Wraps FastMCP with Smithery compatibility
2. Uses `transport="streamable-http"`
3. Parses config from URL parameters automatically
4. Handles the SSE format Smithery expects

## Verification

After deploying with Smithery SDK:

```
✅ Starting server scan
✅ Waking up server...
✅ Setting up authentication...
✅ Inspecting server capabilities...
✅ Found 5 tools
✅ Server scan successful
```

No need for `smithery.json` - config is passed via URL!

## Summary

**Don't add smithery.json** - that's not the issue.

**Do this instead:**
1. Use `uab_docs_server_smithery.py` (Smithery SDK version)
2. Update `Dockerfile` to install `smithery` package
3. Push to GitHub
4. Redeploy

The SDK handles all the protocol compatibility automatically!

## Files You Actually Need

```
your-repo/
├── smithery.yaml              ✅ (defines config schema)
├── Dockerfile                 ✅ (installs smithery SDK)
├── uab_docs_server_smithery.py ✅ (uses SDK)
└── pyproject.toml             ✅ (includes smithery)
```

No `smithery.json` needed for custom containers! 🎉
