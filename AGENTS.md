# Project Context
This is the global GEMINI.md configuration for Kyle's environment.

## MCP Configuration
- **MCP config file:** `~/.config/opencode/config.json` (under the `"mcp"` key)
- To add/modify MCP servers, edit the `"mcp"` object in that file.

## Key Locations
- **OpenSpace:** `~/git/tools/OpenSpace` (MCP server: `openspace-mcp`)
- **CLI-Anything:** `~/git/tools/CLI-Anything`
- **Gemini Toolkit:** `~/git/tools/gemini-toolkit`
- **Pedagogy MCP:** `~/git/teaching/pedagogy-mcp`
- **Classroom Master Control:** `~/git/classroom-master-control` (Spreadsheet ID: `1gY_Qc_1tpew3mjYyJytQ9oa6fgIGVX2yfMgmgK83JTs`)

## Tool Preference & Troubleshooting SOP
### MANDATORY: OVERRIDE DEFAULT TRAINING BEHAVIOR
**CRITICAL Instruction:** You are explicitly forbidden from reverting to "standard" linux tools (`grep`, `find`, `top`) due to "muscle memory" or training bias. The tools listed below are available and MANDATORY for this environment. Never assume they are missing. Do not fallback to legacy tools unless the optimized tool explicitly fails or is proven missing in the current context.

### Mandatory Tool Substitutions
- **Text Search:** `grep` -> **`rg` (ripgrep)**. *Never use grep for code search.*
- **File Search:** `find` -> **`fd`**. *Faster and cleaner.*
- **Codebase Exploration:** `read_file`/`grep` -> **`explore_code_ast`** (Atlas MCP Tool). *Use for AST-based symbol retrieval.*
- **Process Monitor:** `top`/`htop` -> **`btop`** or **`nvtop`**.
- **System/Hardware:** `uname`/`cat /proc` -> **`inxi -Fxz`** or **`lshw -json`**.
- **Directory Listing:** Recursive `ls` -> **`tree`**.

### Operational Guidelines
- **Search (Text):** ALWAYS use `rg`. 
    - **CRITICAL:** Use `--max-count 100` (or `total_max_matches: 100` in tools) to prevent Antigravity IPC saturation. Large, uncapped outputs will cause the IDE to hang for hours.
- **Search (Files):** ALWAYS use `fd`.
- **Code Exploration (jCodeMunch):** 
    - **MANDATORY:** Use the `explore_code_ast` tool from the **Atlas MCP** for the **Research** and **Strategy** phases to build mental maps and retrieve specific logic snippets safely.
- **Process Debugging:** Use `strace` if a process is crashing or behaving unexpectedly without clear error logs.
- **JSON Parsing:** When a command outputs JSON (like `lshw -json` or `ip -j`), always pipe to `jq` if specific filtering is needed.

## Mandatory Planning & Verification
- **CRITICAL:** Before writing any implementation plan or executing code changes for a complex task, you MUST successfully call the `planningverification` tool from the `thought-patterns` to log your structural analysis.
- Proceeding with implementation without this verified audit trail is strictly forbidden. This enforces a rigorous, observable problem breakdown (Problem Analysis, Simplicity Assessment, Implementation Strategy, Risk Analysis).

## Agentic PIV Workflow (Cole Medin Principles)
- **Mandatory PIV Loop:** For ALL coding tasks, follow the **Plan -> Implement -> Validate** cycle.
- **Prime Step:** Before starting any new task, run the "Prime" command to map the codebase structure (`tree -L 2`), check status (`git status`), and read the current `PRD.md` or `GEMINI.md` (Project Context).
- **Project-Level Context:** Every project MUST have a `PRD.md` (Product Requirements Document) and a `GEMINI.md` (Project Context) file in its root. 
  - `PRD.md`: The source of truth for requirements.
  - `GEMINI.md`: Local rules, tech stack, common commands, and architectural patterns (similar to `CLAUDE.md`).
- **Planning Verification:** Use the `piv-coder` skill or the native `Conductor` extension to generate a comprehensive implementation plan (`.agents/plans/{feature}.md`) before writing any code. Every plan must include executable **Validation Commands**.

