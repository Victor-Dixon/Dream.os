# NOISE Tools Migration Plan

**Date**: 2025-12-21 02:24:12
**Phase**: -1 (Signal vs Noise Classification)
**Status**: 📋 READY FOR EXECUTION

## Summary

- **NOISE Tools to Migrate**: 26
- **Target Directory**: `scripts/`
- **Action**: Move or deprecate NOISE tools

## Migration Strategy

1. **Create `scripts/` directory structure**
   - Organize by category (analysis, bi, compliance, testing, etc.)
   - Maintain tool organization for easier discovery

2. **Move NOISE Tools**
   - Move files from `tools/` to appropriate `scripts/` subdirectory
   - Update any import references
   - Create compatibility wrappers if needed (temporary)

3. **Update Toolbelt Registry**
   - Remove NOISE tools from toolbelt registry
   - Update documentation

4. **Update Documentation**
   - Document migration in DEPRECATION_NOTICES.md
   - Update tool usage guides

## NOISE Tools by Category

### cli/ (1 tools)

| File | Lines | Reason |
|------|-------|--------|
| `tools/cli\test_dispatcher.py` | 71 | Small file that just imports and calls other tools; Contains complex control flow structures... |

### coordination/ (1 tools)

| File | Lines | Reason |
|------|-------|--------|
| `tools/coordination\discord_web_test_automation.py` | 366 | Syntax error indicates broken/unmaintained code... |

### root/ (24 tools)

| File | Lines | Reason |
|------|-------|--------|
| `tools/upload_fixed_dadudekc_functions.py` | 12 | Small file that just imports and calls other tools... |
| `tools/check_dadudekc_menu_structure.py` | 38 | Small file that just imports and calls other tools... |
| `tools/test_ssot_preservation.py` | 61 | Small file that just imports and calls other tools... |
| `tools/tmp_menu_fix.py` | 62 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/tmp_cleanup_nav.py` | 68 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/verify_dadudekc_fix_deployment.py` | 69 | Small file that just imports and calls other tools... |
| `tools/activate_hsq_theme_css.py` | 77 | Small file that just imports and calls other tools... |
| `tools/fix_dadudekc_theme_syntax_error.py` | 85 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/post_swarm_site_health_breakthrough.py` | 90 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/post_swarm_introduction.py` | 92 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/post_4agent_mode_blog.py` | 94 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/post_swarm_philosophy_blog.py` | 95 | Small file that just imports and calls other tools; Contains complex control flow structures... |
| `tools/check_all_repos_needing_archive.py` | 113 | Syntax error indicates broken/unmaintained code... |
| `tools/create_merge1_pr.py` | 117 | Syntax error indicates broken/unmaintained code... |
| `tools/create_ariajet_game_posts.py` | 153 | Syntax error indicates broken/unmaintained code... |
| `tools/create_case_variation_prs.py` | 163 | Syntax error indicates broken/unmaintained code... |
| `tools/run_test_suite_validation.py` | 180 | Syntax error indicates broken/unmaintained code... |
| `tools/archive_source_repos.py` | 203 | Syntax error indicates broken/unmaintained code... |
| `tools/check_theme_syntax.py` | 239 | Syntax error indicates broken/unmaintained code... |
| `tools/create_work_session.py` | 289 | Syntax error indicates broken/unmaintained code... |
| `tools/cleanup_superpowered_venv.py` | 317 | Syntax error indicates broken/unmaintained code... |
| `tools/deploy_via_wordpress_admin.py` | 331 | Syntax error indicates broken/unmaintained code... |
| `tools/agent_fuel_monitor.py` | 360 | Syntax error indicates broken/unmaintained code... |
| `tools/test_discord_commands.py` | 364 | Syntax error indicates broken/unmaintained code... |

## Execution Checklist

- [ ] Create `scripts/` directory structure
- [ ] Move NOISE tools to appropriate `scripts/` subdirectories
- [ ] Update toolbelt registry (remove NOISE tools)
- [ ] Update documentation references
- [ ] Test that moved tools still work (if needed)
- [ ] Commit migration

---

🐝 **WE. ARE. SWARM. ⚡🔥**