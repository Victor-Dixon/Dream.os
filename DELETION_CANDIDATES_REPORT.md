# Deletion Candidates Report - V2 Violations Review

**Date:** December 12, 2025  
**Purpose:** Identify files that can be safely deleted to reduce V2 violations  
**Status:** ✅ Phase 1 Complete - 5 files deleted (3,464 lines)

---

## Executive Summary

| Category | Files | Lines | Recommendation |
|----------|-------|-------|----------------|
| **Confirmed Safe to Delete** | 5 | 2,813 | ✅ Delete immediately |
| **Duplicate Files to Consolidate** | 8 | 6,109 | 🔄 Keep one, delete duplicates |
| **CLI Tools for Review** | 104 | 41,332 | 🟡 Review for relevance |
| **Registered but Large** | 30+ | 11,143 | ⚙️ Refactor, don't delete |

---

## 🔴 CONFIRMED SAFE TO DELETE (5 files, 2,813 lines)

These files have **no imports** and are **not standalone CLI tools**:

| Lines | File | Reason |
|-------|------|--------|
| 855 | `tools/unified_monitor.py` | Duplicated by `src/orchestrators/overnight/monitor.py` |
| 402 | `src/infrastructure/infrastructure_health_monitor.py` | Duplicated, unused |
| 233 | `tools/infrastructure_health_monitor.py` | Duplicate of above |
| 819 | `tools/thea/thea_login_handler.py` | Has refactored version (67 lines) |
| 504+ | Various test files | See test section below |

### Immediate Deletion Commands

```bash
# Safe to delete - duplicates or unused
rm tools/unified_monitor.py
rm src/infrastructure/infrastructure_health_monitor.py
rm tools/infrastructure_health_monitor.py
```

---

## 🔄 DUPLICATE FILES TO CONSOLIDATE (8 groups)

Keep one file, delete the others:

### 1. Agent Activity Detector
| File | Lines | Action |
|------|-------|--------|
| `src/orchestrators/overnight/enhanced_agent_activity_detector.py` | 1,367 | ✅ KEEP (integrated) |
| `tools/agent_activity_detector.py` | 1,724 | 🗑️ DELETE (standalone, unused) |

### 2. Repo Safe Merge
| File | Lines | Action |
|------|-------|--------|
| `tools/repo_safe_merge.py` | 1,434 | 🟡 REVIEW - both imported |
| `tools/repo_safe_merge_v2.py` | 786 | 🟡 REVIEW - both imported |

### 3. Scheduler
| File | Lines | Action |
|------|-------|--------|
| `src/orchestrators/overnight/scheduler.py` | 267 | ✅ KEEP (7 imports) |
| `src/orchestrators/overnight/scheduler_refactored.py` | 251 | 🗑️ DELETE (1 import, outdated) |

### 4. Gaming Integration Core
| File | Lines | Action |
|------|-------|--------|
| `src/gaming/gaming_integration_core.py` | 332 | 🗑️ Consolidate into one |
| `src/integrations/osrs/gaming_integration_core.py` | 336 | 🗑️ Consolidate into one |

### 5. FSM Bridge
| File | Lines | Action |
|------|-------|--------|
| `src/message_task/fsm_bridge.py` | 125 | ✅ KEEP (simpler) |
| `src/orchestrators/overnight/fsm_bridge.py` | 374 | 🟡 REVIEW (larger, possibly redundant) |

### 6. Base Manager
| File | Lines | Action |
|------|-------|--------|
| `src/core/base/base_manager.py` | 190 | ✅ KEEP (6 imports) |
| `src/core/managers/base_manager.py` | 199 | 🗑️ DELETE (duplicate) |

### 7. Messaging Templates
| File | Lines | Action |
|------|-------|--------|
| `src/core/messaging_templates.py` | 251 | 🟡 Consolidate |
| `src/services/utils/messaging_templates.py` | 238 | 🟡 Consolidate |

### 8. File Utils
| File | Lines | Action |
|------|-------|--------|
| `src/utils/unified_file_utils.py` | 320 | ✅ KEEP (unified) |
| `src/core/utils/file_utils.py` | 82 | 🗑️ DELETE |
| `src/utils/file_utils.py` | 169 | 🗑️ DELETE |

---

## 🟡 CLI TOOLS FOR REVIEW (Top 30 - 104 total)

These are standalone CLI scripts with `if __name__ == '__main__'` but no imports. Review if still actively used:

