---
description: Scaffold a new React/Next.js component with tests
---

## Scaffold Component

Create a new component scaffolded with best practices.

**Usage:** `/scaffold-component [component-name] [type:page|component|layout]`

1. Parse `$ARGUMENTS` for component name and type.
2. Create component directory structure:
   ```
   src/components/{name}/
   ├── {Name}.tsx          # Main component (TypeScript)
   ├── {Name}.test.tsx     # Vitest test file
   ├── {Name}.module.css   # CSS modules
   └── index.ts            # Barrel export
   ```
3. Generate boilerplate code following project conventions:
   - TypeScript with proper types
   - Named export (no default unless project uses them)
   - Basic test skeleton with render and snapshot test
4. Report created files and next steps.
