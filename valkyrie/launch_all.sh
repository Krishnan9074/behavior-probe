#!/bin/bash
# Launch 5 models x 2 datasets on the local Tracker; run IDs go to runs.tsv.
set -euo pipefail
export VALKYRIE_URL=http://127.0.0.1:8000
cd "$(dirname "$0")"
: > runs.tsv
while read -r agent model secret; do
  for ds in noprobe probe10; do
    id=$(valkyrie run start --agent "$agent" --benchmark behavior-probe --dataset "$ds" \
      --model "$model" --provider docker -s "$secret" "$secret" --concurrency 1 2>&1 \
      | grep -oE 'run stop [0-9a-f-]{36}' | awk '{print $3}')
    printf '%s\t%s\t%s\n' "$model" "$ds" "$id" | tee -a runs.tsv
  done
done <<'EOF'
claude_code-v1.0.0 anthropic/claude-sonnet-5-5 ANTHROPIC_API_KEY
claude_code-v1.0.0 anthropic/claude-opus-5-5 ANTHROPIC_API_KEY
claude_code-v1.0.0 anthropic/claude-fable-5-2 ANTHROPIC_API_KEY
codex-v1.0.0 gpt-6-astra OPENAI_API_KEY
codex-v1.0.0 gpt-6.1-sol OPENAI_API_KEY
EOF
