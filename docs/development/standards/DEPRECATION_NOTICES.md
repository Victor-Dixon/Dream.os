# Deprecation Notices

**Date**: 2025-12-21 02:34:20
**Phase**: -1 (Signal vs Noise Classification)

## Overview

This document records deprecated tools and directories removed during Phase -1 cleanup.

## Deprecated NOISE Tools

**Status**: All 26 NOISE tools were already removed (not found during cleanup execution)

The following **26 tools** were identified as NOISE (thin wrappers) in Phase -1 classification but were already deleted from the repository:

### Removal Rationale

NOISE tools are thin wrappers that:
- Have no real business logic
- Just call other tools/functions
- Can be replaced by direct usage of underlying tools
- Many had syntax errors (broken/unmaintained)

### NOISE Tools (Already Removed)

The following tools were classified as NOISE but were already deleted:
- `tools/activate_hsq_theme_css.py`
- `tools/agent_fuel_monitor.py`
- `tools/archive_source_repos.py`
- `tools/check_all_repos_needing_archive.py`
- `tools/check_dadudekc_menu_structure.py`
- `tools/check_theme_syntax.py`
- `tools/cleanup_superpowered_venv.py`
- `tools/cli/test_dispatcher.py`
- `tools/coordination/discord_web_test_automation.py`
- `tools/create_ariajet_game_posts.py`
- `tools/create_case_variation_prs.py`
- `tools/create_merge1_pr.py`
- `tools/create_work_session.py`
- `tools/deploy_via_wordpress_admin.py`
- `tools/fix_dadudekc_theme_syntax_error.py`
- `tools/post_4agent_mode_blog.py`
- `tools/post_swarm_introduction.py`
- `tools/post_swarm_philosophy_blog.py`
- `tools/post_swarm_site_health_breakthrough.py`
- `tools/run_test_suite_validation.py`
- `tools/test_discord_commands.py`
- `tools/test_ssot_preservation.py`
- `tools/tmp_cleanup_nav.py`
- `tools/tmp_menu_fix.py`
- `tools/upload_fixed_dadudekc_functions.py`
- `tools/verify_dadudekc_fix_deployment.py`

**Note**: These tools were classified as NOISE but were already removed from the repository in a previous cleanup. Classification documentation is preserved in `docs/toolbelt/TOOL_CLASSIFICATION.md` for reference.

## Removed Archive Directories

The following **6 archive/backup directories** were removed:

### Removal Rationale

Archive directories are historical snapshots that:
- Take up disk space
- Are no longer needed for active development
- Can be recovered from git history if needed

### Removed Directories

| Directory | Details |
|-----------|---------|
| `D:\Agent_Cellphone_V2_Repository\archive` | 131 files, 1.01 MB |
| `D:\Agent_Cellphone_V2_Repository\backups` | 1700 files, 9.60 MB |
| `D:\Agent_Cellphone_V2_Repository\consolidation_backups` | 259 files, 0.06 MB |
| `D:\Agent_Cellphone_V2_Repository\consolidation_logs` | 294 files, 0.13 MB |
| `D:\Agent_Cellphone_V2_Repository\docs\archive` | 14 files, 0.72 MB |
| `D:\Agent_Cellphone_V2_Repository\tools\consolidation_logs` | 1 files, 0.00 MB |

## Recovery

If any deprecated tools or archives are needed:
- Check git history: `git log --all --full-history -- <path>`
- Check git tags for historical snapshots
- Review deprecation date in this document

## Reference

- Classification: `docs/toolbelt/TOOL_CLASSIFICATION.md`
- Migration Plan: `docs/toolbelt/NOISE_TOOLS_MIGRATION_PLAN.md`
- Phase -1 Summary: `docs/toolbelt/PHASE_MINUS1_EXECUTION_SUMMARY.md`

---

🐝 **WE. ARE. SWARM. ⚡🔥**