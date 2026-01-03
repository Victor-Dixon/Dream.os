# Phase 3B Duplicate Cleanup Plan
==================================

**Target:** Full codebase systematic duplicate cleanup
**Strategy:** Keep 1 canonical file per group, remove exact duplicates
**Priority:** Largest groups first (biggest impact)

## Executive Summary
- **Duplicate Groups:** 275
- **Duplicate Files:** 588
- **Canonical Files Preserved:** 275
- **Space Saved:** 2,639,201 bytes (2.5 MB)

## Category Breakdown

### Documentation
- Groups: 7
- Files: 44
- Space: 34,554 bytes (0.0 MB)

### Data Files
- Groups: 1
- Files: 2
- Space: 5,784 bytes (0.0 MB)

### Code Files
- Groups: 265
- Files: 533
- Space: 2,541,268 bytes (2.4 MB)

### Other
- Groups: 2
- Files: 9
- Space: 57,595 bytes (0.1 MB)

## Detailed Cleanup Actions

### Group 1: 30 identical files (10 bytes each) - .md

**KEEP:** `phase3b_backup\artifacts\2025-12-12_agent-5_analytics-security-audit.md`
**REMOVE:**
  - `artifacts\2025-12-12_agent-5_analytics-import-validation-results.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_analytics-ssot-coverage-analysis.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_analytics-ssot-verification-complete.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_analytics-validation-approach.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-artifact-index.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-completion-certificate.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-comprehensive-final-report.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-delegation-summary.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-executive-summary.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-final-status.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_audit-metrics-impact.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_bilateral-coordination-activation.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_ci-workflow-validation.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_cleanup-summary-final.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_code-comment-review-response.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_coordination-metrics-summary.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_data-processing-security-scan.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_discord-bot-diagnostic.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_documentation-cleanup-analysis.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_import-structure-delegation.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_message-queue-health-check.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_other-domains-assessment.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_pre-public-audit-final-report.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_pre-public-audit-plan.md`
  - `phase3b_backup\artifacts\2025-12-12_agent-5_session-summary.md`
  - `phase3b_backup\artifacts\2025-12-13_agent-5_daily-coordination-summary.md`
  - `phase3b_backup\artifacts\2025-12-13_agent-5_discord-bot-diagnostic-validation.md`
  - `phase3b_backup\artifacts\2025-12-13_agent-5_session-progress-summary.md`
  - `phase3b_backup\scripts\extract_freeride_error.py`

### Group 2: 6 identical files (4,933 bytes each) - .png

**KEEP:** `phase3b_backup\temp\discord_images\mermaid_33137.png`
**REMOVE:**
  - `phase3b_backup\temp\discord_images\mermaid_32451.png`
  - `phase3b_backup\temp\discord_images\mermaid_80916.png`
  - `phase3b_backup\temp\discord_images\mermaid_85848.png`
  - `phase3b_backup\temp\discord_images\mermaid_9448.png`
  - `temp\discord_images\mermaid_46872.png`

### Group 3: 3 identical files (16,465 bytes each) - .coverage_analyzer; print('✅ Both modules import successfully')

**KEEP:** `.unified_verifier; import tools.coverage_analyzer; print('✅ Both modules import successfully')`
**REMOVE:**
  - `sages - stall recovery round 3 (4 messages Agents 1,2,3,7) + Batch 1 comprehensive status reply to Agent-4`
  - `sages for batch consolidation - Batches 5, 6 SSOT verification and parallel execution coordination`

### Group 4: 3 identical files (9,439 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\memory\storage\conversation_operations.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\conversation_operations.py`
  - `phase3b_backup\systems\memory\memory\storage\conversation_operations.py`

### Group 5: 3 identical files (8,354 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\gui\panels\ai_studio\conversational_ai_component.py`
**REMOVE:**
  - `phase3b_backup\agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio\conversational_ai_component.py`
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\gui\panels\ai_studio\conversational_ai_component.py`

### Group 6: 3 identical files (3,109 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\memory\api\conversation_api.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\conversation_api.py`
  - `phase3b_backup\systems\memory\memory\api\conversation_api.py`

### Group 7: 3 identical files (1,543 bytes each) - .txt

**KEEP:** `phase3b_backup\archive\dreamscape_project\Thea\outputs\data\templates\chatgpt_sent_template_20250711_151139.txt`
**REMOVE:**
  - `archive\dreamscape_project\Thea\outputs\data\templates\chatgpt_sent_template_20250711_150816.txt`
  - `phase3b_backup\archive\dreamscape_project\Thea\outputs\data\templates\chatgpt_sent_template_20250711_151356.txt`

