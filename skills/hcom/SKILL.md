---
name: hcom
description: Multi-agent communication and coordination across terminals. Use when multiple agents need to synchronize, share context, or coordinate on complex tasks.
---

# hcom

`hcom` is used to connect independent agents running in different terminals. 

## When to Use This Skill
- **Syncing Context:** When you need to send context or results to another agent (e.g., "send my last test results to the reviewer agent").
- **Watching Events:** When you want to be notified if another agent modifies a file or goes idle.
- **Spawning Agents:** When a task is too large for one session and you want to delegate a sub-task to a new agent instance.
- **Conflict Prevention:** When multiple agents are working in the same directory (collision detection).

## Core Commands

### Messaging
- `hcom send @target -- message`: Send a message to a specific agent (e.g., `@nova`).
- `hcom send -- message`: Broadcast to all connected agents.
- `hcom listen --wait [SEC]`: Wait for an incoming message or event.

### Coordination
- `hcom list`: See all active agents and their status.
- `hcom events --agent NAME --type status --status listening --wait`: Wait for another agent to become idle.
- `hcom events --collision`: Check for recent file edit collisions between agents.

### Context Sharing (Bundles)
- `hcom bundle prepare`: Get suggestions for context to share (transcript, files, events).
- `hcom send @target --title "Refactoring Plan" --files auth.py --transcript 10-15:full -- "Here is the context."`

## Launching Agents
- `hcom 1 gemini`: Launch a new Gemini agent in a new terminal pane.
- `hcom f <name>`: Fork an existing agent's session to parallelize an investigation.

## Example Workflows
1. **Delegation**: `hcom 1 gemini --hcom-prompt "analyze src/auth.py and report back to @self"`
2. **Review**: `hcom send @reviewer -- "I finished the fix in bug.py. Please audit."`
