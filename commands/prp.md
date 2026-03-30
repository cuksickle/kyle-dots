# /prp

Generate a Product Requirements Prompt (PRP) for a feature.

## Usage
```
/prp <feature description>
```

## Instructions

You are a PRP engineer. Given a feature description, generate a complete PRP document using the template at `~/.config/opencode/templates/prp-template.md`.

### Process:
1. **Prime the workspace:** Read PRD.md, GEMINI.md, and key source files.
2. **Research context:**
   - Use `search_knowledge_base` (Atlas) for relevant past patterns.
   - Use `explore_code_ast` (Atlas) to find existing code patterns to reference.
   - Use web search if external documentation is needed.
3. **Fill every section** of the template with concrete, specific details:
   - **Context:** Link to real files and functions in this codebase.
   - **Examples:** Copy-paste actual code from this project (not generic examples).
   - **Documentation:** Paste relevant API docs excerpts (don't just link).
   - **Validation Gates:** Write real commands that run against this project.
   - **Gotchas:** Include framework-specific pitfalls discovered during research.
4. **Write the PRP** to `.agents/prps/<feature-slug>.md` in the project root.
5. **Output** a summary of what was generated and where.

### Quality bar:
- The PRP must contain enough context for a fresh AI to implement the feature in one pass.
- Every validation gate must be a real, executable command.
- Examples must come from THIS codebase, not generic templates.
- If you can't find a relevant example in the codebase, flag it and ask the user.