### Group 8: 3 identical files (1,543 bytes each) - .txt

**KEEP:** `phase3b_backup\archive\dreamscape_project\Thea\outputs\data\templates\working_demo_template_20250711_035629.txt`
**REMOVE:**
  - `archive\dreamscape_project\Thea\outputs\data\templates\simple_sent_template_20250711_152323.txt`
  - `phase3b_backup\archive\dreamscape_project\Thea\outputs\data\templates\working_demo_template_20250711_150643.txt`

### Group 9: 2 identical files (88,694 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\mmorpg_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\mmorpg_system.py`

### Group 10: 2 identical files (75,808 bytes each) - .py

**KEEP:** `systems\gui\gui\main_window_original_backup.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\main_window_original_backup.py`

### Group 11: 2 identical files (47,344 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\enhanced_skill_resume_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\enhanced_skill_resume_system.py`

### Group 12: 2 identical files (45,217 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\llm_summarization_pipeline.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\llm_summarization_pipeline.py`

### Group 13: 2 identical files (41,959 bytes each) - .py

**KEEP:** `systems\gui\gui\components\shared_components.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\shared_components.py`

### Group 14: 2 identical files (37,719 bytes each) - .py

**KEEP:** `systems\analytics\analytics\analytics_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\analytics_system.py`

### Group 15: 2 identical files (36,247 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\mmorpg_engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\mmorpg_engine.py`

### Group 16: 2 identical files (34,865 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume\resume_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume\resume_system.py`

### Group 17: 2 identical files (34,049 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume_weaponizer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume_weaponizer.py`

### Group 18: 2 identical files (33,421 bytes each) - .py

**KEEP:** `systems\analytics\analytics\content_analytics_integration.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\content_analytics_integration.py`

### Group 19: 2 identical files (32,773 bytes each) - .py

**KEEP:** `systems\gui\gui\components\unified_data_loader.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\unified_data_loader.py`

### Group 20: 2 identical files (31,723 bytes each) - .py

**KEEP:** `systems\gui\gui\components\real_time_debug_dashboard.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\real_time_debug_dashboard.py`

### Group 21: 2 identical files (29,313 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\archive\devlog_panel_old.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\archive\devlog_panel_old.py`

### Group 22: 2 identical files (29,030 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\templates\template_analytics.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\templates\template_analytics.py`

### Group 23: 2 identical files (28,379 bytes each) - .py

**KEEP:** `systems\templates\templates\template_processors.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\template_processors.py`

### Group 24: 2 identical files (26,954 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\prompt_interactor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\prompt_interactor.py`

### Group 25: 2 identical files (26,453 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\content\content_analytics.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\content\content_analytics.py`

### Group 26: 2 identical files (25,892 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\conversational_ai_panel.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\conversational_ai_panel.py`

### Group 27: 2 identical files (25,051 bytes each) - .py

**KEEP:** `systems\gui\gui\components\unified_export_center.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\unified_export_center.py`

### Group 28: 2 identical files (24,663 bytes each) - .py

**KEEP:** `systems\gui\gui\components\refresh_integration_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\refresh_integration_manager.py`

### Group 29: 2 identical files (24,632 bytes each) - .py

**KEEP:** `systems\gui\gui\components\global_refresh_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\global_refresh_manager.py`

### Group 30: 2 identical files (24,083 bytes each) - .py

**KEEP:** `systems\gui\gui\components\advanced_error_recovery.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\advanced_error_recovery.py`

### Group 31: 2 identical files (24,054 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\migration.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\migration.py`

### Group 32: 2 identical files (23,807 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\analytics_database.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\analytics_database.py`

### Group 33: 2 identical files (23,609 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation\unified_conversation_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation\unified_conversation_scraper.py`

### Group 34: 2 identical files (23,457 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\dashboard_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\dashboard_manager.py`

### Group 35: 2 identical files (23,409 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\core\analytics_engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\core\analytics_engine.py`

### Group 36: 2 identical files (22,836 bytes each) - .py

**KEEP:** `systems\gui\gui\components\content_analytics_widget.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\content_analytics_widget.py`

### Group 37: 2 identical files (22,666 bytes each) - .py

**KEEP:** `systems\gui\gui\components\time_series_chart_widget.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\time_series_chart_widget.py`

### Group 38: 2 identical files (22,602 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\character_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\character_system.py`

### Group 39: 2 identical files (22,370 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\report_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\report_generator.py`

### Group 40: 2 identical files (22,185 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\world_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\world_system.py`

