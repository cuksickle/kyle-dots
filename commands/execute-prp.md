# /execute-prp

Execute a Product Requirements Prompt (PRP) document.

## Usage
```
/execute-prp <path-to-prp.md>
```

## Instructions

You are a feature implementer. Given a PRP document, implement the feature described within it by following this strict protocol.

### Process:

1. **Read the PRP** at the given path. Understand ALL context before writing any code.

2. **Plan:** Before writing code, output a brief implementation plan:
   - Files to create/modify
   - Order of operations
   - How each validation gate maps to the implementation

3. **Implement:** Write the code following the PRP's:
   - Context patterns
   - Example code style
   - Documentation references
   - Gotchas and edge cases

4. **Validate:** Run EVERY validation gate in the PRP, in order:
   - Level 1 (Lint & Typecheck): Must pass with 0 errors.
   - Level 2 (Unit Tests): All tests must pass.
   - Level 3 (Integration): Run smoke tests if defined.
   - Level 4 (Manual): List manual verification steps for the user.

5. **Iterate:** If any gate fails:
   - Read the error output carefully.
   - Fix the specific issue.
   - Re-run ONLY the failed level (don't re-run all gates).
   - Max 3 attempts per level before escalating to the user with diagnostics.

6. **Report:** After all gates pass, output:
   - Summary of what was built
   - Files created/modified (with line numbers for key functions)
   - Validation results (which gates passed)
   - Any manual steps remaining for the user

### Rules:
- NEVER skip a validation gate.
- NEVER implement features not described in the PRP.
- If the PRP is ambiguous, ask the user before implementing.
- Follow the codebase patterns exactly — don't introduce new conventions.
