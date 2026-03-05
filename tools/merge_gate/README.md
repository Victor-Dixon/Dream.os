# Merge Gate v1 (patch-only)

Merge Gate v1 is a standalone guardrail for patch workflows.

It is intentionally isolated from core Dream.OS internals so validation can be
added without rewriting architecture.

## What it enforces

- touched files must be inside allowlist globs
- diff size must be within file/line caps
- test command must pass
- optional lint/formatter commands must pass
- required contract output files must exist (and optionally be non-empty)

## Folder layout

```text
tools/merge_gate/
├── gate.py
├── contracts/
│   └── default_contract.yaml
├── tasks/
│   └── day1_patch_gate.yaml
├── runs/
│   └── .gitkeep
└── scripts/
    ├── run_tests.sh
    ├── run_lint.sh
    └── run_formatter.sh
```

## Usage

```bash
python3 tools/merge_gate/gate.py --task tools/merge_gate/tasks/day1_patch_gate.yaml
```

Or via Make:

```bash
make gate
```

Optional:

```bash
python3 tools/merge_gate/gate.py \
  --task tools/merge_gate/tasks/day1_patch_gate.yaml \
  --contract tools/merge_gate/contracts/default_contract.yaml \
  --repo-root /workspace
```

## Result contract

Each run writes artifacts to:

```text
tools/merge_gate/runs/<timestamp>_<task-id>/
```

With:
- `report.json`
- `report.md`
- `task_resolved.yaml`
- `artifacts/*.log`

CLI exits:
- `0` on PASS
- `1` on FAIL
- `2` on config/usage error

## Workflow posture

- manual merge remains in control
- gate produces deterministic PASS/FAIL reasons
- auto-merge should only be considered after stable clean-pass history

## CI enforcement

PR enforcement workflow:

- `.github/workflows/merge-gate.yml`

It runs:

```bash
python3 tools/merge_gate/gate.py --task tools/merge_gate/tasks/day1_patch_gate.yaml
```

To hard-block merges, mark `merge-gate-v1` as a required status check in branch protection.
