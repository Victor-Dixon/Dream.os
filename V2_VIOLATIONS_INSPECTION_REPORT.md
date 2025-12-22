# V2 Compliance Violations Inspection Report

**Date:** December 12, 2025  
**Branch:** `cursor/107-v2-violations-inspection-c578`  
**Analyst:** Cloud Agent

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Total File Size Violations (Python)** | 269 |
| **Unapproved Violations** | 264 |
| **Approved Exceptions** | 5 |
| **JavaScript/TypeScript Violations** | 12 |
| **Function Size Violations** | 1,939 |
| **Parameter Count Violations** | 2 |
| **GRAND TOTAL VIOLATIONS** | ~2,222 |

---

## V2 Compliance Standards Reference

Per `.cursor/rules/v2-compliance.mdc`:

| Rule | Limit |
|------|-------|
| File size | **Maximum 300 lines** |
| Class size | **Maximum 200 lines** |
| Function size | **Maximum 30 lines** |
| Cyclomatic complexity | **Maximum 10** |
| Nesting depth | **Maximum 3 levels** |
| Parameter count | **Maximum 5 parameters** |

---

## Python File Size Violations (269 Total)

### 🔴 CRITICAL Violations (>600 lines) - 29 Files

| Lines | File | Category |
|-------|------|----------|
| 2,692 | `src/discord_commander/unified_discord_bot.py` | Discord |
| 2,383 | `tools/cli/commands/registry.py` | CLI |
| 1,922 | `src/services/messaging_infrastructure.py` | Services |
| 1,724 | `tools/agent_activity_detector.py` | Tools |
| 1,434 | `tools/repo_safe_merge.py` | Tools |
| 1,367 | `src/orchestrators/overnight/enhanced_agent_activity_detector.py` | Orchestrators |
| 1,238 | `tests/integration/test_messaging_templates_integration.py` | Tests |
| 1,229 | `tools/wordpress_manager.py` | Tools ✅ (Exception) |
| 1,164 | `src/discord_commander/github_book_viewer.py` | Discord |
| 1,043 | `src/core/synthetic_github.py` | Core |
| 1,013 | `src/infrastructure/browser/thea_browser_service.py` | Infrastructure |
| 954 | `src/services/chat_presence/twitch_bridge.py` | Services |
| 870 | `src/services/hard_onboarding_service.py` | Services |
| 855 | `tools/unified_monitor.py` | Tools |
| 819 | `src/discord_commander/templates/broadcast_templates.py` | Discord |
| 819 | `tools/thea/thea_login_handler.py` | Tools |
| 811 | `src/discord_commander/status_change_monitor.py` | Discord |
| 796 | `tools/toolbelt_registry.py` | Tools |
| 791 | `src/core/messaging_pyautogui.py` | Core |
| 787 | `tools_v2/categories/intelligent_mission_advisor.py` | Tools V2 |
| 786 | `tools/repo_safe_merge_v2.py` | Tools |
| 772 | `tools/autonomous_task_engine.py` | Tools |
| 753 | `src/discord_commander/views/main_control_panel_view.py` | Discord |
| 753 | `src/core/messaging_template_texts.py` | Core ✅ (Exception) |
| 751 | `src/core/agent_self_healing_system.py` | Core |
| 749 | `src/services/chat_presence/chat_presence_orchestrator.py` | Services |
| 720 | `tools/enhanced_unified_github.py` | Tools |
| 687 | `src/core/auto_gas_pipeline_system.py` | Core |
| 650 | `src/discord_commander/swarm_showcase_commands.py` | Discord |
| 628 | `tools/project_metrics_to_spreadsheet.py` | Tools |
| 619 | `src/core/debate_to_gas_integration.py` | Core |
| 613 | `tools/github_pr_debugger.py` | Tools |

### 🟠 MAJOR Violations (400-600 lines) - 71 Files

<details>
<summary>Click to expand full list</summary>

