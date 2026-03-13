# Ownership Header Rollout Plan (4-Part Tiered Execution)

## Objective
Roll out standardized ownership headers to **all core source files** in controlled tiers so work can be handed off between Codex agents without overloading context, while enforcing:
- **SSOT discipline** (no duplicate ownership boundaries)
- **Python file LOC < 400** after edits
- exclusion of vendor/generated/build/lock artifacts

## Canonical Header Contract
Use this contract for major files (language-appropriate syntax):

- File
- Purpose
- Owns
- Does Not Own
- Inputs
- Outputs
- Dependencies
- Used By
- Status
- Last Updated
- Notes

Optional tags when useful:
- Domain
- Layer
- Risk
- Test

## Execution Rules (Apply in Every Tier)
1. **Do not touch** vendor/generated/build/lock files.
2. For **tiny utility files**, use a shortened 1–3 line variant.
3. Ensure each edited file remains or becomes **SSOT-aligned**:
   - explicit ownership boundary
   - no duplicate module scope claims
4. For Python files, run LOC checks and keep each edited file **< 400 lines**.
5. Keep header wording precise and short; avoid fluffy prose.
6. Preserve shebang and `from __future__` ordering requirements.

## Tier 1 — Core Runtime & Orchestration Foundations
**Goal:** Finish all high-impact runtime control surfaces first.

### Scope
- `src/core/orchestration/**`
- `src/core/base/**`
- `src/core/config/**`
- `src/core/session/**`
- `src/core/messaging*.py`
- `src/core/agent_*.py`
- `src/core/service_*.py`

### Deliverables
- Headers present in all core runtime/controller entry files.
- SSOT language aligned with orchestration ownership boundaries.

### Validation
- `python -m py_compile` on changed Python files
- `wc -l` on changed Python files (must be `< 400`)

---

## Tier 2 — Pipeline, Integration, and Infra Adapters
**Goal:** Cover integration-heavy modules where drift risk is high.

### Scope
- `src/core/gas_pipeline/**`
- `src/core/refactoring/**`
- `src/core/vector_strategic_oversight/**`
- `src/core/unified_*`
- `src/core/*integration*.py`
- `src/core/*pipeline*.py`

### Deliverables
- Header ownership boundaries differentiate orchestration vs adapter roles.
- Dependencies/Used By fields reference real upstream/downstream modules.

### Validation
- compile + LOC checks for all changed Python files
- quick import smoke check on key package roots

---

## Tier 3 — Domain Services and Adjacent Packages
**Goal:** Extend standard to non-core but project-owned domain modules.

### Scope
- `src/quantum/**`
- `src/operational_transformation/**`
- additional project Python modules at repo root used in runtime workflows

### Deliverables
- Domain/Layer tags added where useful (`trading`, `adapter`, `service`, etc.).
- Tiny utility modules receive shortened header variant.

### Validation
- compile + LOC checks for changed Python files
- module-level sanity execution where feasible

---

## Tier 4 — Non-Python Core Source + Completion Sweep
**Goal:** Standardize JS/TS/PHP and run final consistency pass.

### Scope
- project-owned JS/TS/PHP source modules under `sites/**/wp-content/plugins/**`
- other non-generated source files that participate in runtime behavior

### Deliverables
- JS/TS files use JSDoc-style ownership header.
- PHP files use block-comment equivalent.
- Final repository sweep for missing headers in in-scope core files.

### Validation
- lint/syntax checks per language when tooling exists
- final audit list of files still pending (if any)

---

## Handoff Contract for Next Codex Agent
For each tier:
1. Create a file list for that tier only.
2. Apply headers in small batches (10–30 files/commit).
3. Run compile/LOC checks immediately after each batch.
4. Commit with message: `Add ownership headers (tier X batch Y)`.
5. Update a progress tracker (below) before handoff.

## Progress Tracker (Update Per Batch)
- [ ] Tier 1 complete
- [ ] Tier 2 complete
- [ ] Tier 3 complete
- [ ] Tier 4 complete

### Batch Log Template
- Tier:
- Batch:
- Files touched:
- SSOT conflicts resolved:
- LOC exceptions found:
- Validation commands run:
- Commit SHA:

## Recommended Command Snippets
```bash
# list candidate source files (exclude obvious generated/vendor/build dirs)
rg --files src sites \
  -g '!**/node_modules/**' \
  -g '!**/vendor/**' \
  -g '!**/dist/**' \
  -g '!**/build/**' \
  -g '!**/*.min.js' \
  -g '!**/*lock*'

# python line count enforcement for changed files
wc -l <python-files>

# python syntax validation for changed files
python -m py_compile <python-files>
```
