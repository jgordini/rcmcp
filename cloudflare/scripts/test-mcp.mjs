import assert from "node:assert/strict";

const endpoint = process.env.MCP_URL ?? "http://127.0.0.1:8787/mcp";
const origin = process.env.MCP_ORIGIN ?? "https://glama.ai";
const protocolVersion = "2025-06-18";

const claimResponse = await fetch(new URL("/.well-known/glama.json", endpoint));
assert.equal(claimResponse.status, 200);
assert.match(claimResponse.headers.get("content-type") ?? "", /^application\/json/);
assert.deepEqual(await claimResponse.json(), {
  $schema: "https://glama.ai/mcp/schemas/connector.json",
  claim: "glama_claim_jH7kiYE9ANaV0brD8XYw7k6IeNpXp0MF"
});

async function send(payload, expectedStatuses = [200]) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-protocol-version": protocolVersion,
      origin
    },
    body: JSON.stringify(payload)
  });

  const body = await response.text();
  assert.ok(expectedStatuses.includes(response.status), `Expected HTTP ${expectedStatuses.join(" or ")}, received ${response.status}: ${body}`);

  if (!body) return { response, message: undefined };

  const data = body
    .split("\n")
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice("data:".length).trim())
    .join("\n");

  return {
    response,
    message: JSON.parse(data || body)
  };
}

const initialized = await send({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion,
    capabilities: {},
    clientInfo: { name: "rcmcp-integration-test", version: "1.0.0" }
  }
});

assert.equal(initialized.message?.result?.serverInfo?.name, "uab-research-computing-docs");
assert.equal(initialized.message?.result?.protocolVersion, protocolVersion);
assert.equal(initialized.response.headers.get("mcp-session-id"), null);

await send(
  {
    jsonrpc: "2.0",
    method: "notifications/initialized"
  },
  [202, 204]
);

const tools = await send({
  jsonrpc: "2.0",
  id: 2,
  method: "tools/list",
  params: {}
});

const toolNames = tools.message?.result?.tools?.map((tool) => tool.name).sort();
assert.deepEqual(toolNames, ["get_cheaha_quick_start", "get_documentation_page", "get_support_info", "list_documentation_sections", "search_documentation"]);

const toolCall = await send({
  jsonrpc: "2.0",
  id: 3,
  method: "tools/call",
  params: {
    name: "get_support_info",
    arguments: {}
  }
});

assert.match(toolCall.message?.result?.content?.[0]?.text, /https:\/\/docs\.rc\.uab\.edu/);

console.log(`MCP integration test passed: ${endpoint}`);
