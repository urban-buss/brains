---
name: mcp-interop
description: "Patterns for composing cellarbrain and recipebrain at runtime via the MCP host. Load when designing or implementing a cross-brain feature."
---

# MCP interop between brains

`cellarbrain` and `recipebrain` are independent Python packages. They never `import` each other and share no Python types, schemas, or files. They compose **only** at runtime, through the **MCP host**, by one brain calling an MCP tool exposed by the other.

This skill captures the patterns that make that integration reliable.

## Roles

For every cross-brain feature, name one **provider** and one **consumer**:

- *Provider* — exposes the MCP tool/resource. Owns the schema, the data, and the access-control rules.
- *Consumer* — calls the provider tool through the MCP host. Treats the response as untrusted input (validate shape, handle absence).

Canonical example today: recipebrain (consumer) → cellarbrain (provider) for the `cellar_pairing` flow.

## Hard rules

1. **No Python coupling.** Never add `cellarbrain` to `recipebrain`'s `pyproject.toml` (or vice versa). Not even as an optional extra.
2. **No shared schemas.** If both brains use a concept ("varietal", "ingredient"), model each independently and translate at the MCP boundary.
3. **Tools are thin.** Each `@mcp.tool()` returns formatted strings or compact JSON; no business logic at the wire.
4. **Errors don't crash.** A consumer must tolerate the provider being absent from the host (e.g. `provider tool not found`, timeout, malformed response) with a clear user-facing message.
5. **Versioning is a contract.** Document the minimum provider version a consumer requires. Provider authors bump version on any breaking tool change.
6. **Reuse provider security.** Whatever guards the provider's CLI applies (SQL validation, path traversal, output redaction), MCP tools must inherit. Never expose a more-privileged surface via MCP than via CLI.

## Tool surface checklist

When designing a new cross-brain tool:

- [ ] Name is brain-prefixed and verb-shaped (`cellar_pairing`, `recipe_search`).
- [ ] Input schema is minimal — pass identifiers, not whole objects.
- [ ] Output is bounded — no unbounded result sets; paginate or top-K.
- [ ] Side-effect-free unless explicitly mutating (mutating tools must be opt-in and logged).
- [ ] Tested with a temp Parquet dataset in `tests/test_mcp_server.py`.
- [ ] Documented in the provider's `docs/mcp-tools.md`.

## Consumer-side wrapper pattern

Wrap the MCP call in a thin internal client so the rest of the consumer codebase doesn't deal with MCP plumbing. Pseudo-code:

```python
def call_cellar_pairing(recipe_id: str, *, host: MCPHost) -> CellarPairingResult | None:
    """Ask cellarbrain to recommend bottles for a recipe.

    Returns None if cellarbrain is not loaded in the host.
    Raises CrossBrainError for malformed responses.
    """
    if not host.has_tool("cellar_pairing"):
        return None
    raw = host.invoke("cellar_pairing", recipe_id=recipe_id, timeout_s=30)
    return CellarPairingResult.parse(raw)
```

This isolates:
- Absence handling (returns `None`).
- Timeout / transport errors (raised, caller decides whether to surface or fall back).
- Schema validation (`.parse()` does shape checks; never `eval`).

## Composition at the host

End-to-end manual check:

1. Configure the user's MCP host (Claude Desktop, etc.) to load both brain servers.
2. From the consumer brain, invoke the cross-brain flow.
3. Confirm the provider tool was hit (provider's logs / `mcp_server.py` traces).
4. Confirm graceful degradation: unload the provider, re-run, expect the consumer's "provider unavailable" message — **not** a crash.

## What does **not** go here

- Per-brain MCP tool implementations — those live in each submodule's `mcp_server.py` and are documented in that brain's `docs/mcp-tools.md`.
- General Python style — see `skills/python-conventions/` and `instructions/python.instructions.md`.

## Related

- `prompts/cross-brain.prompt.md` — guided workflow for cross-brain features.
- `agents/brains-coordinator.agent.md` — orchestrates the work across submodules.
- Each brain's MCP docs:
  - `cellarbrain/docs/mcp-tools.md`
  - `recipebrain/docs/05-mcp-tools.md`
