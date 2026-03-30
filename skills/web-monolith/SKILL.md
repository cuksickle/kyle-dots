---
name: web-monolith
description: A comprehensive suite of web, network, and data processing CLI tools (xh, curlie, jq, htmlq, nushell, websocat, grpcurl, aria2c).
---

# Skill: Web Monolith CLI Tools

A comprehensive suite of web, network, and data processing CLI tools.

## Core Mandate
This skill provides direct access to high-performance CLI tools for network requests (xh, curlie), data processing (nu, jq, htmlq), and browser automation.

## Available Tools

### Network & APIs
- **xh**: A fast, user-friendly HTTP client. (Path: /home/kyle/.cargo/bin/xh)
  - **Usage**: run_shell_command("/home/kyle/.cargo/bin/xh --ignore-stdin --timeout 10 --check-status [args]")
- **curlie**: A frontend to curl with httpie syntax. (Path: /home/kyle/.local/bin/curlie)

### Data Processing
- **nu (Nushell)**: A modern shell that treats data as structured tables. (Path: /home/kyle/.cargo/bin/nu)
- **jq**: Lightweight JSON processor.
- **htmlq**: HTML extractor using CSS selectors. (Path: /home/kyle/.cargo/bin/htmlq)

## Verification
Run: /home/kyle/.cargo/bin/xh --ignore-stdin --timeout 10 --check-status https://httpbin.org/ip
