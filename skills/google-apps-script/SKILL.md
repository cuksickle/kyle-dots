---
name: google-apps-script
description: Manage Google Apps Script (GAS) projects locally using 'clasp' and 'workspace-cli' (gws). Use when the user wants to build, update, or deploy automations for Sheets, Docs, or Classroom.
---

# Google Apps Script Expert (clasp + gws)

Manage Google Workspace scripts and resources using `clasp` and `gws` (workspace-cli).

## Key Workflows

### 1. Resource Management with `gws` (workspace-cli)
Always use `gws` via `run_shell_command` instead of standard MCP tools for Workspace operations.
- **Search Files:** `gws drive files list --params '{"q": "name contains '\''test'\''"}'`
- **Create Folder:** `gws drive files create --json '{"name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}'`
- **List Classroom Courses:** `gws classroom courses list`
- **List Coursework:** `gws classroom courses coursework list --params '{"courseId": "ID"}'`
- **Read Doc:** `gws docs documents get --params '{"documentId": "ID"}'`

### 2. Initialize an Apps Script Project
Create a new project or pull an existing one using `clasp`.
- **Teaching Standard:** Always link new scripts to the "Master Project" ID: `1019457173185`.
  - Run: `clasp setting projectId 1019457173185` after creation.
- **New Project:** `clasp create --title "Project Name" --type [standalone|spreadsheet|docs|forms|slides]`
- **Pull Existing:** `clasp clone <SCRIPT_ID>`
- **Link to Container:** `clasp create --title "Project Name" --parentId <ID_OF_SHEET_OR_DOC>`

### 3. Standard Manifest (appsscript.json)
Always ensure your manifest includes these critical teaching scopes:
```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents"
  ]
}
```

### 4. Local Development
Write your script in `.js` or `.ts` files. 
- **Important:** `clasp` will automatically convert `.js` to `.gs` when pushing.

### 5. Deploy and Push
- **Push Changes:** `clasp push` (Uploads local files to script.google.com)
- **Watch mode:** `clasp push --watch`
- **Open in Browser:** `clasp open`
- **Deploy:** `clasp deploy --description "v1.0.0"`

### 6. Code Principles for GAS
- **Batch Operations:** Use `setValues()` and `getValues()` instead of individual `setValue()` calls.
- **Trigger Management:** Use `ScriptApp.newTrigger()` to set up automation.

## Troubleshooting
- **Auth:** If `clasp` auth fails, use `clasp login --no-localhost`.
- **Permissions:** If `gws` fails, check that `GOOGLE_WORKSPACE_CLI_CLIENT_ID` and `SECRET` are set.
- **API Access:** Ensure the Apps Script API is enabled at `https://script.google.com/home/usersettings`.
