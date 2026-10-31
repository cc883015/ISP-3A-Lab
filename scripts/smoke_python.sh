#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
if [[ -x "$root/.venv/bin/python3" ]]; then
  PYTHON="$root/.venv/bin/python3"
else
  PYTHON="python3"
fi

files=$(find python -name '*.py' | sort)
fail=0
for f in $files; do
  echo "-------- $f --------"
  if ! "$PYTHON" "$f"; then
    echo "FAILED $f" >&2
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "python smoke failed" >&2
  exit 1
fi
echo "python smoke ok"
