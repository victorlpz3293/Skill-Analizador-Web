#!/usr/bin/env python3
"""Build a Claude.ai-compatible ZIP from the portable Agent Skill folder."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "analizador-web"
DIST = ROOT / "dist"
OUTPUT = DIST / "analizador-web-1.1.0.zip"

def main():
    required = [SKILL / "SKILL.md", SKILL / "references" / "checklist.es.md", SKILL / "references" / "checklist.en.md"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing required bilingual Skill files: " + ", ".join(missing))
    DIST.mkdir(exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, path.relative_to(SKILL))
    print(OUTPUT)

if __name__ == "__main__":
    main()
