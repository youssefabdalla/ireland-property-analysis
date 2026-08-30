#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PATH="$HOME/.local/bin:$PATH"

# If a valid project env already exists, do nothing.
if [ -x .venv/bin/python ]; then
  if .venv/bin/python - <<'PY'
import sys
try:
    import pytest
except Exception:
    raise SystemExit(1)
if not (sys.version_info[:2] >= (3, 12) and sys.version_info[:2] < (3, 13)):
    raise SystemExit(1)
PY
  then
    echo "Existing environment is valid; skipping bootstrap."
    exit 0
  fi
fi

echo "Environment missing or invalid; resetting it."

# Install Poetry if needed
if ! command -v poetry >/dev/null 2>&1; then
  curl -sSL https://install.python-poetry.org | python3 -
fi

# Use a real interpreter before recreating the venv
PYTHON_BIN=""
for candidate in python3.12 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v "$candidate")"
    break
  fi
done

if [ -z "$PYTHON_BIN" ]; then
  echo "No supported Python interpreter found. Need Python 3.12."
  exit 1
fi

rm -rf .venv
poetry env use "$PYTHON_BIN"
poetry config virtualenvs.in-project true
poetry install --with dev --no-root

# Keep your existing repo hook cleanup
rm -f .git/hooks/post-commit .git/hooks/pre-push

echo "Bootstrap complete."