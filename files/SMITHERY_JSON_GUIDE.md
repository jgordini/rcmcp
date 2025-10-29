# Smithery Test Configuration

## What is smithery.json?

The `smithery.json` file provides a test configuration that Smithery uses to scan and verify your MCP server works correctly.

## The File

**smithery.json:**
```json
{
  "testConfig": {
    "githubToken": ""
  }
}
```

## Why It's Needed

When Smithery scans your server, it needs to:
1. Connect to your server
2. Call the `initialize` method
3. List available tools
4. Optionally test tool execution

Since your server accepts an optional `githubToken` config parameter, Smithery needs to know what test values to use.

## Configuration Options

### Option 1: Empty Token (Current - Recommended)

```json
{
  "testConfig": {
    "githubToken": ""
  }
}
```

**Pros:**
- ✅ Works immediately
- ✅ No credentials needed
- ✅ Server functions with 60 requests/hour limit
- ✅ Sufficient for scanning and testing

**Cons:**
- ⚠️ Lower rate limit (60/hour vs 5000/hour)
- ⚠️ May hit limits during heavy testing

### Option 2: With GitHub Token

```json
{
  "testConfig": {
    "githubToken": "ghp_YourGitHubPersonalAccessToken"
  }
}
```

**Pros:**
- ✅ Higher rate limit (5000/hour)
- ✅ Better for extensive testing

**Cons:**
- ⚠️ Requires creating a GitHub token
- ⚠️ Token visible in repository (use fine-grained with minimal permissions)

## Recommended Approach

**Use empty token (Option 1)** because:
1. Your server works fine without a token
2. Smithery's scanner only needs to verify tools exist
3. 60 requests/hour is sufficient for scanning
4. No credential management needed

## If You Want to Add a Token

### Step 1: Create a Fine-Grained GitHub Token

1. Go to https://github.com/settings/tokens?type=beta
2. Click "Generate new token" → "Fine-grained token"
3. Name it: `Smithery MCP Server Scanner`
4. Expiration: Choose appropriate duration
5. Repository access: **Public Repositories (read-only)**
6. Permissions: **NO special permissions needed** (just public repo read)
7. Click "Generate token"
8. Copy the token (starts with `github_pat_` or `ghp_`)

### Step 2: Update smithery.json

```json
{
  "testConfig": {
    "githubToken": "ghp_YourTokenHere"
  }
}
```

### Step 3: Push to GitHub

```bash
git add smithery.json
git commit -m "Add test configuration"
git push
```

## Security Considerations

### For Empty Token (Recommended)
- ✅ No security concerns
- ✅ No credentials exposed
- ✅ Safe to commit to public repos

### For Token Included
- ⚠️ Token visible in repository
- ⚠️ Anyone can see and use it
- ⚠️ Use fine-grained tokens with minimal permissions
- ⚠️ Set short expiration (30-90 days)
- ⚠️ Monitor token usage
- ✅ Read-only access to public repos only (minimal risk)

**Note:** Since the token only accesses public UAB RC documentation (which is already public), the security risk is minimal even if exposed.

## File Placement

Place `smithery.json` in your repository root:

```
your-repo/
├── smithery.yaml          # Smithery configuration
├── smithery.json          # Test configuration (NEW!)
├── Dockerfile
├── uab_docs_server_smithery.py
└── pyproject.toml
```

## What Smithery Does With It

1. **Reads smithery.json** from your repository
2. **Extracts testConfig** values
3. **Passes to your server** as configuration
4. **Runs capability scan:**
   - Initialize connection
   - List tools (should find 5 tools)
   - Verify tool schemas
5. **Optionally tests a tool** (like search_documentation)

## Verification

After adding `smithery.json`, Smithery's scan should succeed:

```
✅ Starting server scan
✅ Waking up server...
✅ Setting up authentication...
✅ Using test config: {"githubToken":""}
✅ Inspecting server capabilities...
✅ Scanning MCP capabilities...
✅ Found 5 tools:
   - search_documentation
   - get_documentation_page
   - get_support_info
   - list_documentation_sections
   - get_cheaha_quick_start
✅ Server scan successful
```

## Alternative: Environment Variables

If you don't want to commit a token to the repo, you can also:

1. Leave `smithery.json` with empty token
2. Set environment variable in Smithery dashboard
3. Token passed at runtime without being in repo

**However**, for public documentation access, this is unnecessary complexity.

## Schema Reference

The `testConfig` object matches your `configSchema` in smithery.yaml:

**smithery.yaml:**
```yaml
configSchema:
  type: object
  properties:
    githubToken:
      type: string
      title: "GitHub Token"
      description: "Optional GitHub Personal Access Token"
      default: ""
```

**smithery.json:**
```json
{
  "testConfig": {
    "githubToken": ""  # Matches the property name
  }
}
```

## Common Issues

### Issue: Smithery still can't scan

**Check:**
1. ✅ `smithery.json` is in repository root
2. ✅ JSON syntax is valid (no trailing commas)
3. ✅ File is committed and pushed to GitHub
4. ✅ Using `uab_docs_server_smithery.py` (Smithery SDK version)
5. ✅ Dockerfile installs `smithery` package

### Issue: "Invalid JSON" error

**Fix:**
```json
{
  "testConfig": {
    "githubToken": ""
  }
}
```
- No trailing comma after `""`
- Double quotes (not single)
- Valid JSON format

### Issue: Token doesn't work

**Check:**
1. Token starts with `ghp_` or `github_pat_`
2. Token hasn't expired
3. Token has read access to public repos
4. No extra spaces or quotes in token string

## Testing Locally

Test that your server accepts the config:

```bash
# Run server
python uab_docs_server_smithery.py

# In another terminal, test with config
curl -X POST http://localhost:8081/mcp?githubToken= \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}'
```

## Summary

**Files needed for successful Smithery scan:**

1. ✅ `smithery.yaml` - Server configuration
2. ✅ `smithery.json` - **Test configuration (NEW!)**
3. ✅ `Dockerfile` - Container build
4. ✅ `uab_docs_server_smithery.py` - Smithery-compatible server
5. ✅ `pyproject.toml` - Dependencies

**Recommended smithery.json:**
```json
{
  "testConfig": {
    "githubToken": ""
  }
}
```

**Next steps:**
1. Add `smithery.json` to your repo
2. Commit and push
3. Smithery will detect it and use for scanning
4. Scan should now succeed! ✅

Your server will work perfectly with or without a GitHub token - the empty string is fine for testing!
