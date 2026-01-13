# Root Directory Organization Plan
**Created:** 2025-12-29  
**Coordinated by:** Agent-3 (Infrastructure) + Agent-6 (Documentation)  
**Status:** In Progress

## Executive Summary

Root directory audit identified 80+ files that need reorganization for professional structure. This plan outlines the categorization, target locations, and execution steps.

## Organizational Issues Identified

### 1. **Loose Documentation Files in Root** (32 files)
- Audit reports (WEBSITE_AUDIT_COMPREHENSIVE_*.md)
- Investigation reports (FREERIDEINVESTOR_500_ERROR_INVESTIGATION_*.md)
- Summary/status reports (MASTER_AGI_TASK_LOG_*.md, various *_SUMMARY.md)
- Task coordination documents (coordination_batches_*.md, ssot_coordination_report.md)

**Target:** Move to `docs/archive/audits/` or `docs/archive/reports/` (by date/type)

### 2. **Temporary Files in Root** (17 files)
- `temp_*.php`, `temp_*.css`, `temp_*.py`, `temp_*.txt`, `temp_*.md`
- Debug/test files (debug_log_*.txt, wp-config-*.php)

**Target:** Archive to `archive/temp/` or delete if obsolete

### 3. **Multiple Task Log Variants** (4 files)
- `MASTER_AGI_TASK_LOG_EVALUATION.md`
- `MASTER_AGI_TASK_LOG_IMPROVEMENTS.md`
- `MASTER_AGI_TASK_LOG_local.md`
- `MASTER_TASK_LOG_INVESTIGATION_REPORT.md`

**Target:** Review, merge if needed, archive historical versions to `docs/archive/task_logs/`

### 4. **Duplicate SSOT Files** (4 files)
- `ssot_batch_assignments.json`
- `ssot_batch_assignments_latest.json`
- `ssot_batch_assignments.md`
- `ssot_batch_assignments_latest.md`

**Target:** Keep latest version in `reports/ssot/`, archive old versions

### 5. **Configuration Files in Root** (Multiple)
- Multiple JSON configs (cursor_agent_coords.json, cursor_agent_coords.json.backup, CURSOR_MCP_CONFIG.json, etc.)
- Various config.py files

**Target:** Consolidate to `config/` directory (Agent-3 responsibility)

### 6. **Investigation/Debug Files** (6 files)
- `FREERIDEINVESTOR_500_ERROR_INVESTIGATION_*.md`
- `MASTER_TASK_LOG_INVESTIGATION_REPORT.md`
- Debug logs and test outputs

**Target:** Move to `docs/archive/investigations/` by date

## Proposed Directory Structure

```
agent_workspaces/
archive/
  audits/          # Historical audit reports (by year/month)
  investigations/  # Historical investigation reports
  reports/         # Historical summary reports
  temp/            # Archived temporary files
config/            # All configuration files
docs/
  archive/         # Current archive location (already exists)
  audits/          # Recent audits (move to archive after 90 days)
  reports/         # Recent reports (move to archive after 90 days)
reports/
  ssot/            # SSOT-related reports
  audits/          # Current audit reports
temp/              # Active temporary files (cleanup regularly)
```

## Execution Plan

### Phase 1: Documentation Organization (Agent-6)
1. ✅ Create organization plan document
2. Create archive directory structure
3. Move historical audit reports to `docs/archive/audits/`
4. Move investigation reports to `docs/archive/investigations/`
5. Consolidate SSOT batch files (keep latest, archive old)
6. Archive or delete temporary files

### Phase 2: Infrastructure Organization (Agent-3)
1. Audit root directory for technical files
2. Consolidate configuration files to `config/`
3. Move debug/test files to appropriate locations
4. Clean up duplicate or obsolete files
5. Update .gitignore if needed

### Phase 3: Validation
1. Verify all files have proper locations
2. Update any hardcoded paths in code
3. Update documentation references
4. Test that no functionality is broken

## File Mapping

### Audit Reports → `docs/archive/audits/2025/`
- `WEBSITE_AUDIT_COMPREHENSIVE_20251220_*.md`
- `WORDPRESS_BLOG_AUDIT_*.md`
- `COMPREHENSIVE_WEBSITE_AUDIT_20251222_*.md`
- `BROKEN_TOOLS_AUDIT_REPORT.md`

### Investigation Reports → `docs/archive/investigations/2025/`
- `FREERIDEINVESTOR_500_ERROR_INVESTIGATION_*.md`
- `MASTER_TASK_LOG_INVESTIGATION_REPORT.md`
- `DEBUG_MESSAGING_COMMAND.md`

### Task Log Variants → `docs/archive/task_logs/`
- `MASTER_AGI_TASK_LOG_EVALUATION.md`
- `MASTER_AGI_TASK_LOG_IMPROVEMENTS.md`
- `MASTER_AGI_TASK_LOG_local.md`
- Keep: `MASTER_TASK_LOG.md` (current active log)

### SSOT Files → `reports/ssot/`
- Archive old: `ssot_batch_assignments.json`, `ssot_batch_assignments.md`
- Keep latest: `ssot_batch_assignments_latest.*`

### Temporary Files → `archive/temp/` or delete
- All `temp_*.php`, `temp_*.css`, `temp_*.py`, `temp_*.txt`, `temp_*.md`
- Review and delete if obsolete, archive if potentially useful

### Configuration Files → `config/` (Agent-3)
- `cursor_agent_coords.json` → `config/cursor_agent_coords.json`
- `CURSOR_MCP_CONFIG.json` → `config/mcp_config.json`
- Review other config files for consolidation

## Execution Status

- [x] Phase 1.1: Organization plan created
- [x] Phase 1.2: Archive directories created
- [x] Phase 1.3: Historical files moved (9+ audit reports, 5+ investigation reports, 3 task log variants)
- [x] Phase 1.4: SSOT files consolidated (moved to reports/ssot/)
- [x] Phase 1.5: Temporary files archived/deleted (17 files moved to archive/temp/)
- [x] Phase 1.6: Documentation strategy refinements created (docs/ROOT_DIRECTORY_ORGANIZATION_REFINEMENTS.md)
- [x] Phase 2: Infrastructure organization (Agent-3) - **COMPLETE** (50+ files organized: JSONs→data/, Python scripts→scripts/, configs→config/)
- [x] Phase 3: Documentation organization (Agent-6) - **COMPLETE** (29 markdown files organized into docs/guides/, docs/standards/, docs/protocols/, docs/architecture/, 14+ historical reports archived)
- [x] Phase 3.1: README.md Project Structure updated with new organization
- [x] Phase 3.2: DOCUMENTATION_INDEX.md updated with new file locations
- [x] Phase 4: Final validation and testing (import paths, documentation links) - **COMPLETE** (Agent-3: Technical validation PASSED - file locations verified, no broken imports; Agent-6: Documentation validation PASSED - links validated and fixed)

## Notes

- Maintain backward compatibility: Check for hardcoded paths before moving files
- Preserve git history: Use `git mv` for tracked files
- Archive strategy: Move to archive after 90 days of inactivity
- Documentation: Update any references in README.md or other docs

---

**Last Updated:** 2025-12-29 19:40:00  
**Status:** ✅ PROJECT COMPLETE - All Phases Complete
**Result:** Root directory reduced from 149 loose files to 3 essential files (README.md, CHANGELOG.md, MASTER_TASK_LOG.md). All files organized into professional structure. Technical and documentation validation passed.

