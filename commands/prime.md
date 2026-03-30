---
description: Prime workspace context before starting a task
---

## Prime

Prepare the workspace context before coding.

1. Run `tree -L 2` (or `fd --max-depth 2 --type f | head -60`) to map project structure.
2. Check `git status` for dirty files, untracked files, current branch.
3. Check for existing `PRD.md` or `GEMINI.md` in project root — read if present.
4. Read `package.json` / `pyproject.toml` / `Cargo.toml` for dependencies and scripts.
5. Check recent `git log --oneline -10` for context on latest changes.
6. Report a concise summary: project type, tech stack, current state, available scripts.
