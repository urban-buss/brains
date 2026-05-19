---
description: "Plan and implement a feature that spans both cellarbrain and recipebrain via MCP. Use when: 'cross-brain feature', 'MCP integration', 'cellar pairing', 'feature touches both brains'."
argument-hint: "Describe the cross-brain feature"
agent: agent
---

You are scoping or implementing a feature that requires **both** `cellarbrain` and `recipebrain` to work together. The two brains compose only at **runtime** via the MCP host — they have **no Python-level coupling** and must not import each other.

## 1. Frame the integration

Identify which brain is the **provider** and which is the **consumer**:

- *Provider* exposes a new (or extended) MCP tool/resource.
- *Consumer* calls that tool through the MCP host as part of its own workflow.

Canonical example: recipebrain's `cellar_pairing` consumes cellarbrain's wine-search MCP tool to pair a recipe with bottles the user owns.

## 2. Design checklist

Before writing code, decide:

- **Tool surface** — exact MCP tool name, input schema, output shape. Keep inputs minimal; return formatted strings or compact JSON.
- **Failure mode** — what happens if the provider brain is offline or the host hasn't loaded it? The consumer should degrade gracefully (informative error, never crash).
- **No shared schema** — never share Parquet schemas or dataclasses across brains. If both brains need the same concept, model it independently and translate at the MCP boundary.
- **Versioning** — the consumer should tolerate provider versions ≥ the version it was built against. Document the minimum provider version in the consumer's docs/README.
- **Security** — neither brain should expose privileged data through MCP without the same guards used by its CLI (path traversal, SQL validation).

## 3. Implement provider first

`cd` into the provider submodule and:

1. Add or extend the MCP tool in `mcp_server.py` (`@mcp.tool()`).
2. Add tests in `tests/test_mcp_server.py`.
3. Update the provider's MCP docs (e.g. `docs/mcp-tools.md`).
4. Commit inside the provider submodule.

## 4. Implement consumer

`cd` into the consumer submodule and:

1. Add the call site (typically wrapped in a thin client that locates the provider tool via the MCP host).
2. Handle the "provider unavailable" path explicitly.
3. Add tests that mock the MCP call (don't require the provider to be running).
4. Update the consumer's docs.
5. Commit inside the consumer submodule.

## 5. Bump pointers in the parent

Use `prompts/pointer-bump.prompt.md` to record both submodule pointer moves in the parent (one commit per submodule, or a combined `chore(submodules): …` if they're tightly coupled).

## 6. Manual end-to-end sanity check

Document (or run) the manual MCP-host check: load both brains in the same MCP host, invoke the consumer tool, confirm it transparently calls the provider.

## 7. Reference

- `skills/mcp-interop/SKILL.md` — patterns for MCP composition, host setup, and tolerated-failure handling.
- Each submodule's `docs/` MCP-tools page is the authoritative tool catalogue.

Topic:

{{input}}
