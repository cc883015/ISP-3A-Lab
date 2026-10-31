#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if [[ -x "$root/.venv/bin/python" ]]; then
  PY="$root/.venv/bin/python"
else
  PY="python3"
fi

"$PY" -c "import fastapi,uvicorn" 2>/dev/null || {
  echo "install API deps:  $PY -m pip install -r requirements.txt" >&2
  exit 1
}

echo "API  http://127.0.0.1:8788"
echo "Web  http://127.0.0.1:5173"
"$PY" "$root/apps/iq_lab/server.py" &
api_pid=$!
trap 'kill "$api_pid" 2>/dev/null || true' EXIT

cd "$root/web"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm run dev
