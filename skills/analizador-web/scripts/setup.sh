#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="${PYTHON:-python3}"

"${PYTHON}" -m pip install -r "${ROOT}/skills/analizador-web/requirements.txt"
"${PYTHON}" -m playwright install chromium

echo "Analizador-Web dependencies installed."
