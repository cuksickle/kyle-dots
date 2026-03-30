---
description: Scaffold a new MCP server project
---

## Scaffold MCP Server

Create a new MCP server project with the official SDK.

**Usage:** `/scaffold-mcp [server-name] [python|typescript]`

1. Parse `$ARGUMENTS` for server name and language (default: typescript).
2. Create project structure:
   ```
   {server-name}/
   ├── src/
   │   └── index.ts        # Server entry point
   ├── tests/
   │   └── server.test.ts  # Basic tests
   ├── package.json        # With @modelcontextprotocol/sdk
   ├── tsconfig.json
   ├── README.md
   └── .gitignore
   ```
3. Generate a minimal MCP server with:
   - One example tool with proper schema
   - One example resource
   - Transport setup (stdio)
   - Error handling
4. Run `npm install` to fetch dependencies.
5. Report structure and how to run: `npx tsx src/index.ts`