### Group 41: 2 identical files (21,497 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\export_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\export_manager.py`

### Group 42: 2 identical files (21,382 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\enhanced_progress_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\enhanced_progress_system.py`

### Group 43: 2 identical files (20,753 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\progress\progress_tracker.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\progress\progress_tracker.py`

### Group 44: 2 identical files (20,423 bytes each) - .py

**KEEP:** `systems\gui\gui\components\conversation_labeling_ui.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\conversation_labeling_ui.py`

### Group 45: 2 identical files (20,246 bytes each) - .py

**KEEP:** `systems\analytics\analytics\time_series_analyzer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\time_series_analyzer.py`

### Group 46: 2 identical files (20,226 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\unified_analytics_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\unified_analytics_system.py`

### Group 47: 2 identical files (20,145 bytes each) - .py

**KEEP:** `systems\templates\templates\template_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\template_manager.py`

### Group 48: 2 identical files (19,937 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\core\mmorpg_engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\core\mmorpg_engine.py`

### Group 49: 2 identical files (19,610 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\tracking\progress_tracker.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\tracking\progress_tracker.py`

### Group 50: 2 identical files (19,481 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume\resume_weaponizer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume\resume_weaponizer.py`

### Group 51: 2 identical files (19,003 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\unified_conversation_manager.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\legacy\unified_conversation_manager.py`

### Group 52: 2 identical files (18,818 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\workflow_base.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\workflow_base.py`

### Group 53: 2 identical files (18,512 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-1\extracted_patterns\utilities\project_scanner.py`
**REMOVE:**
  - `archive\auto_blogger_project\Auto_Blogger\project_scanner.py`

### Group 54: 2 identical files (18,472 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\core\AgentBase.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\core\AgentBase.py`

### Group 55: 2 identical files (18,257 bytes each) - .py

**KEEP:** `systems\analytics\analytics\analytics_optimizer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\analytics_optimizer.py`

### Group 56: 2 identical files (17,841 bytes each) - .py

**KEEP:** `systems\gui\gui\components\topic_cloud_widget.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\topic_cloud_widget.py`

### Group 57: 2 identical files (17,587 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills\enhanced_skill_resume.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills\enhanced_skill_resume.py`

### Group 58: 2 identical files (17,360 bytes each) - .py

**KEEP:** `systems\gui\gui\components\enhanced_dashboard_cards.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\enhanced_dashboard_cards.py`

### Group 59: 2 identical files (17,277 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\combat_engine_panel.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\combat_engine_panel.py`

### Group 60: 2 identical files (17,082 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\ai_studio_base.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\ai_studio_base.py`

### Group 61: 2 identical files (16,896 bytes each) - .py

**KEEP:** `systems\gui\gui\components\unified_load_button.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\unified_load_button.py`

### Group 62: 2 identical files (16,881 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\export_panel_base.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\export_panel_base.py`

### Group 63: 2 identical files (16,665 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\skill_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\skill_system.py`

### Group 64: 2 identical files (16,586 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\expanded_analytics_system_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\expanded_analytics_system_refactored.py`

### Group 65: 2 identical files (16,524 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\scrolling\jquery_scroll_improved.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\scrolling\jquery_scroll_improved.py`

### Group 66: 2 identical files (16,398 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\skill_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\skill_system.py`

### Group 67: 2 identical files (16,225 bytes each) - .py

**KEEP:** `systems\gui\gui\main_window_components\system_initializer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\main_window_components\system_initializer.py`

### Group 68: 2 identical files (16,206 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\data_panel_base.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\data_panel_base.py`

### Group 69: 2 identical files (15,622 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\mmorpg_system_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\mmorpg_system_refactored.py`

### Group 70: 2 identical files (15,238 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\progress_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\progress_system.py`

### Group 71: 2 identical files (15,106 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills\skill_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills\skill_manager.py`

### Group 72: 2 identical files (14,846 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation\conversation_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation\conversation_scraper.py`

### Group 73: 2 identical files (14,836 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\analytics_models.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\analytics_models.py`

### Group 74: 2 identical files (14,479 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\infinite_progression.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\infinite_progression.py`

### Group 75: 2 identical files (14,434 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\panel_controller.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\panel_controller.py`

### Group 76: 2 identical files (14,238 bytes each) - .py

**KEEP:** `systems\gui\gui\main_window.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\main_window.py`

### Group 77: 2 identical files (14,185 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\targeted_scroll_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\targeted_scroll_scraper.py`

### Group 78: 2 identical files (13,811 bytes each) - .py

