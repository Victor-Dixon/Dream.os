# PR #70 Slop-Hunter Audit + Master Integration Prompt

## Purpose
This audit is designed for rapid-fire deployments where multiple PRs land back-to-back (e.g., #68, #69, #70). It protects the project SSOT and prevents duplicate drift from parallel agents.

---

## 1) Collision Check (Duplicate File Slop)

### Audit question
Does PR #70 introduce any new `.py` or `.txt` files not explicitly listed in the batch manifests?

### Why this matters
Unplanned helper files (e.g., `utils_v2.py`, `header_helper.py`) create maintenance drag and token waste.

### Command sequence
```bash
git fetch origin

git diff --name-status origin/main...HEAD \
  | awk '$1=="A" {print $2}' \
  | rg '\\.(py|txt)$' || true
```

### Decision rule
- **PASS**: Every new `.py`/`.txt` file is listed in its batch manifest.
- **FAIL**: Any unplanned file appears. Remove it or explicitly justify and register it.

---

## 2) Lock-In Proof (No Trust Me Merges)

### Audit question
Does PR #70 include successful batch validation for every covered batch?

### Required evidence format
For each covered batch (example: `010`, `011`), show:

```bash
./scripts/validate_batch.sh 010  # exit code 0
./scripts/validate_batch.sh 011  # exit code 0
```

### Decision rule
- **PASS**: Exit code `0` for all covered batches is shown in PR evidence.
- **FAIL**: Missing validation evidence or non-zero exit code.

---

## 3) Registry SSOT Alignment

### Audit question
If headers or recovery-linked files changed, does `docs/recovery/recovery_registry.yaml` stay aligned?

### Command sequence
```bash
git diff --name-only origin/main...HEAD

git diff --name-only origin/main...HEAD \
  | rg '^docs/recovery/recovery_registry\.yaml$' || true
```

### Decision rule
- **PASS**: Registry reflects any introduced/updated IDs referenced by changed files.
- **FAIL**: IDs in headers/docs are missing or mismatched in the registry.

---

## 4) Self-Describing Header Test (AGI Structure Standard)

### Audit question
Can a different agent understand a file's interface from `@summary` + header in 5 seconds?

### 5-second rubric
- What the file does.
- Inputs/outputs.
- Constraints or side effects.
- Where it belongs in the architecture.

### Decision rule
- **PASS**: Header communicates interface and intent immediately.
- **FAIL**: Header is generic, vague, or detached from actual behavior.

---

## Minimal PR #70 Reviewer Comment Template

```md
## PR #70 Slop-Hunter Audit

- Collision Check: PASS/FAIL
- Lock-In Proof: PASS/FAIL
- Registry SSOT Alignment: PASS/FAIL
- Self-Describing Header Test: PASS/FAIL

### Notes
- [ ] Unplanned files removed or justified.
- [ ] Batch validations attached with exit code 0.
- [ ] `docs/recovery/recovery_registry.yaml` alignment verified.
- [ ] Headers are self-describing for handoff.
```

---

## Master Integration Prompt (for final integration agent)

Use this prompt when #68, #69, #70 are all ready and you want one integration-stable branch.

```md
You are the integration agent for Rapid-Fire Deployment.

Goal:
Merge PR branches #68, #69, and #70 into one integration-stable branch with no slop, no SSOT drift, and validated batch lock-in.

Workflow:
1) Checkout integration branch from latest `origin/main`.
2) Merge PR branches in order: #68 -> #69 -> #70.
3) Resolve conflicts by preserving SSOT and removing duplicate helper artifacts.
4) Run Slop-Hunter checks:
   - New `.py`/`.txt` files must be manifest-listed.
   - No duplicate utility scripts with overlapping function.
5) Run per-batch lock-in validations for every batch touched by the merged set:
   - `./scripts/validate_batch.sh <batch_id>` must exit 0 for each.
6) Verify Registry SSOT:
   - `docs/recovery/recovery_registry.yaml` must match any added/edited IDs.
7) Run project-level sanity checks (lint/tests used by this repo).
8) Produce an integration report:
   - merged branch SHA
   - conflict summary
   - duplicate-file removals
   - batch validation results (command + exit code)
   - registry alignment confirmation

Hard gates (must pass):
- No unregistered `.py`/`.txt` additions.
- All touched batches validated with exit code 0.
- Registry alignment confirmed.
- No unresolved merge markers.

If any gate fails, stop and report exact remediation steps; do not declare integration complete.
```

---

## Quick Operator Reminder
Do not merge #68/#69/#70 independently if global behavior can conflict. Merge only after integration branch passes all hard gates above.
