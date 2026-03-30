---
name: google-workspace-cli
description: Official Google Workspace CLI (gws) expert. Use for managing Drive files, Sheets data, Docs content, and Classroom resources directly via the command line.
---

# Google Workspace CLI Expert (gws)

The `gws` tool provides a powerful command-line interface for interacting with the Google Workspace APIs. It is more reliable than standard MCP tools for complex document building and Classroom management.

## Command Syntax
`gws <service> <resource> [sub-resource] <method> [flags]`

### Core Services
- **drive**: Files, folders, permissions, exports.
- **docs**: Reading and updating document content (batchUpdate).
- **sheets**: Managing spreadsheets, reading/writing ranges.
- **classroom**: Courses, coursework, submissions, rosters.
- **forms**: Creating and managing Google Forms.
- **gmail**: Sending, reading, and managing messages/labels.

## Key Workflows

### 1. Drive Operations
- **Search Files:** `gws drive files list --params '{"q": "name contains '\''Test'\''"}'`
- **Create Folder:** `gws drive files create --json '{"name": "Folder Name", "mimeType": "application/vnd.google-apps.folder"}'`
- **Export Doc to Text:** `gws drive files export --params '{"fileId": "ID", "mimeType": "text/plain"}'`

### 2. Google Docs (batchUpdate)
Updating documents requires a JSON payload of requests. Use a temporary file for large payloads.
- **Get Doc Structure:** `gws docs documents get --params '{"documentId": "ID"}'`
- **Apply Updates:** `gws docs documents batchUpdate --params '{"documentId": "ID"}' --json "$(cat payload.json)"`

### 3. Google Classroom
- **List Courses:** `gws classroom courses list --params '{"courseStates": "ACTIVE"}'`
- **List CourseWork:** `gws classroom courses courseWork list --params '{"courseId": "ID"}'`
- **List Submissions:** `gws classroom courses courseWork studentSubmissions list --params '{"courseId": "ID", "courseWorkId": "ID"}'`

### 4. Google Sheets
- **Get Spreadsheet:** `gws sheets spreadsheets get --params '{"spreadsheetId": "ID"}'`
- **Read Values:** `gws sheets spreadsheets values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C10"}'`

## Critical Flags
- `--params <JSON>`: URL/Query parameters (filters, page sizes).
- `--json <JSON>`: Request body for POST/PATCH/PUT operations.
- `--format <json|table|csv>`: Control output format (default is JSON).
- `--page-all`: Automatically fetch all pages of results.

## Configuration & Environment
- **Auth:** If authentication expires, use `clasp login --no-localhost` (as `gws` and `clasp` share credentials in this environment).
- **Project IDs:** Ensure `GOOGLE_WORKSPACE_PROJECT_ID` is set to the Master Project (`1019457173185`) for teaching tools.

## Multi-Account Management
To manage multiple accounts (e.g., Work and Personal), use separate configuration directories via the `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` environment variable.

### Setup Patterns
1. **Work Account:**
   ```bash
   export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-work
   gws auth login
   ```
2. **Personal Account:**
   ```bash
   export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal
   gws auth login
   ```

### Recommended Aliases
Use these aliases in `~/.zshrc` for seamless switching:
- `gws-work`: Points to work config.
- `gws-pers`: Points to personal config.

## Best Practices
- **Escaping:** When using `--params` or `--json` in a shell command, be careful with nested single quotes. Use `'\''` or save the JSON to a file first.
- **Piping:** Pipe output to `jq` for precise data extraction.
- **Validation:** Always verify a file's existence with `gws drive files get` before attempting updates.
- **Isolation:** Always use the appropriate alias (`gws-work` vs `gws-pers`) to avoid data leakage between accounts.
