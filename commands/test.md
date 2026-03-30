---
description: Run project test suite with framework auto-detection
---

## Testing Command

1. Detect the project's test framework and package manager:
   - Check for package.json → npm/pnpm/yarn + jest/vitest/mocha
   - Check for pyproject.toml/setup.cfg/pytest.ini → pytest
   - Check for Cargo.toml → cargo test
   - Check for go.mod → go test

2. Run the appropriate test command based on detection.

3. If tests fail, analyze failures and propose fixes. If a specific test file or pattern is provided as an argument (`$ARGUMENTS`), run only those tests.

4. Report results with pass/fail summary and coverage if available.
