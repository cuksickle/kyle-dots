---
name: git-alchemist
description: AI-powered GitHub repository management. Use when you need to audit repo quality, optimize topics, generate semantic commit messages, or draft technical issues.
---

# Git-Alchemist

`alchemist` is used to automate high-level repository management tasks.

## When to Use This Skill
- **Audit:** When you want to evaluate the quality and health of a repository (e.g., `alchemist audit`).
- **Commits:** When you want consistent, semantic commit messages (e.g., `alchemist commit`).
- **Discovery:** When you need to optimize GitHub topics or generate better repository descriptions.
- **Planning:** When you have an idea and want it drafted into a structured GitHub issue (e.g., `alchemist issue "Add OAuth2 support"`).
- **Automation:** When you want to automatically open a PR from your local branch (e.g., `alchemist forge`).

## Core Commands
- `alchemist commit`: Generates semantic commit suggestions from staged changes.
- `alchemist audit`: Checks the repository's 'Gold' score and metadata health.
- `alchemist topics`: Analyzes the codebase and suggests relevant tags for discoverability.
- `alchemist describe`: Generates a repository description by analyzing the README.
- `alchemist issue "Idea"`: Drafts a technical issue from a prompt.
- `alchemist forge`: Automatically creates and opens a PR for the current branch.
- `alchemist sage "Question"`: Contextual codebase chat with smart chunking (handles large codebases).
- `alchemist scaffold "Description"`: Generates and executes project scaffolding safely.

## Workflow Patterns
1. **Prepare for PR**: `alchemist audit && alchemist topics && alchemist forge`
2. **Quality Check**: `alchemist audit` - Checks for missing docs, tests, and CI/CD best practices.
3. **Commit Workflow**: `git add . && alchemist commit`
