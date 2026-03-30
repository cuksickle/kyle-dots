# PRP: {{FEATURE_NAME}}

## Goal
<!-- What are we building? One paragraph, clear outcome. -->

## Context
<!-- Why does this exist? What problem does it solve? -->
<!-- Link to related PRD.md sections, issues, or discussions. -->

### Tech Stack
<!-- List relevant frameworks, libraries, patterns in this project. -->

### Existing Code Patterns
<!-- Reference specific files/functions that the new code should follow. -->
<!-- Example: `src/services/api.ts` — all API calls use the fetch wrapper pattern. -->

## Documentation
<!-- Links to API docs, library docs, or RFCs needed to implement this. -->
<!-- Paste the most relevant excerpts here so the AI doesn't need external lookups. -->

## Examples
<!-- Copy-paste concrete code examples from this codebase that show the pattern to follow. -->
<!-- The more examples, the fewer assumptions the AI makes. -->

## Validation Gates
<!-- Executable checks that prove the feature works. These run automatically after implementation. -->

### Level 1: Lint & Typecheck
```bash
npm run lint
npm run typecheck
```

### Level 2: Unit Tests
```bash
npm run test -- --run --reporter=verbose
```

### Level 3: Integration / Smoke Test
```bash
# Add specific integration test commands here
```

### Level 4: Manual Verification
<!-- Steps a human would do to verify. -->
- [ ] Step 1
- [ ] Step 2

## Gotchas & Edge Cases
<!-- Known pitfalls, race conditions, API quirks, or things the AI always gets wrong. -->
- 
- 

## Iteration Protocol
<!-- If validation gates fail, what's the retry strategy? -->
1. Run validation gates in order (Level 1 → 4).
2. On failure: read error output, fix, re-run **only the failed level**.
3. Max 3 retry attempts per level before escalating to user.
4. Never skip a validation gate.
