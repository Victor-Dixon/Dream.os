# Toolbelt Health Check - Generated Tasks

**Date:** 2025-12-18  
**Source:** `tools/check_toolbelt_health.py` + `tools/populate_tasks_from_health_check.py`  
**Status:** 41 broken tools identified, tasks generated

## Summary

- **Total tools checked**: 87
- **Healthy tools**: 46 (52.9%)
- **Broken tools**: 41 (47.1%)
- **HIGH priority fixes**: 35
- **MEDIUM priority fixes**: 6

## HIGH PRIORITY TASKS (35)

### Missing Modules (30 tools)
- [ ] Fix 'Project Scanner' (scan) - Module: `tools.run_project_scan`
- [ ] Fix 'V2 Compliance Checker' (v2-check) - Module: `tools.v2_checker_cli`
- [ ] Fix 'Compliance Dashboard' (dashboard) - Module: `tools.dashboard_html_generator`
- [ ] Fix 'Complexity Analyzer' (complexity) - Module: `tools.complexity_analyzer`
- [ ] Fix 'Refactoring Suggestions' (refactor) - Module: `tools.refactoring_suggestions`
- [ ] Fix 'Functionality Verification' (functionality) - Module: `tools.functionality_verification` (missing dependency: `functionality_comparison`)
- [ ] Fix 'Compliance History' (history) - Module: `tools.compliance_history_tracker` (missing dependency: `compliance_history_database`)
- [ ] Fix 'Test Usage Analyzer' (test-usage-analyzer) - Module: `tools.test_usage_analyzer`
- [ ] Fix 'Architecture Pattern Validator' (pattern-validator) - Module: `tools.arch_pattern_validator`
- [ ] Fix 'Import Validator' (validate-imports) - Module: `tools.validate_imports`
- [ ] Fix 'Task CLI' (task) - Module: `tools.task_cli`
- [ ] Fix 'Refactor Analyzer' (refactor-analyze) - Module: `tools.refactor_analyzer`
- [ ] Fix 'Devlog Auto-Poster' (devlog-post) - Module: `tools.devlog_auto_poster`
- [ ] Fix 'Pattern Extractor' (pattern-extract) - Module: `tools.pattern_extractor`
- [ ] Fix 'V2 Batch Checker' (v2-batch) - Module: `tools.v2_checker_cli`
- [ ] Fix 'Coverage Validator' (coverage-check) - Module: `tools.coverage_validator`
- [ ] Fix 'Unified Agent Status Monitor' (agent-status) - Module: `tools.unified_agent_status_monitor`
- [ ] Fix 'Analyze Repository Duplicates' (analyze-duplicates) - Module: `tools.analyze_repo_duplicates`
- [ ] Fix 'Analyze DreamVault Duplicates' (analyze-dreamvault) - Module: `tools.analyze_dreamvault_duplicates`
- [ ] Fix 'Verify Merged Repo CI/CD' (verify-cicd) - Module: `tools.verify_merged_repo_cicd_enhanced`
- [ ] Fix 'Pattern Suggester' (pattern-suggest) - Module: `tools.pattern_suggester`
- [ ] Fix 'Integration Validator' (integration-validate) - Module: `tests.integration.system_integration_validator`
- [ ] Fix 'Swarm Autonomous Orchestrator' (orchestrate) - Module: `tools.swarm_orchestrator` (missing dependency: `tools.gas_messaging`)
- [ ] Fix 'Repo Overlap Analyzer' (repo-overlap) - Module: `tools.repo_overlap_analyzer`
- [ ] Fix 'Consolidation Status Tracker' (consolidation-status) - Module: `tools.consolidation_status_tracker`
- [ ] Fix 'Verify Discord Running' (discord-verify) - Module: `tools.verify_discord_running`
- [ ] Fix 'Diagnose Queue' (queue-diagnose) - Module: `tools.diagnose_queue`
- [ ] Fix 'Fix Stuck Message' (fix-stuck) - Module: `tools.fix_stuck_message`
- [ ] Fix 'Test Health Monitor' (test-health) - Module: `tools.test_health_monitor`
- [ ] Fix 'Infrastructure Health Monitor' (infra-health) - Module: `tools.infrastructure_health_monitor`

### Syntax Errors (4 tools)
- [ ] Fix 'Resolve DreamVault Duplicates' (resolve-duplicates) - Syntax error at line 273
- [ ] Fix 'Execute DreamVault Cleanup' (execute-cleanup) - Syntax error at line 343
- [ ] Fix 'Mission Control' (mission-control) - Syntax error at line 346
- [ ] Fix 'Markov Task Optimizer' (markov-optimize) - Syntax error at line 677

### Import Errors (1 tool)
- [ ] Fix 'Workspace Auto-Cleaner' (workspace-clean) - Import error: `name 'Dict' is not defined`

## MEDIUM PRIORITY TASKS (6)

### Missing main() Functions
- [ ] Fix 'Memory Leak Scanner' (memory-scan) - Add main() function
- [ ] Fix 'Git Commit Verifier' (git-verify) - Add main() function
- [ ] Fix 'Test Pyramid Analyzer' (test-pyramid) - Add main() function
- [ ] Fix 'QA Validation Checklist' (qa-checklist) - Add main() function
- [ ] Fix 'Find Idle Agents' (captain-find-idle) - Add main() function
- [ ] Fix 'Captain Next Task Picker' (captain-next-task) - Add main() function

## Task Generation System

**Tools Created**:
1. `tools/check_toolbelt_health.py` - Checks all tools in registry
2. `tools/populate_tasks_from_health_check.py` - Generates task entries from broken tools

**Usage**:
```bash
# Run health check
python tools/check_toolbelt_health.py

# Generate task entries
python tools/populate_tasks_from_health_check.py
```

**Integration**:
- Tasks can be automatically added to MASTER_TASK_LOG.md
- System categorizes issues by priority (HIGH/MEDIUM)
- Provides actionable task descriptions with module paths and error details

## Next Steps

1. **Review generated tasks** - Determine which tools should be fixed vs deprecated
2. **Prioritize fixes** - Start with syntax errors (easiest), then missing main() functions, then missing modules
3. **Registry cleanup** - Remove deprecated tools from registry if not fixable
4. **Automate task generation** - Integrate into regular health check workflow


