# Header & Batch Validation Report (2026-03-15)

## SSOT
- Source batch manifests: `batches/batch_001.json` through `batches/batch_013.json`
- Source validation workflow: `scripts/validate_batch.sh`
- Source header protocol: `config/file_header_protocol_v1.3.0.yaml`

## Commands executed
1. Enumerated all batch manifests and verified 13 total batches.
2. Ran full validation loop across all batches using `scripts/validate_batch.sh`.
3. Ran direct header-validation summary script to compute violation counts per batch.

## Validation outcome

### Batch completion check
- Total batches discovered: **13**
- Batches with zero header violations: **11** (`001, 002, 003, 004, 007, 008, 009, 010, 011, 012, 013`)
- Batches with header violations remaining: **2** (`005, 006`)

### Header violation status
- Batch `004`: **0** violations across **0** files (resolved).
- Batch `005`: **100** violations across **50** files.
- Batch `006`: **97** violations across **50** files.

### Violation classes observed
- `HDR001`: missing header block
- `HDR004`: header does not follow parser order

## Conclusion
Header violations are **not fully solved** yet, and **not all batches are complete** under batch validation criteria. Batch `004` is now complete; remaining work is concentrated in batches `005` and `006`.
