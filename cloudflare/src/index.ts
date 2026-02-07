import { createMcpHandler, WorkerTransport } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

type Env = {
  // Optional GitHub token to avoid low unauthenticated rate limits.
  GITHUB_TOKEN?: string;
};

const DOCS_BASE_URL = "https://docs.rc.uab.edu";
const RC_BASE_URL = "https://rc.uab.edu";
const GITHUB_API_BASE = "https://api.github.com";
const GITHUB_REPO = "uabrc/uabrc.github.io";
const USER_AGENT = "UAB-RC-MCP-Server/1.0 (Cloudflare Worker)";
const CHARACTER_LIMIT = 100_000;

let cachedEnv: Env | undefined;

function getGithubToken(): string | undefined {
  const token = cachedEnv?.GITHUB_TOKEN?.trim();
  return token ? token : undefined;
}

function truncateContent(content: string, limit = CHARACTER_LIMIT): string {
  if (content.length <= limit) return content;

  const truncated = content.slice(0, limit);
  const notice =
    `\n\n---\n\n` +
    `WARNING: Content Truncated: This response was truncated at ${limit.toLocaleString()} characters ` +
    `(approximately ${Math.floor(limit / 4).toLocaleString()} tokens). ` +
    `Consider requesting specific sections if you need more detail.\n`;

  return truncated + notice;
}

async function githubSearchCode(args: {
  query: string;
  maxResults: number;
  githubToken?: string;
}): Promise<{ totalCount: number; items: Array<{ name: string; path: string; html_url: string }> }> {
  const { query, maxResults, githubToken } = args;

  const url = new URL(`${GITHUB_API_BASE}/search/code`);
  url.searchParams.set("q", `${query} repo:${GITHUB_REPO}`);
  url.searchParams.set("per_page", String(maxResults));

  const headers: Record<string, string> = {
    Accept: "application/vnd.github.v3+json",
    "User-Agent": USER_AGENT,
  };
  if (githubToken) headers.Authorization = `Bearer ${githubToken}`;

  const res = await fetch(url.toString(), { headers });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    if (res.status === 401) throw new Error("GitHub API authentication failed (invalid GITHUB_TOKEN).");
    if (res.status === 403) throw new Error("GitHub API rate limit exceeded. Set GITHUB_TOKEN for higher limits.");
    throw new Error(`GitHub search failed: HTTP ${res.status}${text ? ` - ${text}` : ""}`);
  }

  const data = (await res.json()) as any;
  const totalCount = typeof data?.total_count === "number" ? data.total_count : 0;
  const itemsRaw: any[] = Array.isArray(data?.items) ? data.items : [];
  const items = itemsRaw.map((it) => ({
    name: typeof it?.name === "string" ? it.name : "Unknown",
    path: typeof it?.path === "string" ? it.path : "",
    html_url: typeof it?.html_url === "string" ? it.html_url : "",
  }));

  return { totalCount, items };
}

function repoPathToDocsUrl(filePath: string): string {
  let cleanPath = filePath.replace(/\.md$/i, "").replace(/README$/i, "");
  if (cleanPath.startsWith("docs/")) cleanPath = cleanPath.slice("docs/".length);
  cleanPath = cleanPath.replace(/\/+$/, "");
  return `${DOCS_BASE_URL}/${cleanPath}`;
}