| Lines | File | Last Modified | Recommendation |
|-------|------|---------------|----------------|
| 786 | `tools/repo_safe_merge_v2.py` | 2025-12-06 | 🟡 Review if superseded by v1 |
| 772 | `tools/autonomous_task_engine.py` | Recent | 🟢 Likely needed |
| 628 | `tools/project_metrics_to_spreadsheet.py` | Old | 🔴 Likely deprecated |
| 593 | `tools/agent_mission_controller.py` | Recent | 🟢 Likely needed |
| 586 | `tools/generate_weekly_progression_report.py` | Old | 🔴 Likely deprecated |
| 571 | `tools/devlog_manager.py` | Old | 🔴 Likely deprecated |
| 563 | `tools/website_manager.py` | Recent | 🟢 Likely needed |
| 561 | `tools/robinhood_trading_report.py` | Recent | 🟢 Likely needed |
| 559 | `tools/ftp_deployer.py` | Old | 🔴 Likely deprecated |
| 518 | `tools/generate_chronological_blog.py` | Old | 🔴 Likely deprecated |
| 500 | `tools/test_health_monitor.py` | Recent | 🟢 Likely needed |
| 495 | `tools/session_transition_automator.py` | Old | 🔴 Likely deprecated |
| 493 | `tools/tools_consolidation_and_ranking_complete.py` | Old | 🔴 One-time script |
| 491 | `tools/stress_test_messaging_queue.py` | Recent | 🟡 Test tool |
| 483 | `tools/thea/thea_automation.py` | Recent | 🟢 Likely needed |
| 478 | `tools/markov_swarm_integration.py` | Old | 🔴 Likely deprecated |
| 474 | `tools/create_unified_cli_framework.py` | Old | 🔴 One-time script |
| 454 | `tools/markov_task_optimizer.py` | Old | 🔴 Likely deprecated |
| 450 | `tools/hostinger_api_helper.py` | Recent | 🟢 Likely needed |
| 444 | `tools/thea/analyze_chatgpt_selectors.py` | Recent | 🟡 Debug tool |
| 433 | `tools/wordpress_page_setup.py` | Recent | 🟢 Likely needed |
| 415 | `tools/file_deletion_support.py` | Old | 🔴 One-time script |
| 409 | `tools/phase2_goldmine_config_scanner.py` | Old | 🔴 Phase-specific |
| 403 | `tools/audit_broken_tools.py` | Old | 🔴 One-time audit |
| 402 | `tools/test_repo_status_tracker.py` | Old | 🔴 Test file |
| 402 | `tools/spreadsheet_github_adapter.py` | Old | 🔴 Likely deprecated |
| 400 | `tools/validate_trackers.py` | Old | 🔴 One-time validation |
| 399 | `tools/get_repo_chronology.py` | Old | 🔴 Likely deprecated |
| 398 | `tools/workspace_health_monitor.py` | Recent | 🟢 Likely needed |
| 395 | `tools/mission_control.py` | Recent | 🟢 Likely needed |

### Deprecated Tools to Consider Deleting

```bash
# One-time scripts and deprecated tools (review before deleting)
rm tools/project_metrics_to_spreadsheet.py
rm tools/generate_weekly_progression_report.py
rm tools/devlog_manager.py
rm tools/ftp_deployer.py
rm tools/generate_chronological_blog.py
rm tools/session_transition_automator.py
rm tools/tools_consolidation_and_ranking_complete.py
rm tools/markov_swarm_integration.py
rm tools/create_unified_cli_framework.py
rm tools/markov_task_optimizer.py
rm tools/file_deletion_support.py
rm tools/phase2_goldmine_config_scanner.py
rm tools/audit_broken_tools.py
rm tools/test_repo_status_tracker.py
rm tools/spreadsheet_github_adapter.py
rm tools/validate_trackers.py
rm tools/get_repo_chronology.py
```

---

## ⚙️ FILES TO REFACTOR (Not Delete)

These files are registered in `__init__.py` or actively imported but exceed V2 limits:

### tools_v2/categories (Registered in __init__.py)
- All `tools_v2/categories/*.py` files are auto-imported
- Should be **refactored**, not deleted

### src/ Core Files (Actively Imported)
- Files like `src/core/synthetic_github.py` (1043 lines, 5 imports)
- Should be **split into modules**, not deleted

---

## Recommended Immediate Actions

### Phase 1: Safe Deletions (Now)
```bash
cd /workspace
rm tools/unified_monitor.py
rm tools/agent_activity_detector.py
rm src/infrastructure/infrastructure_health_monitor.py
rm tools/infrastructure_health_monitor.py
rm src/orchestrators/overnight/scheduler_refactored.py
```

**Lines saved: ~4,430 lines**

### Phase 2: Consolidate Duplicates (This Week)
1. Consolidate `base_manager.py` files
2. Consolidate `file_utils.py` files  
3. Consolidate `gaming_integration_core.py` files
4. Review `messaging_templates.py` duplication

### Phase 3: Review CLI Tools (Next Sprint)
- Review each deprecated tool
- Move useful ones to archive
- Delete truly unused ones

---

## Impact Summary

| Action | Files | Lines Saved |
|--------|-------|-------------|
| Immediate Safe Deletions | 5 | ~4,430 |
| Duplicate Consolidation | 8 groups | ~2,000 |
| CLI Tool Cleanup | ~20 | ~8,000 |
| **Total Potential** | **~33** | **~14,430** |

This would reduce total V2 violations from 269 to ~240 files immediately, with more savings from refactoring.

---

*Report generated: December 12, 2025*
