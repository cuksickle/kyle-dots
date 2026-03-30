---
description: Run linters and formatters for the current project
---

## Lint Command

1. Detect available linting/formatting tools:
   - JS/TS: eslint, prettier, biome, oxlint
   - Python: ruff, flake8, black, mypy
   - Rust: clippy, rustfmt
   - Go: golangci-lint, gofmt

2. Run all detected tools in sequence. If `$ARGUMENTS` specifies a tool name, run only that one.

3. Auto-fix what's fixable (--fix flag). Report remaining issues that need manual intervention.

4. Summary: files checked, issues found, issues auto-fixed.