**KEEP:** `systems\templates\templates\template_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\template_system.py`

### Group 79: 2 identical files (13,758 bytes each) - .py

**KEEP:** `systems\analytics\analytics\topic_analyzer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\topic_analyzer.py`

### Group 80: 2 identical files (13,711 bytes each) - .md

**KEEP:** `agent_workspaces\Agent-1\extracted_patterns\templates\project_journal_template.md`
**REMOVE:**
  - `phase3b_backup\archive\auto_blogger_project\Auto_Blogger\Prompts\project entry template prompt.md`

### Group 81: 2 identical files (12,855 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\DebugAgent.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\DebugAgent.py`

### Group 82: 2 identical files (12,823 bytes each) - .py

**KEEP:** `systems\templates\templates\template_engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\template_engine.py`

### Group 83: 2 identical files (12,797 bytes each) - .py

**KEEP:** `systems\gui\gui\debug_handler.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\debug_handler.py`

### Group 84: 2 identical files (12,560 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\smart_scraper_with_fallback.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\smart_scraper_with_fallback.py`

### Group 85: 2 identical files (12,370 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation_list_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation_list_manager.py`

### Group 86: 2 identical files (12,353 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\chatgpt_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\chatgpt_scraper.py`

### Group 87: 2 identical files (12,323 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\improved_conversation_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\improved_conversation_scraper.py`

### Group 88: 2 identical files (12,166 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills.py`

### Group 89: 2 identical files (12,158 bytes each) - .py

**KEEP:** `systems\templates\templates\prompt_deployer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\prompt_deployer.py`

### Group 90: 2 identical files (11,903 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\core\player_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\core\player_manager.py`

### Group 91: 2 identical files (11,838 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\workflow_controller.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\workflow_controller.py`

### Group 92: 2 identical files (11,275 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\analytics_base.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\analytics_base.py`

### Group 93: 2 identical files (11,181 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\achievement_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\achievement_system.py`

### Group 94: 2 identical files (10,931 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\utils\chat_navigation.py`

### Group 95: 2 identical files (10,801 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\quest_log_panel.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\quest_log_panel.py`

### Group 96: 2 identical files (10,759 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\credential_login.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\credential_login.py`

### Group 97: 2 identical files (10,652 bytes each) - .py

**KEEP:** `systems\memory\memory\models\dreamscape_memory.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\models\dreamscape_memory.py`

### Group 98: 2 identical files (10,610 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\progression.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\progression.py`

### Group 99: 2 identical files (10,524 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine.py`

### Group 100: 2 identical files (10,476 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\achievement.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\achievement.py`

### Group 101: 2 identical files (10,291 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\base\base_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\base\base_scraper.py`

### Group 102: 2 identical files (10,182 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\content_extractor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\content_extractor.py`

### Group 103: 2 identical files (10,159 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\status_controller.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\status_controller.py`

### Group 104: 2 identical files (10,003 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AgentGUI.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AgentGUI.py`

### Group 105: 2 identical files (9,934 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\episode_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\episode_generator.py`

### Group 106: 2 identical files (9,816 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume\resume_tracker.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume\resume_tracker.py`

### Group 107: 2 identical files (9,791 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume\resume_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume\resume_generator.py`

### Group 108: 2 identical files (9,640 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\mmorpg_models.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\mmorpg_models.py`

### Group 109: 2 identical files (9,471 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\weaponizer.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\weaponizer.py`

### Group 110: 2 identical files (9,437 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models.py`

### Group 111: 2 identical files (9,424 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\index_operations.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\index_operations.py`

### Group 112: 2 identical files (9,341 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\data_extractor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\data_extractor.py`

### Group 113: 2 identical files (8,880 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\driver_config.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\driver_config.py`

### Group 114: 2 identical files (8,821 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\database.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\database.py`

### Group 115: 2 identical files (8,794 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\core\game_state.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\core\game_state.py`

### Group 116: 2 identical files (8,665 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\game_engine.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\game_engine.py`

### Group 117: 2 identical files (8,591 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\base_panel.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\base_panel.py`

### Group 118: 2 identical files (8,568 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\DeepSeekModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\DeepSeekModel.py`

### Group 119: 2 identical files (8,457 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\prompt_operations.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\prompt_operations.py`

### Group 120: 2 identical files (8,366 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\message_operations.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\message_operations.py`

### Group 121: 2 identical files (8,323 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\core\AIClient.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\core\AIClient.py`

### Group 122: 2 identical files (8,202 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\player.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\player.py`

### Group 123: 2 identical files (7,964 bytes each) - .py

