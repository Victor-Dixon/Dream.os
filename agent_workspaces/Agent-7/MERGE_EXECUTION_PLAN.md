# Merge Execution Plan - Agent-7
**Date**: 2025-11-26  
**Status**: Ready for execution when API rate limit allows

---

## Execution Order

### Priority 1: Case Variations (3 repos)
1. focusforge → FocusForge (Repo #32 → #24)
2. tbowtactics → TBOWTactics (Repo #33 → #26)
3. superpowered_ttrpg → Superpowered-TTRPG (Repo #37 → #50)

### Priority 2: Consolidation Logs (5 repos)
4. my_personal_templates → my-resume (Repo #54 → #12) - ✅ DRY_RUN_SUCCESS (ready)
5. gpt_automation → selfevolving_ai (Repo #57 → #39) - ❌ FAILED (need re-merge)
6. intelligent-multi-agent → Agent_Cellphone (Repo #45 → #6) - ❌ FAILED (need re-merge)
7. my_resume → my-resume (Repo #53 → #12) - ❌ FAILED (need re-merge)
8. trade-analyzer → trading-leads-bot (Repo #4 → #17) - ❌ FAILED (need re-merge)

---

## Execution Command Template

```bash
python tools/repo_safe_merge.py <TARGET> <SOURCE> --execute
```

---

## Post-Merge Checklist (Per Repo)

1. **Check for venv files**: `python tools/detect_venv_files.py <repo_path>`
2. **Check for duplicates**: `python tools/duplication_analyzer.py --scan`
3. **Verify integration**: Ensure logic unified, not just files merged
4. **Test functionality**: Verify all features work
5. **Fix any issues**: Address venv files, duplicates, broken functionality
6. **Goal**: 0 issues like Agent-3

## Rate Limit Management

- Check rate limit before each merge: `gh api rate_limit`
- Wait for reset if rate limit exceeded
- Execute merges in batches to avoid rate limits
- Use dry runs first to verify readiness

