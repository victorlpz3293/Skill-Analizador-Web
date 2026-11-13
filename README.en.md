# Analizador-Web

**Bilingual Website Audit & Inspection Agent Skill**

Analizador-Web is an independent, portable Agent Skill maintained by [@victorlpz3293](https://github.com/victorlpz3293). It helps compatible AI agents inspect public websites using a real Chromium browser powered by the official [Playwright for Python](https://playwright.dev/python/) framework.

The Skill and its documentation are available in Spanish and English. The agent should respond in the user's language and can produce complete reports in either language.

**Documentación en español:** consulta [README.md](README.md).

## What it does

- Renders JavaScript-driven websites in Chromium.
- Captures full-page desktop and mobile screenshots.
- Collects technical SEO metadata and heading structure.
- Measures browser timing and transferred-resource indicators.
- Identifies potentially heavy resources and technology signatures (heuristic).
- Reports selected accessibility indicators.
- Reviews HTTPS/TLS status and common security response headers.
- Records browser console errors, failed requests, and HTTP error responses.
- Checks a bounded number of same-host links using HEAD requests only.
- Exports JSON and Markdown evidence for human or AI review.

## What it does not do

Analizador-Web is designed for passive inspection of public websites. It does not perform penetration testing, exploit vulnerabilities, enumerate ports, probe databases or APIs, bypass access controls, defeat bot protections, or submit real forms by default.

## Requirements

- Python 3.10 or later.
- Playwright for Python.
- Chromium installed through Playwright. If using a system-managed Chromium binary, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to its full path.
- Network access during initial dependency/browser setup and to the public target site.

## Quick start

From the repository root:

```bash
bash skills/analizador-web/scripts/setup.sh
.venv/bin/python skills/analizador-web/scripts/analyze_site.py https://example.com --out ./website-audit
```

Windows PowerShell setup:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r skills/analizador-web/requirements.txt
python -m playwright install chromium
python skills/analizador-web/scripts/analyze_site.py https://example.com --out .\website-audit
```

See [SKILL.md](skills/analizador-web/SKILL.md) for agent instructions, options, and safety rules. Checklists are available in [English](skills/analizador-web/references/checklist.en.md) and [Spanish](skills/analizador-web/references/checklist.es.md). Run the automated safety checks with `python -m unittest discover -s tests -v`.

## Install as an Agent Skill

This repository follows the open Agent Skills folder convention. Install or copy `skills/analizador-web/` into the skill directory documented by your agent.

Examples:

- Claude Code (user scope): `~/.claude/skills/analizador-web/`
- Claude Code (project scope): `.claude/skills/analizador-web/`
- Other Agent Skills-compatible clients: use the client's documented skills directory.

For Claude.ai, create the upload ZIP with `python scripts/package_skill.py` (Windows: `py scripts/package_skill.py`). Upload `dist/analizador-web-1.1.0.zip` through **Settings / Customize → Skills** (availability and menu labels may vary by plan and client version). The packaging script places `SKILL.md` at the ZIP root, as required by the Skill upload flow.

The skill instructions can be loaded in clients that support Agent Skills. Actual script execution still depends on the client's code-execution environment having Python, Playwright, Chromium, and permitted network access.

## Safety model

By default, the scripts:

- Accept HTTP(S) URLs on standard ports 80 and 443 only.
- Reject hosts that resolve to loopback, private, link-local, reserved, or otherwise non-public IP addresses.
- Apply the destination check to browser HTTP(S) requests, including redirects and subresources.
- Block write-method HTTP requests (`POST`, `PUT`, `PATCH`, `DELETE`, etc.).
- Keep interaction actions (`click`, `fill`, `press`) disabled unless explicitly enabled.
- Avoid retrying failed HEAD link checks with GET.
- Limit crawling to 20 pages total.
- Omit rendered page-text excerpts unless explicitly requested.

These application-level controls reduce risk but are not a hardened sandbox and cannot eliminate DNS rebinding, browser, dependency, or infrastructure risks. Browser request interception can also affect observed load timings. Use a dedicated isolated environment and obtain authorization before testing a site.

## Privacy

Audit artifacts can contain website titles, metadata, URLs, resource names, browser errors, and screenshots. Query-string values are redacted in URLs written by the scripts, and page-text excerpts are disabled by default. Screenshots and page metadata may still contain sensitive information. Inspect artifacts before publishing or sharing them.

## Project structure

```text
skills/analizador-web/
├── SKILL.md
├── references/
│   ├── checklist.md
│   ├── checklist.es.md
│   └── checklist.en.md
├── scripts/
│   ├── analyze_site.py
│   ├── interact.py
│   └── safety.py
└── requirements.txt
```

## Attribution and independence

Analizador-Web is an independent community skill maintained by **@victorlpz3293**. It uses the Playwright framework; Playwright is a Microsoft project distributed under the Apache License 2.0. This repository is not affiliated with, sponsored by, or endorsed by Microsoft or Anthropic. Product and company names are used only to identify compatible software.

## License

The original material in this repository is made available under the MIT License. See [LICENSE](LICENSE). Third-party software (including Playwright and Chromium) remains subject to its own licenses.

## Contributions and security

Contributions are welcome. Read [CONTRIBUTING.en.md](CONTRIBUTING.en.md) and [SECURITY.en.md](SECURITY.en.md). Spanish versions are available as [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).