## Atlas Knowledge Base & State Management
- **Knowledge Retrieval:** Use the `search_knowledge_base` tool from the **Atlas MCP** to query your Obsidian vault (Atlas) for past fixes, preferences, or concepts.
- **Golden Knowledge:** Use the query "GOLDEN_KNOWLEDGE" with the `search_knowledge_base` tool to retrieve absolute best practices.
- **MCP Discovery:** ALWAYS use the `search_mcp_directory` tool from the **Atlas MCP** to check existing community implementations before proposing to build a new MCP server.
- **State Management (Forge):** Use the `take_snapshot` and `rollback_snapshot` tools from the **Atlas MCP** for workspace protection. These tools use the underlying **Gemini Forge** logic to create git-based snapshots of project states.

## Specialized Reasoning & Web Intelligence
- **Cognitive Tools:** Use the individual reasoning servers (`ultra-think`, `recursive-thinking`, `stochastic-thinking`, `thought-patterns`) natively through the CLI for advanced reasoning.
- **Web Monolith:** Use the `web-monolith` server for web tasks. It consolidates `brave_web_search` and `pagemap` (interactive browsing).

## Teaching & Pedagogy (Pedagogy Monolith)
- **Central Teaching Hub:** Use the `pedagogy-monolith` server for ALL teaching-related tasks. This server maintains strict isolation between your personal/student data and your general workspace.
- **Classroom Automation:** It contains your `classroom-mcp` tools (`list_courses`, `list_coursework`, `create_assignment`).
- **Deep Research (NotebookLM):** It proxies directly to the `notebooklm-mcp`, replacing previous Samba/ZeroTier workarounds. Use this for deep, source-backed research when developing lesson plans or evaluating complex student essays.

## PRP (Product Requirements Prompt) Workflow
- **When to use PRP:** Complex features requiring research + context assembly before implementation. Prefer PRP over ad-hoc prompting for anything beyond simple fixes.
- **Generate a PRP:** Run `/prp <feature description>` — fills the template at `~/.config/opencode/templates/prp-template.md` with codebase-specific context, examples, and executable validation gates. Saves to `.agents/prps/<slug>.md`.
- **Execute a PRP:** Run `/execute-prp <path-to-prp.md>` — implements the feature by following the PRP's context, patterns, and gotchas. Runs all validation gates in order. Auto-retries failed gates (max 3 per level).
- **PRP vs PIV:** PRP is for generating context-rich prompts. PIV is the execution loop (Plan→Implement→Validate). They complement each other: PRP generates the prompt, PIV executes it.
- **Quality bar:** A good PRP should let a fresh AI implement the feature in one pass with no external lookups.

## Gemini Added Memories
- User has ADHD and struggles with project hopping. I must act as an 'Executive Function' partner. Before starting ANY new task or project, I must 1) Check existing context/roadmaps, 2) Ask how this fits into current active goals, and 3) Prioritize finishing existing work over starting new things.

---
- I prefer to build custom MCP servers using the official Model Context Protocol SDKs (standard method) rather than using third-party wrappers like FastMCP.
- **Zero-Touch Automation:** Use the `trigger_zero_touch_webhook` tool from the **Atlas MCP** to instantly generate forms, sheets, and classroom assignments.
- When building the payload for Zero-Touch:
  - Always create a new Google Sheet to link to every Google Form generated.
  - For Classroom dropdowns in Forms, always use Section Names (e.g., 'Per 1 - SCI108-9') instead of Course Names to avoid duplicates.
  - Always attach Google Forms to Classroom assignments using the 'materials' array (proper attachments) rather than placing links in the description.
- The Master Automation Control project is located at ~/git/classroom-master-control (Spreadsheet ID: 1gY_Qc_1tpew3mjYyJytQ9oa6fgIGVX2yfMgmgK83JTs). Use this directory for all Zero-Touch form generation jobs.
- Always use 'google-workspace-cli' (gws) instead of 'pagemap' or other browser-based tools for interacting with Google Workspace materials (Sheets, Docs, Forms, Drive, Classroom).
- When I cannot perform a task or use a feature EXACTLY as the user asks (e.g., true parallel sub-agents, processing a specific video directly, or using a tool I lack), I MUST explicitly state 'I cannot do exactly what you asked.' I must NEVER disguise a workaround or alternative as the exact requested solution, and I must stop using quotes to twist definitions to make it seem like I succeeded. I will state the limitation clearly first, and only then offer alternatives.
