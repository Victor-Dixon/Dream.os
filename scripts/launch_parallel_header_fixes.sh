#!/bin/bash
set -euo pipefail
BATCHES=(001 002 003 004 005 006 007 008 009 010 011 012 013)
MAX_PARALLEL=${MAX_PARALLEL:-4}
echo "🚀 Launching ${#BATCHES[@]} batches (${MAX_PARALLEL} at a time)"
for BATCH in "${BATCHES[@]}"; do
  while [ "$(jobs -r | wc -l)" -ge "$MAX_PARALLEL" ]; do sleep 2; done
  echo "▶️  Starting batch $BATCH"
  if [ -f tools/codex_batch_processor.py ]; then
    python tools/codex_batch_processor.py --batch "batches/batch_${BATCH}.json" --branch "codex/fix-headers-batch-${BATCH}" --pr-template "templates/pr_batch_${BATCH}.md" &
  else
    echo "⚠️ tools/codex_batch_processor.py not found; placeholder launch for batch $BATCH" &
  fi
done
wait
echo "✅ All batches launched"