**KEEP:** `systems\templates\templates\prompt_orchestrator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\prompt_orchestrator.py`

### Group 124: 2 identical files (7,831 bytes each) - .py

**KEEP:** `systems\analytics\analytics\analyze_conversations_ai.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\analyze_conversations_ai.py`

### Group 125: 2 identical files (7,828 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AIAgentWithMemory.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AIAgentWithMemory.py`

### Group 126: 2 identical files (7,667 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation_extractor_legacy.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation_extractor_legacy.py`

### Group 127: 2 identical files (7,590 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\devlog_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\devlog_generator.py`

### Group 128: 2 identical files (7,583 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AgentActor.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AgentActor.py`

### Group 129: 2 identical files (7,509 bytes each) - .py

**KEEP:** `systems\templates\templates\template_models.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\template_models.py`

### Group 130: 2 identical files (7,002 bytes each) - .md

**KEEP:** `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\scrapers\MIGRATION_GUIDE.md`
**REMOVE:**
  - `systems\scrapers\scrapers\MIGRATION_GUIDE.md`

### Group 131: 2 identical files (6,982 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\login_handler.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\login_handler.py`

### Group 132: 2 identical files (6,843 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\ErrorDetector.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\ErrorDetector.py`

### Group 133: 2 identical files (6,772 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\two_factor_auth.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\two_factor_auth.py`

### Group 134: 2 identical files (6,726 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\OpenAIModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\OpenAIModel.py`

### Group 135: 2 identical files (6,664 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\cookie_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\cookie_manager.py`

### Group 136: 2 identical files (6,565 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\core\base_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\core\base_system.py`

### Group 137: 2 identical files (6,384 bytes each) - .md

**KEEP:** `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\scrapers\SCRAPER_CONSOLIDATION_GUIDE.md`
**REMOVE:**
  - `systems\scrapers\scrapers\SCRAPER_CONSOLIDATION_GUIDE.md`

### Group 138: 2 identical files (6,369 bytes each) - .py

**KEEP:** `systems\memory\memory\api\memory_api.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\memory_api.py`

### Group 139: 2 identical files (6,369 bytes each) - .py

**KEEP:** `systems\gui\gui\components\loading_screen.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\loading_screen.py`

### Group 140: 2 identical files (6,307 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\schema_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\schema_manager.py`

### Group 141: 2 identical files (6,298 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\analytics_helpers.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\analytics_helpers.py`

### Group 142: 2 identical files (6,260 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\login_status.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\login_status.py`

### Group 143: 2 identical files (5,784 bytes each) - .json

**KEEP:** `CURSOR_MCP_CONFIG.json`
**REMOVE:**
  - `config\mcp`

### Group 144: 2 identical files (5,652 bytes each) - .py

**KEEP:** `systems\gui\gui\components\ftue_welcome_modal.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\ftue_welcome_modal.py`

### Group 145: 2 identical files (5,616 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\CustomAgent.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\CustomAgent.py`

### Group 146: 2 identical files (5,547 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\settings\api_settings.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\settings\api_settings.py`

### Group 147: 2 identical files (5,530 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\process_all_conversations_demo.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\legacy\process_all_conversations_demo.py`

### Group 148: 2 identical files (5,460 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AgentRegistry.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AgentRegistry.py`

### Group 149: 2 identical files (5,181 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\browser_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\browser_manager.py`

### Group 150: 2 identical files (5,170 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\thread_safe_db.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\thread_safe_db.py`

### Group 151: 2 identical files (5,132 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\driver_creator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\driver_creator.py`

### Group 152: 2 identical files (5,076 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\process_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\process_manager.py`

### Group 153: 2 identical files (5,043 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\JournalAgent.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\JournalAgent.py`

### Group 154: 2 identical files (4,948 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\blog_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\blog_generator.py`

### Group 155: 2 identical files (4,759 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\ingest_chatgpt_json.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\legacy\ingest_chatgpt_json.py`

### Group 156: 2 identical files (4,730 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\final_working_scraper.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\final_working_scraper.py`

### Group 157: 2 identical files (4,571 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\settings\general_settings.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\settings\general_settings.py`

### Group 158: 2 identical files (4,505 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\ingest_conversation_files.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\legacy\ingest_conversation_files.py`

### Group 159: 2 identical files (4,237 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\skill.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\skill.py`

### Group 160: 2 identical files (4,174 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation_extractor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation_extractor.py`

### Group 161: 2 identical files (4,005 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\settings\memory_settings.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\settings\memory_settings.py`

