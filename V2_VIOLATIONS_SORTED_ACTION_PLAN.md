# V2 Violations - Sorted Action Plan

**Date:** December 12, 2025  
**Total Violations:** 277 files  
**Status:** Categorized and prioritized for action

---

## Executive Summary

| Category | Files | Lines | Action |
|----------|-------|-------|--------|
| **MUST MODULARIZE** | 168 | 82,285 | Split into smaller modules |
| **CLI TOOLS - REVIEW** | 88 | 34,151 | Human review for relevance |
| **TEST FILES - REVIEW** | 18 | 7,800 | Split or consolidate |
| **DELETED THIS SESSION** | 6 | 3,781 | ✅ Complete |

---

## 🔧 MUST MODULARIZE (168 files)

These files are **actively imported** or **registered in `__init__.py`** - they CANNOT be deleted.

### Priority 1: CRITICAL (>600 lines) - 26 files

| Lines | Imports | File | Suggested Action |
|-------|---------|------|------------------|
| 2,692 | 4 | `src/discord_commander/unified_discord_bot.py` | Split into cogs/command modules |
| 2,383 | 4 | `tools/cli/commands/registry.py` | Split by command category |
| 1,922 | 28 | `src/services/messaging_infrastructure.py` | Extract services |
| 1,434 | 2 | `tools/repo_safe_merge.py` | Split merge strategies |
| 1,367 | 6 | `src/orchestrators/overnight/enhanced_agent_activity_detector.py` | Extract detection modules |
| 1,229 | 2 | `tools/wordpress_manager.py` | ✅ Approved exception |
| 1,164 | 3 | `src/discord_commander/github_book_viewer.py` | Split viewer components |
| 1,043 | 5 | `src/core/synthetic_github.py` | Extract API operations |
| 1,013 | 8 | `src/infrastructure/browser/thea_browser_service.py` | Split browser ops |
| 954 | 14 | `src/services/chat_presence/twitch_bridge.py` | Extract bridge components |
| 870 | 3 | `src/services/hard_onboarding_service.py` | Split onboarding steps |
| 819 | 2 | `src/discord_commander/templates/broadcast_templates.py` | Split by template type |
| 819 | 0 | `tools/thea/thea_login_handler.py` | Extract login flows |
| 811 | 2 | `src/discord_commander/status_change_monitor.py` | Extract monitors |
| 796 | 5 | `tools/toolbelt_registry.py` | Split by tool category |
| 791 | 3 | `src/core/messaging_pyautogui.py` | Extract delivery methods |
| 787 | 2 | `tools/categories/intelligent_mission_advisor.py` | Split advisor components |
| 753 | 2 | `src/discord_commander/views/main_control_panel_view.py` | Extract view components |
| 753 | 3 | `src/core/messaging_template_texts.py` | ✅ Approved exception |
| 751 | 2 | `src/core/agent_self_healing_system.py` | Extract healing strategies |
| 749 | 10 | `src/services/chat_presence/chat_presence_orchestrator.py` | Extract handlers |
| 720 | 2 | `tools/enhanced_unified_github.py` | Split GitHub operations |
| 687 | 1 | `src/core/auto_gas_pipeline_system.py` | Extract pipeline stages |
| 650 | 2 | `src/discord_commander/swarm_showcase_commands.py` | Split commands |
| 619 | 1 | `src/core/debate_to_gas_integration.py` | Extract integration logic |
| 613 | 1 | `tools/github_pr_debugger.py` | Split debug utilities |

### Priority 2: MAJOR (400-600 lines) - 70 files

<details>
<summary>Click to expand</summary>

