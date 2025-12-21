# Tool Classification - Phase -1 Results

**Date**: 2025-12-21 02:21:39  
**Classification**: Signal vs Noise Analysis  
**Purpose**: Filter V2 refactoring to SIGNAL tools only (Phase -1 of V2 Compliance Refactoring Plan)

---

## 📊 Classification Summary

- **Total Tools Analyzed**: 795
- **SIGNAL Tools** (Real Infrastructure - REFACTOR): 719
- **NOISE Tools** (Thin Wrappers - DEPRECATE/MOVE): 26
- **UNKNOWN Tools** (Needs Manual Review): 50
- **Errors**: 0

---

## Classification Criteria

### ✅ SIGNAL Tools (Real Infrastructure - REFACTOR THESE)

**Criteria**:
- Contains **real business logic** (not just wrappers)
- **Reusable infrastructure** (used across codebase/projects)
- Has **modular architecture** (extractable components)
- Provides **core functionality** (not convenience wrappers)

**Action**: Include in V2 refactoring phases (these are worth fixing)

### ❌ NOISE Tools (Thin Wrappers - DEPRECATE/MOVE THESE)

**Criteria**:
- Just **CLI wrappers** around existing functionality
- No real business logic (calls other tools/functions)
- **One-off convenience scripts** (not reusable infrastructure)
- Can be replaced by direct usage of underlying tool

