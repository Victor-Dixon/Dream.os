# A++ Session Closure Standard

## Quick Reference

All session closures must follow the A++ format. See:
- **Full Standard:** `.cursor/rules/session-closure.mdc`
- **Template:** `templates/session-closure-template.md`
- **Validation:** `python tools/validate_closure_format.py <file.md>`

## Required Format

```markdown
- **Task:** [Brief description]
- **Project:** [Project name]

- **Actions Taken:**
  - [Factual action 1]
  - [Factual action 2]

- **Artifacts Created / Updated:**
  - [Exact file path 1]
  - [Exact file path 2]

- **Verification:**
  - [Proof/evidence 1]
  - [Proof/evidence 2]

- **Public Build Signal:**
  [One sentence describing what changed]

- **Status:**
  ✅ Ready
```

## Forbidden Elements

- ❌ "Next steps" or future-facing language
- ❌ Narration or summaries
- ❌ Speculation ("should work", "may need")
- ❌ Progress reports ("made progress")

## Why This Matters

- **Zero context loss** between sessions
- **Build-in-public readiness** for Discord/changelogs
- **Queryable truth** in Swarm Brain
- **No work leakage** across sessions

## Validation

Before submitting a closure, validate it:

```bash
python tools/validate_closure_format.py agent_workspaces/Agent-X/session_closures/closure.md
```

## Examples

See: `agent_workspaces/Agent-4/session_closures/2025-12-26_trading_dashboard_closure.md`


