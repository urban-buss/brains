<!--
  Pull-request template for the brains parent repo.

  Remember: source-code changes for a brain belong in that brain's own repo.
  This parent repo is an aggregator — most PRs here are submodule pointer
  bumps, .github/ coordinator tooling, or top-level docs.
-->

## Summary

<!-- One or two sentences describing the change. -->

## Type of change

- [ ] Submodule pointer bump (cellarbrain / recipebrain)
- [ ] Coordinator tooling under `.github/` (prompts, agents, instructions, skills, tools, workflows)
- [ ] Documentation (`README.md`, `LICENSE`, `.github/*.md`)
- [ ] `.gitmodules` change (added/removed/retargeted a submodule)
- [ ] Other (please describe)

## Submodule pointer changes

<!-- Fill in this block ONLY if this PR moves a submodule pointer. -->

| Submodule | Old SHA | New SHA | Inbound version | Notes |
|-----------|---------|---------|------------------|-------|
| cellarbrain | | | | |
| recipebrain | | | | |

- [ ] Each new pointer commit is **pushed to the submodule's `origin`** (verified with `python .github/tools/check-submodule-pointers.py`).
- [ ] No submodule has uncommitted changes (no "dirty" state).
- [ ] Commit message follows `chore(<submodule>): bump to <short-sha>` and lists the inbound commit range in the body.

## Checks

- [ ] CI is green (lint, pytest matrix, submodule-sanity).
- [ ] If this PR touches `.github/copilot-instructions.md` or the agent catalogue, the changes are reflected in `AGENTS.md`.
- [ ] No source files outside the legitimate parent surface were edited (see `.github/instructions/submodule-workflow.instructions.md`).
- [ ] No `.memories/`, `.proposals/`, or `.scratch/` paths are staged.