| Lines | File |
|-------|------|
| 600 | `src/discord_commander/discord_gui_modals.py` |
| 598 | `src/services/vector_database_service_unified.py` |
| 585 | `tools/unified_validator.py` |
| 584 | `tools/categories/github_consolidation_tools.py` |
| 576 | `tools/categories/autonomous_workflow_tools.py` |
| 542 | `src/core/message_queue_processor.py` |
| 533 | `src/services/soft_onboarding_service.py` |
| 531 | `tools/github_pusher_agent.py` |
| 526 | `src/core/messaging_core.py` |
| 523 | `src/orchestrators/overnight/orchestrator.py` |
| 523 | `src/core/stress_test_metrics.py` |
| 521 | `tools/start_discord_system.py` |
| 511 | `tools/swarm_system_inventory.py` |
| 499 | `src/services/thea/thea_service.py` |
| 498 | `src/core/optimized_stall_resume_prompt.py` |
| 497 | `src/core/utilities/handler_utilities.py` |
| 488 | `src/core/local_repo_layer.py` |
| 486 | `src/core/vector_strategic_oversight/.../swarm_analyzer.py` |
| 486 | `src/core/message_queue.py` |
| 477 | `src/gaming/dreamos/ui_integration.py` |
| 476 | `src/services/trader_replay/repositories.py` |
| 475 | `tools/categories/coordination_tools.py` |
| 464 | `src/orchestrators/overnight/listener.py` |
| 457 | `src/discord_commander/controllers/swarm_tasks_controller_view.py` |
| 455 | `src/core/repository_merge_improvements.py` |
| 448 | `src/workflows/engine.py` |
| 441 | `src/orchestrators/overnight/monitor.py` |
| 438 | `tools/projectscanner_modular_reports.py` |
| 430 | `src/core/multi_agent_responder.py` |
| 430 | `tools/categories/import_fix_tools.py` |
| 426 | `src/core/error_handling/component_management.py` |
| 426 | `src/core/config/config_dataclasses.py` |
| 425 | `src/discord_commander/messaging_commands.py` |
| 418 | `src/repositories/message_repository.py` |
| 416 | `src/core/stress_test_metrics_analyzer.py` |
| 414 | `tools/categories/ssot_validation_tools.py` |
| 412 | `src/core/message_queue_persistence.py` |
| 412 | `src/services/chatgpt/session.py` |
| 410 | `tools/categories/memory_safety_tools.py` |
| 409 | `src/discord_commander/webhook_commands.py` |
| 409 | `src/core/error_handling/error_intelligence.py` |
| 404 | `src/infrastructure/browser/unified_cookie_manager.py` |
| 404 | `src/integrations/jarvis/memory_system.py` |
| 402 | `tools/spreadsheet_github_adapter.py` |
| 400 | `src/services/trader_replay/replay_engine.py` |

*(+25 more files in 400-500 range)*

</details>

### Priority 3: THRESHOLD (300-400 lines) - 72 files

Files slightly over limit - lower priority for refactoring.

---

## 🟡 CLI TOOLS - NEEDS REVIEW (88 files)

These are **standalone CLI scripts** with no imports. Human must decide if still needed.

### Likely DEPRECATED (One-time/Phase-specific scripts)

| Lines | File | Reason |
|-------|------|--------|
| 786 | `tools/repo_safe_merge_v2.py` | v2 likely superseded |
| 628 | `tools/project_metrics_to_spreadsheet.py` | One-time report tool |
| 586 | `tools/generate_weekly_progression_report.py` | Old reporting |
| 559 | `tools/ftp_deployer.py` | Legacy deployment |
| 518 | `tools/generate_chronological_blog.py` | One-time generation |
| 493 | `tools/tools_consolidation_and_ranking_complete.py` | One-time consolidation |
| 478 | `tools/markov_swarm_integration.py` | Experimental |
| 474 | `tools/create_unified_cli_framework.py` | Setup script |
| 454 | `tools/markov_task_optimizer.py` | Experimental |
| 415 | `tools/file_deletion_support.py` | Utility script |
| 409 | `tools/phase2_goldmine_config_scanner.py` | Phase-specific |
| 403 | `tools/audit_broken_tools.py` | One-time audit |
| 400 | `tools/validate_trackers.py` | One-time validation |
| 399 | `tools/get_repo_chronology.py` | One-time analysis |

