# Root Directory Organization Plan

**Date**: 2025-11-22  
**Status**: IN PROGRESS  
**Goal**: Move 150+ files from root to proper locations

---

## 📋 File Categories & Destinations

### **1. Emergency/Restoration Docs** → `docs/emergency/`
- `FINAL_PUSH_INSTRUCTIONS.md`
- `FINAL_PUSH_SECRET_REMOVAL.ps1`
- `FINAL_STATUS_README.md`
- `PROJECT_RESTORATION_COMPLETE.md`
- `PUSH_SUCCESS.md`

### **2. DUP-* Reports** → `docs/consolidation/`
- `DUP-001_ANALYSIS.md`
- `DUP-001_COMPLETION_REPORT.md`
- `DUP-001_CONFIGMANAGER_FIX_PROGRESS.md`
- `DUP-004_COMPLETION_REPORT.md`
- `DUP-004_MANAGER_HIERARCHY_DESIGN.md`
- `DUP-004_SSOT_VALIDATION_REPORT.md`
- `DUP-006_COMPLETION_REPORT.md`
- `DUP-006_ERROR_HANDLING_ANALYSIS.md`
- `DUP-007_COMPLETION_REPORT.md`
- `DUP-007_LOGGING_MIGRATION_GUIDE.md`

### **3. DISCORD_* Files** → `docs/discord/` or `archive/discord/`
- `DISCORD_AGENT7_RANK1_RECLAIMED.md`
- `DISCORD_AGENT8_PHASES_12_EXECUTING.md`
- `DISCORD_AUTONOMOUS_SESSION_COMPLETE_ALL_TODOS.md`
- `DISCORD_AUTONOMOUS_SESSION_FINAL_COMPLETE.md`
- `DISCORD_COMMANDER_RETURN_STATUS.md`
- `DISCORD_DUAL_PHASE_COMPLETION.md`
- `DISCORD_GAS_PIPELINE_PERFECTION.md`
- `DISCORD_LEGACY_MASTER_ROADMAP_COMPLETE.md`
- `DISCORD_SESSION_COMPLETE_FINAL.md`
- `DISCORD_TODOS_COMPLETED_STRATEGIC_DOCS.md`
- `DISCORD_TRANSFORMATION_ROADMAP_FINAL.md`

### **4. QUARANTINE_* Files** → `quarantine/` or `docs/quarantine/`
- `BROKEN_COMPONENTS_QUARANTINE_LIST.md`
- `BROKEN_TOOLS_MANIFEST.json`
- `BROKEN_TOOLS_QUICK_AUDIT.txt`
- `QUARANTINE_BROKEN_COMPONENTS.md`
- `QUARANTINE_FIX_EXECUTION_ORDERS.md`
- `QUARANTINE_MASTER_TRACKER.md`
- `DUPLICATE_LOGIC_AUDIT_QUARANTINE.md`
- `DUPLICATE_QUARANTINE_SWARM_FIXES.md`
- `TOOL_RUNTIME_AUDIT_REPORT.md`
- `TOOLBELT_QUARANTINE_README.md`
- `TOOLS_QUARANTINE_STRATEGY.md`

### **5. Analysis Scripts** → `tools/analysis/`
- `analyze_messaging_files.py`
- `analyze_src_directories.py`
- `audit_github_repos.py`
- `github_architecture_audit.py`
- `project_analyzer_core.py`
- `project_analyzer_file.py`
- `project_analyzer_reports.py`
- `src_directory_analyzers.py`
- `src_directory_report_generator.py`
- `scan_technical_debt.py`
- `temp_violation_scanner.py`

### **6. Test Files** → `tests/` or appropriate test directories
- `test_analysis.json`
- `test_config_consolidation.py`
- `test_config.json`
- `test_cookie_check.py`
- `test_cookie_loading.py`
- `test_discord_bot_c057.py`
- `test_discord_integration.py`
- `test_discord_simple.py`
- `test_thea_v2_working.py`
- `test_unified_system.py`

### **7. Thea Files** → `tools/thea/`
- `demo_thea_interactive.py`
- `demo_thea_live.py`
- `demo_thea_simple.py`
- `demo_working_thea.py`
- `setup_thea_cookies.py`
- `simple_thea_communication.py`
- `tell_thea_session_summary.py`
- `thea_authentication_handler.py`
- `thea_automation_browser.py`
- `thea_automation_cookie_manager.py`
- `thea_automation_messaging.py`
- `thea_automation.py`
- `thea_cookie_manager.py`
- `thea_cookies.json`
- `thea_login_detector.py`
- `thea_login_handler_refactored.py`
- `thea_login_handler.py`
- `thea_undetected_helper.py`