| Lines | File |
|-------|------|
| 600 | `src/discord_commander/discord_gui_modals.py` |
| 598 | `src/services/vector_database_service_unified.py` |
| 593 | `tools/agent_mission_controller.py` |
| 586 | `tools/generate_weekly_progression_report.py` |
| 585 | `tools/unified_validator.py` |
| 584 | `tools_v2/categories/github_consolidation_tools.py` |
| 576 | `tools_v2/categories/autonomous_workflow_tools.py` |
| 571 | `tools/devlog_manager.py` |
| 563 | `tools/website_manager.py` |
| 561 | `tools/robinhood_trading_report.py` |
| 559 | `tools/ftp_deployer.py` |
| 542 | `src/core/message_queue_processor.py` ✅ (Exception) |
| 533 | `src/services/soft_onboarding_service.py` |
| 531 | `tools/github_pusher_agent.py` |
| 526 | `src/core/messaging_core.py` ✅ (Exception) |
| 523 | `src/orchestrators/overnight/orchestrator.py` |
| 523 | `src/core/stress_test_metrics.py` |
| 521 | `tools/start_discord_system.py` |
| 518 | `tools/generate_chronological_blog.py` |
| 512 | `tests/unit/services/trader_replay/test_repositories.py` |
| 511 | `tools/swarm_system_inventory.py` |
| 509 | `tests/services/chat_presence/test_twitch_bridge_errors.py` |
| 500 | `tools/test_health_monitor.py` |
| 499 | `src/services/thea/thea_service.py` |
| 498 | `src/core/optimized_stall_resume_prompt.py` |
| 497 | `src/core/utilities/handler_utilities.py` |
| 495 | `tools/session_transition_automator.py` |
| 493 | `tools/tools_consolidation_and_ranking_complete.py` |
| 491 | `tools/stress_test_messaging_queue.py` |
| 488 | `src/core/local_repo_layer.py` |
| 487 | `tools/unified_blogging_automation.py` |
| 486 | `src/core/message_queue.py` |
| 486 | `src/core/vector_strategic_oversight/unified_strategic_oversight/analyzers/swarm_analyzer.py` |
| 483 | `tools/thea/thea_automation.py` |
| 478 | `tools/markov_swarm_integration.py` |
| 477 | `src/gaming/dreamos/ui_integration.py` |
| 476 | `src/services/trader_replay/repositories.py` |
| 475 | `tools_v2/categories/coordination_tools.py` |
| 474 | `tools/create_unified_cli_framework.py` |
| 464 | `src/orchestrators/overnight/listener.py` |
| 461 | `tools/verify_file_usage_enhanced.py` |
| 457 | `src/discord_commander/controllers/swarm_tasks_controller_view.py` |
| 455 | `src/core/repository_merge_improvements.py` |
| 454 | `tools/markov_task_optimizer.py` |
| 451 | `tests/unit/core/test_config_ssot.py` |
| 450 | `tools/hostinger_api_helper.py` |
| 448 | `src/workflows/engine.py` |
| 444 | `tools/thea/analyze_chatgpt_selectors.py` |
| 441 | `src/orchestrators/overnight/monitor.py` |
| 438 | `tools/projectscanner_modular_reports.py` |
| 433 | `tools/wordpress_page_setup.py` |
| 430 | `src/core/multi_agent_responder.py` |
| 430 | `tools_v2/categories/import_fix_tools.py` |
| 426 | `src/core/error_handling/component_management.py` |
| 426 | `src/core/config/config_dataclasses.py` |
| 426 | `tools/unified_github_pr_creator.py` |
| 425 | `src/discord_commander/messaging_commands.py` |
| 418 | `src/repositories/message_repository.py` |
| 416 | `src/core/stress_test_metrics_analyzer.py` |
| 415 | `tools/file_deletion_support.py` |
| 414 | `tools_v2/categories/discord_webhook_tools.py` |
| 414 | `tools_v2/categories/ssot_validation_tools.py` |
| 412 | `src/core/message_queue_persistence.py` |
| 412 | `src/services/chatgpt/session.py` |
| 410 | `tools_v2/categories/memory_safety_tools.py` |
| 409 | `src/discord_commander/webhook_commands.py` |
| 409 | `src/core/error_handling/error_intelligence.py` |
| 409 | `tools/phase2_goldmine_config_scanner.py` |
| 408 | `tools/devlog_poster.py` |
| 406 | `tests/integration/trader_replay/test_cli_smoke.py` |
| 404 | `src/infrastructure/browser/unified_cookie_manager.py` |
| 404 | `src/integrations/jarvis/memory_system.py` |
| 403 | `tools/audit_broken_tools.py` |
| 403 | `tools/unified_analyzer.py` |
| 402 | `src/infrastructure/infrastructure_health_monitor.py` |
| 402 | `tools/test_repo_status_tracker.py` |
| 402 | `tools/spreadsheet_github_adapter.py` |

</details>

### 🟡 THRESHOLD Violations (300-400 lines) - 164 Files

*(Not expanded for brevity - see `V2_VIOLATIONS_INSPECTION_REPORT.json` for full list)*

---

## JavaScript/TypeScript Violations (12 Total)

| Lines | File | Severity |
|-------|------|----------|
| 460 | `src/web/static/js/dashboard/dashboard-view-repository-merge.js` | MAJOR |
| 450 | `src/web/static/js/dashboard-ui-helpers.js` | MAJOR |
| 443 | `src/web/static/js/dashboard-view-engine-discovery.js` | MAJOR |
| 420 | `src/web/static/js/gaming/gamification-ui.js` | MAJOR |
| 405 | `src/web/static/js/dashboard/dom-utils-orchestrator.js` | MAJOR |
| 378 | `src/web/static/js/trading-robot/websocket-subscription-optimized.js` | THRESHOLD |
| 371 | `src/web/static/js/dashboard-view-queue.js` | THRESHOLD |
| 370 | `src/web/static/js/performance/frontend-performance-monitor.js` | THRESHOLD |
| 348 | `src/web/static/js/services-orchestrator.js` | THRESHOLD |
| 343 | `src/web/static/js/dashboard-view-renderer.js` | THRESHOLD |
| 339 | `src/web/static/js/utilities/logging-utils.js` | THRESHOLD |
| 305 | `src/web/static/js/vector-database/analytics.js` | THRESHOLD |

