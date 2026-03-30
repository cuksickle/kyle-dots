---
name: classroom-form-wizard
description: Use when user wants to A "Zero-Touch" automation assistant that turns text prompts or lesson materials into live-graded Google Forms and Classroom assignments. It uses a Master Control project to bypass school IT blocks and Gemini Flash for real-time grading.
---

# Classroom Form Wizard (Master Edition)

Automate the full pipeline from Curriculum -> Form -> Classroom -> Real-time Grading.

## Core Setup
- **Webhook URL:** `https://script.google.com/macros/s/AKfycbzeZ2yQfEiIyDK8aSqqWlyY3bIDlDTlyzECk_B6M0PIz_1kZnsljTsbi4LaqjR9eqTH/exec`
- **Local Project Path:** `~/git/classroom-master-control`
- **Grading Engine:** The webhook uses `gemini-2.5-flash` natively within Workspace for subject-agnostic evaluation.

## Zero-Touch Workflow

### 1. Material Discovery (Optional)
If the user asks for a specific lesson (e.g., "Unit 2 Lesson 10"), search Google Drive for the source material (Docs/PDFs) to ensure the form content is accurate.
- **Tools:** `google-workspace.drive.search`, `google-workspace.docs.getText`.

### 2. Job Execution (True Zero-Touch)
Analyze the request or lesson materials, construct a JSON payload, and send it directly to the Webhook. Do NOT write `Job.js` or use `clasp` anymore.

- **Payload Schema:**
  ```json
  {
    "title": "Assignment Title",
    "description": "Instructions for students...",
    "subjectSearchTerm": "Biology", 
    "questions": [
      { "title": "Question 1?", "type": "paragraph" },
      { "title": "Question 2?", "type": "choice", "choices": ["A", "B"] }
    ]
  }
  ```

- **Execution Script:** Use a Python script (e.g., `trigger_webhook.py`) to send the JSON payload to the Webhook URL. The webhook will automatically:
  1. Create the Form.
  2. Create the Sheet.
  3. Attach the Auto-Grader trigger.
  4. Draft the Assignment in Classroom.

### 3. Handoff
Provide the user with the Form and Sheet URLs returned by the Webhook. The assignment is already drafted in Classroom!

## Real-time Grading
The script automatically attaches a trigger to all generated sheets. Every student submission is graded instantly.
- **Personalities:** Automatically swaps between "CONCEPTUAL" (Engineering/Brainstorms) and "FACTUAL" (Biology/Quizzes) based on header context.

## Troubleshooting
- **401/404 Errors:** Never use local Python tools to access Workspace files. Always use the `Master Control` Apps Script environment via `UrlFetchApp`.
- **Missing Courses:** If `findTargetCourses` fails, ensure the `subjectSearchTerm` matches a partial name of the course in Classroom.
