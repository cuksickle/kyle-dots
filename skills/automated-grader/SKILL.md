---
name: automated-grader
description: Evaluate student submissions (text, code, or video transcripts) based on a strict local rubric. Use when the user wants to generate high-quality feedback or first-pass grades.
---

# Automated Grader Framework

Evaluate student work against a strictly defined rubric to ensure consistency and minimize hallucination.

## Grading Protocol

### 1. Preparation (Context Building)
Before grading, you MUST:
- **Read the Rubric:** Read a local `RUBRIC.md` or a rubric snippet in the context.
- **Read the Context:** Understand the original assignment instructions and goals.
- **Read the Submission:** Fetch the student's work (e.g., from a Google Doc using `google_all_in_one` or a local text file).

### 2. Evaluation Logic
Assess the student's work category-by-category. For each category in the rubric, provide:
- **Raw Score:** (e.g., 1-4, 0-10) based on the criteria.
- **Evidence:** Quote 1-2 sentences from the student's work that justify the score.
- **Improvement Tip:** Concrete, non-judgmental feedback on how to move to the next tier.

### 3. Feedback Principles
- **Growth Mindset:** Frame feedback as "Here's how to improve" rather than "Here's why you failed."
- **Empathetic Voice:** Use the teacher's voice ("I noticed you used X effectively... I wonder if you could try Y next time?").
- **Clarity over Brevity:** Explain the reasoning behind the grade so the student understands the "Why."

### 4. Output Formats
Generate one of the following based on the request:
- **Full Report:** (Markdown) A detailed breakdown for the student.
- **Gradebook Entry:** (CSV or JSON) A summary for easy import into Google Sheets.
- **Google Doc Comment:** A concise summary of 2-3 key feedback points to be posted as a comment.

## Specialized Workflows

### 1. Form/Sheet Handoff
When grading submissions from a Google Form (created via `classroom-form-wizard`):
1.  **Access Data:** Retrieve the linked Google Sheet URL from the user or Drive.
2.  **Match Rubric:** Locate the associated Rubric Doc created during the assignment setup.
3.  **Evaluate:** Use the Python backend to iterate through Sheet rows, matching names to Classroom students, and apply the rubric logic to the paragraph responses.
4.  **Feedback:** Generate a CSV or update the Sheet with suggested grades and feedback strings.

## Troubleshooting
- If the submission is too long for a single prompt, evaluate it section-by-section.
- If the rubric is ambiguous, ask the teacher for clarification before finalizing the grade.
