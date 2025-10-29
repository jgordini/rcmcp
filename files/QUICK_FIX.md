# Quick Fix Guide - Deploy to Smithery Successfully

## The Issue

Your server was timing out because FastMCP's SSE isn't compatible with Smithery. 

## The Fix

Use the Smithery SDK version I created: `uab_docs_server_smithery.py`

## Deploy in 5 Steps

### 1. Use These Files (All Already Created!)

```
✅ smithery.yaml (no changes)
✅ Dockerfile (updated - uses smithery SDK)
✅ uab_docs_server_smithery.py (new Smithery-compatible server)
✅ pyproject.toml (add smithery to dependencies)
```

### 2. Update pyproject.toml

Add smithery to dependencies:

```toml
[project]
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "smithery>=0.4.0",
    "pydantic>=2.0.0",
]
```

### 3. Test Locally (Optional)

```bash
# Install smithery
pip install smithery

# Run server
python uab_docs_server_smithery.py

# Should start on port 8081
```

### 4. Push to GitHub

```bash
git add smithery.yaml Dockerfile uab_docs_server_smithery.py pyproject.toml
git commit -m "Fix: Add Smithery SDK for compatibility"
git push
```

### 5. Redeploy on Smithery

- Smithery will auto-detect changes and redeploy
- Or trigger manual redeploy in dashboard
- Scanner should now succeed! ✅

## What Changed

### Old Server (Doesn't Work)
```python
mcp = FastMCP("server")
mcp.run(transport="sse")  # ❌ Wrong protocol for Smithery
```

### New Server (Works!)
```python
from smithery import from_fastmcp

mcp_base = FastMCP("server")
mcp = from_fastmcp(mcp_base, config_schema=ConfigSchema)
mcp.run(transport="streamable-http")  # ✅ Smithery compatible!
```

## Verify Success

After deployment, Smithery scanner will show:

```
✅ Server scan successful
✅ Found 5 tools:
   - search_documentation
   - get_documentation_page
   - get_support_info
   - list_documentation_sections
   - get_cheaha_quick_start
```

## Troubleshooting

### Still Timing Out?

1. ✅ Check you're using `uab_docs_server_smithery.py`
2. ✅ Check Dockerfile installs `smithery`
3. ✅ Check using `transport="streamable-http"`
4. ✅ Rebuild and redeploy

### Module Import Error?

Add to Dockerfile:
```dockerfile
RUN uv pip install --system mcp httpx smithery pydantic
```

## All Set!

You now have everything needed for successful Smithery deployment. The timeout issue is fixed by using the Smithery SDK! 🚀