### **8. Agent Coordination Scripts** → `tools/coordination/`
- `agent1_coordination.py`
- `agent1_response.py`
- `agent_devlog_watcher.py`
- `assignment_confirmation.py`
- `hard_onboard_agent4.py`
- `implementation_leadership_confirmation.py`
- `onboard_survey_agents.py`
- `respond_to_agent6.py`
- `response_detector.py`
- `simple_agent_onboarding.py`
- `swarm_workspace_broadcast.py`
- `pyautogui_training_broadcast.py`

### **9. JSON Data Files** → `data/` or appropriate location
- `AGENT2_INDEPENDENT_ARCHITECTURE_AUDIT.json`
- `chatgpt_project_context.json`
- `cleanup_summary.json`
- `COMPLETE_GITHUB_ROI_RESULTS.json`
- `cursor_agent_coords.json`
- `dependency_cache.json`
- `github_75_repos_master_list.json`
- `GITHUB_ARCHITECTURE_AUDIT_RESULTS.json`
- `GITHUB_AUDIT_RESULTS.json`
- `github_repos_full_list_agent5.json`
- `project_analysis.json`
- `status.json`
- `test_analysis.json`
- `v2_violations_full_report.json`

### **10. Run Scripts** → `scripts/` or `tools/`
- `run_discord_bot.py`
- `run_discord_commander.py`
- `run_discord_messaging.py`
- `run_unified_discord_bot_with_restart.py`
- `run_unified_discord_bot.py`
- `run_unified.py`

### **11. Discord Bot Scripts** → `tools/discord/` or `scripts/discord/`
- `discord_command_handlers.py`

### **12. Consolidation Scripts** → `tools/consolidation/`
- `consolidate_messaging.py`
- `validate_consolidation.py`

### **13. Cleanup Scripts** → `tools/cleanup/`
- `cleanup_obsolete_files.py`
- `cleanup_stub_files.py`

### **14. Fix Scripts** → `tools/fixes/`
- `fix_src_imports.py`

### **15. Other Scripts** → `tools/` or appropriate location
- `add_license_automation.py`
- `comprehensive_project_analyzer.py`
- `comprehensive_project_analyzer_BACKUP_PRE_REFACTOR.py`
- `cycle_1_backup_partial.py`
- `cycle_1_dependency_progress.py`
- `independent_architecture_review.py`

### **16. Text/Data Files** → `data/` or `archive/`
- `Agent-8_to_Agent-2_Coordination_Message.txt`
- `audit_results.txt`
- `empty_subdirs_list.txt`
- `github_final_output.txt`
- `scan_output.txt`
- `team_delta_scan_results.txt`

### **17. XML/Schema Files** → `schemas/` or `data/schemas/`
- `debate_schema.xsd`
- `swarm_debate_consolidation_backup.xml`
- `swarm_debate_consolidation.xml`

### **18. Other Files** → Appropriate locations
- `hancaptaidbook` → `data/` or `archive/`
- `notify_agents.bat` → `scripts/`

---

## 🎯 Root Files to KEEP

1. `README.md` - Main project readme
2. `AGENTS.md` - Agent instructions
3. `CHANGELOG.md` - Version history
4. `STANDARDS.md` - Coding standards
5. `LICENSE` - License file (if exists)
6. `requirements.txt` - Python dependencies
7. `package.json` - Node dependencies
8. `pyproject.toml` - Python project config
9. `jest.config.js` - Jest config
10. `Makefile` - Build automation
11. `importlinter.ini` - Import linting config
12. `.gitignore` - Git ignore rules
13. `.pre-commit-config.yaml` - Pre-commit hooks
14. `.eslintrc.cjs` - ESLint config
15. `env.example` - Environment template

---

## 📊 Expected Results

**Before**: ~150+ files in root  
**After**: ~15 essential files in root  
**Reduction**: ~90% cleanup

---

## ✅ Execution Status

- [ ] Emergency docs moved
- [ ] DUP-* reports moved
- [ ] DISCORD_* files moved
- [ ] QUARANTINE_* files moved
- [ ] Analysis scripts moved
- [ ] Test files moved
- [ ] Thea files moved
- [ ] Agent coordination scripts moved
- [ ] JSON data files moved
- [ ] Run scripts moved
- [ ] Other scripts moved
- [ ] Text/data files moved
- [ ] XML/schema files moved

---

**Status**: IN PROGRESS  
**Agent**: Agent-4 (Captain)

