#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "[ERROR] .venv not found. Create it first:"
  echo "  python3 -m venv .venv"
  exit 1
fi

source .venv/bin/activate
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/matplotlib-config}"
mkdir -p "$MPLCONFIGDIR"

echo "[1/4] import check"
python -c "import fastapi, numpy, pandas, sklearn, matplotlib; print('imports ok')"

echo "[2/4] backend practice run check"
python backend/app/chapters/chapter07/practice.py >/tmp/ch07.out
python backend/app/chapters/chapter100/practice.py >/tmp/ch100.out
python backend/app/chapters/chapter103/practice.py >/tmp/ch103.out
python backend/app/chapters/chapter112/practice.py >/tmp/ch112.out
echo "practice checks ok"

echo "[3/4] api smoke check"
uvicorn backend.app.main:app --host 127.0.0.1 --port 8888 >/tmp/uvicorn_smoke.log 2>&1 &
UVICORN_PID=$!
trap 'kill "$UVICORN_PID" >/dev/null 2>&1 || true' EXIT

READY=0
for i in $(seq 1 15); do
  if curl -fsS http://127.0.0.1:8888/api/health >/tmp/api_health.json 2>/tmp/api_health.err; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" -ne 1 ]]; then
  echo "[ERROR] API did not become ready in time."
  echo "--- uvicorn log ---"
  sed -n '1,200p' /tmp/uvicorn_smoke.log || true
  echo "--- health curl error ---"
  sed -n '1,200p' /tmp/api_health.err || true
  exit 1
fi

curl -fsS http://127.0.0.1:8888/api/chapters >/tmp/api_chapters.json
curl -fsS -X POST http://127.0.0.1:8888/api/chapters/chapter07/run >/tmp/api_run_ch07.json
echo "api checks ok"

echo "[4/4] summary"
python - <<'PY'
import json
from pathlib import Path

health = json.loads(Path("/tmp/api_health.json").read_text())
chapters = json.loads(Path("/tmp/api_chapters.json").read_text())
run_ch07 = json.loads(Path("/tmp/api_run_ch07.json").read_text())

print("health:", health)
print("chapters_count:", len(chapters))
print("chapter07_run_keys:", sorted(run_ch07.keys()))
PY

echo "runtime smoke check completed"
