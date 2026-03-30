---
name: terminal-coach
description: A hands-on Linux terminal trainer that creates safe practice environments (levels) and verifies user progress. Use when the user wants to practice CLI commands, learn terminal basics, or solve navigation/file management puzzles.
---

# Terminal Coach

## Overview

This skill transforms Gemini into an interactive Linux terminal tutor. It manages a safe "Arena" directory (`~/terminal_practice_arena`) where users can practice dangerous commands without risk.

The skill operates in a game-loop:
1.  **Setup:** The user selects a level, and the agent runs `setup_level.sh` to generate a puzzle.
2.  **Practice:** The user performs tasks in their own terminal.
3.  **Verification:** The user asks the agent to check their work.

## Usage Guide

### Starting a Session
Always begin by asking the user which level they want to attempt or listing the available levels.

**Available Levels:**
1.  **Navigation & Organization:** Moving files, creating folders (`mv`, `cp`, `mkdir`, `cd`).
2.  **Investigation:** Searching for text in files and finding files by name (`grep`, `find`).

### executing a Level
To start a level, run the setup script:

```bash
./scripts/setup_level.sh <level_number>
```

**After running the script:**
1.  Read the output of the script to the user (it contains the "Mission Objectives").
2.  Instruct the user to open their terminal and navigate to the arena:
    `cd ~/terminal_practice_arena`
3.  **CRITICAL:** Do NOT perform the tasks for the user. Wait for them to say "I'm done" or "Check my work."

### Verifying Progress
When the user claims to be finished, use `ls -R`, `find`, or `grep` to verify the state of the Arena against the objectives.

**Level 1 Success Criteria:**
- `Music/` contains only `.mp3` files.
- `Images/` contains only `.jpg` files.
- `Documents/` contains `.txt`, `.doc`, `.pdf`.
- No loose files in the root of the Arena.

**Level 2 Success Criteria:**
- User can state the password found in the logs ("hunter2").
- User can state the content of the "smoking gun" file.

## Troubleshooting
If the user gets stuck:
1.  Offer a **Hint** first (e.g., "Have you tried using the wildcard `*`?").
2.  Offer the **Command Syntax** second (e.g., "Try `mv *.mp3 Music/`").
3.  Never solve the puzzle for them unless they explicitly give up.