# Security Policy

The `brains` repository is a **parent aggregator** — it contains no application source code of its own. Application-level vulnerabilities live in the individual brain repositories.

## Reporting a vulnerability

- **cellarbrain** vulnerabilities: report at https://github.com/urban-buss/cellarbrain/security/advisories
- **recipebrain** vulnerabilities: report at https://github.com/urban-buss/recipebrain/security/advisories
- **Parent / coordinator tooling** (anything under `.github/`, `tools/`, workflows, or the submodule-pointer bookkeeping itself): please use this repo's [Security advisories](https://github.com/urban-buss/brains/security/advisories) tab, or contact the repository owner privately.

Do **not** open a public issue for a security report.

## Scope at parent level

The parent repo's security surface is limited to:

- GitHub Actions workflows under `.github/workflows/`.
- Helper scripts under `.github/tools/` (Python; runs against local checkouts and in CI).
- Submodule pointer integrity (a malicious pointer bump could direct collaborators to an attacker-controlled commit; mitigated by `submodule-sanity.yml` and `check-submodule-pointers.py`).

Cross-brain MCP integration runs in user-controlled MCP hosts and is governed by each brain's own security guarantees (path traversal checks, SQL validation, TLS, timeouts). See each brain's `SECURITY.md` for details.

## Supported versions

This parent repo follows a rolling-main model. Only the latest commit on `main` is supported. Per-brain support windows are documented in the respective submodule repositories.
