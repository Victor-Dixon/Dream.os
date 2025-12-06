# Agent Toolbelt - Tool Registry (SSOT)

**Last Updated**: 2025-12-04  
**SSOT Domain**: Communication  
**Total Tools**: 60+  
**Registry Source**: `tools/toolbelt_registry.py`

---

## 📋 Registry Format

Each tool entry includes:
- **Name**: Human-readable tool name
- **Flags**: CLI flags to invoke tool
- **Module**: Python module path
- **Description**: One-line purpose
- **Category**: Tool category

---

## 1. Core Project Analysis Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Project Scanner | `--scan`, `-s` | `tools.run_project_scan` | Scan project structure and generate analysis |
| V2 Compliance Checker | `--v2-check`, `--v2`, `-v` | `tools.v2_checker_cli` | Check V2 compliance violations |
| Compliance Dashboard | `--dashboard`, `-d` | `tools.dashboard_html_generator` | Open compliance tracking dashboard |
| Complexity Analyzer | `--complexity`, `-c` | `tools.complexity_analyzer` | Analyze code complexity metrics |
| Refactoring Suggestions | `--refactor`, `-r` | `tools.refactoring_suggestions` | Get intelligent refactoring suggestions |
| Duplication Analyzer | `--duplication`, `--dup` | `tools.duplication_analyzer` | Find duplicate code across project |
| Functionality Verification | `--functionality`, `--verify` | `tools.functionality_verification` | Verify functionality preservation |
| Autonomous Leaderboard | `--leaderboard`, `-l` | `tools.autonomous_leaderboard` | Show agent performance leaderboard |
| Compliance History | `--history` | `tools.compliance_history_tracker` | Track compliance history over time |

---

## 2. QA & Validation Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Test Usage Analyzer | `--test-usage-analyzer`, `--test-usage`, `--unused-via-tests` | `tools.test_usage_analyzer` | Identify unused functionality via test coverage analysis |
| Quick Line Counter | `--line-count`, `--count-lines`, `--lc`, `--linecount`, `--lines` | `tools.quick_linecount` | Quickly count lines in files for V2 compliance |
| SSOT Validator | `--ssot-validate`, `--ssot-check` | `tools.ssot_validator` | Check documentation-code alignment (prevent SSOT violations) |
| Import Chain Validator | `--check-imports`, `--import-check` | `tools.import_chain_validator` | Validate import chains and find missing modules |
| Import Validator | `--validate-imports`, `--imports` | `tools.validate_imports` | Validate import statements and dependencies |
| Memory Leak Scanner | `--memory-scan`, `--memleak` | `tools.memory_leak_scanner` | Detect unbounded caches, lists, and memory leaks |
| Git Commit Verifier | `--git-verify`, `--verify-commits` | `tools.git_commit_verifier` | Verify claimed work exists in git history |
| Test Pyramid Analyzer | `--test-pyramid`, `--pyramid` | `tools.test_pyramid_analyzer` | Analyze test distribution vs 60/30/10 target |
| V2 Batch Checker | `--v2-batch`, `--batch` | `tools.v2_checker_cli` | Quick V2 compliance check for multiple files |
| Coverage Validator | `--coverage-check`, `--cov` | `tools.coverage_validator` | Validate test coverage meets thresholds |
| QA Validation Checklist | `--qa-checklist`, `--qa` | `tools.qa_validation_checklist` | Automated QA validation checklist |
| Extension Test Runner | `--extension-test`, `--ext-test` | `tools.extension_test_runner` | VSCode extension testing with coverage |
| Real Violation Scanner | `--real-violations`, `--real-v2` | `tools.real_violation_scanner` | Verify actual V2 violations (intelligent verification) |

---

## 3. Agent Coordination & Communication Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Unified Agent Status Monitor | `--agent-status`, `--status-check` | `tools.unified_agent_status_monitor` | Unified agent status monitoring (consolidates 15+ tools) |
| Agent Message History | `--message-history`, `--msg-history` | `tools.agent_message_history` | View recent agent message exchanges |
| Work Completion Verifier | `--verify-complete`, `--verify-work` | `tools.work_completion_verifier` | Verify work completion before sending messages |
| Send Message | `--message-cli`, `--msg` | `src.services.messaging_cli` | Send messages to agents via messaging system |
| Get Next Task | `--get-task`, `--next-task` | `src.services.messaging_cli` | Claim next task from centralized task system |
| List Tasks | `--tasks`, `--task-list` | `src.services.messaging_cli` | List all available tasks in queue |

