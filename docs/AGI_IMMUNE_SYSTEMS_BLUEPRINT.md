<!-- SSOT Domain: architecture -->
# Dream.os AGI Immune Systems Blueprint

## Purpose
Translate the identified failure modes (AI slop, drift, break-fix regressions) into structural controls that enforce SSOT-first behavior.

## 1) Entropic Lockdown (Prevent Slop)

### Design
- Introduce a **Shadow Filesystem (VFS)** for agent write actions.
- Route every create/rename/delete request through a **Janitor Gate**.
- Janitor checks against SSOT registries before allowing materialization to disk.

### Core checks
1. **Duplication check**: semantic similarity against existing modules.
2. **Registry binding**: file must map to a valid SSOT domain entry.
3. **Complexity budget check**: added files/LOC require an explicit entropy justification.

### Enforcement outcome
- `ALLOW`: writes to real filesystem.
- `QUARANTINE`: stores patch in review queue.
- `DENY`: blocked with remediation guidance.

## 2) Genetic Drift Monitor (Prevent Logic Mutation)

### Design
- Stamp each governed file with:
  - protocol version (`protocol_vX.Y.Z`)
  - rule hash (derived from active governance spec)
  - domain ID from SSOT registry
- Add a scheduled **Alignment Auditor** job that compares implementation intent to SSOT contract.

### Drift signals
- Header hash mismatch.
- File behavior deviates from declared domain capability.
- New logic path introduced without corresponding registry update.

### Enforcement outcome
- `PASS`: no action.
- `MUTATED`: open rollback candidate + create repair task.
- `CRITICAL_MUTATION`: auto-revert on protected branches.

## 3) Proof-Based Whack-a-Mole Defense (Prevent Empty Changes)

### Design
For every meaningful code change, require proof artifacts:
1. **Positive proof**: changed behavior works.
2. **Negative proof**: behavior fails without the patch.
3. **Non-overlap proof**: no duplicate logic introduced.

### CI policy
- Reject PRs that modify production code without updated proof tests.
- Reject PRs where negative test does not fail on pre-change baseline.
- Flag suspiciously low assertion delta for high-LOC changes.

## Priority Recommendation (Current Bottleneck)
Start with **Entropic Lockdown** first.

Reason:
- Physical clutter compounds every downstream problem.
- Drift detection quality collapses when duplicate files/functions exist.
- Debugging cost rises superlinearly when multiple near-identical paths compete.

Second, add **Genetic Drift Monitor** for continuous alignment.
Third, enforce **Proof-Based Testing** to stabilize release quality over time.

## Minimal Rollout Plan
1. Week 1: Janitor Gate in advisory mode (log-only).
2. Week 2: Turn on deny/quarantine for unbound file creations.
3. Week 3: Introduce protocol hash headers on high-risk domains.
4. Week 4: Add negative-test CI requirement on protected branches.

## SSOT Enforcement Rules
- No new file can be merged without domain mapping.
- No protocol change can be merged without hash/version update.
- No behavior change can be merged without positive + negative proof.
