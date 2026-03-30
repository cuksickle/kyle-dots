---
name: e2e-validator
description: Automated browser-based smoke tests for frontend validation using web-monolith-mcp.
---

# E2E Validator: The Browser-Based Smoke Test

## Core Mission
Ensure that frontend changes are verified exactly as a user would. This skill detects UI breakage, navigation failures, and "silent" errors (like console logs or broken forms) that static analysis and unit tests miss.

## Workflow Patterns

### 1. Preparation
- **Dev Server Check:** Ensure the local dev server is running (e.g., `npm run dev`, `python server.py`).
- **Target URL:** Identify the primary URL for testing (e.g., `http://localhost:5173`).

### 2. Execution (The Smoke Test)
- **Navigate:** Use `get_page_map(url="...")` to open the app.
- **Map State:** Analyze the `Actions` and `web_content` in the page map to find points of interest.
- **Interact:** Use `execute_action` to perform critical user flows:
    - Click primary navigation links.
    - Fill and submit forms (`fill_form`).
    - Trigger dynamic UI elements (modals, dropdowns).
- **Wait for Stability:** Use `wait_for` to ensure transitions or content loads are complete.

### 3. Verification
- **Visual Checks:** Verify that key text elements are present.
- **Error Detection:** Check if the browser returned a `navigation_blocked` or if the page content indicates an error state.
- **Page State:** Use `get_page_state` to confirm the final URL is correct.

## Self-Healing Loop
If an E2E test fails (e.g., a button is missing, or a form submission does not show success text):
1. **Analyze Failure:** Read the `get_page_map` output for clues (e.g., a "404" message or a malformed UI).
2. **Diagnose:** Compare the current UI against the intended implementation in your plan.
3. **Correct:** Return to **Plan Mode**, adjust your implementation strategy, and apply a fix.
4. **Re-Validate:** Restart the E2E validator until the smoke test passes.

## Example Command
"Activate the `e2e-validator` skill and perform a smoke test on the login flow at `http://localhost:3000/login`."
