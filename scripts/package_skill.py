#!/usr/bin/env python3
"""Build a Claude.ai-compatible ZIP from the portable Agent Skill folder."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "analizador-web"
DIST = ROOT / "dist"
OUTPUT = DIST / "analizador-web-1.0.0.zip"

def main():
    if not (SKILL / "SKILL.md").is_file():
        raise SystemExit("Skill folder or SKILL.md not found")
    DIST.mkdir(exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, path.relative_to(SKILL))
    print(OUTPUT)

if __name__ == "__main__":
    main()