### Group 162: 2 identical files (3,995 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\ContextManager.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\ContextManager.py`

### Group 163: 2 identical files (3,894 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\refresh_chatgpt_cookies.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\refresh_chatgpt_cookies.py`

### Group 164: 2 identical files (3,764 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\quest.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\quest.py`

### Group 165: 2 identical files (3,753 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\api_helpers.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\api_helpers.py`

### Group 166: 2 identical files (3,744 bytes each) - .py

**KEEP:** `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\update_conversation_stats.py`
**REMOVE:**
  - `phase3b_backup\archive\dreamscape_project\Thea\src\dreamscape\core\legacy\update_conversation_stats.py`

### Group 167: 2 identical files (3,624 bytes each) - .py

**KEEP:** `systems\memory\memory\processing\content_processor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\processing\content_processor.py`

### Group 168: 2 identical files (3,590 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AIAgent.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AIAgent.py`

### Group 169: 2 identical files (3,551 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\base\login_utils.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\base\login_utils.py`

### Group 170: 2 identical files (3,549 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\login_utils.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\login_utils.py`

### Group 171: 2 identical files (3,502 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\core\AgentPlanner.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\core\AgentPlanner.py`

### Group 172: 2 identical files (3,467 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\system_utils.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\system_utils.py`

### Group 173: 2 identical files (3,286 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\content_processor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\content_processor.py`

### Group 174: 2 identical files (3,060 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\core\ExternalAIAdapter.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\core\ExternalAIAdapter.py`

### Group 175: 2 identical files (3,008 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\content_helpers.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\content_helpers.py`

### Group 176: 2 identical files (2,991 bytes each) - .py

**KEEP:** `systems\memory\memory\search\search_storage.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\search\search_storage.py`

### Group 177: 2 identical files (2,772 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\social_content_generator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\social_content_generator.py`

### Group 178: 2 identical files (2,683 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\demo_conversations.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\demo_conversations.py`

### Group 179: 2 identical files (2,628 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\cli_handler.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\cli_handler.py`

### Group 180: 2 identical files (2,511 bytes each) - .py

**KEEP:** `systems\memory\memory\convenience.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\convenience.py`

### Group 181: 2 identical files (2,456 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation_fetcher.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation_fetcher.py`

### Group 182: 2 identical files (2,372 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\templated_prompts.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\templated_prompts.py`

### Group 183: 2 identical files (2,241 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\SubprocessAIModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\SubprocessAIModel.py`

### Group 184: 2 identical files (1,950 bytes each) - .py

**KEEP:** `systems\memory\memory\search\vector_search.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\search\vector_search.py`

### Group 185: 2 identical files (1,852 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\__init__.py`

### Group 186: 2 identical files (1,840 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\community_templates_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\community_templates_panel_refactored.py`

### Group 187: 2 identical files (1,822 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\__init__.py`

### Group 188: 2 identical files (1,768 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\enums.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\enums.py`

### Group 189: 2 identical files (1,687 bytes each) - .py

**KEEP:** `systems\memory\memory\api\prompt_api.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\prompt_api.py`

### Group 190: 2 identical files (1,624 bytes each) - .py

**KEEP:** `systems\memory\memory\processing\prompt_processor.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\processing\prompt_processor.py`

### Group 191: 2 identical files (1,542 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\analysis\knowledge_graph_backend.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\analysis\knowledge_graph_backend.py`

### Group 192: 2 identical files (1,533 bytes each) - .py

**KEEP:** `tools\lead_exports\outputs.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\outputs.py`

### Group 193: 2 identical files (1,517 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\main_controller.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\main_controller.py`

### Group 194: 2 identical files (1,506 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\consolidated_memory_weaponization_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\consolidated_memory_weaponization_panel_refactored.py`

### Group 195: 2 identical files (1,456 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\enhanced_devlog_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\enhanced_devlog_panel_refactored.py`

### Group 196: 2 identical files (1,440 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\voice_modeling_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\voice_modeling_panel_refactored.py`

### Group 197: 2 identical files (1,425 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\content_analytics_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\content_analytics_panel_refactored.py`

### Group 198: 2 identical files (1,412 bytes each) - .py

**KEEP:** `systems\gui\gui\components\data_loader.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\data_loader.py`

### Group 199: 2 identical files (1,398 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\weworkremotely.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\weworkremotely.py`

### Group 200: 2 identical files (1,386 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\craigslist.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\craigslist.py`

### Group 201: 2 identical files (1,339 bytes each) - .py

**KEEP:** `systems\gui\gui\components\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\__init__.py`

