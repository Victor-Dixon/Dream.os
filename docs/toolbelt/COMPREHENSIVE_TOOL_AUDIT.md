# Comprehensive Tool Audit Report

**Total Assets Found:** 301

## 🛠️ Tool Classes
Found 170 tool classes in `tools/categories/`.

| Tool Class | Module | Category |
|------------|--------|----------|
| `AgentActivityTrackerTool` | `tools.categories.agent_activity_tools` | `agent_activity` |
| `AgentActivityMonitorTool` | `tools.categories.agent_activity_tools` | `agent_activity` |
| `AgentStatusTool` | `tools.categories.agent_ops_tools` | `agent_ops` |
| `ClaimTaskTool` | `tools.categories.agent_ops_tools` | `agent_ops` |
| `ProjectScanTool` | `tools.categories.analysis_tools` | `analysis` |
| `ComplexityTool` | `tools.categories.analysis_tools` | `analysis` |
| `DuplicationTool` | `tools.categories.analysis_tools` | `analysis` |
| `QuickMetricsTool` | `tools.categories.bi_tools` | `bi` |
| `RepoROICalculatorTool` | `tools.categories.bi_tools` | `bi` |
| `TaskROICalculatorTool` | `tools.categories.bi_tools` | `bi` |
| `MarkovROIOptimizerTool` | `tools.categories.bi_tools` | `bi` |
| `CompletionProcessorTool` | `tools.categories.captain_coordination_tools` | `captain_coordination` |
| `LeaderboardUpdaterTool` | `tools.categories.captain_coordination_tools` | `captain_coordination` |
| `NextTaskPickerTool` | `tools.categories.captain_coordination_tools` | `captain_coordination` |
| `ROIQuickCalculatorTool` | `tools.categories.captain_coordination_tools` | `captain_coordination` |
| `PointsCalculatorTool` | `tools.categories.captain_tools_advanced` | `captain_advanced` |
| `MissionAssignTool` | `tools.categories.captain_tools_advanced` | `captain_advanced` |
| `MarkovOptimizerTool` | `tools.categories.captain_tools_advanced` | `captain_advanced` |
| `ArchitecturalCheckerTool` | `tools.categories.captain_tools_architecture` | `captain_architecture` |
| `MorningBriefingTool` | `tools.categories.captain_tools_coordination` | `captain_coordination` |
| `StatusCheckTool` | `tools.categories.captain_tools_core` | `captain_core` |
| `GitVerifyTool` | `tools.categories.captain_tools_core` | `captain_core` |
| `WorkVerifyTool` | `tools.categories.captain_tools_core` | `captain_core` |
| `IntegrityCheckTool` | `tools.categories.captain_tools_core` | `captain_core` |
| `SelfMessageTool` | `tools.categories.captain_tools_messaging` | `captain_messaging` |
| `MessageAllAgentsTool` | `tools.categories.captain_tools_messaging` | `captain_messaging` |
| `GasDeliveryTool` | `tools.categories.captain_tools_monitoring` | `captain_monitoring` |
| `LeaderboardUpdateTool` | `tools.categories.captain_tools_monitoring` | `captain_monitoring` |
| `CycleReportTool` | `tools.categories.captain_tools_monitoring` | `captain_monitoring` |
| `FindIdleAgentsTool` | `tools.categories.captain_tools_utilities` | `captain_utilities` |
| `GasCheckTool` | `tools.categories.captain_tools_utilities` | `captain_utilities` |
| `UpdateLogTool` | `tools.categories.captain_tools_utilities` | `captain_utilities` |
| `ToolbeltHelpTool` | `tools.categories.captain_tools_utilities` | `captain_utilities` |
| `ComplianceHistoryTool` | `tools.categories.compliance_tools` | `compliance` |
| `PolicyCheckTool` | `tools.categories.compliance_tools` | `compliance` |
| `ValidateConfigSSOTAdapter` | `tools.categories.config_tools` | `config` |
| `ListConfigSourcesAdapter` | `tools.categories.config_tools` | `config` |
| `CheckConfigImportsAdapter` | `tools.categories.config_tools` | `config` |
| `FindDomainExpertAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `RequestExpertReviewAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `CheckCoordinationPatternsAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `SwarmOrchestratorAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `SwarmStatusBroadcasterAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `MissionControlAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `CoordinateValidatorAdapter` | `tools.categories.coordination_tools` | `coordination` |
| `DashboardGenerateTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DashboardDataAggregateTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DashboardHTMLTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DashboardChartsTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DashboardStylesTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DiscordStatusDashboardTool` | `tools.categories.dashboard_tools` | `dashboard` |
| `DebateStartTool` | `tools.categories.debate_tools` | `debate` |
| `DebateVoteTool` | `tools.categories.debate_tools` | `debate` |
| `DebateStatusTool` | `tools.categories.debate_tools` | `debate` |
| `DebateNotifyTool` | `tools.categories.debate_tools` | `debate` |
| `DiscordProfileViewerTool` | `tools.categories.discord_profile_tools` | `discord_profile` |
| `DiscordBotHealthTool` | `tools.categories.discord_tools` | `discord` |
| `DiscordBotStartTool` | `tools.categories.discord_tools` | `discord` |
| `DiscordTestMessageTool` | `tools.categories.discord_tools` | `discord` |
| `CreateWebhookTool` | `tools.categories.discord_webhook_tools` | `discord_webhook` |
| `ListWebhooksTool` | `tools.categories.discord_webhook_tools` | `discord_webhook` |
| `SaveWebhookTool` | `tools.categories.discord_webhook_tools` | `discord_webhook` |
| `TestWebhookTool` | `tools.categories.discord_webhook_tools` | `discord_webhook` |
| `WebhookManagerTool` | `tools.categories.discord_webhook_tools` | `discord_webhook` |
| `DocsSearchTool` | `tools.categories.docs_tools` | `docs` |
| `DocsExportTool` | `tools.categories.docs_tools` | `docs` |
| `GitHubRepoSimilarityAnalyzerTool` | `tools.categories.github_consolidation_tools` | `github_consolidation` |
| `GitHubRepoConsolidationPlannerTool` | `tools.categories.github_consolidation_tools` | `github_consolidation` |
| `GitHubRepoMergeExecutorTool` | `tools.categories.github_consolidation_tools` | `github_consolidation` |
| `HealthPingTool` | `tools.categories.health_tools` | `health` |
| `SnapshotTool` | `tools.categories.health_tools` | `health` |
| `ImportValidatorTool` | `tools.categories.import_fix_tools` | `import_fix` |
| `ModuleExtractorTool` | `tools.categories.import_fix_tools` | `import_fix` |
| `QuickLineCountTool` | `tools.categories.import_fix_tools` | `import_fix` |
| `PublicAPIImportValidatorTool` | `tools.categories.import_fix_tools` | `import_fix` |
| `ImportChainValidatorTool` | `tools.categories.import_fix_tools` | `import_fix` |
| `OrchestratorScanTool` | `tools.categories.infrastructure_audit_tools` | `infrastructure_audit` |
| `FileLineCounterTool` | `tools.categories.infrastructure_audit_tools` | `infrastructure_audit` |
| `ToolRuntimeAuditTool` | `tools.categories.infrastructure_audit_tools` | `infrastructure_audit` |
| `BrokenToolsAuditTool` | `tools.categories.infrastructure_audit_tools` | `infrastructure_audit` |
| `ProjectComponentsAuditTool` | `tools.categories.infrastructure_audit_tools` | `infrastructure_audit` |
| `ModuleExtractorPlannerTool` | `tools.categories.infrastructure_utility_tools` | `infrastructure_utility` |
| `InfrastructureROICalculatorTool` | `tools.categories.infrastructure_utility_tools` | `infrastructure_utility` |
| `BrowserPoolManagerTool` | `tools.categories.infrastructure_utility_tools` | `infrastructure_utility` |
| `WorkspaceHealthMonitorTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `WorkspaceAutoCleanerTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `AgentStatusQuickCheckTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `AutoStatusUpdaterTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `SessionTransitionAutomatorTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `SwarmStatusBroadcasterTool` | `tools.categories.infrastructure_workspace_tools` | `infrastructure_workspace` |
| `FindSSOTViolationsAdapter` | `tools.categories.integration_tools` | `integration` |
| `FindDuplicateFunctionalityAdapter` | `tools.categories.integration_tools` | `integration` |
| `FindIntegrationOpportunitiesAdapter` | `tools.categories.integration_tools` | `integration` |
| `CheckImportDependenciesAdapter` | `tools.categories.integration_tools` | `integration` |
| `AuditImportsTool` | `tools.categories.integration_tools` | `integration` |
| `MissionAdvisorTool` | `tools.categories.intelligent_mission_advisor_adapter` | `intelligent_mission_advisor_adapter` |
| `OrderValidatorTool` | `tools.categories.intelligent_mission_advisor_adapter` | `intelligent_mission_advisor_adapter` |
| `SwarmAnalyzerTool` | `tools.categories.intelligent_mission_advisor_adapter` | `intelligent_mission_advisor_adapter` |
| `RealtimeGuidanceTool` | `tools.categories.intelligent_mission_advisor_adapter` | `intelligent_mission_advisor_adapter` |
| `MemoryLeakDetectorTool` | `tools.categories.memory_safety_adapters` | `memory_safety_adapters` |
| `FileVerificationTool` | `tools.categories.memory_safety_adapters` | `memory_safety_adapters` |
| `UnboundedScanTool` | `tools.categories.memory_safety_adapters` | `memory_safety_adapters` |
| `MemorySafetyImportValidatorTool` | `tools.categories.memory_safety_adapters` | `memory_safety_adapters` |
| `FileHandleCheckTool` | `tools.categories.memory_safety_adapters` | `memory_safety_adapters` |
| `MessagePatternAnalyzerTool` | `tools.categories.message_analytics_tools` | `message_analytics` |
| `MessageMetricsDashboardTool` | `tools.categories.message_analytics_tools` | `message_analytics` |
| `MessageLearningExtractorTool` | `tools.categories.message_analytics_tools` | `message_analytics` |
| `MessageHistoryViewerTool` | `tools.categories.message_history_tools` | `message_history` |
| `MessageHistoryAnalyzerTool` | `tools.categories.message_history_tools` | `message_history` |
| `MessageCompressionTool` | `tools.categories.message_history_tools` | `message_history` |
| `MessageIngestTool` | `tools.categories.message_task_tools` | `message_task` |
| `TaskParserTool` | `tools.categories.message_task_tools` | `message_task` |
| `TaskFingerprintTool` | `tools.categories.message_task_tools` | `message_task` |
| `SendMessageTool` | `tools.categories.messaging_tools` | `messaging` |
| `BroadcastTool` | `tools.categories.messaging_tools` | `messaging` |
| `InboxCheckTool` | `tools.categories.messaging_tools` | `messaging` |
| `MetricsSnapshotTool` | `tools.categories.observability_tools` | `observability` |
| `MetricsTool` | `tools.categories.observability_tools` | `observability` |
| `SystemHealthTool` | `tools.categories.observability_tools` | `observability` |
| `SLOCheckTool` | `tools.categories.observability_tools` | `observability` |
| `SoftOnboardTool` | `tools.categories.onboarding_tools` | `onboarding` |
| `HardOnboardTool` | `tools.categories.onboarding_tools` | `onboarding` |
| `OSSCloneTool` | `tools.categories.oss_tools` | `oss` |
| `OSSFetchIssuesTool` | `tools.categories.oss_tools` | `oss` |
| `OSSImportIssuesTool` | `tools.categories.oss_tools` | `oss` |
| `OSSPortfolioTool` | `tools.categories.oss_tools` | `oss` |
| `OSSStatusTool` | `tools.categories.oss_tools` | `oss` |
| `CreateProposalTool` | `tools.categories.proposal_tools` | `proposal` |
| `ListProposalsTool` | `tools.categories.proposal_tools` | `proposal` |
| `ViewProposalTool` | `tools.categories.proposal_tools` | `proposal` |
| `ContributeProposalTool` | `tools.categories.proposal_tools` | `proposal` |
| `StartDebateTool` | `tools.categories.proposal_tools` | `proposal` |
| `QueueStatusMonitorTool` | `tools.categories.queue_monitor_tools` | `queue_monitor` |
| `FileSizeCheckTool` | `tools.categories.refactoring_tools` | `refactoring` |
| `AutoExtractTool` | `tools.categories.refactoring_tools` | `refactoring` |
| `TestPyramidAnalyzerTool` | `tools.categories.refactoring_tools` | `refactoring` |
| `LintFixTool` | `tools.categories.refactoring_tools` | `refactoring` |
| `SessionCleanupTool` | `tools.categories.session_tools` | `session` |
| `PassdownTool` | `tools.categories.session_tools` | `session` |
| `SessionPointsCalculatorTool` | `tools.categories.session_tools` | `session` |
| `TakeNoteTool` | `tools.categories.swarm_brain_tools` | `swarm_brain` |
| `ShareLearningTool` | `tools.categories.swarm_brain_tools` | `swarm_brain` |
| `SearchKnowledgeTool` | `tools.categories.swarm_brain_tools` | `swarm_brain` |
| `LogSessionTool` | `tools.categories.swarm_brain_tools` | `swarm_brain` |
| `GetAgentNotesTool` | `tools.categories.swarm_brain_tools` | `swarm_brain` |
| `SwarmPulseTool` | `tools.categories.swarm_consciousness` | `swarm_consciousness` |
| `SystemDateTimeTool` | `tools.categories.system_tools` | `system` |
| `CheckInSystemTool` | `tools.categories.system_tools` | `system` |
| `CheckInViewerTool` | `tools.categories.system_tools` | `system` |
| `TestFileGeneratorTool` | `tools.categories.test_generation_tools` | `test_generation` |
| `CoveragePyramidReportTool` | `tools.categories.test_generation_tools` | `test_generation` |
| `CoverageReportTool` | `tools.categories.testing_tools` | `testing` |
| `MutationGateTool` | `tools.categories.testing_tools` | `testing` |
| `V2CheckTool` | `tools.categories.v2_tools` | `v2` |
| `V2ReportTool` | `tools.categories.v2_tools` | `v2` |
| `SmokeTestTool` | `tools.categories.validation_tools` | `validation` |
| `FeatureFlagTool` | `tools.categories.validation_tools` | `validation` |
| `RollbackTool` | `tools.categories.validation_tools` | `validation` |
| `ValidationReportTool` | `tools.categories.validation_tools` | `validation` |
| `IntegrityValidatorTool` | `tools.categories.validation_tools` | `validation` |
| `SSOTValidatorTool` | `tools.categories.validation_tools` | `validation` |
| `TaskContextTool` | `tools.categories.vector_tools` | `vector` |
| `VectorSearchTool` | `tools.categories.vector_tools` | `vector` |
| `IndexWorkTool` | `tools.categories.vector_tools` | `vector` |
| `DiscordMermaidRendererTool` | `tools.categories.web_tools` | `web` |
| `DiscordWebTestTool` | `tools.categories.web_tools` | `web` |
| `InboxCleanupTool` | `tools.categories.workflow_tools` | `workflow` |
| `MissionClaimTool` | `tools.categories.workflow_tools` | `workflow` |
| `ROICalculatorTool` | `tools.categories.workflow_tools` | `workflow` |
| `DiscordPostTool` | `tools.categories.communication_tools` | `communication` |

## 📜 Standalone Scripts
Found 131 scripts with `main()` entry points.

- `scripts\activate_vector_database_integration.py`
- `scripts\add_ci_cd_to_github_repos.py`
- `scripts\agent_documentation_cli.py`
- `scripts\agent_fuel_monitor.py`
- `scripts\agent_onboarding.py`
- `scripts\archive_source_repos.py`
- `scripts\auto_assign_violations.py`
- `scripts\captain_add_knowledge_to_swarm_brain.py`
- `scripts\captain_update_log.py`
- `scripts\check_all_repos_needing_archive.py`
- `scripts\check_dashboard_page.py`
- `scripts\check_duplicate_accomplishments.py`
- `scripts\check_keyboard_lock_status.py`
- `scripts\check_push_status.py`
- `scripts\check_system_updates.py`
- `scripts\check_theme_syntax.py`
- `scripts\cleanup_superpowered_venv.py`
- `scripts\cleanup_v2_compliance.py`
- `scripts\code_comment_mismatch_detector.py`
- `scripts\create_ariajet_game_posts.py`
- `scripts\create_case_variation_prs.py`
- `scripts\create_merge1_pr.py`
- `scripts\create_work_session.py`
- `scripts\deploy_via_wordpress_admin.py`
- `scripts\enforce_python_standards.py`
- `scripts\execute_end_of_cycle_push.py`
- `scripts\extract_integration_files.py`
- `scripts\fix_and_ingest_vector_database.py`
- `scripts\fix_dadudekc_theme_syntax_error.py`
- `scripts\generate_state_of_project.py`
- `scripts\get_file_line_counts.py`
- `scripts\identify_infrastructure_files.py`
- `scripts\index_v2_refactoring.py`
- `scripts\init_daily_cycle.py`
- `scripts\list_discord_commands.py`
- `scripts\post_4agent_mode_blog.py`
- `scripts\post_agent2_update_to_discord.py`
- `scripts\post_agent4_update_to_discord.py`
- `scripts\post_agent7_update_to_discord.py`
- `scripts\post_agent8_update_to_discord.py`
- `scripts\post_swarm_introduction.py`
- `scripts\post_swarm_philosophy_blog.py`
- `scripts\post_swarm_site_health_breakthrough.py`
- `scripts\reset_stuck_messages.py`
- `scripts\run_canon_extraction.py`
- `scripts\run_test_suite_validation.py`
- `scripts\run_unified.py`
- `scripts\scan_core_domain_files.py`
- `scripts\scan_core_domain_quality.py`
- `scripts\setup_chat_mate.py`
- `scripts\setup_dream_os_dreamvault.py`
- `scripts\setup_enhanced_discord.py`
- `scripts\setup_gpt_automation.py`
- `scripts\start_queue_processor.py`
- `scripts\status_embedding_refresh.py`
- `scripts\task_cli.py`
- `scripts\terminal_completion_monitor.py`
- `scripts\test_activity_tracking.py`
- `scripts\test_compression_integration.py`
- `scripts\test_discord_commands.py`
- `scripts\test_end_to_end_message_flow.py`
- `scripts\test_enhanced_discord.py`
- `scripts\test_message_delivery.py`
- `scripts\test_message_logging_all_paths.py`
- `scripts\test_pyautogui_delivery_verbose.py`
- `scripts\test_queue_processing_delivery_logging.py`
- `scripts\tmp_cleanup_nav.py`
- `scripts\tmp_menu_fix.py`
- `scripts\v2_compliance_mcp_ci_checks.py`
- `scripts\v2_refactoring_tracker.py`
- `scripts\v2_release_summary.py`
- `scripts\validate_config_ssot.py`
- `scripts\validate_imports.py`
- `scripts\validate_refactored_files.py`
- `scripts\validate_v2_compliance.py`
- `scripts\validate_workspace_coords.py`
- `scripts\verify_agent8_ssot_files.py`
- `scripts\verify_message_logging.py`
- `tools\START_CHAT_BOT_NOW.py`
- `tools\add_mcp_to_cursor_settings.py`
- `tools\advisor_cli.py`
- `tools\agent_bump_script.py`
- `tools\audit_broken_tools_phase3.py`
- `tools\audit_toolbelt_comprehensive.py`
- `tools\calibrate_agent_coordinates.py`
- `tools\capture_agent_coordinates.py`
- `tools\check_audit_evidence.py`
- `tools\comprehensive_audit.py`
- `tools\configuration_sync_checker.py`
- `tools\deploy_tradingrobotplug_now.py`
- `tools\deploy_weareswarm_feed_system.py`
- `tools\deploy_weareswarm_font_fix.py`
- `tools\devlog_manager.py`
- `tools\devlog_poster_agent_channel.py`
- `tools\discord_health_monitor.py`
- `tools\execute_ssot_batch.py`
- `tools\find_missing_ssot_tags.py`
- `tools\fix_ssot_tag_syntax.py`
- `tools\generate_blog_preview.py`
- `tools\generate_cycle_accomplishments_report.py`
- `tools\manage_env.py`
- `tools\master_task_log_to_cycle_planner.py`
- `tools\multi_site_content_generator.py`
- `tools\post_cycle_report_to_blog.py`
- `tools\protocol_validator.py`
- `tools\setup_cursor_mcp.py`
- `tools\soft_onboard_cli.py`
- `tools\ssot_coordination_report.py`
- `tools\ssot_tagging_batch_assigner.py`
- `tools\ssot_tagging_distributor.py`
- `tools\ssot_tagging_validator.py`
- `tools\start_discord_bot.py`
- `tools\start_discord_system.py`
- `tools\swarm_to_wordpress_automation.py`
- `tools\sync_feed_to_weareswarm.py`
- `tools\system_health_dashboard.py`
- `tools\tag_analyzer.py`
- `tools\tag_web_domain_ssot.py`
- `tools\test_bi_tools.py`
- `tools\test_deployment_staging.py`
- `tools\test_mcp_server_connectivity.py`
- `tools\test_risk_websocket.py`
- `tools\test_toolbelt_basic.py`
- `tools\test_twitch_config.py`
- `tools\test_unified_tool_registry_mcp.py`
- `tools\unified_cycle_accomplishments_report.py`
- `tools\update_github_repo_description.py`
- `tools\validate_closure_format.py`
- `tools\verify_deployment_integration.py`
- `tools\verify_mcp_server_protocol.py`
- `tools\wordpress_manager.py`