**Action**: Move to `scripts/`, deprecate, or remove (don't refactor wrappers)

---

## ✅ SIGNAL Tools (719)

**Status**: Real infrastructure - Include in V2 refactoring

- **30day_launch_system** (`tools\30day_launch_system.py`)
  - Lines: 359, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **START_CHAT_BOT_NOW** (`tools\START_CHAT_BOT_NOW.py`)
  - Lines: 293, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **add_business_readiness_tasks** (`tools\add_business_readiness_tasks.py`)
  - Lines: 148, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **add_css_to_wordpress_customizer** (`tools\add_css_to_wordpress_customizer.py`)
  - Lines: 124, Functions: 0, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture

- **add_css_to_wordpress_theme** (`tools\add_css_to_wordpress_theme.py`)
  - Lines: 227, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **add_dadudekc_home_cta** (`tools\add_dadudekc_home_cta.py`)
  - Lines: 186, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **add_dadudekc_home_cta_wpcli** (`tools\add_dadudekc_home_cta_wpcli.py`)
  - Lines: 143, Functions: 2, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Contains complex control flow structures

- **add_dadudekc_proof_assets** (`tools\add_dadudekc_proof_assets.py`)
  - Lines: 190, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **add_hsq_header_cta** (`tools\add_hsq_header_cta.py`)
  - Lines: 304, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **add_license_automation** (`tools\add_license_automation.py`)
  - Lines: 165, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **add_remaining_swarm_knowledge** (`tools\add_remaining_swarm_knowledge.py`)
  - Lines: 198, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **add_signal_tools_to_toolbelt** (`tools\add_signal_tools_to_toolbelt.py`)
  - Lines: 372, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **add_type_annotations** (`tools\add_type_annotations.py`)
  - Lines: 183, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **add_typing_imports** (`tools\add_typing_imports.py`)
  - Lines: 187, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **add_ux_tasks_to_grade_cards** (`tools\add_ux_tasks_to_grade_cards.py`)
  - Lines: 135, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **agent2_session_cleanup_2025-12-15** (`tools\agent2_session_cleanup_2025-12-15.py`)
  - Lines: 401, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **agent3_session_cleanup_2025-12-15** (`tools\agent3_session_cleanup_2025-12-15.py`)
  - Lines: 309, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **agent7_stage1_support_checklist** (`tools\agent7_stage1_support_checklist.py`)
  - Lines: 170, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **agent_activity_detector** (`tools\agent_activity_detector.py`)
  - Lines: 133, Functions: 3, Classes: 2
  - Rationale: Contains classes (2) indicate modular architecture; Contains complex control flow structures

- **agent_bump_script** (`tools\agent_bump_script.py`)
  - Lines: 162, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **agent_cellphone_config_dependency_scanner** (`tools\agent_cellphone_config_dependency_scanner.py`)
  - Lines: 162, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **agent_checkin** (`tools\agent_checkin.py`)
  - Lines: 130, Functions: 14, Classes: 2
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (2) indicate modular architecture

- **agent_cycle_v2_report_validator** (`tools\agent_cycle_v2_report_validator.py`)
  - Lines: 324, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **agent_lifecycle_automator** (`tools\agent_lifecycle_automator.py`)
  - Lines: 241, Functions: 14, Classes: 3
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (3) indicate modular architecture

- **agent_message_history** (`tools\agent_message_history.py`)
  - Lines: 289, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **agent_mission_controller** (`tools\agent_mission_controller.py`)
  - Lines: 593, Functions: 13, Classes: 4
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (4) indicate modular architecture

- **agent_orient** (`tools\agent_orient.py`)
  - Lines: 212, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **agent_task_finder** (`tools\agent_task_finder.py`)
  - Lines: 142, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **audit_github_repos** (`tools\analysis\audit_github_repos.py`)
  - Lines: 223, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **github_architecture_audit** (`tools\analysis\github_architecture_audit.py`)
  - Lines: 361, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **scan_technical_debt** (`tools\analysis\scan_technical_debt.py`)
  - Lines: 233, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **src_directory_report_generator** (`tools\analysis\src_directory_report_generator.py`)
  - Lines: 166, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **temp_violation_scanner** (`tools\analysis\temp_violation_scanner.py`)
  - Lines: 50, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **analysis_toolkit** (`tools\analysis_toolkit.py`)
  - Lines: 257, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **analyze_ai_slop** (`tools\analyze_ai_slop.py`)
  - Lines: 374, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **analyze_batch1_business_value** (`tools\analyze_batch1_business_value.py`)
  - Lines: 264, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **analyze_blog_styling_issues** (`tools\analyze_blog_styling_issues.py`)
  - Lines: 217, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **analyze_browser_automation_duplication** (`tools\analyze_browser_automation_duplication.py`)
  - Lines: 258, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **analyze_comment_code_mismatches** (`tools\analyze_comment_code_mismatches.py`)
  - Lines: 532, Functions: 9, Classes: 2
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (2) indicate modular architecture

- **analyze_dadudekc_blog_readability** (`tools\analyze_dadudekc_blog_readability.py`)
  - Lines: 549, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **analyze_dadudekc_primary_offer** (`tools\analyze_dadudekc_primary_offer.py`)
  - Lines: 170, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **analyze_documentation_sprawl** (`tools\analyze_documentation_sprawl.py`)
  - Lines: 406, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **analyze_merge_failures** (`tools\analyze_merge_failures.py`)
  - Lines: 216, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **analyze_merge_plans** (`tools\analyze_merge_plans.py`)
  - Lines: 104, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **analyze_project_scan** (`tools\analyze_project_scan.py`)
  - Lines: 321, Functions: 11, Classes: 0
  - Rationale: Multiple functions (11) indicate business logic; Contains complex control flow structures

- **analyze_queue_processor_metrics** (`tools\analyze_queue_processor_metrics.py`)
  - Lines: 363, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **analyze_runtime_errors** (`tools\analyze_runtime_errors.py`)
  - Lines: 131, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **analyze_swarm_coordination_patterns** (`tools\analyze_swarm_coordination_patterns.py`)
  - Lines: 495, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **analyze_test_patterns** (`tools\analyze_test_patterns.py`)
  - Lines: 230, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **analyze_web_integration_gaps** (`tools\analyze_web_integration_gaps.py`)
  - Lines: 278, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **apply_hsq_astros_theme** (`tools\apply_hsq_astros_theme.py`)
  - Lines: 352, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **architecture_review** (`tools\architecture_review.py`)
  - Lines: 128, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **archive_consolidated_tools** (`tools\archive_consolidated_tools.py`)
  - Lines: 112, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **archive_consolidation_candidates** (`tools\archive_consolidation_candidates.py`)
  - Lines: 176, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **archive_deprecated_tools** (`tools\archive_deprecated_tools.py`)
  - Lines: 159, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **archive_merge_plans** (`tools\archive_merge_plans.py`)
  - Lines: 68, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **archive_remaining_candidates** (`tools\archive_remaining_candidates.py`)
  - Lines: 177, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **audit_broken_tools** (`tools\audit_broken_tools.py`)
  - Lines: 403, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **audit_broken_tools_split** (`tools\audit_broken_tools_split.py`)
  - Lines: 311, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **audit_cleanup** (`tools\audit_cleanup.py`)
  - Lines: 260, Functions: 13, Classes: 0
  - Rationale: Multiple functions (13) indicate business logic; Contains complex control flow structures

- **audit_dadudekc_blog_content** (`tools\audit_dadudekc_blog_content.py`)
  - Lines: 165, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **audit_dadudekc_blog_posts** (`tools\audit_dadudekc_blog_posts.py`)
  - Lines: 334, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **audit_dadudekc_blog_ux** (`tools\audit_dadudekc_blog_ux.py`)
  - Lines: 611, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **audit_dadudekc_site** (`tools\audit_dadudekc_site.py`)
  - Lines: 311, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **audit_imports** (`tools\audit_imports.py`)
  - Lines: 149, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **audit_toolbelt** (`tools\audit_toolbelt.py`)
  - Lines: 138, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **audit_websites_grade_cards** (`tools\audit_websites_grade_cards.py`)
  - Lines: 631, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **audit_wordpress_blogs** (`tools\audit_wordpress_blogs.py`)
  - Lines: 686, Functions: 10, Classes: 2
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (2) indicate modular architecture

- **auto_assign_next_round** (`tools\auto_assign_next_round.py`)
  - Lines: 248, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **auto_fix_missing_imports** (`tools\auto_fix_missing_imports.py`)
  - Lines: 261, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **auto_inbox_processor** (`tools\auto_inbox_processor.py`)
  - Lines: 328, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **auto_learn_preferences** (`tools\auto_learn_preferences.py`)
  - Lines: 382, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **auto_remediate_loc** (`tools\auto_remediate_loc.py`)
  - Lines: 292, Functions: 11, Classes: 0
  - Rationale: Multiple functions (11) indicate business logic; Contains complex control flow structures

- **auto_status_updater** (`tools\auto_status_updater.py`)
  - Lines: 304, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **auto_validate_cycle_v2** (`tools\auto_validate_cycle_v2.py`)
  - Lines: 164, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **auto_workspace_cleanup** (`tools\auto_workspace_cleanup.py`)
  - Lines: 246, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **task_models** (`tools\autonomous\task_models.py`)
  - Lines: 69, Functions: 0, Classes: 3
  - Rationale: Contains classes (3) indicate modular architecture

- **autonomous_leaderboard** (`tools\autonomous_leaderboard.py`)
  - Lines: 173, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **autonomous_task_engine** (`tools\autonomous_task_engine.py`)
  - Lines: 798, Functions: 24, Classes: 3
  - Rationale: Multiple functions (24) indicate business logic; Contains classes (3) indicate modular architecture

- **batch1_reanalysis_investigation** (`tools\batch1_reanalysis_investigation.py`)
  - Lines: 197, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **batch2_dependency_analyzer** (`tools\batch2_dependency_analyzer.py`)
  - Lines: 352, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **batch2_ssot_verifier** (`tools\batch2_ssot_verifier.py`)
  - Lines: 274, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **batch_sales_funnel_p0_execution** (`tools\batch_sales_funnel_p0_execution.py`)
  - Lines: 382, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **batch_seo_ux_improvements** (`tools\batch_seo_ux_improvements.py`)
  - Lines: 452, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **batch_wordpress_seo_ux_deploy** (`tools\batch_wordpress_seo_ux_deploy.py`)
  - Lines: 435, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **browser_pool_manager** (`tools\browser_pool_manager.py`)
  - Lines: 268, Functions: 12, Classes: 2
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (2) indicate modular architecture

- **captain_architectural_checker** (`tools\captain_architectural_checker.py`)
  - Lines: 208, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **captain_cycle_scheduler** (`tools\captain_cycle_scheduler.py`)
  - Lines: 130, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **captain_find_idle_agents** (`tools\captain_find_idle_agents.py`)
  - Lines: 169, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_gas_check** (`tools\captain_gas_check.py`)
  - Lines: 150, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_import_validator** (`tools\captain_import_validator.py`)
  - Lines: 166, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **captain_inbox_assistant** (`tools\captain_inbox_assistant.py`)
  - Lines: 389, Functions: 14, Classes: 1
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_inbox_helper** (`tools\captain_inbox_helper.py`)
  - Lines: 295, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_inbox_manager** (`tools\captain_inbox_manager.py`)
  - Lines: 219, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **captain_leaderboard_update** (`tools\captain_leaderboard_update.py`)
  - Lines: 122, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_loop_closer** (`tools\captain_loop_closer.py`)
  - Lines: 214, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_loop_detector** (`tools\captain_loop_detector.py`)
  - Lines: 275, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_message_processor** (`tools\captain_message_processor.py`)
  - Lines: 357, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_morning_briefing** (`tools\captain_morning_briefing.py`)
  - Lines: 208, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **captain_next_task_picker** (`tools\captain_next_task_picker.py`)
  - Lines: 86, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_pattern_optimizer** (`tools\captain_pattern_optimizer.py`)
  - Lines: 164, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_progress_dashboard** (`tools\captain_progress_dashboard.py`)
  - Lines: 245, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_roi_quick_calc** (`tools\captain_roi_quick_calc.py`)
  - Lines: 125, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_send_jet_fuel** (`tools\captain_send_jet_fuel.py`)
  - Lines: 258, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **captain_snapshot** (`tools\captain_snapshot.py`)
  - Lines: 112, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **captain_swarm_coordinator** (`tools\captain_swarm_coordinator.py`)
  - Lines: 333, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_swarm_response_generator** (`tools\captain_swarm_response_generator.py`)
  - Lines: 273, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_task_assigner** (`tools\captain_task_assigner.py`)
  - Lines: 242, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **captain_update_log** (`tools\captain_update_log.py`)
  - Lines: 60, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **capture_performance_baseline** (`tools\capture_performance_baseline.py`)
  - Lines: 76, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **cast_agent3_tools_ranking_votes** (`tools\cast_agent3_tools_ranking_votes.py`)
  - Lines: 161, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **cast_all_tools_ranking_votes** (`tools\cast_all_tools_ranking_votes.py`)
  - Lines: 163, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **chat_presence_cli** (`tools\chat_presence_cli.py`)
  - Lines: 188, Functions: 1, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Contains complex control flow structures

- **check_active_theme_and_deploy_css** (`tools\check_active_theme_and_deploy_css.py`)
  - Lines: 258, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_and_activate_hsq_theme** (`tools\check_and_activate_hsq_theme.py`)
  - Lines: 127, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_and_apply_hsq_baby_blue_theme** (`tools\check_and_apply_hsq_baby_blue_theme.py`)
  - Lines: 369, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **check_css_in_html_output** (`tools\check_css_in_html_output.py`)
  - Lines: 97, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **check_dashboard_page** (`tools\check_dashboard_page.py`)
  - Lines: 58, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_file_implementation_status** (`tools\check_file_implementation_status.py`)
  - Lines: 158, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **check_freerideinvestor_htaccess** (`tools\check_freerideinvestor_htaccess.py`)
  - Lines: 176, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_freerideinvestor_php_errors** (`tools\check_freerideinvestor_php_errors.py`)
  - Lines: 126, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_functionality_existence** (`tools\check_functionality_existence.py`)
  - Lines: 303, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **check_keyboard_lock_status** (`tools\check_keyboard_lock_status.py`)
  - Lines: 53, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_queue_status** (`tools\check_queue_status.py`)
  - Lines: 106, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_sensitive_files** (`tools\check_sensitive_files.py`)
  - Lines: 172, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **check_service_status** (`tools\check_service_status.py`)
  - Lines: 145, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **check_stuck_messages** (`tools\check_stuck_messages.py`)
  - Lines: 102, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_system_readiness** (`tools\check_system_readiness.py`)
  - Lines: 200, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **check_toolbelt_health** (`tools\check_toolbelt_health.py`)
  - Lines: 168, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **check_twitch_bot_live_status** (`tools\check_twitch_bot_live_status.py`)
  - Lines: 84, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_twitch_bot_status** (`tools\check_twitch_bot_status.py`)
  - Lines: 208, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **check_wordpress_deployment_readiness** (`tools\check_wordpress_deployment_readiness.py`)
  - Lines: 296, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **check_wp_admin_blockers** (`tools\check_wp_admin_blockers.py`)
  - Lines: 314, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **chunk_reports** (`tools\chunk_reports.py`)
  - Lines: 168, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **circular_import_detector** (`tools\circular_import_detector.py`)
  - Lines: 195, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **claim_and_fix_master_task** (`tools\claim_and_fix_master_task.py`)
  - Lines: 404, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **clarify_dadudekc_homepage_offer** (`tools\clarify_dadudekc_homepage_offer.py`)
  - Lines: 131, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **classify_all_tools_phase1** (`tools\classify_all_tools_phase1.py`)
  - Lines: 345, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **classify_all_tools_signal_noise** (`tools\classify_all_tools_signal_noise.py`)
  - Lines: 398, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **classify_tools** (`tools\classify_tools.py`)
  - Lines: 275, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **clean_agent1_inbox_patterns** (`tools\clean_agent1_inbox_patterns.py`)
  - Lines: 141, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **clean_agent1_workspace** (`tools\clean_agent1_workspace.py`)
  - Lines: 278, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **clean_agent1_workspace_simple** (`tools\clean_agent1_workspace_simple.py`)
  - Lines: 97, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **clean_agent2_workspace** (`tools\clean_agent2_workspace.py`)
  - Lines: 210, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **clean_agent6_workspace** (`tools\clean_agent6_workspace.py`)
  - Lines: 280, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **clean_dadudekc_wordpress_defaults** (`tools\clean_dadudekc_wordpress_defaults.py`)
  - Lines: 178, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **clean_message_queue** (`tools\clean_message_queue.py`)
  - Lines: 148, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **cleanup_obsolete_files** (`tools\cleanup\cleanup_obsolete_files.py`)
  - Lines: 120, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **cleanup_stub_files** (`tools\cleanup\cleanup_stub_files.py`)
  - Lines: 219, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **cleanup_dadudekc_site** (`tools\cleanup_dadudekc_site.py`)
  - Lines: 195, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **cleanup_documentation_refactored** (`tools\cleanup_documentation_refactored.py`)
  - Lines: 337, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **cleanup_obsolete_docs** (`tools\cleanup_obsolete_docs.py`)
  - Lines: 135, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **cleanup_old_merge_directories** (`tools\cleanup_old_merge_directories.py`)
  - Lines: 129, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **cleanup_repository_for_migration** (`tools\cleanup_repository_for_migration.py`)
  - Lines: 357, Functions: 10, Classes: 0
  - Rationale: Multiple functions (10) indicate business logic; Contains complex control flow structures

- **cleanup_root_comprehensive** (`tools\cleanup_root_comprehensive.py`)
  - Lines: 287, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **cleanup_root_documentation** (`tools\cleanup_root_documentation.py`)
  - Lines: 203, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **command_discovery** (`tools\cli\command_discovery.py`)
  - Lines: 274, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **registry** (`tools\cli\commands\registry.py`)
  - Lines: 4307, Functions: 0, Classes: 0
  - Rationale: Large file size indicates substantial business logic

- **unified_dispatcher** (`tools\cli\dispatchers\unified_dispatcher.py`)
  - Lines: 111, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **code_analysis_tool** (`tools\code_analysis_tool.py`)
  - Lines: 286, Functions: 20, Classes: 6
  - Rationale: Multiple functions (20) indicate business logic; Contains classes (6) indicate modular architecture

- **migrate_managers** (`tools\codemods\migrate_managers.py`)
  - Lines: 113, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **migrate_orchestrators** (`tools\codemods\migrate_orchestrators.py`)
  - Lines: 70, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **replace_prints_with_logger** (`tools\codemods\replace_prints_with_logger.py`)
  - Lines: 144, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **agent_status_validator** (`tools\communication\agent_status_validator.py`)
  - Lines: 340, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **coordination_pattern_validator** (`tools\communication\coordination_pattern_validator.py`)
  - Lines: 202, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **coordination_validator** (`tools\communication\coordination_validator.py`)
  - Lines: 239, Functions: 8, Classes: 2
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (2) indicate modular architecture

- **integration_validator** (`tools\communication\integration_validator.py`)
  - Lines: 211, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **message_validator** (`tools\communication\message_validator.py`)
  - Lines: 222, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **messaging_infrastructure_validator** (`tools\communication\messaging_infrastructure_validator.py`)
  - Lines: 208, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **multi_agent_validator** (`tools\communication\multi_agent_validator.py`)
  - Lines: 206, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_status_validator** (`tools\communication\swarm_status_validator.py`)
  - Lines: 207, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_communication_validator** (`tools\communication\unified_communication_validator.py`)
  - Lines: 138, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **compare_duplicate_files_finalization** (`tools\compare_duplicate_files_finalization.py`)
  - Lines: 182, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **compare_performance_metrics** (`tools\compare_performance_metrics.py`)
  - Lines: 106, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **complete_batch2_remaining_merges** (`tools\complete_batch2_remaining_merges.py`)
  - Lines: 244, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **complete_merge_into_main** (`tools\complete_merge_into_main.py`)
  - Lines: 217, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **compliance_dashboard** (`tools\compliance_dashboard.py`)
  - Lines: 131, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **compliance_history_tracker** (`tools\compliance_history_tracker.py`)
  - Lines: 200, Functions: 10, Classes: 5
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (5) indicate modular architecture

- **comprehensive_disk_cleanup** (`tools\comprehensive_disk_cleanup.py`)
  - Lines: 241, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **comprehensive_tool_analyzer** (`tools\comprehensive_tool_analyzer.py`)
  - Lines: 378, Functions: 14, Classes: 1
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (1) indicate modular architecture

- **comprehensive_v2_check** (`tools\comprehensive_v2_check.py`)
  - Lines: 162, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **comprehensive_website_audit** (`tools\comprehensive_website_audit.py`)
  - Lines: 328, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidate_activate_wordpress_theme_duplicates** (`tools\consolidate_activate_wordpress_theme_duplicates.py`)
  - Lines: 297, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch1_groups_5_6_13_14** (`tools\consolidate_batch1_groups_5_6_13_14.py`)
  - Lines: 236, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch1_groups_9_10_11_12** (`tools\consolidate_batch1_groups_9_10_11_12.py`)
  - Lines: 237, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch2_duplicates** (`tools\consolidate_batch2_duplicates.py`)
  - Lines: 276, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **consolidate_batch3_duplicates** (`tools\consolidate_batch3_duplicates.py`)
  - Lines: 236, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch4_duplicates** (`tools\consolidate_batch4_duplicates.py`)
  - Lines: 268, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch5_duplicates** (`tools\consolidate_batch5_duplicates.py`)
  - Lines: 235, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch6_duplicates** (`tools\consolidate_batch6_duplicates.py`)
  - Lines: 218, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_batch7_duplicates** (`tools\consolidate_batch7_duplicates.py`)
  - Lines: 240, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **consolidate_ci_workflows** (`tools\consolidate_ci_workflows.py`)
  - Lines: 180, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidate_cli_entry_points** (`tools\consolidate_cli_entry_points.py`)
  - Lines: 193, Functions: 4, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Multiple functions (4) indicate business logic

- **consolidate_duplicate_tools** (`tools\consolidate_duplicate_tools.py`)
  - Lines: 154, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **consolidate_messaging** (`tools\consolidation\consolidate_messaging.py`)
  - Lines: 125, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_consolidation** (`tools\consolidation\validate_consolidation.py`)
  - Lines: 241, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_analyzer** (`tools\consolidation_analyzer.py`)
  - Lines: 204, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_executor** (`tools\consolidation_executor.py`)
  - Lines: 375, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_progress_tracker** (`tools\consolidation_progress_tracker.py`)
  - Lines: 150, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_runner** (`tools\consolidation_runner.py`)
  - Lines: 236, Functions: 8, Classes: 2
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (2) indicate modular architecture

- **consolidation_strategy_reviewer** (`tools\consolidation_strategy_reviewer.py`)
  - Lines: 313, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_verifier** (`tools\consolidation_verifier.py`)
  - Lines: 214, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **coordinate_implementation_tasks** (`tools\coordinate_implementation_tasks.py`)
  - Lines: 383, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **discord_commands_test_helper** (`tools\coordination\discord_commands_test_helper.py`)
  - Lines: 184, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **discord_commands_tester** (`tools\coordination\discord_commands_tester.py`)
  - Lines: 388, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **discord_simple_test** (`tools\coordination\discord_simple_test.py`)
  - Lines: 148, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_queue_blocking** (`tools\coordination\test_queue_blocking.py`)
  - Lines: 212, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **coordination_metrics_dashboard** (`tools\coordination_metrics_dashboard.py`)
  - Lines: 163, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **changed_file_report** (`tools\coverage\changed_file_report.py`)
  - Lines: 106, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **mutation_gate** (`tools\coverage\mutation_gate.py`)
  - Lines: 168, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **coverage_analyzer** (`tools\coverage_analyzer.py`)
  - Lines: 279, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **create_batch1_prs** (`tools\create_batch1_prs.py`)
  - Lines: 204, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_batch2_prs** (`tools\create_batch2_prs.py`)
  - Lines: 190, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_content_blog_prs** (`tools\create_content_blog_prs.py`)
  - Lines: 180, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **create_content_blog_prs_direct** (`tools\create_content_blog_prs_direct.py`)
  - Lines: 211, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_cycle_planner_tasks** (`tools\create_cycle_planner_tasks.py`)
  - Lines: 226, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_dadudekc_contact_page** (`tools\create_dadudekc_contact_page.py`)
  - Lines: 158, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_dadudekc_initial_post** (`tools\create_dadudekc_initial_post.py`)
  - Lines: 172, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_dadudekc_thank_you_page** (`tools\create_dadudekc_thank_you_page.py`)
  - Lines: 142, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_pytest_assignments** (`tools\create_pytest_assignments.py`)
  - Lines: 219, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_trading_repo_branch** (`tools\create_trading_repo_branch.py`)
  - Lines: 278, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_trading_repo_pr** (`tools\create_trading_repo_pr.py`)
  - Lines: 137, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_unified_cli_framework** (`tools\create_unified_cli_framework.py`)
  - Lines: 474, Functions: 8, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Multiple functions (8) indicate business logic

- **create_vibe_coded_review_blog** (`tools\create_vibe_coded_review_blog.py`)
  - Lines: 152, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_weareswarm_theme** (`tools\create_weareswarm_theme.py`)
  - Lines: 245, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **create_wordpress_page** (`tools\create_wordpress_page.py`)
  - Lines: 181, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **create_wordpress_site_config** (`tools\create_wordpress_site_config.py`)
  - Lines: 177, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **cross_reference_analysis** (`tools\cross_reference_analysis.py`)
  - Lines: 318, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **cycle_1_backup_partial** (`tools\cycle_1_backup_partial.py`)
  - Lines: 208, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **cycle_1_dependency_progress** (`tools\cycle_1_dependency_progress.py`)
  - Lines: 246, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **cycle_v2_to_spreadsheet_integration** (`tools\cycle_v2_to_spreadsheet_integration.py`)
  - Lines: 391, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **debate_execution_tracker_hook** (`tools\debate_execution_tracker_hook.py`)
  - Lines: 350, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **debug_a2a_messaging** (`tools\debug_a2a_messaging.py`)
  - Lines: 71, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **debug_freerideinvestor_login** (`tools\debug_freerideinvestor_login.py`)
  - Lines: 207, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **debug_message_queue** (`tools\debug_message_queue.py`)
  - Lines: 486, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **debug_twitch_bot** (`tools\debug_twitch_bot.py`)
  - Lines: 278, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **debug_twitch_irc_connection** (`tools\debug_twitch_irc_connection.py`)
  - Lines: 160, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **debug_wordpress_deployer** (`tools\debug_wordpress_deployer.py`)
  - Lines: 276, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **delete_deprecated_tools** (`tools\delete_deprecated_tools.py`)
  - Lines: 103, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **delete_hello_world** (`tools\delete_hello_world.py`)
  - Lines: 68, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **delete_old_dream_os_post** (`tools\delete_old_dream_os_post.py`)
  - Lines: 119, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **delete_outdated_docs** (`tools\delete_outdated_docs.py`)
  - Lines: 98, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **deploy_astros_css_to_active_theme** (`tools\deploy_astros_css_to_active_theme.py`)
  - Lines: 166, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **deploy_css_to_wordpress_customizer** (`tools\deploy_css_to_wordpress_customizer.py`)
  - Lines: 360, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **deploy_css_via_wordpress_rest_api** (`tools\deploy_css_via_wordpress_rest_api.py`)
  - Lines: 327, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **deploy_freeride_menu_fix** (`tools\deploy_freeride_menu_fix.py`)
  - Lines: 157, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **deploy_hsq_site_content** (`tools\deploy_hsq_site_content.py`)
  - Lines: 479, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **deploy_sales_funnel_p0** (`tools\deploy_sales_funnel_p0.py`)
  - Lines: 245, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **deploy_sales_funnel_p0_to_wordpress** (`tools\deploy_sales_funnel_p0_to_wordpress.py`)
  - Lines: 233, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **deploy_theme_via_blogging_api** (`tools\deploy_theme_via_blogging_api.py`)
  - Lines: 272, Functions: 7, Classes: 2
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (2) indicate modular architecture

- **deploy_via_sftp** (`tools\deploy_via_sftp.py`)
  - Lines: 115, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **deploy_via_wordpress_rest_api** (`tools\deploy_via_wordpress_rest_api.py`)
  - Lines: 351, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **detect_duplicate_files** (`tools\detect_duplicate_files.py`)
  - Lines: 157, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **devlog_compressor** (`tools\devlog_compressor.py`)
  - Lines: 370, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **devlog_manager** (`tools\devlog_manager.py`)
  - Lines: 571, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **devlog_poster** (`tools\devlog_poster.py`)
  - Lines: 408, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **diagnose_freeride_status** (`tools\diagnose_freeride_status.py`)
  - Lines: 126, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **diagnose_github_cli_auth** (`tools\diagnose_github_cli_auth.py`)
  - Lines: 370, Functions: 7, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Multiple functions (7) indicate business logic

- **diagnose_message_queue** (`tools\diagnose_message_queue.py`)
  - Lines: 242, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **diagnose_message_queue_flow** (`tools\diagnose_message_queue_flow.py`)
  - Lines: 170, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **diagnose_messaging_delivery** (`tools\diagnose_messaging_delivery.py`)
  - Lines: 292, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **direct_fix_swarm_post** (`tools\direct_fix_swarm_post.py`)
  - Lines: 212, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **discord_mermaid_renderer** (`tools\discord_mermaid_renderer.py`)
  - Lines: 264, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **discord_startup_listener** (`tools\discord_startup_listener.py`)
  - Lines: 305, Functions: 7, Classes: 2
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (2) indicate modular architecture

- **discover_all_sftp_credentials** (`tools\discover_all_sftp_credentials.py`)
  - Lines: 217, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **discover_ftp_credentials** (`tools\discover_ftp_credentials.py`)
  - Lines: 216, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **disk_space_cleanup** (`tools\disk_space_cleanup.py`)
  - Lines: 233, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **disk_space_optimization** (`tools\disk_space_optimization.py`)
  - Lines: 230, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **document_ssot_registry** (`tools\document_ssot_registry.py`)
  - Lines: 162, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **documentation_assistant** (`tools\documentation_assistant.py`)
  - Lines: 282, Functions: 14, Classes: 1
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (1) indicate modular architecture

- **dtemp_repo_cache_manager** (`tools\dtemp_repo_cache_manager.py`)
  - Lines: 234, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **duplication_checker** (`tools\duplication_checker.py`)
  - Lines: 238, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **enable_freerideinvestor_debug** (`tools\enable_freerideinvestor_debug.py`)
  - Lines: 177, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **enhance_repo_merge_v2** (`tools\enhance_repo_merge_v2.py`)
  - Lines: 234, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **enhanced_duplicate_detector** (`tools\enhanced_duplicate_detector.py`)
  - Lines: 309, Functions: 10, Classes: 0
  - Rationale: Multiple functions (10) indicate business logic; Contains complex control flow structures

- **enhanced_integration_analyzer** (`tools\enhanced_integration_analyzer.py`)
  - Lines: 379, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **enhanced_unified_github** (`tools\enhanced_unified_github.py`)
  - Lines: 720, Functions: 16, Classes: 3
  - Rationale: Multiple functions (16) indicate business logic; Contains classes (3) indicate modular architecture

- **ensure_twitch_env** (`tools\ensure_twitch_env.py`)
  - Lines: 65, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **execute_batch1_groups_8_10_12** (`tools\execute_batch1_groups_8_10_12.py`)
  - Lines: 124, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **execute_batch2_dedupe_from_json** (`tools\execute_batch2_dedupe_from_json.py`)
  - Lines: 204, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **execute_captain_pattern** (`tools\execute_captain_pattern.py`)
  - Lines: 347, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **execute_case_variations_consolidation** (`tools\execute_case_variations_consolidation.py`)
  - Lines: 238, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **execute_consolidation_deprecations** (`tools\execute_consolidation_deprecations.py`)
  - Lines: 158, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **execute_dreamvault_cleanup** (`tools\execute_dreamvault_cleanup.py`)
  - Lines: 362, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **execute_duplicate_resolution** (`tools\execute_duplicate_resolution.py`)
  - Lines: 236, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **execute_file_deletion** (`tools\execute_file_deletion.py`)
  - Lines: 89, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **execute_phase1_file_deletion** (`tools\execute_phase1_file_deletion.py`)
  - Lines: 243, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **execute_streamertools_duplicate_resolution** (`tools\execute_streamertools_duplicate_resolution.py`)
  - Lines: 241, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **execute_tools_consolidation** (`tools\execute_tools_consolidation.py`)
  - Lines: 119, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **extension_test_runner** (`tools\extension_test_runner.py`)
  - Lines: 279, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **extract_ai_framework_logic** (`tools\extract_ai_framework_logic.py`)
  - Lines: 241, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **extract_all_75_repos** (`tools\extract_all_75_repos.py`)
  - Lines: 103, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **extract_autoblogger_patterns** (`tools\extract_autoblogger_patterns.py`)
  - Lines: 252, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **extract_git_commits** (`tools\extract_git_commits.py`)
  - Lines: 305, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **extract_integration_files** (`tools\extract_integration_files.py`)
  - Lines: 44, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **extract_portfolio_logic** (`tools\extract_portfolio_logic.py`)
  - Lines: 221, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **extraction_roadmap_generator** (`tools\extraction_roadmap_generator.py`)
  - Lines: 210, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **fetch_blog_post_structure** (`tools\fetch_blog_post_structure.py`)
  - Lines: 178, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **fetch_repo_names** (`tools\fetch_repo_names.py`)
  - Lines: 326, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **file_deletion_support** (`tools\file_deletion_support.py`)
  - Lines: 420, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **file_locking_optimizer** (`tools\file_locking_optimizer.py`)
  - Lines: 213, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **file_refactor_detector** (`tools\file_refactor_detector.py`)
  - Lines: 255, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **find_easy_deletions** (`tools\find_easy_deletions.py`)
  - Lines: 169, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **find_easy_documentation_deletions** (`tools\find_easy_documentation_deletions.py`)
  - Lines: 165, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **find_file_size_violations** (`tools\find_file_size_violations.py`)
  - Lines: 57, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **find_more_redundant_files** (`tools\find_more_redundant_files.py`)
  - Lines: 144, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **find_redundant_docs** (`tools\find_redundant_docs.py`)
  - Lines: 198, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **fix_agent2_toolbelt_tools** (`tools\fix_agent2_toolbelt_tools.py`)
  - Lines: 195, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **fix_blog_highlighted_sections** (`tools\fix_blog_highlighted_sections.py`)
  - Lines: 247, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **fix_broken_tools_imports** (`tools\fix_broken_tools_imports.py`)
  - Lines: 94, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_consolidated_imports** (`tools\fix_consolidated_imports.py`)
  - Lines: 242, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_crosbyultimateevents_blog_page** (`tools\fix_crosbyultimateevents_blog_page.py`)
  - Lines: 221, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_dadudekc_blog_post** (`tools\fix_dadudekc_blog_post.py`)
  - Lines: 414, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_dadudekc_copy_glitches** (`tools\fix_dadudekc_copy_glitches.py`)
  - Lines: 240, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_dadudekc_css_duplicate** (`tools\fix_dadudekc_css_duplicate.py`)
  - Lines: 153, Functions: 0, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture

- **fix_dadudekc_dreamos_learnmore_links** (`tools\fix_dadudekc_dreamos_learnmore_links.py`)
  - Lines: 156, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **fix_dadudekc_font_rendering** (`tools\fix_dadudekc_font_rendering.py`)
  - Lines: 306, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_freeride_crosby_menu_links** (`tools\fix_freeride_crosby_menu_links.py`)
  - Lines: 294, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **fix_freeride_redirect_loop** (`tools\fix_freeride_redirect_loop.py`)
  - Lines: 175, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_freerideinvestor_audit_issues** (`tools\fix_freerideinvestor_audit_issues.py`)
  - Lines: 262, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **fix_freerideinvestor_blog_page** (`tools\fix_freerideinvestor_blog_page.py`)
  - Lines: 227, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_freerideinvestor_footer_contact_link** (`tools\fix_freerideinvestor_footer_contact_link.py`)
  - Lines: 155, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_github_prs** (`tools\fix_github_prs.py`)
  - Lines: 232, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **fix_hsq_astros_css** (`tools\fix_hsq_astros_css.py`)
  - Lines: 307, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_hsq_astros_css_deployment** (`tools\fix_hsq_astros_css_deployment.py`)
  - Lines: 187, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_invalid_agent_workspaces** (`tools\fix_invalid_agent_workspaces.py`)
  - Lines: 167, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_message_queue** (`tools\fix_message_queue.py`)
  - Lines: 168, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_message_queue_processes** (`tools\fix_message_queue_processes.py`)
  - Lines: 137, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_real_import_errors** (`tools\fix_real_import_errors.py`)
  - Lines: 344, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_stuck_queue_messages** (`tools\fix_stuck_queue_messages.py`)
  - Lines: 84, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_swarm_post_sections** (`tools\fix_swarm_post_sections.py`)
  - Lines: 250, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **fix_theme_header_branding** (`tools\fix_theme_header_branding.py`)
  - Lines: 174, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_tradingrobotplug_all_pages** (`tools\fix_tradingrobotplug_all_pages.py`)
  - Lines: 394, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_tradingrobotplug_features_page** (`tools\fix_tradingrobotplug_features_page.py`)
  - Lines: 279, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_tradingrobotplug_products_page** (`tools\fix_tradingrobotplug_products_page.py`)
  - Lines: 247, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_twitch_config** (`tools\fix_twitch_config.py`)
  - Lines: 218, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **fix_weareswarm_github_link** (`tools\fix_weareswarm_github_link.py`)
  - Lines: 245, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **fix_weareswarm_theme_branding** (`tools\fix_weareswarm_theme_branding.py`)
  - Lines: 143, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_wpadmin_dashboard_redirect** (`tools\fix_wpadmin_dashboard_redirect.py`)
  - Lines: 176, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_wpadmin_redirect_loop** (`tools\fix_wpadmin_redirect_loop.py`)
  - Lines: 149, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **fix_src_imports** (`tools\fixes\fix_src_imports.py`)
  - Lines: 60, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **flush_wordpress_cache_rest_api** (`tools\flush_wordpress_cache_rest_api.py`)
  - Lines: 356, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **force_multiplier_monitor** (`tools\force_multiplier_monitor.py`)
  - Lines: 218, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **force_multiplier_progress_monitor** (`tools\force_multiplier_progress_monitor.py`)
  - Lines: 168, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **force_push_consolidations** (`tools\force_push_consolidations.py`)
  - Lines: 257, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **ftp_deployer** (`tools\ftp_deployer.py`)
  - Lines: 585, Functions: 11, Classes: 2
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (2) indicate modular architecture

- **functionality_comparison** (`tools\functionality_comparison.py`)
  - Lines: 98, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **functionality_reports** (`tools\functionality_reports.py`)
  - Lines: 28, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture

- **functionality_signature** (`tools\functionality_signature.py`)
  - Lines: 89, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **functionality_tests** (`tools\functionality_tests.py`)
  - Lines: 79, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **functionality_verification** (`tools\functionality_verification.py`)
  - Lines: 238, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **generate_22_file_list** (`tools\generate_22_file_list.py`)
  - Lines: 176, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **generate_agent7_repo_checklists** (`tools\generate_agent7_repo_checklists.py`)
  - Lines: 181, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **generate_blog_post** (`tools\generate_blog_post.py`)
  - Lines: 352, Functions: 19, Classes: 1
  - Rationale: Multiple functions (19) indicate business logic; Contains classes (1) indicate modular architecture

- **generate_chronological_blog** (`tools\generate_chronological_blog.py`)
  - Lines: 518, Functions: 24, Classes: 1
  - Rationale: Multiple functions (24) indicate business logic; Contains classes (1) indicate modular architecture

- **generate_cycle_accomplishments_report** (`tools\generate_cycle_accomplishments_report.py`)
  - Lines: 270, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **generate_master_task_log_tasks** (`tools\generate_master_task_log_tasks.py`)
  - Lines: 99, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **generate_monitoring_dashboard** (`tools\generate_monitoring_dashboard.py`)
  - Lines: 284, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **generate_tools_consolidation_prs** (`tools\generate_tools_consolidation_prs.py`)
  - Lines: 195, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **generate_utils_catalog_enhanced** (`tools\generate_utils_catalog_enhanced.py`)
  - Lines: 244, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **generate_weekly_progression_report** (`tools\generate_weekly_progression_report.py`)
  - Lines: 586, Functions: 15, Classes: 1
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (1) indicate modular architecture

- **get_repo_chronology** (`tools\get_repo_chronology.py`)
  - Lines: 398, Functions: 9, Classes: 0
  - Rationale: Multiple functions (9) indicate business logic; Contains complex control flow structures

- **get_swarm_time** (`tools\get_swarm_time.py`)
  - Lines: 87, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **git_based_merge_primary** (`tools\git_based_merge_primary.py`)
  - Lines: 328, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **git_commit_verifier** (`tools\git_commit_verifier.py`)
  - Lines: 151, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **git_work_verifier** (`tools\git_work_verifier.py`)
  - Lines: 318, Functions: 7, Classes: 4
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (4) indicate modular architecture

- **github_consolidation_recovery** (`tools\github_consolidation_recovery.py`)
  - Lines: 395, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **github_create_and_push_repo** (`tools\github_create_and_push_repo.py`)
  - Lines: 340, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **github_pr_debugger** (`tools\github_pr_debugger.py`)
  - Lines: 613, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **github_pusher_agent** (`tools\github_pusher_agent.py`)
  - Lines: 531, Functions: 12, Classes: 2
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (2) indicate modular architecture

- **github_repo_roi_calculator** (`tools\github_repo_roi_calculator.py`)
  - Lines: 283, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **goldmine_batch_preparer** (`tools\goldmine_batch_preparer.py`)
  - Lines: 121, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **goldmine_config_scanner** (`tools\goldmine_config_scanner.py`)
  - Lines: 162, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **hard_onboard_agents_6_7_8** (`tools\hard_onboard_agents_6_7_8.py`)
  - Lines: 131, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **heal_stalled_agents** (`tools\heal_stalled_agents.py`)
  - Lines: 227, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **hostinger_api_helper** (`tools\hostinger_api_helper.py`)
  - Lines: 460, Functions: 9, Classes: 2
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (2) indicate modular architecture

- **hostinger_wordpress_manager** (`tools\hostinger_wordpress_manager.py`)
  - Lines: 634, Functions: 21, Classes: 1
  - Rationale: Multiple functions (21) indicate business logic; Contains classes (1) indicate modular architecture

- **houstonsipqueen_theme_and_post** (`tools\houstonsipqueen_theme_and_post.py`)
  - Lines: 424, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **identify_consolidation_candidates** (`tools\identify_consolidation_candidates.py`)
  - Lines: 173, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **identify_unnecessary_files** (`tools\identify_unnecessary_files.py`)
  - Lines: 292, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **implement_dadudekc_positioning_unification** (`tools\implement_dadudekc_positioning_unification.py`)
  - Lines: 264, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **import_chain_validator** (`tools\import_chain_validator.py`)
  - Lines: 140, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **improve_hsq_seo** (`tools\improve_hsq_seo.py`)
  - Lines: 346, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **independent_architecture_review** (`tools\independent_architecture_review.py`)
  - Lines: 243, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **infrastructure_automation_suite** (`tools\infrastructure_automation_suite.py`)
  - Lines: 175, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **integrate_auto_learning** (`tools\integrate_auto_learning.py`)
  - Lines: 143, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **integration_test_coordinator** (`tools\integration_test_coordinator.py`)
  - Lines: 284, Functions: 8, Classes: 3
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (3) indicate modular architecture

- **integration_workflow_automation** (`tools\integration_workflow_automation.py`)
  - Lines: 147, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **investigate_freerideinvestor_500_error** (`tools\investigate_freerideinvestor_500_error.py`)
  - Lines: 409, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **investigate_runtime_errors** (`tools\investigate_runtime_errors.py`)
  - Lines: 247, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **irc_connection_diagnostics** (`tools\irc_connection_diagnostics.py`)
  - Lines: 126, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **list_github_repos** (`tools\list_github_repos.py`)
  - Lines: 83, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **manual_theme_activation** (`tools\manual_theme_activation.py`)
  - Lines: 138, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **map_dadudekc_smoke_session_cta** (`tools\map_dadudekc_smoke_session_cta.py`)
  - Lines: 249, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **markov_8agent_roi_optimizer** (`tools\markov_8agent_roi_optimizer.py`)
  - Lines: 369, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **markov_cycle_simulator** (`tools\markov_cycle_simulator.py`)
  - Lines: 367, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **markov_swarm_integration** (`tools\markov_swarm_integration.py`)
  - Lines: 478, Functions: 18, Classes: 1
  - Rationale: Multiple functions (18) indicate business logic; Contains classes (1) indicate modular architecture

- **markov_task_optimizer** (`tools\markov_task_optimizer.py`)
  - Lines: 454, Functions: 16, Classes: 3
  - Rationale: Multiple functions (16) indicate business logic; Contains classes (3) indicate modular architecture

- **master_import_fixer** (`tools\master_import_fixer.py`)
  - Lines: 310, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **master_task_log_to_cycle_planner** (`tools\master_task_log_to_cycle_planner.py`)
  - Lines: 237, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **mcp_tools_self_test** (`tools\mcp_tools_self_test.py`)
  - Lines: 217, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **measure_delegation_overhead** (`tools\measure_delegation_overhead.py`)
  - Lines: 130, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **memory_leak_scanner** (`tools\memory_leak_scanner.py`)
  - Lines: 166, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **merge_dreambank_pr1_via_git** (`tools\merge_dreambank_pr1_via_git.py`)
  - Lines: 257, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **merge_duplicate_file_functionality** (`tools\merge_duplicate_file_functionality.py`)
  - Lines: 191, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **merge_prs_via_api** (`tools\merge_prs_via_api.py`)
  - Lines: 290, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **message_compression_automation** (`tools\message_compression_automation.py`)
  - Lines: 273, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **message_delivery_verifier** (`tools\message_delivery_verifier.py`)
  - Lines: 361, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **meta_tag_completeness_checker** (`tools\meta_tag_completeness_checker.py`)
  - Lines: 260, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **metrics_dashboard_updater** (`tools\metrics_dashboard_updater.py`)
  - Lines: 279, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **mission_control** (`tools\mission_control.py`)
  - Lines: 419, Functions: 11, Classes: 2
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (2) indicate modular architecture

- **module_extractor** (`tools\module_extractor.py`)
  - Lines: 176, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **monitor_4agent_dependency_chain** (`tools\monitor_4agent_dependency_chain.py`)
  - Lines: 159, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **monitor_twitch_bot** (`tools\monitor_twitch_bot.py`)
  - Lines: 81, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **monitor_twitch_bot_status** (`tools\monitor_twitch_bot_status.py`)
  - Lines: 101, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **nightly_site_audit** (`tools\nightly_site_audit.py`)
  - Lines: 433, Functions: 14, Classes: 0
  - Rationale: Multiple functions (14) indicate business logic; Contains complex control flow structures

- **onboarding_architecture_reporter** (`tools\onboarding_architecture_reporter.py`)
  - Lines: 202, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **onboarding_test_runner** (`tools\onboarding_test_runner.py`)
  - Lines: 54, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **opportunity_scanners** (`tools\opportunity_scanners.py`)
  - Lines: 52, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic

- **organize_repo_consolidation_groups** (`tools\organize_repo_consolidation_groups.py`)
  - Lines: 238, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **phase1_signal_noise_classifier** (`tools\phase1_signal_noise_classifier.py`)
  - Lines: 501, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **phase2_agent_cellphone_dependency_analyzer** (`tools\phase2_agent_cellphone_dependency_analyzer.py`)
  - Lines: 215, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **phase2_goldmine_config_scanner** (`tools\phase2_goldmine_config_scanner.py`)
  - Lines: 409, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **pin_houstonsipqueen_post** (`tools\pin_houstonsipqueen_post.py`)
  - Lines: 201, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **pipeline_gas_scheduler** (`tools\pipeline_gas_scheduler.py`)
  - Lines: 275, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **populate_swarm_mission_logs** (`tools\populate_swarm_mission_logs.py`)
  - Lines: 203, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **populate_tasks_from_health_check** (`tools\populate_tasks_from_health_check.py`)
  - Lines: 190, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **post_agent2_devlog_2025-12-15** (`tools\post_agent2_devlog_2025-12-15.py`)
  - Lines: 84, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_agent3_devlog_session_cleanup** (`tools\post_agent3_devlog_session_cleanup.py`)
  - Lines: 138, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_agent5_seo_breakthrough_blog** (`tools\post_agent5_seo_breakthrough_blog.py`)
  - Lines: 309, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_completion_report_to_discord** (`tools\post_completion_report_to_discord.py`)
  - Lines: 139, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_cycle_accomplishments_dual** (`tools\post_cycle_accomplishments_dual.py`)
  - Lines: 433, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **post_cycle_report_to_discord** (`tools\post_cycle_report_to_discord.py`)
  - Lines: 231, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **post_dadudekc_family_business_blog** (`tools\post_dadudekc_family_business_blog.py`)
  - Lines: 275, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **post_dadudekc_football_team_blog** (`tools\post_dadudekc_football_team_blog.py`)
  - Lines: 191, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **post_devlog_to_discord** (`tools\post_devlog_to_discord.py`)
  - Lines: 87, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_dream_os_review** (`tools\post_dream_os_review.py`)
  - Lines: 100, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_dream_os_review_blog** (`tools\post_dream_os_review_blog.py`)
  - Lines: 127, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **post_session_cleanup_devlog** (`tools\post_session_cleanup_devlog.py`)
  - Lines: 164, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **prepare_integration_testing** (`tools\prepare_integration_testing.py`)
  - Lines: 237, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **prioritize_duplicate_groups** (`tools\prioritize_duplicate_groups.py`)
  - Lines: 324, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **prioritize_test_coverage** (`tools\prioritize_test_coverage.py`)
  - Lines: 220, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **process_agent8_workspace_messages** (`tools\process_agent8_workspace_messages.py`)
  - Lines: 221, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **process_captain_inbox_complete** (`tools\process_captain_inbox_complete.py`)
  - Lines: 143, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **progress_auto_tracker** (`tools\progress_auto_tracker.py`)
  - Lines: 215, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **project_metrics_to_spreadsheet** (`tools\project_metrics_to_spreadsheet.py`)
  - Lines: 628, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **project_scan** (`tools\project_scan.py`)
  - Lines: 202, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **projectscanner_modular_reports** (`tools\projectscanner_modular_reports.py`)
  - Lines: 438, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **publish_all_unprocessed_blogs** (`tools\publish_all_unprocessed_blogs.py`)
  - Lines: 133, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **push_to_new_github_account** (`tools\push_to_new_github_account.py`)
  - Lines: 116, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **pytest_quick_report** (`tools\pytest_quick_report.py`)
  - Lines: 142, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **qa_validation_checklist** (`tools\qa_validation_checklist.py`)
  - Lines: 172, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **quarantine_manager** (`tools\quarantine_manager.py`)
  - Lines: 236, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **quick_linecount** (`tools\quick_linecount.py`)
  - Lines: 150, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **quick_metrics** (`tools\quick_metrics.py`)
  - Lines: 211, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **real_violation_scanner** (`tools\real_violation_scanner.py`)
  - Lines: 144, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **reduce_delegation_overhead** (`tools\reduce_delegation_overhead.py`)
  - Lines: 167, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **refactoring_ast_analyzer** (`tools\refactoring_ast_analyzer.py`)
  - Lines: 13, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **refactoring_cli** (`tools\refactoring_cli.py`)
  - Lines: 140, Functions: 2, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Contains complex control flow structures

- **refactoring_models** (`tools\refactoring_models.py`)
  - Lines: 36, Functions: 0, Classes: 3
  - Rationale: Contains classes (3) indicate modular architecture

- **refactoring_suggestion_engine** (`tools\refactoring_suggestion_engine.py`)
  - Lines: 338, Functions: 13, Classes: 2
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (2) indicate modular architecture

- **refresh_cache** (`tools\refresh_cache.py`)
  - Lines: 228, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **remove_dadudekc_developer_tools_menu** (`tools\remove_dadudekc_developer_tools_menu.py`)
  - Lines: 172, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **repo_analysis_enforcer** (`tools\repo_analysis_enforcer.py`)
  - Lines: 245, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **repo_consolidation_continuation** (`tools\repo_consolidation_continuation.py`)
  - Lines: 344, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **repo_safe_merge** (`tools\repo_safe_merge.py`)
  - Lines: 1434, Functions: 19, Classes: 1
  - Rationale: Multiple functions (19) indicate business logic; Contains classes (1) indicate modular architecture

- **repo_safe_merge_v2** (`tools\repo_safe_merge_v2.py`)
  - Lines: 488, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **repo_status_tracker** (`tools\repo_status_tracker.py`)
  - Lines: 313, Functions: 15, Classes: 2
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (2) indicate modular architecture

- **report_truthfulness_enhancer** (`tools\report_truthfulness_enhancer.py`)
  - Lines: 422, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **repository_analyzer** (`tools\repository_analyzer.py`)
  - Lines: 289, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **repository_cleanup_for_migration** (`tools\repository_cleanup_for_migration.py`)
  - Lines: 318, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **reset_stuck_messages** (`tools\reset_stuck_messages.py`)
  - Lines: 124, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **resolve_dreamvault_duplicates** (`tools\resolve_dreamvault_duplicates.py`)
  - Lines: 291, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **resolve_dreamvault_pr3** (`tools\resolve_dreamvault_pr3.py`)
  - Lines: 175, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **resolve_master_list_duplicates** (`tools\resolve_master_list_duplicates.py`)
  - Lines: 206, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **resolve_merge_conflicts** (`tools\resolve_merge_conflicts.py`)
  - Lines: 327, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **resolve_pr_blockers** (`tools\resolve_pr_blockers.py`)
  - Lines: 181, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **resolve_pr_conflicts** (`tools\resolve_pr_conflicts.py`)
  - Lines: 358, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **restart_discord_bot_direct** (`tools\restart_discord_bot_direct.py`)
  - Lines: 90, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **review_64_files_duplicates** (`tools\review_64_files_duplicates.py`)
  - Lines: 311, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **review_and_delete_candidates** (`tools\review_and_delete_candidates.py`)
  - Lines: 232, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **review_consolidation_candidates** (`tools\review_consolidation_candidates.py`)
  - Lines: 105, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **review_dreamvault_integration** (`tools\review_dreamvault_integration.py`)
  - Lines: 354, Functions: 9, Classes: 0
  - Rationale: Multiple functions (9) indicate business logic; Contains complex control flow structures

- **review_temp_repos** (`tools\review_temp_repos.py`)
  - Lines: 239, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **robinhood_trading_report** (`tools\robinhood_trading_report.py`)
  - Lines: 561, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **run_bot_with_monitoring** (`tools\run_bot_with_monitoring.py`)
  - Lines: 128, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **run_integration_checks_agent7** (`tools\run_integration_checks_agent7.py`)
  - Lines: 165, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **run_publication** (`tools\run_publication.py`)
  - Lines: 256, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **run_stress_test_with_metrics** (`tools\run_stress_test_with_metrics.py`)
  - Lines: 183, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **run_unified_discord_bot_with_restart** (`tools\run_unified_discord_bot_with_restart.py`)
  - Lines: 127, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **run_weekly_dashboard_and_report** (`tools\run_weekly_dashboard_and_report.py`)
  - Lines: 214, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **schedule_daily_reports** (`tools\schedule_daily_reports.py`)
  - Lines: 200, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **schedule_dashboard_updates** (`tools\schedule_dashboard_updates.py`)
  - Lines: 102, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **schedule_strategy_blog** (`tools\schedule_strategy_blog.py`)
  - Lines: 79, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **schema_org_validator** (`tools\schema_org_validator.py`)
  - Lines: 289, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **send_inbox_audit_message** (`tools\send_inbox_audit_message.py`)
  - Lines: 238, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **send_jet_fuel_direct** (`tools\send_jet_fuel_direct.py`)
  - Lines: 135, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **send_message_to_agent** (`tools\send_message_to_agent.py`)
  - Lines: 89, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **send_resume_directives_all_agents** (`tools\send_resume_directives_all_agents.py`)
  - Lines: 153, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **seo_meta_tag_extractor** (`tools\seo_meta_tag_extractor.py`)
  - Lines: 222, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **service_migration_helper** (`tools\service_migration_helper.py`)
  - Lines: 276, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **session_cleanup_automation** (`tools\session_cleanup_automation.py`)
  - Lines: 302, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **session_cleanup_automation_agent3** (`tools\session_cleanup_automation_agent3.py`)
  - Lines: 275, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **session_cleanup_complete** (`tools\session_cleanup_complete.py`)
  - Lines: 108, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **session_cleanup_helper** (`tools\session_cleanup_helper.py`)
  - Lines: 254, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **session_cleanup_shortcut** (`tools\session_cleanup_shortcut.py`)
  - Lines: 65, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **session_quick_checkin** (`tools\session_quick_checkin.py`)
  - Lines: 66, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **session_transition_automator** (`tools\session_transition_automator.py`)
  - Lines: 495, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **session_transition_helper** (`tools\session_transition_helper.py`)
  - Lines: 299, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **setup_freerideinvestor_redirects** (`tools\setup_freerideinvestor_redirects.py`)
  - Lines: 244, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **setup_github_keys** (`tools\setup_github_keys.py`)
  - Lines: 437, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **setup_hsq_autoblogger** (`tools\setup_hsq_autoblogger.py`)
  - Lines: 429, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **setup_websites_repo** (`tools\setup_websites_repo.py`)
  - Lines: 226, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **setup_windows_startup** (`tools\setup_windows_startup.py`)
  - Lines: 152, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **share_mission_to_swarm_brain** (`tools\share_mission_to_swarm_brain.py`)
  - Lines: 244, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **site_audit_automation** (`tools\site_audit_automation.py`)
  - Lines: 324, Functions: 15, Classes: 1
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (1) indicate modular architecture

- **sites_registry** (`tools\sites_registry.py`)
  - Lines: 225, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **soft_onboard_cli** (`tools\soft_onboard_cli.py`)
  - Lines: 241, Functions: 2, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Contains complex control flow structures

- **source_analyzer** (`tools\source_analyzer.py`)
  - Lines: 224, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **spreadsheet_github_adapter** (`tools\spreadsheet_github_adapter.py`)
  - Lines: 402, Functions: 9, Classes: 2
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (2) indicate modular architecture

- **ssot_batch2_tagger** (`tools\ssot_batch2_tagger.py`)
  - Lines: 213, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **ssot_config_validator** (`tools\ssot_config_validator.py`)
  - Lines: 316, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **ssot_tag_report** (`tools\ssot_tag_report.py`)
  - Lines: 290, Functions: 7, Classes: 2
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (2) indicate modular architecture

- **ssot_validator** (`tools\ssot_validator.py`)
  - Lines: 144, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **stage1_duplicate_resolution_config** (`tools\stage1_duplicate_resolution_config.py`)
  - Lines: 292, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **stage1_duplicate_resolution_interfaces** (`tools\stage1_duplicate_resolution_interfaces.py`)
  - Lines: 283, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **stage1_duplicate_resolution_models** (`tools\stage1_duplicate_resolution_models.py`)
  - Lines: 290, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **stage1_duplicate_resolution_utilities** (`tools\stage1_duplicate_resolution_utilities.py`)
  - Lines: 224, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **stage1_phase2_import_migration** (`tools\stage1_phase2_import_migration.py`)
  - Lines: 214, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **stage1_readiness_checker** (`tools\stage1_readiness_checker.py`)
  - Lines: 160, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **start_discord_system** (`tools\start_discord_system.py`)
  - Lines: 521, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **start_github_pusher_service** (`tools\start_github_pusher_service.py`)
  - Lines: 102, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **start_message_queue_processor** (`tools\start_message_queue_processor.py`)
  - Lines: 79, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **start_monitoring_system** (`tools\start_monitoring_system.py`)
  - Lines: 111, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **start_services_direct** (`tools\start_services_direct.py`)
  - Lines: 115, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **start_twitchbot_with_fixes** (`tools\start_twitchbot_with_fixes.py`)
  - Lines: 202, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **strategy_blog_automation** (`tools\strategy_blog_automation.py`)
  - Lines: 634, Functions: 11, Classes: 0
  - Rationale: Multiple functions (11) indicate business logic; Contains complex control flow structures

- **stress_test_messaging_queue** (`tools\stress_test_messaging_queue.py`)
  - Lines: 491, Functions: 9, Classes: 0
  - Rationale: Multiple functions (9) indicate business logic; Contains complex control flow structures

- **swarm_activity_feed_poster** (`tools\swarm_activity_feed_poster.py`)
  - Lines: 283, Functions: 9, Classes: 0
  - Rationale: Multiple functions (9) indicate business logic; Contains complex control flow structures

- **swarm_brain_cli** (`tools\swarm_brain_cli.py`)
  - Lines: 158, Functions: 4, Classes: 0
  - Rationale: Name matches NOISE pattern: cli; Multiple functions (4) indicate business logic

- **swarm_coordination_dashboard** (`tools\swarm_coordination_dashboard.py`)
  - Lines: 307, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_orchestrator** (`tools\swarm_orchestrator.py`)
  - Lines: 316, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_profile_manager** (`tools\swarm_profile_manager.py`)
  - Lines: 222, Functions: 14, Classes: 1
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_site_health_automation** (`tools\swarm_site_health_automation.py`)
  - Lines: 452, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_status_broadcaster** (`tools\swarm_status_broadcaster.py`)
  - Lines: 303, Functions: 8, Classes: 2
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (2) indicate modular architecture

- **swarm_system_inventory** (`tools\swarm_system_inventory.py`)
  - Lines: 511, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_website_auto_update** (`tools\swarm_website_auto_update.py`)
  - Lines: 99, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **switch_agent_mode** (`tools\switch_agent_mode.py`)
  - Lines: 116, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **sync_websites_repo** (`tools\sync_websites_repo.py`)
  - Lines: 384, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **task_verification_tool** (`tools\task_verification_tool.py`)
  - Lines: 250, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **tech_debt_ci_summary** (`tools\tech_debt_ci_summary.py`)
  - Lines: 289, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **technical_debt_analyzer** (`tools\technical_debt_analyzer.py`)
  - Lines: 343, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **template_customizer** (`tools\template_customizer.py`)
  - Lines: 297, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **template_structure_linter** (`tools\template_structure_linter.py`)
  - Lines: 207, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **test_all_agent_discord_channels** (`tools\test_all_agent_discord_channels.py`)
  - Lines: 161, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **test_batch2_web_routes** (`tools\test_batch2_web_routes.py`)
  - Lines: 204, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **test_batch2_web_routes_phase2_3** (`tools\test_batch2_web_routes_phase2_3.py`)
  - Lines: 769, Functions: 11, Classes: 0
  - Rationale: Multiple functions (11) indicate business logic; Contains complex control flow structures

- **test_blog_template** (`tools\test_blog_template.py`)
  - Lines: 89, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_blogging_api_connectivity** (`tools\test_blogging_api_connectivity.py`)
  - Lines: 239, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **test_ci_locally** (`tools\test_ci_locally.py`)
  - Lines: 148, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_consolidation_comprehensive** (`tools\test_consolidation_comprehensive.py`)
  - Lines: 244, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **test_discord_agent_routing** (`tools\test_discord_agent_routing.py`)
  - Lines: 103, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **test_discord_bot_debug** (`tools\test_discord_bot_debug.py`)
  - Lines: 136, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_dreambank_pr1_enhanced** (`tools\test_dreambank_pr1_enhanced.py`)
  - Lines: 146, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_new_tools** (`tools\test_new_tools.py`)
  - Lines: 144, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **test_phase2_activity_sources** (`tools\test_phase2_activity_sources.py`)
  - Lines: 70, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_pyramid_analyzer** (`tools\test_pyramid_analyzer.py`)
  - Lines: 176, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **test_remaining_plugins** (`tools\test_remaining_plugins.py`)
  - Lines: 180, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_resume_cycle_planner_integration** (`tools\test_resume_cycle_planner_integration.py`)
  - Lines: 135, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_runtime_errors** (`tools\test_runtime_errors.py`)
  - Lines: 102, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_twitch_auth_fix** (`tools\test_twitch_auth_fix.py`)
  - Lines: 137, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_twitch_bot_connection** (`tools\test_twitch_bot_connection.py`)
  - Lines: 322, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **test_twitch_connection_tdd** (`tools\test_twitch_connection_tdd.py`)
  - Lines: 200, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **test_twitch_irc_auth** (`tools\test_twitch_irc_auth.py`)
  - Lines: 128, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **test_usage_analyzer** (`tools\test_usage_analyzer.py`)
  - Lines: 155, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **test_vector_db_service** (`tools\test_vector_db_service.py`)
  - Lines: 178, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **analyze_chatgpt_selectors** (`tools\thea\analyze_chatgpt_selectors.py`)
  - Lines: 444, Functions: 12, Classes: 1
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (1) indicate modular architecture

- **debug_chatgpt_elements** (`tools\thea\debug_chatgpt_elements.py`)
  - Lines: 153, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **demo_thea_interactive** (`tools\thea\demo_thea_interactive.py`)
  - Lines: 169, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **demo_thea_live** (`tools\thea\demo_thea_live.py`)
  - Lines: 133, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **demo_working_thea** (`tools\thea\demo_working_thea.py`)
  - Lines: 77, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **run_headless_refresh** (`tools\thea\run_headless_refresh.py`)
  - Lines: 38, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **send_prompt_file** (`tools\thea\send_prompt_file.py`)
  - Lines: 128, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **setup_thea_cookies** (`tools\thea\setup_thea_cookies.py`)
  - Lines: 369, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **simple_thea_communication** (`tools\thea\simple_thea_communication.py`)
  - Lines: 363, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **tell_thea_session_summary** (`tools\thea\tell_thea_session_summary.py`)
  - Lines: 148, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **thea_authentication_handler** (`tools\thea\thea_authentication_handler.py`)
  - Lines: 187, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_automation** (`tools\thea\thea_automation.py`)
  - Lines: 483, Functions: 15, Classes: 2
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (2) indicate modular architecture

- **thea_automation_browser** (`tools\thea\thea_automation_browser.py`)
  - Lines: 196, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_automation_cookie_manager** (`tools\thea\thea_automation_cookie_manager.py`)
  - Lines: 168, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_automation_messaging** (`tools\thea\thea_automation_messaging.py`)
  - Lines: 171, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_cookie_manager** (`tools\thea\thea_cookie_manager.py`)
  - Lines: 143, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_headless_send** (`tools\thea\thea_headless_send.py`)
  - Lines: 123, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **thea_keepalive** (`tools\thea\thea_keepalive.py`)
  - Lines: 92, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **thea_login_detector** (`tools\thea\thea_login_detector.py`)
  - Lines: 180, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_login_handler** (`tools\thea\thea_login_handler.py`)
  - Lines: 819, Functions: 15, Classes: 2
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (2) indicate modular architecture

- **thea_login_handler_refactored** (`tools\thea\thea_login_handler_refactored.py`)
  - Lines: 67, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **thea_undetected_helper** (`tools\thea\thea_undetected_helper.py`)
  - Lines: 225, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **thea_code_review** (`tools\thea_code_review.py`)
  - Lines: 307, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **theme_deployment_manager** (`tools\theme_deployment_manager.py`)
  - Lines: 308, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **tighten_dadudekc_about_story** (`tools\tighten_dadudekc_about_story.py`)
  - Lines: 144, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **timeout_constant_replacer** (`tools\timeout_constant_replacer.py`)
  - Lines: 286, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **timeout_sweep_report** (`tools\timeout_sweep_report.py`)
  - Lines: 143, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **toolbelt** (`tools\toolbelt.py`)
  - Lines: 120, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **agent_executor** (`tools\toolbelt\executors\agent_executor.py`)
  - Lines: 65, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **compliance_executor** (`tools\toolbelt\executors\compliance_executor.py`)
  - Lines: 225, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **compliance_tracking_executor** (`tools\toolbelt\executors\compliance_tracking_executor.py`)
  - Lines: 101, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **consolidation_executor** (`tools\toolbelt\executors\consolidation_executor.py`)
  - Lines: 136, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **leaderboard_executor** (`tools\toolbelt\executors\leaderboard_executor.py`)
  - Lines: 101, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **messaging_executor** (`tools\toolbelt\executors\messaging_executor.py`)
  - Lines: 40, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **onboarding_executor** (`tools\toolbelt\executors\onboarding_executor.py`)
  - Lines: 115, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **refactor_executor** (`tools\toolbelt\executors\refactor_executor.py`)
  - Lines: 135, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **swarm_executor** (`tools\toolbelt\executors\swarm_executor.py`)
  - Lines: 92, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **v2_executor** (`tools\toolbelt\executors\v2_executor.py`)
  - Lines: 39, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **vector_executor** (`tools\toolbelt\executors\vector_executor.py`)
  - Lines: 61, Functions: 1, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **toolbelt_help** (`tools\toolbelt_help.py`)
  - Lines: 114, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **toolbelt_registry** (`tools\toolbelt_registry.py`)
  - Lines: 800, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **toolbelt_runner** (`tools\toolbelt_runner.py`)
  - Lines: 95, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **tools_consolidation_and_ranking_complete** (`tools\tools_consolidation_and_ranking_complete.py`)
  - Lines: 493, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **tools_consolidation_quick** (`tools\tools_consolidation_quick.py`)
  - Lines: 147, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **tools_ranking_debate** (`tools\tools_ranking_debate.py`)
  - Lines: 220, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **tracker_status_validator** (`tools\tracker_status_validator.py`)
  - Lines: 162, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **transfer_repos_to_new_github** (`tools\transfer_repos_to_new_github.py`)
  - Lines: 385, Functions: 9, Classes: 0
  - Rationale: Multiple functions (9) indicate business logic; Contains complex control flow structures

- **troop_config_dependency_scanner** (`tools\troop_config_dependency_scanner.py`)
  - Lines: 116, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **tsla_call_put_analyzer** (`tools\tsla_call_put_analyzer.py`)
  - Lines: 155, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **tsla_daily_plan_poster** (`tools\tsla_daily_plan_poster.py`)
  - Lines: 156, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **twitch_connection_diagnostics** (`tools\twitch_connection_diagnostics.py`)
  - Lines: 279, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **twitch_eventsub_subscription_manager** (`tools\twitch_eventsub_subscription_manager.py`)
  - Lines: 310, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **twitch_oauth_setup** (`tools\twitch_oauth_setup.py`)
  - Lines: 164, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **type_annotation_fixer** (`tools\type_annotation_fixer.py`)
  - Lines: 266, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_agent** (`tools\unified_agent.py`)
  - Lines: 360, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_analyzer** (`tools\unified_analyzer.py`)
  - Lines: 403, Functions: 13, Classes: 1
  - Rationale: Multiple functions (13) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_blogging_automation** (`tools\unified_blogging_automation.py`)
  - Lines: 487, Functions: 12, Classes: 4
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (4) indicate modular architecture

- **unified_captain** (`tools\unified_captain.py`)
  - Lines: 380, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_cleanup** (`tools\unified_cleanup.py`)
  - Lines: 335, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_discord** (`tools\unified_discord.py`)
  - Lines: 300, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_github** (`tools\unified_github.py`)
  - Lines: 318, Functions: 10, Classes: 1
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_github_pr_creator** (`tools\unified_github_pr_creator.py`)
  - Lines: 444, Functions: 10, Classes: 2
  - Rationale: Multiple functions (10) indicate business logic; Contains classes (2) indicate modular architecture

- **unified_monitor** (`tools\unified_monitor.py`)
  - Lines: 860, Functions: 12, Classes: 2
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (2) indicate modular architecture

- **unified_test_analysis** (`tools\unified_test_analysis.py`)
  - Lines: 217, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_test_coverage** (`tools\unified_test_coverage.py`)
  - Lines: 298, Functions: 14, Classes: 2
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (2) indicate modular architecture

- **unified_verifier** (`tools\unified_verifier.py`)
  - Lines: 390, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **unified_wordpress** (`tools\unified_wordpress.py`)
  - Lines: 334, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **unstick_agent3_assignment** (`tools\unstick_agent3_assignment.py`)
  - Lines: 140, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **update_all_sites_branding** (`tools\update_all_sites_branding.py`)
  - Lines: 288, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **update_aria_preferences** (`tools\update_aria_preferences.py`)
  - Lines: 204, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **update_blog_posts_with_fixed_links** (`tools\update_blog_posts_with_fixed_links.py`)
  - Lines: 159, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **update_crosby_contact_info** (`tools\update_crosby_contact_info.py`)
  - Lines: 158, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **update_freerideinvestor_menus** (`tools\update_freerideinvestor_menus.py`)
  - Lines: 117, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **update_freerideinvestor_premium_report** (`tools\update_freerideinvestor_premium_report.py`)
  - Lines: 267, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **update_ftp_credentials** (`tools\update_ftp_credentials.py`)
  - Lines: 179, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **update_github_repo_description** (`tools\update_github_repo_description.py`)
  - Lines: 278, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **update_master_consolidation_plan** (`tools\update_master_consolidation_plan.py`)
  - Lines: 178, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **update_master_list_from_analysis** (`tools\update_master_list_from_analysis.py`)
  - Lines: 123, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **update_swarm_brain** (`tools\update_swarm_brain.py`)
  - Lines: 264, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **upload_file_to_discord** (`tools\upload_file_to_discord.py`)
  - Lines: 118, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **v2_checker_formatters** (`tools\v2_checker_formatters.py`)
  - Lines: 192, Functions: 3, Classes: 2
  - Rationale: Contains classes (2) indicate modular architecture; Contains complex control flow structures

- **v2_compliance_checker** (`tools\v2_compliance_checker.py`)
  - Lines: 264, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **v2_compliance_dashboard_sync** (`tools\v2_compliance_dashboard_sync.py`)
  - Lines: 210, Functions: 7, Classes: 0
  - Rationale: Multiple functions (7) indicate business logic; Contains complex control flow structures

- **v2_compliance_summary** (`tools\v2_compliance_summary.py`)
  - Lines: 111, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **v2_function_size_checker** (`tools\v2_function_size_checker.py`)
  - Lines: 137, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_batch_consolidation** (`tools\validate_batch_consolidation.py`)
  - Lines: 236, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **validate_bilateral_coordination** (`tools\validate_bilateral_coordination.py`)
  - Lines: 124, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **validate_duplicate_analysis** (`tools\validate_duplicate_analysis.py`)
  - Lines: 136, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_file_locking_after_duplicate_removal** (`tools\validate_file_locking_after_duplicate_removal.py`)
  - Lines: 117, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_grade_cards** (`tools\validate_grade_cards.py`)
  - Lines: 188, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_import_fixes** (`tools\validate_import_fixes.py`)
  - Lines: 278, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **validate_readme** (`tools\validate_readme.py`)
  - Lines: 408, Functions: 12, Classes: 2
  - Rationale: Multiple functions (12) indicate business logic; Contains classes (2) indicate modular architecture

- **validate_resume_cycle_planner_integration** (`tools\validate_resume_cycle_planner_integration.py`)
  - Lines: 114, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_stall_detection_enhancement** (`tools\validate_stall_detection_enhancement.py`)
  - Lines: 83, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_stress_test_integration** (`tools\validate_stress_test_integration.py`)
  - Lines: 386, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **validate_swarm_snapshot_view** (`tools\validate_swarm_snapshot_view.py`)
  - Lines: 79, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **validate_trackers** (`tools\validate_trackers.py`)
  - Lines: 400, Functions: 9, Classes: 3
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (3) indicate modular architecture

- **verify_all_ci_workflows** (`tools\verify_all_ci_workflows.py`)
  - Lines: 312, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **verify_archived_repos** (`tools\verify_archived_repos.py`)
  - Lines: 328, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **verify_batch1_main_branches** (`tools\verify_batch1_main_branches.py`)
  - Lines: 162, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_batch1_main_content** (`tools\verify_batch1_main_content.py`)
  - Lines: 192, Functions: 6, Classes: 0
  - Rationale: Multiple functions (6) indicate business logic; Contains complex control flow structures

- **verify_batch1_merge_commits** (`tools\verify_batch1_merge_commits.py`)
  - Lines: 198, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **verify_batch2_prs** (`tools\verify_batch2_prs.py`)
  - Lines: 109, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **verify_batch2_ssot** (`tools\verify_batch2_ssot.py`)
  - Lines: 153, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_batch2_target_repos** (`tools\verify_batch2_target_repos.py`)
  - Lines: 178, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **verify_batch3_ssot** (`tools\verify_batch3_ssot.py`)
  - Lines: 96, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_batch4_ssot** (`tools\verify_batch4_ssot.py`)
  - Lines: 94, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_batch5_ssot** (`tools\verify_batch5_ssot.py`)
  - Lines: 92, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_batch_ssot** (`tools\verify_batch_ssot.py`)
  - Lines: 105, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_bulk_deletion_ssot** (`tools\verify_bulk_deletion_ssot.py`)
  - Lines: 237, Functions: 7, Classes: 1
  - Rationale: Multiple functions (7) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_contract_leads_merge** (`tools\verify_contract_leads_merge.py`)
  - Lines: 130, Functions: 2, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **verify_discord_buttons** (`tools\verify_discord_buttons.py`)
  - Lines: 229, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_dream_os_ci** (`tools\verify_dream_os_ci.py`)
  - Lines: 133, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_failed_merge_repos** (`tools\verify_failed_merge_repos.py`)
  - Lines: 294, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_file_comprehensive** (`tools\verify_file_comprehensive.py`)
  - Lines: 258, Functions: 4, Classes: 1
  - Rationale: Multiple functions (4) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_file_usage_batch** (`tools\verify_file_usage_batch.py`)
  - Lines: 311, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_file_usage_enhanced** (`tools\verify_file_usage_enhanced.py`)
  - Lines: 461, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_file_usage_enhanced_v2** (`tools\verify_file_usage_enhanced_v2.py`)
  - Lines: 397, Functions: 11, Classes: 1
  - Rationale: Multiple functions (11) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_hostinger_credentials** (`tools\verify_hostinger_credentials.py`)
  - Lines: 186, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_hsq_astros_css** (`tools\verify_hsq_astros_css.py`)
  - Lines: 193, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_import_errors** (`tools\verify_import_errors.py`)
  - Lines: 128, Functions: 2, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_master_list** (`tools\verify_master_list.py`)
  - Lines: 154, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_merges** (`tools\verify_merges.py`)
  - Lines: 331, Functions: 8, Classes: 0
  - Rationale: Multiple functions (8) indicate business logic; Contains complex control flow structures

- **verify_phase1_repos** (`tools\verify_phase1_repos.py`)
  - Lines: 246, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_remaining_branches** (`tools\verify_remaining_branches.py`)
  - Lines: 194, Functions: 3, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_ssot_tags_analytics** (`tools\verify_ssot_tags_analytics.py`)
  - Lines: 177, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_task** (`tools\verify_task.py`)
  - Lines: 234, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_toolbelt_after_archive** (`tools\verify_toolbelt_after_archive.py`)
  - Lines: 146, Functions: 4, Classes: 0
  - Rationale: Multiple functions (4) indicate business logic; Contains complex control flow structures

- **verify_tools_consolidation_execution** (`tools\verify_tools_consolidation_execution.py`)
  - Lines: 251, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **verify_v2_function_class_limits** (`tools\verify_v2_function_class_limits.py`)
  - Lines: 222, Functions: 9, Classes: 1
  - Rationale: Multiple functions (9) indicate business logic; Contains classes (1) indicate modular architecture

- **verify_website_fixes** (`tools\verify_website_fixes.py`)
  - Lines: 274, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **violation_consolidation_analyzer** (`tools\violation_consolidation_analyzer.py`)
  - Lines: 313, Functions: 15, Classes: 4
  - Rationale: Multiple functions (15) indicate business logic; Contains classes (4) indicate modular architecture

- **violation_domain_analyzer** (`tools\violation_domain_analyzer.py`)
  - Lines: 317, Functions: 8, Classes: 1
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (1) indicate modular architecture

- **vote_tools_ranking_debate** (`tools\vote_tools_ranking_debate.py`)
  - Lines: 158, Functions: 1, Classes: 0
  - Rationale: Contains complex control flow structures

- **web_domain_security_audit** (`tools\web_domain_security_audit.py`)
  - Lines: 252, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **website_manager** (`tools\website_manager.py`)
  - Lines: 563, Functions: 14, Classes: 1
  - Rationale: Multiple functions (14) indicate business logic; Contains classes (1) indicate modular architecture

- **wordpress_admin_deployer** (`tools\wordpress_admin_deployer.py`)
  - Lines: 389, Functions: 5, Classes: 1
  - Rationale: Multiple functions (5) indicate business logic; Contains classes (1) indicate modular architecture

- **wordpress_deployment_manager** (`tools\wordpress_deployment_manager.py`)
  - Lines: 62, Functions: 3, Classes: 1
  - Rationale: Contains classes (1) indicate modular architecture; Contains complex control flow structures

- **wordpress_manager** (`tools\wordpress_manager.py`)
  - Lines: 1440, Functions: 34, Classes: 2
  - Rationale: Multiple functions (34) indicate business logic; Contains classes (2) indicate modular architecture

- **work_attribution_tool** (`tools\work_attribution_tool.py`)
  - Lines: 316, Functions: 8, Classes: 2
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (2) indicate modular architecture

- **work_completion_verifier** (`tools\work_completion_verifier.py`)
  - Lines: 319, Functions: 6, Classes: 1
  - Rationale: Multiple functions (6) indicate business logic; Contains classes (1) indicate modular architecture

- **workspace_auto_cleaner** (`tools\workspace_auto_cleaner.py`)
  - Lines: 234, Functions: 5, Classes: 0
  - Rationale: Multiple functions (5) indicate business logic; Contains complex control flow structures

- **workspace_health_monitor** (`tools\workspace_health_monitor.py`)
  - Lines: 398, Functions: 8, Classes: 2
  - Rationale: Multiple functions (8) indicate business logic; Contains classes (2) indicate modular architecture


---

## ❌ NOISE Tools (26)

**Status**: Thin wrappers - Move to scripts/, deprecate, or remove

- **activate_hsq_theme_css** (`tools\activate_hsq_theme_css.py`)
  - Lines: 77, Functions: 0
  - Rationale: Small file that just imports and calls other tools

- **agent_fuel_monitor** (`tools\agent_fuel_monitor.py`)
  - Lines: 360, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **archive_source_repos** (`tools\archive_source_repos.py`)
  - Lines: 203, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **check_all_repos_needing_archive** (`tools\check_all_repos_needing_archive.py`)
  - Lines: 113, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **check_dadudekc_menu_structure** (`tools\check_dadudekc_menu_structure.py`)
  - Lines: 38, Functions: 0
  - Rationale: Small file that just imports and calls other tools

- **check_theme_syntax** (`tools\check_theme_syntax.py`)
  - Lines: 239, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **cleanup_superpowered_venv** (`tools\cleanup_superpowered_venv.py`)
  - Lines: 317, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **test_dispatcher** (`tools\cli\test_dispatcher.py`)
  - Lines: 71, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **discord_web_test_automation** (`tools\coordination\discord_web_test_automation.py`)
  - Lines: 366, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **create_ariajet_game_posts** (`tools\create_ariajet_game_posts.py`)
  - Lines: 153, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **create_case_variation_prs** (`tools\create_case_variation_prs.py`)
  - Lines: 163, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **create_merge1_pr** (`tools\create_merge1_pr.py`)
  - Lines: 117, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **create_work_session** (`tools\create_work_session.py`)
  - Lines: 289, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **deploy_via_wordpress_admin** (`tools\deploy_via_wordpress_admin.py`)
  - Lines: 331, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **fix_dadudekc_theme_syntax_error** (`tools\fix_dadudekc_theme_syntax_error.py`)
  - Lines: 85, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **post_4agent_mode_blog** (`tools\post_4agent_mode_blog.py`)
  - Lines: 94, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **post_swarm_introduction** (`tools\post_swarm_introduction.py`)
  - Lines: 92, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **post_swarm_philosophy_blog** (`tools\post_swarm_philosophy_blog.py`)
  - Lines: 95, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **post_swarm_site_health_breakthrough** (`tools\post_swarm_site_health_breakthrough.py`)
  - Lines: 90, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **run_test_suite_validation** (`tools\run_test_suite_validation.py`)
  - Lines: 180, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **test_discord_commands** (`tools\test_discord_commands.py`)
  - Lines: 364, Functions: 0
  - Rationale: Syntax error indicates broken/unmaintained code

- **test_ssot_preservation** (`tools\test_ssot_preservation.py`)
  - Lines: 61, Functions: 0
  - Rationale: Small file that just imports and calls other tools

- **tmp_cleanup_nav** (`tools\tmp_cleanup_nav.py`)
  - Lines: 68, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **tmp_menu_fix** (`tools\tmp_menu_fix.py`)
  - Lines: 62, Functions: 1
  - Rationale: Small file that just imports and calls other tools; Contains complex control flow structures

- **upload_fixed_dadudekc_functions** (`tools\upload_fixed_dadudekc_functions.py`)
  - Lines: 12, Functions: 0
  - Rationale: Small file that just imports and calls other tools

- **verify_dadudekc_fix_deployment** (`tools\verify_dadudekc_fix_deployment.py`)
  - Lines: 69, Functions: 0
  - Rationale: Small file that just imports and calls other tools


---

## ❓ UNKNOWN Tools (50)

**Status**: Needs manual review before classification

- **activate_wordpress_theme** (`tools\activate_wordpress_theme.py`)
  - Lines: 0, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **analyze_and_fix_dadudekc_duplicates** (`tools\analyze_and_fix_dadudekc_duplicates.py`)
  - Lines: 163, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **analyze_incomplete_loops** (`tools\analyze_incomplete_loops.py`)
  - Lines: 105, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_agent_coordination_opportunities** (`tools\check_agent_coordination_opportunities.py`)
  - Lines: 37, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_batches_2_8_status** (`tools\check_batches_2_8_status.py`)
  - Lines: 29, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_dadudekc_pages** (`tools\check_dadudekc_pages.py`)
  - Lines: 26, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_dadudekc_pages_list** (`tools\check_dadudekc_pages_list.py`)
  - Lines: 32, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_queue_issue** (`tools\check_queue_issue.py`)
  - Lines: 33, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **check_tsla_posts** (`tools\check_tsla_posts.py`)
  - Lines: 22, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **cleanup_broken_files** (`tools\cleanup_broken_files.py`)
  - Lines: 44, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **debug_queue** (`tools\debug_queue.py`)
  - Lines: 147, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **delete_easy_files** (`tools\delete_easy_files.py`)
  - Lines: 40, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **detect_comment_code_mismatches** (`tools\detect_comment_code_mismatches.py`)
  - Lines: 3, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **discord_bot_cleanup** (`tools\discord_bot_cleanup.py`)
  - Lines: 113, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **discord_bot_troubleshoot** (`tools\discord_bot_troubleshoot.py`)
  - Lines: 179, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **extract_freeride_error** (`tools\extract_freeride_error.py`)
  - Lines: 5, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **fix_dadudekc_font_direct_embed** (`tools\fix_dadudekc_font_direct_embed.py`)
  - Lines: 122, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **fix_dadudekc_functions_sftp** (`tools\fix_dadudekc_functions_sftp.py`)
  - Lines: 140, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **fix_dadudekc_functions_syntax** (`tools\fix_dadudekc_functions_syntax.py`)
  - Lines: 111, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **fix_duplicate_class** (`tools\fix_duplicate_class.py`)
  - Lines: 23, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **gas_messaging** (`tools\gas_messaging.py`)
  - Lines: 25, Functions: 1
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **generate_comprehensive_report** (`tools\generate_comprehensive_report.py`)
  - Lines: 224, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **get_dadudekc_page_content** (`tools\get_dadudekc_page_content.py`)
  - Lines: 37, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **identify_batch1_agent7_groups** (`tools\identify_batch1_agent7_groups.py`)
  - Lines: 32, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **identify_redundant_coordination_docs** (`tools\identify_redundant_coordination_docs.py`)
  - Lines: 57, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **remove_duplicate_content** (`tools\remove_duplicate_content.py`)
  - Lines: 25, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **restore_coords** (`tools\restore_coords.py`)
  - Lines: 22, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_a2a_template_update_ack** (`tools\send_a2a_template_update_ack.py`)
  - Lines: 75, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_audit_completion_status** (`tools\send_audit_completion_status.py`)
  - Lines: 71, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_blog_css_complete** (`tools\send_blog_css_complete.py`)
  - Lines: 56, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_business_plan_ack** (`tools\send_business_plan_ack.py`)
  - Lines: 77, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_discord_monitor_fix** (`tools\send_discord_monitor_fix.py`)
  - Lines: 53, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_jet_fuel_completion_report** (`tools\send_jet_fuel_completion_report.py`)
  - Lines: 92, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_jetfuel_agent4** (`tools\send_jetfuel_agent4.py`)
  - Lines: 48, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_monitor_fix_complete** (`tools\send_monitor_fix_complete.py`)
  - Lines: 57, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_status_acknowledgment** (`tools\send_status_acknowledgment.py`)
  - Lines: 74, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **send_truthfulness_complete** (`tools\send_truthfulness_complete.py`)
  - Lines: 54, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **status_monitor_recovery_trigger** (`tools\status_monitor_recovery_trigger.py`)
  - Lines: 189, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **stop_twitchbot** (`tools\stop_twitchbot.py`)
  - Lines: 39, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **task_creator** (`tools\task_creator.py`)
  - Lines: 25, Functions: 1
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **test_discord_gui_command** (`tools\test_discord_gui_command.py`)
  - Lines: 72, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **test_twitch_bot_clean_startup** (`tools\test_twitch_bot_clean_startup.py`)
  - Lines: 168, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **test_twitch_ping_pong** (`tools\test_twitch_ping_pong.py`)
  - Lines: 102, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **demo_thea_simple** (`tools\thea\demo_thea_simple.py`)
  - Lines: 57, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **update_swarm_brain_entry** (`tools\update_swarm_brain_entry.py`)
  - Lines: 74, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **update_swarm_brain_session_cleanup** (`tools\update_swarm_brain_session_cleanup.py`)
  - Lines: 72, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **validate_stall_detection** (`tools\validate_stall_detection.py`)
  - Lines: 72, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **verify_dadudekc_font_fix** (`tools\verify_dadudekc_font_fix.py`)
  - Lines: 59, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **verify_oauth_token_format** (`tools\verify_oauth_token_format.py`)
  - Lines: 84, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review

- **verify_remaining_batches** (`tools\verify_remaining_batches.py`)
  - Lines: 36, Functions: 0
  - Rationale: Does not match clear SIGNAL/NOISE patterns - needs manual review


---

## 📋 Next Steps (Phase -1 Actions)

1. **Review UNKNOWN Tools**: Manually classify tools that couldn't be auto-classified
2. **Move NOISE Tools**: Move NOISE tools to `scripts/` directory
3. **Update Toolbelt Registry**: Remove NOISE tools from toolbelt registry
4. **Update Refactoring Scope**: Filter all V2 refactoring phases to SIGNAL tools only
5. **Update Compliance Baseline**: Recalculate compliance percentages (remove NOISE from denominator)

---

## 🔗 References

- **V2 Compliance Refactoring Plan**: `docs/V2_COMPLIANCE_REFACTORING_PLAN.md`
- **Signal vs Noise Analysis**: `agent_workspaces/Agent-1/TOOLBELT_SIGNAL_VS_NOISE_ANALYSIS.md`
- **Classification Tool**: `tools/phase1_signal_noise_classifier.py`

---

*Generated by Phase -1 Signal vs Noise Classification Tool*
*Part of V2 Compliance Refactoring Plan - Phase -1*
