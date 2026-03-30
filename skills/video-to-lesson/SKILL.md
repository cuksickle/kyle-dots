---
name: video-to-lesson
description: Convert any video (YouTube, local, or archive) into a structured Google Classroom lesson. Use when the user wants to turn video content into an educational activity.
---

# Video-to-Lesson Architect

Turn video content into structured lesson materials for students.

## Workflow Patterns

### 1. Source Context Gathering
- **Fetch Transcript:** Use local STT tools or `yt-dlp` to get the video's transcript.
- **Analyze Content:** Extract key concepts, timeline events, and educational outcomes.
- **Identify Target:** Determine the target grade level or subject area.

### 2. Lesson Structure Generation
Generate the following components for each lesson:
- **Title:** Engaging, inquiry-based title.
- **Hook:** A "warm-up" question to engage students before they watch.
- **Guided Notes:** 5-10 fill-in-the-blank or short-answer questions based on the transcript.
- **Check for Understanding:** 3-5 multiple-choice questions or a reflection prompt.
- **Extension Activity:** A higher-order thinking task (e.g., "Imagine if X didn't happen...").

### 3. Google Workspace Integration
- **Create Google Doc:** Use `google_all_in_one` to generate the lesson as a Doc.
- **Upload to Classroom:** Use `classroom-admin` or `google_all_in_one` to attach the Doc to a new Classroom material.
- **Link Video:** Ensure the original YouTube/Archive link is attached.

### 4. Educational Standards Alignment
- **Rubric Construction:** (Optionally) Build a simple rubric for the lesson's activities.
- **Alignment:** Tag the lesson with relevant standards (e.g., CCSS.ELA-LITERACY.RI.9-10.1).

## Troubleshooting
- If the video is long, focus on the most educationally dense 5-10 minutes.
- If the transcript is noisy (bad STT), ask the user for a summary or to verify key points before building the lesson.
