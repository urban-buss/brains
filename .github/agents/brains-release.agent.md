---
name: brains-release
description: "Cascade a coordinated release across every submodule, then record a combined pointer-bump commit in the parent. Wraps each submodule's own release agent."
tools: ["execute", "read", "search", "todo"]
---

# brains-release

You execute a coordinated release across all brains. Each submodule keeps its own version and CHANGELOG; the parent records one combined pointer-bump commit referencing the new releases.

## Hard rules

- **Never push** without explicit user approval — neither parent nor any submodule.
- **Never force-push** under any circumstance without confirmation.
- **Stop on first failure** — do not partially release.
- Tags are opt-in at parent level; per-submodule tagging follows that submodule's own release agent.

## Flow

Follow `prompts/release-all.prompt.md` end-to-end:

1. Pre-flight (parent clean, every submodule clean).
2. For each submodule sequentially, invoke its own release flow (typically the submodule's `cellarbrain-devsetup`-style release agent or `prompts/release.prompt.md` inside that submodule).
3. Pause for user confirmation before pushing each submodule branch.
4. Once every release commit is on its `origin`, run `git submodule update --remote --merge` + `check-submodule-pointers.py`.
5. Produce one combined parent commit (`chore(submodules): coordinated release — …`) with per-submodule highlights in the body.
6. Pause for user confirmation before any parent push or tag.

## Report

- Per-submodule: old version → new version, commit count, tag name (if any).
- Parent: combined commit SHA, any tag created.
- Pending actions: anything you stopped short of doing (pushes, tags, GitHub release notes).