---

## Function Size Violations (1,939 Total)

### Top 20 Worst Offenders

| Lines | Function | File |
|-------|----------|------|
| 431 | `_execute_delivery_operations` | `src/core/messaging_pyautogui.py:332` |
| 282 | `_is_logged_in` | `tools/thea/thea_login_handler.py:328` |
| 273 | `resolve_conflicts_with_ours` | `tools/resolve_merge_conflicts.py:25` |
| 248 | `main` | `tools/start_discord_system.py:272` |
| 228 | `_setup_buttons` | `src/discord_commander/views/main_control_panel_view.py:43` |
| 226 | `_execute_merge_local_first` | `tools/repo_safe_merge.py:357` |
| 219 | `build_message_plan` | `src/orchestrators/overnight/message_plans.py:56` |
| 215 | `generate_report` | `tools/robinhood_trading_report.py:254` |
| 212 | `analyze_coordination_efficiency` | `src/swarm_pulse/intelligence.py:118` |
| 212 | `session` | `src/discord_commander/unified_discord_bot.py:2311` |
| 203 | `_handle_twitch_message` | `src/services/chat_presence/chat_presence_orchestrator.py:218` |
| 199 | `main` | `tools/analyze_merge_failures.py:13` |
| 195 | `create_messaging_parser` | `src/services/messaging_infrastructure.py:477` |
| 192 | `main` | `tools/START_CHAT_BOT_NOW.py:97` |
| 191 | `_send_resume_message_to_agent` | `src/discord_commander/status_change_monitor.py:438` |
| 190 | `assign_tasks_to_8_agents` | `tools/markov_8agent_roi_optimizer.py:173` |
| 190 | `complete_digitaldreamscape_merge` | `tools/complete_batch2_remaining_merges.py:41` |
| 188 | `detect_agent_activity` | `src/orchestrators/overnight/enhanced_agent_activity_detector.py:44` |
| 188 | `get_trading_robot_systems` | `tools/robinhood_trading_report.py:66` |
| 187 | `send_startup_message` | `src/discord_commander/unified_discord_bot.py:670` |

---

## Parameter Count Violations (2 Total)

| Params | Function | File |
|--------|----------|------|
| 8 | `generate_final_report` | `tools/tools_consolidation_and_ranking_complete.py:299` |
| 6 | `send` | `tools/send_a2a_status_and_tasks.py:20` |

---

## Approved Exceptions (5 Matched in Core Directories)

| File | Lines | Reason |
|------|-------|--------|
| `src/core/message_queue_processor.py` | 542 | Queue processing with fallback pattern |
| `src/core/messaging_core.py` | 526 | Unified messaging SSOT |
| `src/core/messaging_template_texts.py` | 753 | Template strings SSOT |
| `tools/wordpress_manager.py` | 1,229 | Comprehensive WordPress management |

*Note: Some approved exceptions are under 300 lines now or in different directories*

---

## Priority Refactoring Recommendations

### Tier 1: Critical (Immediate Attention Required)

| Priority | File | Lines | Recommended Action |
|----------|------|-------|-------------------|
| 1 | `src/discord_commander/unified_discord_bot.py` | 2,692 | Split into separate command/cog modules |
| 2 | `tools/cli/commands/registry.py` | 2,383 | Break into command-specific registry modules |
| 3 | `src/services/messaging_infrastructure.py` | 1,922 | Extract services into separate files |
| 4 | `tools/agent_activity_detector.py` | 1,724 | Modularize detection sources |
| 5 | `tools/repo_safe_merge.py` | 1,434 | Split merge strategies |

### Tier 2: High Priority

| File | Lines | Recommended Action |
|------|-------|-------------------|
| `src/orchestrators/overnight/enhanced_agent_activity_detector.py` | 1,367 | Extract analyzers |
| `src/discord_commander/github_book_viewer.py` | 1,164 | Modularize viewers |
| `src/core/synthetic_github.py` | 1,043 | Split API operations |
| `src/infrastructure/browser/thea_browser_service.py` | 1,013 | Extract browser operations |
| `src/services/chat_presence/twitch_bridge.py` | 954 | Separate bridge components |

---

## Compliance Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| File Compliance Rate | 73.2% | 99%+ | 🔴 Below Target |
| Exception Rate | 0.5% | <5% | ✅ Acceptable |
| Critical Violations | 29 | 0 | 🔴 Requires Action |
| Function Compliance | ~85% | 99%+ | 🔴 Below Target |

---

## Next Steps

1. **Prioritize Critical Files**: Focus on files >1000 lines first
2. **Review Exception Criteria**: Consider if more files qualify
3. **Create Refactoring Plan**: Systematic breakdown of large files
4. **Update README**: Remove "100% Compliant" claim until resolved
5. **Assign to Agents**: Distribute refactoring tasks via contract system

---

*Report generated: December 12, 2025*  
*Scanned directories: src/, tools/, tools_v2/, scripts/, tests/*  
*Excluded: archive/, agent_workspaces/, deprecated directories*
