<!-- SSOT Domain: documentation -->

# Autonomous Header Remediation SSOT (Local + Cloud Agents)

## Purpose
This document is the shared coordination SSOT for **all agents** (local and cloud) working header remediation.

If an agent joins mid-cycle, this file is the first stop for current status, validation commands, and next executable steps.

## Authoritative Inputs (SSOT)
- Header protocol: `config/file_header_protocol_v1.3.0.yaml`
- Batch manifests: `batches/batch_001.json` .. `batches/batch_013.json`
- Batch validator: `scripts/validate_batch.sh`
- Status report: `docs/recovery/header_batch_validation_2026-03-15.md`
- Recovery registry: `docs/recovery/recovery_registry.yaml`

## Current State
- Total batches: **13**
- Completed (zero header violations): `001, 002, 003, 004, 007, 008, 009, 010, 011, 012, 013`
- Remaining: `005, 006`
- Remaining violation classes: `HDR001`, `HDR004`

## Standard Agent Workflow (Autonomous)
1. Pick one remaining batch (`005` or `006`) and claim it in your working log.
2. Add required header fields per protocol to every file in the batch:
   - `Header-Variant`
   - `Owner`
   - `Purpose`
   - `SSOT`
3. Validate the batch:
   - `./scripts/validate_batch.sh <batch_id>`
4. Recompute per-batch violation counts to confirm net progress.
5. Update both:
   - `docs/recovery/header_batch_validation_2026-03-15.md`
   - `MASTER_TASK_LOG.md`
6. Commit and publish PR evidence with exact commands + outcomes.

## Non-Negotiable Guardrails
- Do not introduce placeholder metadata values (`TODO`, `TBD`, `FIXME`, `???`).
- Keep Python files below 400 LOC for new files/splits; if a file approaches limit during edits, split deliberately.
- Preserve shebang and encoding lines ahead of header block when present.
- SSOT must be explicit in touched docs and headers so both local/cloud agents can resolve source authority quickly.

## Validation Commands
### Batch-level validation
```bash
./scripts/validate_batch.sh 005
./scripts/validate_batch.sh 006
```

### Direct per-batch header count verification
```bash
python - <<'PY'
import json
from pathlib import Path
from tools.file_header_validator import HeaderValidator
root = Path.cwd()
protocol = root / 'config/file_header_protocol_v1.3.0.yaml'
for bid in ['001','002','003','004','005','006','007','008','009','010','011','012','013']:
    batch = json.loads((root / f'batches/batch_{bid}.json').read_text())
    validator = HeaderValidator(root, protocol, 'audit_only', False)
    exceptions = validator.load_exceptions()
    paths = {entry['path'] for entry in batch['files']}
    for entry in batch['files']:
        validator.validate_file(root / entry['path'], exceptions)
    violations = [v for v in validator.violations if v.path in paths]
    print(bid, len(violations), len({v.path for v in violations}))
PY
```

## Expected End State
- Batches `005` and `006` reach `0` violations.
- Validation report reflects `13/13` complete.
- Master task log shows header-remediation epic fully closed with artifact links.