### Group 202: 2 identical files (1,276 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\enhanced_analytics_panel_refactored.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\enhanced_analytics_panel_refactored.py`

### Group 203: 2 identical files (1,251 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\MyAIModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\MyAIModel.py`

### Group 204: 2 identical files (1,227 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills\skill_tracker.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills\skill_tracker.py`

### Group 205: 2 identical files (1,224 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\settings\accessibility_settings.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\settings\accessibility_settings.py`

### Group 206: 2 identical files (1,207 bytes each) - .py

**KEEP:** `systems\gui\gui\components\menu_bar.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\menu_bar.py`

### Group 207: 2 identical files (1,180 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills\skill_calculator.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills\skill_calculator.py`

### Group 208: 2 identical files (1,174 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\reddit.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\reddit.py`

### Group 209: 2 identical files (1,150 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\remoteok.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\remoteok.py`

### Group 210: 2 identical files (995 bytes each) - .txt

**KEEP:** `phase3b_backup\archive\dreamscape_project\Thea\outputs\data\templates\context_sent_template_20250711_153258.txt`
**REMOVE:**
  - `archive\dreamscape_project\Thea\outputs\data\templates\context_sent_template_20250711_152714.txt`

### Group 211: 2 identical files (987 bytes each) - .py

**KEEP:** `systems\memory\memory\api\agent_api.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\agent_api.py`

### Group 212: 2 identical files (979 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\OllamaModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\OllamaModel.py`

### Group 213: 2 identical files (918 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\__init__.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\__init__.py`

### Group 214: 2 identical files (909 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\modular\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\modular\__init__.py`

### Group 215: 2 identical files (887 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\helpers.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\helpers.py`

### Group 216: 2 identical files (851 bytes each) - .py

**KEEP:** `systems\gui\gui\components\toolbar.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\toolbar.py`

### Group 217: 2 identical files (833 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\scrolling\scroll_manager.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\scrolling\scroll_manager.py`

### Group 218: 2 identical files (732 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\__init__.py`

### Group 219: 2 identical files (703 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\event_controller.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\event_controller.py`

### Group 220: 2 identical files (698 bytes each) - .js

**KEEP:** `agent_workspaces\Agent-1\extracted_patterns\testing_patterns\jest.teardown.js`
**REMOVE:**
  - `archive\auto_blogger_project\Auto_Blogger\tests\jest.teardown.js`

### Group 221: 2 identical files (694 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\config.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\config.py`

### Group 222: 2 identical files (626 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\ai_studio\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\ai_studio\__init__.py`

### Group 223: 2 identical files (617 bytes each) - .py

**KEEP:** `systems\templates\templates\models\template.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\models\template.py`

### Group 224: 2 identical files (578 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\base.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\base.py`

### Group 225: 2 identical files (568 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\equipment_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\equipment_system.py`

### Group 226: 2 identical files (565 bytes each) - .py

**KEEP:** `systems\templates\templates\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\__init__.py`

### Group 227: 2 identical files (553 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\knowledge.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\knowledge.py`

### Group 228: 2 identical files (518 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\AIModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\AIModel.py`

### Group 229: 2 identical files (506 bytes each) - .py

**KEEP:** `systems\memory\memory\models\memory_chunk.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\models\memory_chunk.py`

### Group 230: 2 identical files (498 bytes each) - .py

**KEEP:** `systems\memory\memory\storage\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\storage\__init__.py`

### Group 231: 2 identical files (497 bytes each) - .py

**KEEP:** `systems\memory\memory\weaponization\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\weaponization\__init__.py`

### Group 232: 2 identical files (497 bytes each) - .py

**KEEP:** `systems\analytics\analytics\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\__init__.py`

### Group 233: 2 identical files (487 bytes each) - .py

**KEEP:** `systems\analytics\analytics\expanded\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\expanded\__init__.py`

### Group 234: 2 identical files (425 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\__init__.py`

### Group 235: 2 identical files (419 bytes each) - .py

**KEEP:** `systems\gui\gui\components\status_bar.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\status_bar.py`

### Group 236: 2 identical files (419 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\base\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\base\__init__.py`

### Group 237: 2 identical files (417 bytes each) - .py

**KEEP:** `systems\gui\gui\components\refresh_types.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\components\refresh_types.py`

### Group 238: 2 identical files (400 bytes each) - .py

**KEEP:** `systems\gui\gui\viewmodels\panel_viewmodels.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\viewmodels\panel_viewmodels.py`

### Group 239: 2 identical files (394 bytes each) - .py

**KEEP:** `systems\gui\gui\controllers\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\controllers\__init__.py`