---

## 4. Code Refactoring & Extraction Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Module Extractor | `--extract-module`, `--extract` | `tools.module_extractor` | Extract functions/classes into focused modules |
| Refactor Analyzer | `--refactor-analyze`, `--analyze-refactor` | `tools.refactor_analyzer` | Smart refactoring suggestions based on file analysis |
| Pattern Extractor | `--pattern-extract`, `--extract` | `tools.pattern_extractor` | Semi-automated code pattern extraction (30min → 5min!) |
| Pattern Suggester | `--pattern-suggest`, `--suggest-pattern` | `tools.pattern_suggester` | Suggest consolidation patterns for refactoring |
| Extraction Roadmap Generator | `--extraction-roadmap`, `--roadmap` | `tools.extraction_roadmap_generator` | Auto-generate extraction plans (30min → 5min!) |

---

## 5. Architecture & Integration Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Architecture Pattern Validator | `--validate-patterns`, `--patterns` | `tools.arch_pattern_validator` | Validate architectural patterns (Agent-2's tool) |
| Architecture Review | `--arch-review`, `--review` | `tools.architecture_review` | Request/provide expert architecture reviews |
| Integration Validator | `--check-integration`, `--int-check` | `tools.communication.integration_validator` | Unified integration validator - checks integration issues, health, and readiness |
| Integration Validator (System) | `--integration-validate`, `--int-val` | `tests.integration.system_integration_validator` | Comprehensive system integration validation (C-048-5) |
| Analyze Repository Duplicates | `--analyze-duplicates`, `--dup-analyze` | `tools.analyze_repo_duplicates` | General-purpose duplicate file analyzer for any repository |
| Analyze DreamVault Duplicates | `--analyze-dreamvault`, `--dreamvault-dup` | `tools.analyze_dreamvault_duplicates` | DreamVault-specific duplicate detection (Agent-2's tool) |
| Resolve DreamVault Duplicates | `--resolve-duplicates`, `--dup-resolve` | `tools.resolve_dreamvault_duplicates` | Detailed duplicate resolution analysis and planning (Agent-2's tool) |
| Review DreamVault Integration | `--review-integration`, `--int-review` | `tools.review_dreamvault_integration` | Comprehensive integration review for merged repos (Agent-2's tool) |

---

## 6. Consolidation & Repository Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Repository Analyzer | `--repo-batch`, `--batch-analyze`, `--repository-analyzer` | `tools.repository_analyzer` | Unified repository and project analysis (consolidates repo_batch_analyzer and 7 other tools) |
| Repo Overlap Analyzer | `--repo-overlap`, `--overlap` | `tools.repo_overlap_analyzer` | Analyze repository overlaps for consolidation |
| Consolidation Executor | `--consolidation-exec`, `--consolidate` | `tools.consolidation_executor` | Execute repository consolidations |
| Consolidation Status Tracker | `--consolidation-status`, `--consolidation-track` | `tools.consolidation_status_tracker` | Track GitHub consolidation progress and identify next opportunities |
| Verify Phase 1 Repos | `--verify-phase1`, `--phase1-verify` | `tools.verify_phase1_repos` | Verify Phase 1 consolidation repos |
| Merge Duplicate File Functionality | `--merge-duplicates`, `--dup-merge` | `tools.merge_duplicate_file_functionality` | Compare duplicate files and generate merge suggestions (Agent-3's tool) |
| Verify Merged Repo CI/CD | `--verify-cicd`, `--cicd-verify` | `tools.verify_merged_repo_cicd_enhanced` | Verify CI/CD pipelines for merged repositories (Agent-3's tool) |

---

## 7. Agent & Captain Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Agent Orientation | `--agent-orient`, `--orient` | `tools.agent_orient` | Agent orientation and onboarding |
| Agent Task Finder | `--agent-task-finder`, `--find-tasks` | `tools.agent_task_finder` | Find tasks assigned to agents |
| Find Idle Agents | `--find-idle`, `--idle-agents` | `tools.captain_find_idle_agents` | Find agents that are idle |
| Captain Next Task Picker | `--next-task`, `--pick-task` | `tools.captain_next_task_picker` | Pick next task for agents |
| Task CLI | `--task`, `-t` | `tools.task_cli` | Quick task management (get/list/status/complete) |

---

## 8. Discord & Messaging Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Start Discord System | `--discord-start`, `--start-discord` | `tools.start_discord_system` | Start Discord bot system |
| Verify Discord Running | `--discord-verify`, `--verify-discord` | `tools.verify_discord_running` | Verify Discord bot is running |
| Start Message Queue Processor | `--queue-start`, `--start-queue` | `tools.start_message_queue_processor` | Start message queue processor |
| Diagnose Queue | `--queue-diagnose`, `--diagnose-queue` | `tools.diagnose_queue` | Diagnose message queue issues |
| Messaging Infrastructure Validator | `--queue-status`, `--q-status` | `tools.communication.messaging_infrastructure_validator` | Unified messaging infrastructure validator - checks queue status, persistence, and configuration |

---

## 9. Workflow & Automation Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Soft Onboarding | `--soft-onboard`, `--soft` | `tools.soft_onboard_cli` | Soft onboard agents (6-step session cleanup protocol) |
| Swarm Brain Update | `--swarm-brain`, `--brain` | `tools.update_swarm_brain`, `tools.swarm_brain_cli` | Update swarm brain with insights/lessons/patterns OR Easy Swarm Brain contributions (10min → 1min!) |
| Devlog Auto-Poster | `--devlog-post`, `--post-devlog` | `tools.devlog_auto_poster` | Auto-post devlogs to Discord (10min → 30sec!) |
| Progress Auto-Tracker | `--auto-track`, `--track-progress` | `tools.progress_auto_tracker` | Auto-update status.json from git commits |
| Workspace Auto-Cleaner | `--workspace-clean`, `--clean` | `tools.workspace_auto_cleaner` | Automated workspace cleanup (15min → 2min!) |

---

## 10. Masterpiece Tools ⭐

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Swarm Autonomous Orchestrator | `--orchestrate`, `--gas-station`, `--swarm` | `tools.swarm_orchestrator` | The Gas Station - Autonomous swarm coordination and gas delivery |
| Mission Control | `--mission-control`, `--mission`, `--mc` | `tools.mission_control` | THE masterpiece - Runs all 5 workflow steps, generates conflict-free mission brief |

---

## 11. Utility & Helper Tools

| Tool Name | Flags | Module | Description |
|-----------|-------|--------|-------------|
| Fix Stuck Message | `--fix-stuck`, `--unstuck` | `tools.fix_stuck_message` | Fix stuck messages in queue |
| Workspace Health Monitor | `--workspace-health`, `--health` | `tools.workspace_health_monitor` | Check workspace health (consolidates workspace_health_checker.py) |
| Git Work Verifier | `--git-work-verify`, `--verify-work` | `tools.git_work_verifier` | Verify work in git history |
| Execute DreamVault Cleanup | `--execute-cleanup`, `--cleanup` | `tools.execute_dreamvault_cleanup` | Execute cleanup operations for DreamVault (Agent-2's tool) |

---

## 🔍 Flag Conflicts & Notes

### Duplicate Flags
- `--extract` appears in both `--extract-module` and `--pattern-extract` (check actual registry)
- `--verify-work` appears in both `--git-work-verify` and `--verify-complete` (check actual registry)
- `--swarm-brain` appears in both `tools.update_swarm_brain` and `tools.swarm_brain_cli` (check actual registry)

### Module Consolidations
- `tools.communication.integration_validator` - Consolidates multiple integration checkers
- `tools.unified_agent_status_monitor` - Consolidates 15+ status check tools
- `tools.repository_analyzer` - Consolidates repo_batch_analyzer and 7 other tools

---

## ⚠️ Known Drift

**Status**: Verification pending  
**Action**: Run `python -m tools.toolbelt --list` and compare with this registry

---

**SSOT Registry** ✅  
**Source**: `tools/toolbelt_registry.py`  
**Maintained by**: Agent-6  
**Last Verified**: 2025-12-04

🐝 **WE. ARE. SWARM. ⚡🔥**