function normalizeDocsRepoPath(input: string): { repoPath: string; displayPath: string } {
  let pagePath = input.trim();

  if (pagePath.startsWith("http")) {
    if (!pagePath.includes("github.com")) {
      throw new Error(`URL provided is not a GitHub URL: ${pagePath}`);
    }
    const parts = pagePath.split("/blob/");
    if (parts.length < 2) throw new Error(`Could not extract file path from GitHub URL: ${pagePath}`);
    const afterBlob = parts[1];
    const firstSlash = afterBlob.indexOf("/");
    if (firstSlash === -1) throw new Error(`Could not extract file path from GitHub URL: ${pagePath}`);
    pagePath = afterBlob.slice(firstSlash + 1);
  }

  pagePath = pagePath.replace(/^\/+/, "");
  if (!pagePath.startsWith("docs/")) pagePath = `docs/${pagePath}`;
  if (!pagePath.endsWith(".md")) pagePath = `${pagePath}.md`;

  const displayPath = pagePath.replace(/^docs\//, "").replace(/\.md$/, "").replace(/\/+$/, "");
  return { repoPath: pagePath, displayPath };
}

async function fetchRawGithubFile(args: { repoPath: string; branch: "main" | "master" }): Promise<string | null> {
  const { repoPath, branch } = args;
  const rawUrl = `https://raw.githubusercontent.com/${GITHUB_REPO}/${branch}/${repoPath}`;
  const res = await fetch(rawUrl, { headers: { "User-Agent": USER_AGENT } });
  if (!res.ok) return null;
  return await res.text();
}

const server = new McpServer({
  name: "uab-research-computing-docs",
  version: "1.0.0",
});

server.tool(
  "search_documentation",
  "Search the UAB Research Computing documentation for relevant content.",
  {
    query: z
      .string()
      .describe("The search term or phrase to look for in the UAB Research Computing documentation."),
    max_results: z
      .number()
      .int()
      .min(1)
      .max(10)
      .optional()
      .describe("Maximum number of search results to return (default: 5, max: 10)."),
  },
  async (args: { query: string; max_results?: number }) => {
    const { query, max_results } = args;
    const maxResults = Math.min(max_results ?? 5, 10);
    const token = getGithubToken();

    let data: { totalCount: number; items: Array<{ name: string; path: string; html_url: string }> };
    try {
      data = await githubSearchCode({ query, maxResults, githubToken: token });
    } catch (e: any) {
      return { content: [{ type: "text", text: `Error searching documentation: ${String(e?.message ?? e)}` }] };
    }

    if (!data.items.length) {
      return {
        content: [
          { type: "text", text: `No results found for '${query}' in the UAB Research Computing documentation.` },
        ],
      };
    }

    const lines: string[] = [];
    lines.push(`Found ${data.totalCount} results for '${query}':\n`);
    data.items.slice(0, maxResults).forEach((item, idx) => {
      const docUrl = repoPathToDocsUrl(item.path);
      lines.push(
        `\n${idx + 1}. **${item.name}**\n` +
          `   URL: ${docUrl}\n` +
          `   Repository: ${item.html_url}\n` +
          `   Path: ${item.path}\n`
      );
    });
    lines.push(`\nTip: Use 'get_documentation_page' to retrieve the full content of a specific page.`);

    return { content: [{ type: "text", text: truncateContent(lines.join("")) }] };
  }
);

server.tool(
  "get_documentation_page",
  "Retrieve the full content of a specific documentation page.",
  {
    page_path: z
      .string()
      .describe("Path to a docs page: repo path (docs/.../page.md), short path, or a GitHub URL."),
  },
  async (args: { page_path: string }) => {
    const { page_path } = args;
    let repoPath: string;
    let displayPath: string;
    try {
      ({ repoPath, displayPath } = normalizeDocsRepoPath(page_path));
    } catch (e: any) {
      return { content: [{ type: "text", text: `Error: ${String(e?.message ?? e)}` }] };
    }

    const mainContent = await fetchRawGithubFile({ repoPath, branch: "main" });
    const content = mainContent ?? (await fetchRawGithubFile({ repoPath, branch: "master" }));
    if (content == null) {
      return {
        content: [
          {
            type: "text",
            text: `Error: Unable to fetch content from GitHub. The file may not exist at path: ${repoPath}`,
          },
        ],
      };
    }

    const docsSiteUrl = `${DOCS_BASE_URL}/${displayPath}`;
    const result =
      `# Documentation Page: ${repoPath}\n` +
      `URL: ${docsSiteUrl}\n\n---\n\n` +
      `${content}\n\n---\n\n` +
      `Source: UAB Research Computing Documentation\n` +
      `Base URL: ${DOCS_BASE_URL}\n`;

    return { content: [{ type: "text", text: truncateContent(result) }] };
  }
);

server.tool("get_support_info", "Get support info for UAB Research Computing.", {}, async () => {
  const text =
    `# UAB Research Computing Support Information\n\n` +
    `## Primary Documentation Site\n${DOCS_BASE_URL}\n\n` +
    `## Cheaha Access Portal\n${RC_BASE_URL}\n\n` +
    `## Getting Support\n\n` +
    `### Office Hours\n${DOCS_BASE_URL}/help/office_hours\n\n` +
    `### Support Portal\n${DOCS_BASE_URL}/help/support\n\n` +
    `### Contributing to Documentation\n${DOCS_BASE_URL}/contributing/contributor_guide/\n\n` +
    `## Quick Links\n\n` +
    `- Main Documentation: ${DOCS_BASE_URL}\n` +
    `- Cheaha Login: ${RC_BASE_URL}\n` +
    `- Getting Started Guides: ${DOCS_BASE_URL}/getting-started/\n` +
    `- Software Documentation: ${DOCS_BASE_URL}/software/\n` +
    `- Storage & Data: ${DOCS_BASE_URL}/storage/\n\n` +
    `## About UAB Research Computing\n\n` +
    `UAB Research Computing is part of UAB IT. Services include Cheaha HPC, data storage, software support, consultation/training, and cloud integration.\n\n` +
    `For the most up-to-date information, refer to ${DOCS_BASE_URL}.\n`;

  return { content: [{ type: "text", text }] };
});

server.tool("list_documentation_sections", "List the main sections in UAB Research Computing documentation.", {}, async () => {
  const text =
    `# UAB Research Computing Documentation Structure\n\n` +
    `## 1. Getting Started\nAccount setup, access, first steps, basic HPC concepts.\n\n` +
    `## 2. Help & Support\nOffice hours, support portal, contact information, troubleshooting.\n\n` +
    `## 3. Software & Applications\nSoftware catalog, modules, installing software, containers, licensed software.\n\n` +
    `## 4. Storage & Data Management\nStorage systems, quotas, data transfer, backup/archival, compliance.\n\n` +
    `## 5. Job Scheduling (SLURM)\nSubmission scripts, resource requests, policies, arrays/dependencies.\n\n` +
    `## 6. Best Practices\nWorkflow optimization, efficiency, reproducibility, collaboration.\n\n` +
    `## 7. Contributing\nContributor guide, documentation standards, submitting changes.\n\n` +
    `## Quick Access\n` +
    `- Main Site: ${DOCS_BASE_URL}\n` +
    `- Cheaha Portal: ${RC_BASE_URL}\n` +
    `- GitHub Repository: https://github.com/${GITHUB_REPO}\n\n` +
    `Use 'search_documentation' to find topics, or 'get_documentation_page' to fetch full content.\n`;

  return { content: [{ type: "text", text }] };
});

server.tool("get_cheaha_quick_start", "Quick start for the Cheaha HPC cluster.", {}, async () => {
  const text =
    `# Cheaha HPC Quick Start Guide\n\n` +
    `## Access\n` +
    `- Web Portal (recommended): ${RC_BASE_URL}\n` +
    `- SSH: ssh YOUR_BLAZERID@cheaha.rc.uab.edu\n\n` +
    `## Important Rule\nDo not run compute-intensive work on login nodes. Use SLURM for jobs.\n\n` +
    `## Compute Partitions (examples)\n` +
    `- GPU: pascalnodes, amperenodes\n` +
    `- General: amd-hdr100\n` +
    `- Time-based: express, short, medium, long\n` +
    `- Specialized: largemem\n\n` +
    `## Software\nUse the module system; Anaconda is commonly recommended for Python workflows.\n\n` +
    `## Support\n` +
    `- Docs: ${DOCS_BASE_URL}\n` +
    `- Office Hours: ${DOCS_BASE_URL}/help/office_hours\n` +
    `- Support Portal: ${DOCS_BASE_URL}/help/support\n\n` +
    `## Next Steps\n` +
    `- search_documentation(\"slurm tutorial\")\n` +
    `- search_documentation(\"modules\")\n` +
    `- search_documentation(\"partitions\")\n` +
    `- search_documentation(\"storage\")\n\n` +
    `For the most current information, refer to ${DOCS_BASE_URL}.\n`;

  return { content: [{ type: "text", text }] };
});

// The handler connects the server to the provided transport once, then reuses it
// across requests. This avoids reconnecting the same server to a new transport per request.
const transport = new WorkerTransport({
  sessionIdGenerator: () => crypto.randomUUID(),
});
const mcpHandler = createMcpHandler(server, { route: "/mcp", transport });

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    cachedEnv = env;
    return mcpHandler(request, env, ctx);
  },
};