### Group 240: 2 identical files (386 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\models\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\models\__init__.py`

### Group 241: 2 identical files (366 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\engine\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\engine\__init__.py`

### Group 242: 2 identical files (348 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume_tracker.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume_tracker.py`

### Group 243: 2 identical files (341 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\MistralModel.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\MistralModel.py`

### Group 244: 2 identical files (333 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\settings\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\settings\__init__.py`

### Group 245: 2 identical files (329 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\skills\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\skills\__init__.py`

### Group 246: 2 identical files (325 bytes each) - .py

**KEEP:** `systems\gui\gui\viewmodels\main_viewmodel.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\viewmodels\main_viewmodel.py`

### Group 247: 2 identical files (323 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\resume\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\resume\__init__.py`

### Group 248: 2 identical files (312 bytes each) - .py

**KEEP:** `tools\lead_harvesting\scrapers\__init__.py`
**REMOVE:**
  - `archive\lead_harvester\contract-leads\scrapers\__init__.py`

### Group 249: 2 identical files (299 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\core\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\core\__init__.py`

### Group 250: 2 identical files (295 bytes each) - .py

**KEEP:** `tools\code_analysis\Agents\core\__init__.py`
**REMOVE:**
  - `archive\agent_refactor_project\agentproject\Agents\core\__init__.py`

### Group 251: 2 identical files (293 bytes each) - .py

**KEEP:** `systems\memory\memory\api\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\api\__init__.py`

### Group 252: 2 identical files (284 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\scrolling\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\scrolling\__init__.py`

### Group 253: 2 identical files (280 bytes each) - .py

**KEEP:** `systems\gui\gui\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\__init__.py`

### Group 254: 2 identical files (277 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\scrolling\scroll_strategies.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\scrolling\scroll_strategies.py`

### Group 255: 2 identical files (249 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\conversation\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\conversation\__init__.py`

### Group 256: 2 identical files (219 bytes each) - .py

**KEEP:** `systems\memory\memory\processing\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\processing\__init__.py`

### Group 257: 2 identical files (219 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\__init__.py`

### Group 258: 2 identical files (215 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\progress\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\progress\__init__.py`

### Group 259: 2 identical files (213 bytes each) - .py

**KEEP:** `systems\gui\gui\viewmodels\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\viewmodels\__init__.py`

### Group 260: 2 identical files (211 bytes each) - .py

**KEEP:** `systems\memory\memory\models\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\models\__init__.py`

### Group 261: 2 identical files (209 bytes each) - .py

**KEEP:** `systems\gui\gui\main_window_components\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\main_window_components\__init__.py`

### Group 262: 2 identical files (207 bytes each) - .py

**KEEP:** `systems\memory\memory\search\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\search\__init__.py`

### Group 263: 2 identical files (199 bytes each) - .py

**KEEP:** `systems\scrapers\scrapers\base\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\scrapers\base\__init__.py`

### Group 264: 2 identical files (189 bytes each) - .py

**KEEP:** `systems\memory\memory\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\memory\__init__.py`

### Group 265: 2 identical files (174 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\analysis\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\analysis\__init__.py`

### Group 266: 2 identical files (164 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\templates\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\templates\__init__.py`

### Group 267: 2 identical files (162 bytes each) - .py

**KEEP:** `systems\templates\templates\analytics\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\analytics\__init__.py`

### Group 268: 2 identical files (162 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\content\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\content\__init__.py`

### Group 269: 2 identical files (160 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\tracking\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\tracking\__init__.py`

### Group 270: 2 identical files (160 bytes each) - .py

**KEEP:** `systems\gui\gui\panels\archive\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\gui\panels\archive\__init__.py`

### Group 271: 2 identical files (160 bytes each) - .py

**KEEP:** `systems\analytics\analytics\unified\core\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\analytics\unified\core\__init__.py`

### Group 272: 2 identical files (158 bytes each) - .py

**KEEP:** `systems\templates\templates\engine\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\engine\__init__.py`

### Group 273: 2 identical files (158 bytes each) - .py

**KEEP:** `systems\templates\templates\runners\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\runners\__init__.py`

### Group 274: 2 identical files (144 bytes each) - .py

**KEEP:** `systems\templates\templates\models\__init__.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\templates\models\__init__.py`

### Group 275: 2 identical files (58 bytes each) - .py

**KEEP:** `systems\gamification\mmorpg\systems\quest_system.py`
**REMOVE:**
  - `archive\dreamscape_project\Thea\src\dreamscape\core\mmorpg\systems\quest_system.py`
