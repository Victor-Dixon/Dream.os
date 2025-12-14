<!-- SSOT Domain: architecture -->
# Root Directory Cleanup Plan - Professional Organization
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-14  
**Status**: 🟡 In Progress

---

## Executive Summary

**Problem**: Root directory contains many loose files making repository look unprofessional.  
**Solution**: Move files to appropriate organized directories.

---

## Files to Move from Root

### Scripts → `scripts/` or `tools/`
- `agent1_response.py`
- `agent_devlog_watcher.py`
- `assignment_confirmation.py`
- `check_activation_messages.py`
- `check_queue_status.py`
- `check_recent_activations.py`
- `final_status_check.py`
- `find_agent8_message.py`
- `hard_onboard_agent4.py`
- `onboard_survey_agents.py`

### Analysis/Status JSON → `analysis/` or `docs/archive/root_cleanup_2025-12-14/analysis/`
- `coverage.json`
- `coverage_config_ssot.json`
- `dream_os_ci_diagnostic.json`
- `import_errors_report.json`
- `import_errors_report_updated.json`
- `import_errors_report_v2.json`
- `integration_issues_report.json`
- `project_analysis.json`
- `dashboard_metrics.json`
- `dependency_cache.json`

### Config/Status JSON → `config/` or `docs/archive/root_cleanup_2025-12-14/config/`
- `agent_mode_config.json`
- `chatgpt_project_context.json`
- `cursor_agent_coords.json`
- `deferred_push_queue.json`
- `github_sandbox_mode.json` (move to `src/` if used by code, else archive)
- `passdown.json`

### Temporary/Debug Files → `docs/archive/root_cleanup_2025-12-14/`
- `PYTEST_DEBUGGING_COMPLETE_SUMMARY.txt`
- `integration_issues_report.txt`
- `manager_files_list.txt`

---

## Files to Keep in Root (Standard Practice)

✅ **KEEP**:
- `README.md` - Standard project readme
- `CHANGELOG.md` - Standard changelog
- `STANDARDS.md` - Project standards
- `AGENTS.md` - Project documentation
- `package.json` / `package-lock.json` - Node.js standard
- `requirements.txt` / `requirements-dev.txt` - Python standard
- `pyproject.toml` - Python project config
- `.pre-commit-config-*.yaml` - Pre-commit configs
- `jest.config.js` - Jest config
- `importlinter.ini` - Import linter config
- `conftest.py` - Pytest config (standard location)
- `__init__.py` - If needed for root package
- `config.py` - If it's a root-level config (verify usage first)

---

## Action Plan

1. ✅ Create archive directories
2. ⏳ Move script files to `scripts/`
3. ⏳ Move analysis JSON files to `analysis/` or archive
4. ⏳ Move config JSON files to `config/` or archive
5. ⏳ Move temporary/debug files to archive
6. ⏳ Verify no broken imports
7. ⏳ Commit and push

---

**Status**: 🟡 Planning complete - Ready for execution  
**Agent**: Agent-2 (Architecture & Design Specialist)
