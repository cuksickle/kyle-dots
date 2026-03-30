---
name: gemini-forge
description: Context discovery, semantic code search, and system state management (snapshots/rollbacks). Use when you need to understand large codebases, find specific logic across multiple files, or protect the system before making significant configuration changes.
---

# Gemini Forge

Gemini Forge is your primary tool for navigating and protecting the workspace. It consists of a vector-based search engine and a git-based snapshotting system.

## Core Workflows

### 1. The "Snapshot-First" Safety Protocol
**MANDATORY**: Before executing any command that modifies system configurations (e.g., editing `fstab`, `hyprland.conf`, or `stt-server.service`), you must create a snapshot.

```bash
export PYTHONPATH=$PYTHONPATH:~/git/research/gemini-forge
python3 -c "from forge_plumbing import ForgePlumbing; print(ForgePlumbing.create_snapshot('~/.config/hypr', 'Pre-edit backup'))"
```

### 2. Semantic Context Discovery
When a user asks a vague question about the codebase (e.g., "Where is the resolution logic?"), use semantic search instead of `rg`.

```bash
export PYTHONPATH=$PYTHONPATH:~/git/research/gemini-forge
python3 -c "from forge_indexer import ForgeIndexer; idx = ForgeIndexer(); [print(f'{r[/"path/"]}: {r[/"text/"][:200]}') for r in idx.search('hypr-config', 'resolution switching logic')]"
```

## Available Projects
The Forge currently tracks:
- `gemini-forge`: ~/git/research/gemini-forge
- `stt-project`: ~/Gemini-Projects/stt-project
- `hypr-config`: ~/.config/hypr
- `hyprland-dots`: ~/Hyprland-Dots
- `gemini-toolkit`: ~/git/tools/gemini-toolkit

## Rollback Procedure
If a change causes a regression, use `ForgePlumbing.list_snapshots(path)` to find the last known good state and `rollback(path, ref)` to restore it.
