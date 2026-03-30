---
name: splitrail-usage
description: Real-time token usage and cost monitoring for AI coding tools. Use when you need to track your usage stats, analyze costs across different tools, or get a daily summary of your AI consumption.
---

# Splitrail Usage

`splitrail` is a token usage and cost monitor for Gemini CLI, Claude Code, and other AI coding agents.

## When to Use This Skill
- **Usage Analysis:** When you need to see your token consumption across sessions or tools.
- **Cost Tracking:** When you want a cost breakdown for a specific date range.
- **MCP Queries:** When you need to programmatically query usage statistics.

## Core Commands
- `splitrail stats --json`: Get current usage statistics as a JSON payload.
- `splitrail config`: Manage configuration (API tokens, upload settings).
- `splitrail upload`: Manually sync local usage data to the Splitrail Cloud.

## MCP Tools (Available via `splitrail` server)
- `get_daily_stats`: Date-filtered usage statistics.
- `get_model_usage`: Analysis of model distribution (Pro, Flash, etc.).
- `get_cost_breakdown`: Cost monitoring over a date range.
- `get_file_operations`: Statistics on how many files were modified.
- `compare_tools`: Compare your usage across different AI tools (Gemini CLI vs others).

## Example Queries
1. **Stats**: `splitrail stats --json`
2. **Cost**: `splitrail mcp call get_cost_breakdown --start-date 2024-01-01`
