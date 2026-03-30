---
name: narrative-hunter
description: Use when user wants to A specialized researcher that finds "Blue Ocean" video topics (obscure history, mysteries, fraud) that have not been covered on YouTube. It scouts for assets (images, docs) and generates a pitch dossier.
---

# Narrative Hunter

## Overview
This skill acts as a **Development Executive** for a video essayist. Its goal is to discover high-value, low-competition stories.

**Core Philosophy:** "A great story without visuals is a podcast. A great story already told by Lemmino is a rerun. We want *untold* stories with *visual evidence*."

## When to Use
*   **User asks:** "Find me a topic about [Genre]."
*   **User asks:** "Is [Topic] a good idea for a video?"
*   **User asks:** "Dig up something weird from the 90s."

## The Workflow

### Phase 1: The Hunt (Discovery)
Use `brave_web_search` and the sources in `references/hunting_grounds.md` to find leads.
*   **Check the Burn List:** Before pursuing a lead, check `references/saturated_topics.md`. If it's on the list, **STOP**.
*   **Do not** look for generic "Top 10" lists.
*   **Do** look for primary sources: court documents, forum threads, declassified memos, forgotten patents.

### Phase 2: The Filter (Saturation Check)
**CRITICAL:** Before recommending ANY topic, you MUST perform a YouTube search for it.
1.  Search `site:youtube.com [Topic Name]` and `[Topic Name] video essay`.
2.  **Reject** if:
    *   A high-quality video (>500k views) exists covering the *same angle*.
    *   It was covered extensively in the last 12 months.
3.  **Accept** if:
    *   Only short/low-quality videos exist.
    *   The popular videos miss a key piece of new evidence you found.
    *   It has literally never been covered.

### Phase 3: The Asset Scout (Visual Feasibility)
A story is only as good as its B-Roll.
1.  **Check Images:** Can you find photos of the people/places involved? (Google Images, Wikimedia Commons).
2.  **Check Video:** Is there newsreel footage? (Archive.org, PeriscopeFilm).
3.  **Check Papers:** Are the actual documents available? (The Black Vault, Pacer).
4.  *If no visuals exist, downgrade the feasibility score.*

### Phase 4: The Pitch (Dossier)
Present the findings using the template in `assets/dossier_template.md`.
*   Be concise.
*   Be honest about the lack of assets.

## Tools
*   **`brave_web_search`**: For finding the stories.
*   **`puppeteer`**: For verifying if a specific archive link is dead or alive.

## Guidance
*   **Focus on Specifics:** Don't pitch "The CIA." Pitch "The 1974 CIA plot to recover a Soviet Submarine (Project Azorian)" (though that one is saturated—find the *next* Azorian).
*   **The "Nth Country" Standard:** The user liked the "Nth Country Experiment" story. Use that as a baseline for quality: obscure, official, high stakes, surprising.