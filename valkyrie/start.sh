#!/bin/bash
# Start the behavior-probe benchmark service (port 8001, probe server 8020) and a local
# Valkyrie Tracker (port 8000) with Docker sandboxes. Ctrl-C stops both.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HERE/.bin:$PATH"   # uv >= 0.13.5 for the tracker

cd "$HERE/behavior-probe-benchmark-service"
CBS_DOCKER_ENABLED=true .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 &
SVC=$!
trap 'kill $SVC 2>/dev/null' EXIT

cd "$HERE/Valkyrie"
export EXECUTOR_BOOTSTRAP_KEY="${EXECUTOR_BOOTSTRAP_KEY:-$(openssl rand -hex 24)}"
make local-tracker
