#!/bin/bash
# Connect your local Modal login (~/.modal.toml, active profile) to the hosted Valkyrie org
# as the "modal" sandbox provider, with the VM runtime that multi-container (sidecar) tasks need.
# The token is passed straight from the file to `valkyrie secret set`; nothing is printed.
set -euo pipefail
unset VALKYRIE_URL
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
"$(dirname "$0")/../valkyrie/.bin/uv" run --quiet --no-project --python 3.12 python - "$tmp" <<'EOF'
import json, sys, tomllib
from pathlib import Path
cfg = tomllib.loads((Path.home() / ".modal.toml").read_text())
prof = next((v for v in cfg.values() if isinstance(v, dict) and v.get("active")), None) or next(v for v in cfg.values() if isinstance(v, dict))
json.dump({"MODAL_TOKEN_ID": prof["token_id"], "MODAL_TOKEN_SECRET": prof["token_secret"], "runtime": "vm"}, open(sys.argv[1], "w"))
EOF
valkyrie secret set modal-credentials < "$tmp"
valkyrie provider set modal modal-credentials
valkyrie provider default modal
valkyrie provider list
