#!/bin/bash
# Launch hard datasets for the given agent/model/secret lines (stdin); IDs append to runs.tsv.
set -euo pipefail
export VALKYRIE_URL=http://127.0.0.1:8000
cd "$(dirname "$0")"
while read -r agent model secret; do
  for ds in hard-noprobe hard-probe10; do
    id=$(valkyrie run start --agent "$agent" --benchmark behavior-probe --dataset "$ds" \
      --model "$model" --provider docker -s "$secret" "$secret" --concurrency "${CONC:-2}" 2>&1 \
      | grep -oE 'run stop [0-9a-f-]{36}' | awk '{print $3}')
    printf '%s\t%s\t%s\n' "$model" "$ds" "$id" | tee -a runs.tsv
  done
done
