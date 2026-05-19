# brains

Parent repository that aggregates the various "brain" projects as Git submodules.

## Submodules

| Submodule | Repository |
| --- | --- |
| [`cellarbrain`](./cellarbrain) | https://github.com/urban-buss/cellarbrain |
| [`recipebrain`](./recipebrain) | https://github.com/urban-buss/recipebrain |

## Cloning

Clone the repository together with all submodules:

```powershell
git clone --recurse-submodules https://github.com/urban-buss/brains.git
```

If you already cloned without `--recurse-submodules`, initialize them afterwards:

```powershell
git submodule update --init --recursive
```

## Updating submodules

Pull the latest changes for all submodules from their tracked branches:

```powershell
git submodule update --remote --merge
```

## Adding a new submodule

```powershell
git submodule add <repo-url> <path>
```

## Working inside a submodule

Each submodule is a full Git repository. `cd` into it and use Git normally
(commit, push, pull). After committing inside a submodule, remember to commit
the updated submodule pointer in the parent `brains` repository as well.