### Likely ACTIVE (Recent/Core functionality)

| Lines | File | Reason |
|-------|------|--------|
| 772 | `tools/autonomous_task_engine.py` | Core task system |
| 593 | `tools/agent_mission_controller.py` | Agent control |
| 571 | `tools/devlog_manager.py` | DevOps logging |
| 563 | `tools/website_manager.py` | Active website mgmt |
| 561 | `tools/robinhood_trading_report.py` | Trading reports |
| 495 | `tools/session_transition_automator.py` | Session management |
| 491 | `tools/stress_test_messaging_queue.py` | Testing tool |
| 450 | `tools/hostinger_api_helper.py` | Hosting integration |
| 444 | `tools/thea/analyze_chatgpt_selectors.py` | Thea debugging |
| 433 | `tools/wordpress_page_setup.py` | WordPress setup |
| 398 | `tools/workspace_health_monitor.py` | Health monitoring |
| 395 | `tools/mission_control.py` | Mission control |
| 389 | `tools/wordpress_admin_deployer.py` | WordPress deployment |
| 389 | `tools/captain_inbox_assistant.py` | Captain tools |

---

## 🧪 TEST FILES - NEEDS REVIEW (18 files)

Test files may need splitting or consolidation.

| Lines | File | Action |
|-------|------|--------|
| 1,238 | `tests/integration/test_messaging_templates_integration.py` | Split by feature |
| 512 | `tests/unit/services/trader_replay/test_repositories.py` | Split by repo |
| 509 | `tests/services/chat_presence/test_twitch_bridge_errors.py` | Keep (error coverage) |
| 500 | `tools/test_health_monitor.py` | Review if needed |
| 451 | `tests/unit/core/test_config_ssot.py` | Split by config |
| 406 | `tests/integration/trader_replay/test_cli_smoke.py` | Keep (smoke tests) |
| 402 | `tools/test_repo_status_tracker.py` | Review if needed |
| 400 | `tests/unit/swarm_brain/test_agent_notes.py` | Keep |

---

## ✅ DELETED THIS SESSION (6 files, 3,781 lines)

| File | Lines | Reason |
|------|-------|--------|
| `tools/agent_activity_detector.py` | 1,724 | Duplicate |
| `tools/unified_monitor.py` | 855 | Duplicate |
| `src/infrastructure/infrastructure_health_monitor.py` | 402 | Unused |
| `tools/infrastructure_health_monitor.py` | 232 | Unused |
| `src/orchestrators/overnight/scheduler_refactored.py` | 251 | Superseded |
| `src/core/message_formatters.py` | 317 | Dead code |

---

## Recommended Workflow

### Phase 1: Delete Deprecated CLI Tools (Human Review)
Review the "Likely DEPRECATED" CLI tools list and delete those confirmed unused.

### Phase 2: Modularize Critical Files
Focus on the 26 CRITICAL files (>600 lines) first:
1. `unified_discord_bot.py` (2,692 lines)
2. `registry.py` (2,383 lines)
3. `messaging_infrastructure.py` (1,922 lines)

### Phase 3: Refactor Major Files
Work through the 70 MAJOR files (400-600 lines).

### Phase 4: Clean Threshold Files
Address the 72 THRESHOLD files as time permits.

---

## Impact Projection

| Action | Files | Lines Saved |
|--------|-------|-------------|
| Already Deleted | 6 | 3,781 |
| Deprecated CLI Deletion | ~14 | ~6,500 |
| **Subtotal Deletions** | **~20** | **~10,281** |
| Modularization (no line reduction) | 168 | 0 (compliance only) |

**Projected Final State:**
- Violations reduced from 277 → ~257 (through deletions)
- Remaining 257 files need modularization for full compliance

---

*Generated: December 12, 2025*
