# Cloudflare Remote MCP Server

This directory contains a Cloudflare Workers deployment of the UAB Research Computing Docs MCP server.

It exposes an MCP endpoint at:

- `https://<your-worker>.<your-subdomain>.workers.dev/mcp`

## Prereqs

- Node.js 18+ (or 20+)
- A Cloudflare account

## Install

```bash
cd /Users/jeremy/repos/rcmcp/cloudflare
pnpm install
```

## Local Dev

```bash
pnpm dev
```

Wrangler will print the local URL. The MCP endpoint is `/mcp`.

## Test

With the local server running, use a second terminal:

```bash
pnpm test:mcp
```

To test a deployed endpoint:

```bash
MCP_URL=https://example.workers.dev/mcp pnpm test:mcp
```

The test sends Glama's browser origin by default. Set `MCP_ORIGIN` to test a
different allowed browser client.

## Deploy

```bash
pnpm deploy
```

## Optional: GitHub Token (Recommended)

GitHub's code search endpoint is heavily rate limited without authentication.

Set a Cloudflare secret so `search_documentation` has higher rate limits:

```bash
cd /Users/jeremy/repos/rcmcp/cloudflare
wrangler secret put GITHUB_TOKEN
```

## Notes

- Tools are implemented in `src/index.ts`.
- Responses are truncated at ~100k characters to avoid overly large payloads.
