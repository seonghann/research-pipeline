#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import tomllib' 2>/dev/null; then
    exec "$candidate" "$SCRIPT_DIR/scripts/codex_setup.py" "$@"
  fi
done
if command -v uv >/dev/null 2>&1; then
  exec uv run --python 3.11 --no-project "$SCRIPT_DIR/scripts/codex_setup.py" "$@"
fi
echo 'Python 3.11+ or uv is required.' >&2
exit 1
