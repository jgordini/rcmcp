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
npm install
```

## Local Dev

```bash
npm run dev
```

Wrangler will print the local URL. The MCP endpoint is `/mcp`.

## Deploy

```bash
npm run deploy
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

