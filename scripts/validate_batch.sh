#!/bin/bash
set -euo pipefail

BATCH_ID=${1:-}
if [ -z "$BATCH_ID" ]; then
  echo "Usage: $0 <batch_id>"
  exit 1
fi

BATCH_FILE="batches/batch_${BATCH_ID}.json"
if [ ! -f "$BATCH_FILE" ]; then
  echo "Missing $BATCH_FILE"
  exit 1
fi

echo "🔍 Validating batch $BATCH_ID"
python - "$BATCH_ID" <<'PYCODE'
import json
import sys
from pathlib import Path
from tools.file_header_validator import HeaderValidator

batch_id = sys.argv[1]
root = Path.cwd()
protocol = root / 'config/file_header_protocol_v1.3.0.yaml'
batch = json.loads((root / f'batches/batch_{batch_id}.json').read_text(encoding='utf-8'))
validator = HeaderValidator(root, protocol, 'audit_only', False)
exceptions = validator.load_exceptions()

paths = {entry['path'] for entry in batch['files']}
for entry in batch['files']:
    validator.validate_file(root / entry['path'], exceptions)

violations = [v for v in validator.violations if v.path in paths]
if violations:
    for violation in violations:
        print(f"{violation.path}: {violation.rule_id} {violation.message}")
    raise SystemExit(1)

print('batch header checks passed')
PYCODE

python tools/validation/check_recovery_registry.py
pytest --collect-only -q || true

echo "✅ Batch $BATCH_ID validation complete"
