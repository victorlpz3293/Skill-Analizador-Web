---
name: analizador-web
description: "Inspect and audit public websites with a real Chromium browser powered by Playwright for Python. Use when asked to analyze, review, audit, compare, inspect, or navigate a website, landing page, or online store; capture desktop/mobile screenshots; examine technical SEO, performance indicators, accessibility signals, security headers, browser errors, or internal links."
---

# Analizador-Web

Analizador-Web gives an AI agent a repeatable workflow for inspecting rendered websites instead of relying only on raw HTML or text extraction. It uses Chromium through the official Playwright for Python library.

## Safety and authorization

- Default scope: passive inspection of publicly accessible HTTP(S) pages.
- Only inspect a site the user owns or is authorized to assess. For third-party sites, limit work to ordinary public-page observation.
- Do not attempt exploitation, vulnerability validation, authentication bypass, port scanning, directory brute force, API enumeration, database access, or bot-protection circumvention.
- Never submit forms, create accounts, place orders, post comments, upload files, or change remote state as part of a default audit.
- Do not enter credentials, tokens, cookies, or personal data into a target site.
- Do not follow links to non-public network destinations. The scripts enforce public-address checks, but those checks are defense-in-depth, not a hardened network sandbox.
- Stop if the target requests authentication, presents a challenge, or blocks automated access. Report the limitation instead of trying to bypass it.
- Obtain explicit authorization before using the optional interaction mode. Even then, avoid actions that submit or modify data.

## Setup

From the repository root:

```bash
bash skills/analizador-web/scripts/setup.sh
```

Or install dependencies manually:

```bash
python -m pip install -r skills/analizador-web/requirements.txt
python -m playwright install chromium
```

## Run an audit

```bash
python skills/analizador-web/scripts/analyze_site.py https://example.com --out ./website-audit
```

Options:

- `--crawl N`: inspect up to N additional same-host HTML pages (default 0; maximum 20).
- `--no-mobile`: skip mobile viewport screenshot.
- `--wait MS`: extra wait after page load (default 1000).
- `--timeout MS`: navigation timeout (default 30000).
- `--check-links N`: check up to N same-host links with HEAD only (default 0; maximum 40).
- `--include-text-excerpt`: include a short rendered-text excerpt in the JSON report. Off by default.

Output includes `report.json`, `summary.md`, and screenshots under `screenshots/`.

## Review the evidence

1. Read `summary.md` and `report.json`.
2. Open desktop and mobile screenshots. Do not infer visual quality from metrics alone.
3. Separate observed facts from hypotheses. Technology detection is heuristic.
4. Treat browser timing as a single-run field observation, not a laboratory benchmark.
5. Report unavailable measurements explicitly. Do not label the audit a penetration test or formal accessibility certification.
6. Use `references/checklist.md` to interpret findings and prioritize remediation.

## Optional controlled interaction

The interaction script is read-only by default. It supports navigation, waits, scrolling, screenshots, and text extraction without enabling page controls.

```bash
python skills/analizador-web/scripts/interact.py https://example.com --steps ./steps.json --out ./website-audit
```

The optional `click`, `fill`, and `press` actions require `--allow-interactions`. This flag is not permission to submit forms or change production data. Use only on an authorized test environment with test accounts, and do not activate purchase, delete, publish, payment, or submission controls.

Example read-only steps:

```json
[
  {"action": "wait", "ms": 1000},
  {"action": "scroll", "y": 700},
  {"action": "screenshot", "name": "below-fold", "full_page": true},
  {"action": "text", "selector": "main"}
]
```

## Reporting format

Include:
1. Scope, target URL, date/time, and limitations.
2. Executive summary with the highest-impact observations.
3. Visual review of desktop and mobile screenshots.
4. Technical SEO observations.
5. Performance indicators and resource findings.
6. Accessibility signals requiring manual review.
7. HTTPS and response-header observations.
8. Console errors, failed requests, and HTTP errors.
9. Prioritized recommendations with evidence and confidence.
10. Items not tested.

Never claim a vulnerability solely because a header is absent. Describe missing headers as configuration observations and explain context.
