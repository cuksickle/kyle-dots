---
name: piv-coder
description: Implements Cole Medin's PIV (Plan, Implement, Validate) workflow. Use this for building production-grade software in a structured, "no-fluff" agentic way. It enforces a strict planning phase before any code is written.
---

# PIV Coder: The Agentic Workflow

## Core Philosophy
**Plan first, Code second, Validate always.** 
We do NOT write code until a comprehensive implementation plan exists. This prevents architectural drift, redundant logic, and "hallucinated" implementations.

## The PIV Loop

### 1. Prime (Context Discovery)
Before starting ANY task, run the "Prime" command to map the codebase.
- **Action:** List tracked files (`git ls-files`), show directory structure (`tree -L 2`), and read the current `PRD.md` or `GEMINI.md`.
- **Goal:** Build an accurate mental map of the project status and conventions.

### 2. Plan (Systematic Analysis & User Consultation)
Transform the feature request into a **comprehensive implementation plan** (`.agents/plans/feature-name.md`).
- **Action:** Enter **Plan Mode** (`enter_plan_mode`).
- **MANDATORY Decision Points:** For any technical choice (choice of library, architectural pattern, or implementation approach), you MUST present the user with a multiple-choice question using the `ask_user` tool before finalizing the plan. 
- **Plan Structure:**
  - **Decision Log**: Record each architectural choice and the user's selected option.
  - **Feature Description & User Story**: What are we building and why?
  - **Context References**: Which specific files and line numbers are relevant? (READ these files!)
  - **New Files**: What new files are needed?
  - **Implementation Steps**: Atomic, step-by-step tasks (CREATE, UPDATE, ADD, MIRROR).
  - **Testing Strategy**: Unit, Integration, and Edge Case requirements.
  - **Validation Commands**: Executable shell commands to verify each task.

### 3. Implement (Surgical Execution)
Execute the plan task-by-task without guessing.
- **Action:** Switch to **Execution Mode**.
- **Rule:** Do not deviate from the plan. If the plan is flawed, stop, return to Plan Mode, update the plan, and restart.
- **Interactive Checkpoints:** If a non-trivial error occurs or an unforeseen choice arises during implementation, use `ask_user` with multiple-choice options for the next step.

### 4. Validate (Finality)
Run all validation commands defined in the plan.
- **Action:** Run the specified `npm test`, `pytest`, `eslint --fix`, etc.
- **Frontend Check:** For any frontend-related task, activate and execute the `e2e-validator` skill to perform a browser-based smoke test. This is mandatory to confirm that the UI remains functional and free of regressions.
- **Rule:** A task is only "Complete" when all validation commands and smoke tests pass with zero errors.

## Usage Guide
When starting a **New Project**, always begin by copying the global template to the project root:
`cp ~/conductor/GEMINI-template.md ./GEMINI.md`
Then, define the project-specific tech stack, architecture, and validation rules within that file.

When a user says "Let's build X using PIV," follow these steps:
1.  **Call `/prime`**: (Perform context discovery).
2.  **Consult User**: Identify key technical decisions and use `ask_user` to present multiple-choice options.
3.  **Call `/plan`**: (Enter Plan Mode and generate the plan, incorporating user decisions).
4.  **Ask for Approval**: Show the plan to the user.
5.  **Call `/execute`**: (Implement the plan).

## Skill Metadata
- **Workflow:** Plan -> Act -> Validate
- **Source of Truth:** `.agents/plans/`
- **User Consultation:** Mandatory via `ask_user` multiple-choice questions for technical decisions.
- **Architectural Reference:** `GEMINI.md` (Project Context)
