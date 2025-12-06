# 🚨 CODE VIOLATION SCAN REPORT

**Date**: 2025-12-04

**Focus**: Actual violations, not architectural patterns


## 📊 SUMMARY

**Total Violations Found**: 1415


- Duplicate Class Names: 218

- Duplicate Function Names: 1001

- Identical Code Blocks: 88

- SSOT Violations: 56

- Same Filename (Different Locations): 52


## 🚨 DUPLICATE CLASS NAMES


### `Task` (10 locations)

- `src\domain\entities\task.py:16`

- `src\gaming\dreamos\fsm_models.py:35`

- `src\gaming\dreamos\fsm_orchestrator.py:28`

- `src\infrastructure\persistence\persistence_models.py:46`

- `src\orchestrators\overnight\scheduler_models.py:19`

- `src\services\contract_system\models.py:44`

- `tools\autonomous_task_engine.py:23`

- `tools\markov_task_optimizer.py:19`

- `tools\autonomous\task_models.py:18`

- `tools_v2\categories\autonomous_workflow_tools.py:32`



### `SearchResult` (7 locations)

- `src\core\vector_database.py:39`

- `src\core\vector_database.py:215`

- `src\core\intelligent_context\context_results.py:24`

- `src\core\intelligent_context\search_models.py:21`

- `src\core\intelligent_context\unified_intelligent_context\models.py:48`

- `src\services\models\vector_models.py:104`

- `src\web\vector_database\models.py:75`



### `SearchQuery` (7 locations)

- `src\core\vector_database.py:196`

- `src\services\agent_management.py:46`

- `src\services\learning_recommender.py:34`

- `src\services\performance_analyzer.py:32`

- `src\services\recommendation_engine.py:32`

- `src\services\swarm_intelligence_manager.py:32`

- `src\services\models\vector_models.py:93`



### `Config` (5 locations)

- `src\ai_training\dreamvault\config.py:11`

- `src\message_task\schemas.py:28`

- `src\message_task\schemas.py:47`

- `src\message_task\schemas.py:75`

- `src\message_task\schemas.py:92`



### `IntegrationStatus` (5 locations)

- `src\architecture\system_integration.py:30`

- `src\gaming\gaming_integration_core.py:46`

- `src\gaming\integration\models.py:11`

- `src\gaming\models\gaming_models.py:16`

- `src\integrations\osrs\gaming_integration_core.py:49`



### `AgentStatus` (5 locations)

- `src\core\intelligent_context\context_enums.py:29`

- `src\core\intelligent_context\enums.py:26`

- `src\integrations\osrs\osrs_agent_core.py:41`

- `tools_v2\categories\autonomous_workflow_tools.py:291`

- `examples\quickstart_demo\dashboard_demo.py:11`



### `MetricType` (5 locations)

- `src\core\managers\monitoring\metric_manager.py:22`

- `src\core\managers\monitoring\monitoring_crud.py:31`

- `src\core\performance\coordination_performance_monitor.py:32`

- `src\core\performance\performance_collector.py:19`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\templates\template_models.py:22`



### `ConversationAnalyzer` (5 locations)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\analytics\analyze_conversations_ai.py:64`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\demos\training_data_extraction\conversation_analyzer.py:118`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\analytics\analyze_conversations_ai.py:64`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\intelligence\analysis\conversation_analyzer.py:19`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\conversation_system.py:49`



### `DocumentType` (4 locations)

- `src\core\vector_database.py:22`

- `src\core\vector_database.py:177`

- `src\services\work_indexer.py:35`

- `src\services\models\vector_models.py:27`



### `VectorDocument` (4 locations)

- `src\core\vector_database.py:49`

- `src\core\vector_database.py:168`

- `src\services\work_indexer.py:40`

- `src\services\models\vector_models.py:45`



### `RetryStrategy` (4 locations)

- `src\core\config\config_dataclasses.py:33`

- `src\core\error_handling\error_models_enums.py:74`

- `src\core\error_handling\recovery_strategies.py:123`

- `agent_workspaces\Agent-7\C-024_PRIORITY2_UNIFIED_CONFIGS.py:24`



### `ErrorContext` (4 locations)

- `src\core\error_handling\error_context_models.py:19`

- `src\core\error_handling\error_models_core.py:24`

- `src\core\error_handling\error_responses.py:24`

- `src\core\error_handling\error_response_models_core.py:24`



### `Agent` (4 locations)

- `src\domain\entities\agent.py:16`

- `src\infrastructure\persistence\persistence_models.py:27`

- `tools_v2\categories\autonomous_workflow_tools.py:47`

- `examples\quickstart_demo\workflow_demo.py:11`



### `GameType` (4 locations)

- `src\gaming\gaming_integration_core.py:55`

- `src\gaming\integration\models.py:19`

- `src\gaming\models\gaming_models.py:26`

- `src\integrations\osrs\gaming_integration_core.py:58`



### `GameSession` (4 locations)

- `src\gaming\gaming_integration_core.py:66`

- `src\gaming\integration\models.py:29`

- `src\gaming\models\gaming_models.py:40`

- `src\integrations\osrs\gaming_integration_core.py:69`



### `EntertainmentSystem` (4 locations)

- `src\gaming\gaming_integration_core.py:92`

- `src\gaming\integration\models.py:42`

- `src\gaming\models\gaming_models.py:53`

- `src\integrations\osrs\gaming_integration_core.py:95`



### `QuestType` (4 locations)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\mmorpg_models.py:11`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\mmorpg\models.py:20`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\mmorpg\models\mmorpg_models.py:45`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\conversation_system.py:141`



### `MockCog` (3 locations)

- `src\discord_commander\github_book_viewer.py:67`

- `src\discord_commander\messaging_commands.py:24`

- `src\discord_commander\controllers\messaging_controller_view.py:60`



### `MockCommands` (3 locations)

- `src\discord_commander\github_book_viewer.py:76`

- `src\discord_commander\messaging_commands.py:38`

- `src\discord_commander\controllers\messaging_controller_view.py:69`



### `MockExt` (3 locations)

- `src\discord_commander\github_book_viewer.py:81`

- `src\discord_commander\messaging_commands.py:44`

- `src\discord_commander\controllers\messaging_controller_view.py:74`



## 🔧 DUPLICATE FUNCTION NAMES


### `main` (401 locations)

⚠️ **2 identical implementations found**

- `hard_onboard_agent4.py:14` (251 lines)

- `onboard_survey_agents.py:63` (63 lines)

- `simple_agent_onboarding.py:198` (67 lines)

- `src\architecture\design_patterns.py:261` (15 lines)

- `src\architecture\system_integration.py:329` (11 lines)



### `execute` (228 locations)

- `src\ai_training\dreamvault\database.py:125` (24 lines)

- `src\application\use_cases\assign_task_uc.py:62` (79 lines)

- `src\application\use_cases\complete_task_uc.py:59` (68 lines)

- `src\core\engines\analysis_core_engine.py:26` (19 lines)

- `src\core\engines\communication_core_engine.py:26` (19 lines)



### `validate` (170 locations)

⚠️ **10 identical implementations found**

- `src\discord_commander\discord_models.py:81` (4 lines)

- `src\core\coordinator_models.py:191` (6 lines)

- `src\core\analytics\models\coordination_analytics_models.py:108` (9 lines)

- `src\core\config\config_manager.py:147` (19 lines)

- `src\core\engines\contracts.py:87` (0 lines)



### `get_spec` (161 locations)

- `tools_v2\categories\agent_ops_tools.py:25` (9 lines)

- `tools_v2\categories\agent_ops_tools.py:59` (9 lines)

- `tools_v2\categories\analysis_tools.py:24` (9 lines)

- `tools_v2\categories\analysis_tools.py:63` (9 lines)

- `tools_v2\categories\analysis_tools.py:103` (9 lines)



### `to_dict` (88 locations)

⚠️ **14 identical implementations found**

- `src\discord_commander\discord_models.py:99` (9 lines)

- `src\core\coordinator_models.py:84` (10 lines)

- `src\core\coordinator_models.py:109` (10 lines)

- `src\core\coordinator_models.py:139` (15 lines)

- `src\core\message_queue_interfaces.py:36` (0 lines)



### `get_status` (62 locations)

⚠️ **3 identical implementations found**

- `src\core\agent_documentation_service.py:275` (10 lines)

- `src\core\agent_lifecycle.py:304` (2 lines)

- `src\core\coordinator_interfaces.py:33` (0 lines)

- `src\core\analytics\coordinators\analytics_coordinator.py:85` (7 lines)

- `src\core\analytics\engines\batch_analytics_engine.py:102` (7 lines)



### `cleanup` (58 locations)

⚠️ **9 identical implementations found**

- `src\core\engines\analysis_core_engine.py:142` (10 lines)

- `src\core\engines\communication_core_engine.py:113` (10 lines)

- `src\core\engines\contracts.py:47` (0 lines)

- `src\core\engines\coordination_core_engine.py:132` (9 lines)

- `src\core\engines\data_core_engine.py:99` (10 lines)



### `initialize` (50 locations)

⚠️ **6 identical implementations found**

- `src\core\engines\analysis_core_engine.py:16` (8 lines)

- `src\core\engines\communication_core_engine.py:16` (8 lines)

- `src\core\engines\contracts.py:45` (0 lines)

- `src\core\engines\coordination_core_engine.py:39` (2 lines)

- `src\core\engines\data_core_engine.py:16` (8 lines)



### `get_name` (38 locations)

- `src\services\coordinator.py:27` (2 lines)

- `tools_v2\categories\discord_tools.py:26` (1 lines)

- `tools_v2\categories\discord_tools.py:67` (1 lines)

- `tools_v2\categories\discord_tools.py:101` (1 lines)

- `tools_v2\categories\discord_webhook_tools.py:36` (1 lines)



### `get_description` (37 locations)

- `tools_v2\categories\discord_tools.py:29` (1 lines)

- `tools_v2\categories\discord_tools.py:70` (1 lines)

- `tools_v2\categories\discord_tools.py:104` (1 lines)

- `tools_v2\categories\discord_webhook_tools.py:39` (1 lines)

- `tools_v2\categories\discord_webhook_tools.py:106` (1 lines)



### `get_logger` (31 locations)

⚠️ **1 identical implementations found**

- `src\core\unified_logging_system.py:81` (2 lines)

- `src\core\unified_logging_system.py:70` (4 lines)

- `src\core\performance\coordination_performance_monitor.py:75` (1 lines)

- `src\core\performance\coordination_performance_monitor.py:79` (2 lines)

- `src\core\utilities\standardized_logging.py:160` (15 lines)



### `generate_report` (29 locations)

- `src\core\vector_integration_analytics.py:68` (12 lines)

- `src\core\performance\performance_monitoring_system.py:153` (32 lines)

- `src\utils\config_consolidator.py:44` (1 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio\ai_analytics_component.py:281` (18 lines)

- `tools\audit_broken_tools.py:207` (88 lines)



### `get_github_token` (29 locations)

⚠️ **6 identical implementations found**

- `tools\github_create_and_push_repo.py:27` (18 lines)

- `tools\fetch_repo_names.py:26` (13 lines)

- `tools\repo_safe_merge.py:75` (19 lines)

- `tools\get_repo_chronology.py:30` (11 lines)

- `tools\verify_merges.py:95` (2 lines)



### `send_message` (23 locations)

⚠️ **1 identical implementations found**

- `src\core\messaging_core.py:408` (12 lines)

- `src\core\messaging_core.py:49` (2 lines)

- `src\core\messaging_core.py:114` (76 lines)

- `src\core\messaging_protocol_models.py:34` (10 lines)

- `src\core\messaging_pyautogui.py:187` (44 lines)



### `get` (20 locations)

- `src\ai_training\dreamvault\config.py:71` (11 lines)

- `src\core\coordinator_models.py:183` (2 lines)

- `src\core\metrics.py:38` (3 lines)

- `src\core\metrics.py:84` (3 lines)

- `src\core\analytics\engines\caching_engine_fixed.py:42` (15 lines)



### `get_summary` (20 locations)

⚠️ **1 identical implementations found**

- `src\core\analytics\models\coordination_analytics_models.py:62` (9 lines)

- `src\core\constants\fsm\configuration_models.py:53` (11 lines)

- `src\core\constants\fsm\state_models.py:45` (11 lines)

- `src\core\constants\fsm\transition_models.py:47` (10 lines)

- `src\core\error_handling\error_reporting_core.py:40` (11 lines)



### `from_dict` (19 locations)

- `src\core\message_queue_interfaces.py:39` (0 lines)

- `src\core\message_queue_persistence.py:409` (10 lines)

- `src\services\contract_system\models.py:76` (2 lines)

- `src\services\contract_system\models.py:129` (2 lines)

- `src\services\models\vector_models.py:56` (9 lines)



### `init_ui` (17 locations)

⚠️ **2 identical implementations found**

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\main_window_original_backup.py:220` (46 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\multi_model_panel.py:28` (13 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\voice_modeling_panel.py:104` (32 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio_panel.py:168` (29 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\consolidated_ai_studio_panel.py:70` (35 lines)



### `run` (16 locations)

⚠️ **2 identical implementations found**

- `src\core\orchestration\contracts.py:54` (2 lines)

- `src\orchestrators\overnight\listener.py:407` (10 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\analytics\analyze_conversations_ai.py:73` (51 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\voice_modeling_panel.py:58` (23 lines)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio_panel.py:63` (20 lines)



### `get_metrics` (15 locations)

- `src\core\analytics\intelligence\business_intelligence_engine_core.py:162` (2 lines)

- `src\core\file_locking\file_locking_manager.py:131` (2 lines)

- `src\core\file_locking\file_locking_engine.py:137` (2 lines)

- `src\core\intelligent_context\intelligent_context_engine.py:107` (2 lines)

- `src\core\managers\base_manager.py:177` (2 lines)



## 📝 IDENTICAL CODE BLOCKS


### Block Hash: `1b58ef4a` (6 occurrences)

- `tools\communication\message_validator.py:177`

- `tools\communication\coordination_validator.py:184`

- `tools\communication\multi_agent_validator.py:115`

**Preview**:
```python
if self.errors:
print("❌ VALIDATION ERRORS:")
for error in self.errors:
print(f"  • {error}")
if self.warnings:
print("⚠️  WARNINGS:")
for warning in self.warnings:
print(f"  • {warning}")
if not self
```


### Block Hash: `dd569d8d` (5 occurrences)

- `src\core\messaging_core.py:352`

- `src\services\messaging_infrastructure.py:1228`

- `tools\captain_check_agent_status.py:69`

**Preview**:
```python
agents = [
"Agent-1",
"Agent-2",
"Agent-3",
"Agent-4",
"Agent-5",
"Agent-6",
"Agent-7",
"Agent-8",
]
```


### Block Hash: `79a28ea5` (5 occurrences)

- `tools\resolve_merge_conflicts.py:45`

- `tools\complete_merge_into_main.py:39`

- `tools\review_dreamvault_integration.py:70`

**Preview**:
```python
if dir_path.exists():
print(f"🧹 Removing existing {name} directory: {dir_path}")
try:
shutil.rmtree(dir_path, ignore_errors=True)
time.sleep(0.5)
if dir_path.exists():
def remove_readonly(func, path, 
```


### Block Hash: `c183edd6` (4 occurrences)

- `src\core\messaging_core.py:114`

- `src\core\stress_testing\messaging_core_protocol.py:24`

- `src\core\stress_testing\mock_messaging_core.py:46`

**Preview**:
```python
def send_message(
self,
content: str,
sender: str,
recipient: str,
message_type: UnifiedMessageType,
priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
tags: list[UnifiedMessageTag] | 
```


### Block Hash: `294bd627` (4 occurrences)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_chat_navigation.py:217`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_direct_chat.py:158`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_final_chat.py:220`

**Preview**:
```python
response_elements = []
for selector in response_selectors:
try:
elements = orch.driver.find_elements("css selector", selector)
if elements:
response_elements = elements
print(f"✅ Found {len(elements)}
```


### Block Hash: `bd538728` (3 occurrences)

- `src\services\performance_analyzer.py:16`

- `src\services\recommendation_engine.py:16`

- `src\services\swarm_intelligence_manager.py:16`

**Preview**:
```python
try:
from .vector_database_service_unified import (
get_vector_database_service,
search_vector_database,
)
from .vector_database.vector_database_models import SearchQuery
VECTOR_DB_AVAILABLE = True
ex
```


### Block Hash: `935e54ad` (3 occurrences)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_chat_navigation.py:182`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_final_chat.py:185`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_working_chat.py:120`

**Preview**:
```python
print("🔍 Looking for any button that might be send...")
try:
all_buttons = orch.driver.find_elements("css selector", "button")
for button in all_buttons:
text = button.text.lower()
aria_label = (butto
```


### Block Hash: `7a8778c5` (3 occurrences)

- `tools\repo_safe_merge.py:83`

- `tools\git_based_merge_primary.py:34`

- `tools\repo_safe_merge_v2.py:49`

**Preview**:
```python
env_file = project_root / ".env"
if env_file.exists():
try:
with open(env_file, "r") as f:
for line in f:
line = line.strip()
if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
retur
```


### Block Hash: `7328062d` (3 occurrences)

- `tools\create_batch2_prs.py:58`

- `tools\create_merge1_pr.py:58`

- `tools\merge_prs_via_api.py:102`

**Preview**:
```python
url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
headers = {
"Authorization": f"token {token}",
"Accept": "application/vnd.github.v3+json",
"Content-Type": "application/json"
}
data = {
"tit
```


### Block Hash: `c7401dbf` (3 occurrences)

- `tools\create_batch2_prs.py:82`

- `tools\create_merge1_pr.py:83`

- `tools\merge_prs_via_api.py:126`

**Preview**:
```python
list_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
list_response = requests.get(
list_url,
headers=headers,
params={"head": f"{owner}:{head}", "state": "open"},
timeout=30
)
if list_respo
```


## 🔐 SSOT VIOLATIONS


### `timeout=30` (175 locations)

- `src\discord_commander\unified_discord_bot.py`

- `src\discord_commander\unified_discord_bot.py`

- `src\discord_commander\webhook_commands.py`

- `src\discord_commander\status_change_monitor.py`

- `src\ai_training\dreamvault\scrapers\login_handler.py`

- `src\core\local_repo_layer.py`

- `src\core\local_repo_layer.py`

- `src\core\local_repo_layer.py`

- `src\core\synthetic_github.py`

- `src\core\synthetic_github.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\opensource\github_integration.py`

- `src\services\messaging_cli_handlers.py`

- `src\services\messaging_infrastructure.py`

- `src\services\messaging_infrastructure.py`

- `src\services\soft_onboarding_service.py`

- `src\services\soft_onboarding_service.py`

- `src\tools\github_scanner.py`

- `src\tools\github_scanner.py`

- `src\tools\github_scanner.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\main_window_original_backup.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\refresh_chatgpt_cookies.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\content\enrich_conversation_data.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py`

- `tools\agent_fuel_monitor.py`

- `tools\mission_control.py`

- `tools\discord_mermaid_renderer.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\verify_merges.py`

- `tools\verify_merges.py`

- `tools\verify_merges.py`

- `tools\verify_merges.py`

- `tools\verify_merges.py`

- `tools\verify_merges.py`

- `tools\create_batch1_prs.py`

- `tools\create_batch1_prs.py`

- `tools\verify_batch1_main_branches.py`

- `tools\verify_batch1_main_branches.py`

- `tools\verify_batch1_main_branches.py`

- `tools\verify_batch1_merge_commits.py`

- `tools\verify_batch1_merge_commits.py`

- `tools\verify_batch2_target_repos.py`

- `tools\verify_batch2_target_repos.py`

- `tools\verify_batch1_main_content.py`

- `tools\verify_batch1_main_content.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\create_batch2_prs.py`

- `tools\create_batch2_prs.py`

- `tools\create_merge1_pr.py`

- `tools\create_merge1_pr.py`

- `tools\verify_batch2_prs.py`

- `tools\merge_prs_via_api.py`

- `tools\merge_prs_via_api.py`

- `tools\merge_prs_via_api.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\verify_contract_leads_merge.py`

- `tools\verify_contract_leads_merge.py`

- `tools\verify_contract_leads_merge.py`

- `tools\verify_contract_leads_merge.py`

- `tools\verify_contract_leads_merge.py`

- `tools\review_dreamvault_integration.py`

- `tools\review_dreamvault_integration.py`

- `tools\review_dreamvault_integration.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\unified_github_pr_creator.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\create_content_blog_prs_direct.py`

- `tools\create_content_blog_prs_direct.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\deploy_via_wordpress_rest_api.py`

- `tools\deploy_via_wordpress_rest_api.py`

- `tools\create_work_session.py`

- `tools\extract_git_commits.py`

- `tools\process_captain_inbox_complete.py`

- `tools\process_agent8_workspace_messages.py`

- `tools\create_ariajet_game_posts.py`

- `tools\coordination\test_queue_blocking.py`

- `tools_v2\categories\coordination_tools.py`

- `tools_v2\categories\discord_tools.py`

- `tools_v2\categories\github_consolidation_tools.py`

- `tools_v2\categories\captain_tools_messaging.py`

- `tools_v2\categories\captain_tools_messaging.py`

- `tools_v2\utils\discord_mermaid_renderer.py`

- `systems\output_flywheel\publication\github_publisher.py`

- `systems\technical_debt\auto_task_assigner.py`



### `timeout=10` (69 locations)

- `src\discord_commander\contract_notifications.py`

- `src\discord_commander\contract_notifications.py`

- `src\discord_commander\contract_notifications.py`

- `src\discord_commander\contract_notifications.py`

- `src\discord_commander\discord_service.py`

- `src\gaming\dreamos\fsm_monitoring.py`

- `src\orchestrators\overnight\monitor_discord_alerts.py`

- `src\orchestrators\overnight\monitor_discord_alerts.py`

- `src\orchestrators\overnight\monitor_discord_alerts.py`

- `src\services\portfolio_service.py`

- `src\services\chat_presence\chat_presence_orchestrator.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation\conversation_scraper.py`

- `tools\audit_broken_tools.py`

- `tools\devlog_manager.py`

- `tools\devlog_manager.py`

- `tools\mission_control.py`

- `tools\mission_control.py`

- `tools\swarm_status_broadcaster.py`

- `tools\discord_mermaid_renderer.py`

- `tools\discord_mermaid_renderer.py`

- `tools\discord_mermaid_renderer.py`

- `tools\discord_mermaid_renderer.py`

- `tools\fetch_repo_names.py`

- `tools\fetch_repo_names.py`

- `tools\get_repo_chronology.py`

- `tools\get_repo_chronology.py`

- `tools\test_all_agent_discord_channels.py`

- `tools\verify_merged_repo_cicd_enhanced.py`

- `tools\verify_merged_repo_cicd_enhanced.py`

- `tools\devlog_poster.py`

- `tools\devlog_poster.py`

- `tools\restart_discord_bot.py`

- `tools\github_consolidation_recovery.py`

- `tools\github_consolidation_recovery.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\hostinger_api_helper.py`

- `tools\hostinger_api_helper.py`

- `tools\hostinger_api_helper.py`

- `tools\hostinger_api_helper.py`

- `tools\hostinger_api_helper.py`

- `tools\verify_website_fixes.py`

- `tools\verify_website_fixes.py`

- `tools\verify_website_fixes.py`

- `tools\sftp_credential_troubleshooter.py`

- `tools\ftp_deployer.py`

- `tools\check_theme_syntax.py`

- `tools\discover_ftp_credentials.py`

- `tools\create_work_session.py`

- `tools\extract_git_commits.py`

- `tools\extract_git_commits.py`

- `tools\aria_active_response.py`

- `tools\verify_repo_merge_status.py`

- `tools\post_completion_report_to_discord.py`

- `tools\verify_failed_merge_repos.py`

- `tools_v2\categories\discord_webhook_tools.py`

- `tools_v2\categories\communication_tools.py`

- `tools_v2\utils\discord_mermaid_renderer.py`

- `tools_v2\utils\discord_mermaid_renderer.py`

- `tools_v2\utils\discord_mermaid_renderer.py`

- `systems\output_flywheel\integration\agent_session_hooks.py`

- `systems\output_flywheel\integration\agent_session_hooks.py`

- `scripts\post_monitor_update_to_discord.py`

- `scripts\post_agent7_update_to_discord.py`

- `scripts\post_agent2_update_to_discord.py`

- `scripts\post_agent8_update_to_discord.py`

- `scripts\post_agent4_update_to_discord.py`



### `timeout=60` (53 locations)

- `src\discord_commander\discord_gui_modals.py`

- `src\ai_training\dreamvault\scrapers\scraper_login.py`

- `src\core\local_repo_layer.py`

- `src\core\synthetic_github.py`

- `src\core\synthetic_github.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\error_handling\circuit_breaker\provider.py`

- `src\integrations\jarvis\ollama_integration.py`

- `src\services\messaging_cli_handlers.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\chatgpt_scraper.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_chat_navigation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_direct_chat.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_final_chat.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\unit\test_working_chat.py`

- `tools\autonomous_task_engine.py`

- `tools\work_completion_verifier.py`

- `tools\infrastructure_automation_suite.py`

- `tools\infrastructure_automation_suite.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\unified_github_pr_creator.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\resolve_pr_blockers.py`

- `tools\resolve_pr_blockers.py`

- `tools\deploy_via_wordpress_admin.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\upload_file_to_discord.py`



### `timeout=120` (45 locations)

- `src\core\local_repo_layer.py`

- `src\core\local_repo_layer.py`

- `tools\mission_control.py`

- `tools\work_completion_verifier.py`

- `tools\work_completion_verifier.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\repo_safe_merge.py`

- `tools\verify_merges.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\resolve_merge_conflicts.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\complete_merge_into_main.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_pr_conflicts.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\resolve_dreamvault_pr3.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\git_based_merge_primary.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\force_push_consolidations.py`

- `tools\phase2_goldmine_config_scanner.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\merge_dreambank_pr1_via_git.py`

- `tools\coordination\discord_web_test_automation.py`

- `tools_v2\categories\coordination_tools.py`



### `port={` (37 locations)

- `src\discord_commander\trading_commands.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\merge_conflict_resolver.py`

- `src\core\stress_test_analysis_report.py`

- `src\core\consolidation\utility_consolidation\utility_consolidation_orchestrator.py`

- `src\core\error_handling\component_management.py`

- `src\core\vector_strategic_oversight\simple_oversight.py`

- `src\services\chatgpt\navigator.py`

- `agent_workspaces\Agent-3\compare_audits.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\workflow\pipelines\daily_pipeline.py`

- `tools\agent_fuel_monitor.py`

- `tools\audit_cleanup.py`

- `tools\cleanup_documentation_refactored.py`

- `tools\workspace_auto_cleaner.py`

- `tools\repo_consolidation_continuation.py`

- `tools\repo_safe_merge.py`

- `tools\tools_consolidation_quick.py`

- `tools\execute_tools_consolidation.py`

- `tools\verify_merges.py`

- `tools\phase2_agent_cellphone_dependency_analyzer.py`

- `tools\repo_safe_merge_v2.py`

- `tools\repo_safe_merge_v2.py`

- `tools\verify_website_fixes.py`

- `tools\captain_swarm_coordinator.py`

- `tools\captain_loop_closer.py`

- `tools\consolidate_duplicate_tools.py`

- `tools\master_import_fixer.py`

- `tools\validate_import_fixes.py`

- `tools\analyze_merge_failures.py`

- `tools\consolidation_strategy_reviewer.py`

- `tools\analyze_project_scan.py`

- `tools\coordination\discord_commands_tester.py`

- `tools_v2\categories\validation_tools.py`

- `money_ops\tools\validate_trading_session.py`

- `money_ops\tools\review_money_map.py`

- `systems\output_flywheel\ssot_verifier.py`

- `systems\output_flywheel\weekly_report_generator.py`



### `timeout=300` (33 locations)

- `src\discord_commander\discord_gui_modals.py`

- `src\discord_commander\unified_discord_bot.py`

- `src\discord_commander\controllers\status_controller_view.py`

- `src\discord_commander\controllers\swarm_tasks_controller_view.py`

- `src\discord_commander\views\swarm_status_view.py`

- `src\discord_commander\views\help_view.py`

- `src\discord_commander\views\unstall_agent_view.py`

- `src\discord_commander\views\bump_agent_view.py`

- `src\discord_commander\views\aria_profile_view.py`

- `src\discord_commander\views\carmyn_profile_view.py`

- `src\core\managers\execution\base_execution_manager.py`

- `src\opensource\project_manager.py`

- `tools\functionality_tests.py`

- `tools\refresh_cache.py`

- `tools\infrastructure_automation_suite.py`

- `tools\review_dreamvault_integration.py`

- `tools\resolve_dreamvault_duplicates.py`

- `tools\execute_streamertools_duplicate_resolution.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\extract_portfolio_logic.py`

- `tools\extract_ai_framework_logic.py`

- `tools\enhanced_duplicate_detector.py`

- `tools\integration_workflow_automation.py`

- `tools\integration_workflow_automation.py`

- `tools\disk_space_optimization.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\complete_batch2_remaining_merges.py`

- `tools\file_deletion_support.py`

- `tools\run_test_suite_validation.py`

- `tools\analysis\audit_github_repos.py`

- `systems\output_flywheel\integration\agent_session_hooks.py`



### `timeout=5` (29 locations)

- `src\core\synthetic_github.py`

- `src\core\synthetic_github.py`

- `src\core\synthetic_github.py`

- `src\core\synthetic_github.py`

- `src\core\stress_test_runner.py`

- `src\core\managers\monitoring\monitoring_lifecycle.py`

- `src\core\performance\coordination_performance_monitor.py`

- `src\gaming\dreamos\fsm_monitoring.py`

- `src\gaming\dreamos\fsm_orchestrator.py`

- `src\orchestrators\overnight\enhanced_agent_activity_detector.py`

- `src\orchestrators\overnight\listener.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamvault\deployment\model_manager.py`

- `tools\audit_broken_tools.py`

- `tools\discord_mermaid_renderer.py`

- `tools\start_discord_system.py`

- `tools\start_discord_system.py`

- `tools\test_discord_commands.py`

- `tools\test_discord_commands.py`

- `tools\fetch_repo_names.py`

- `tools\get_repo_chronology.py`

- `tools\restart_discord_bot.py`

- `tools\agent_activity_detector.py`

- `tools\wordpress_admin_deployer.py`

- `tools\deploy_via_wordpress_rest_api.py`

- `tools\monitor_twitch_bot.py`

- `tools\coordination\discord_web_test_automation.py`

- `tools_v2\categories\discord_tools.py`

- `tools_v2\utils\discord_mermaid_renderer.py`

- `tools_v2\utils\discord_mermaid_renderer.py`



### `port=f` (25 locations)

- `src\core\vector_integration_analytics.py`

- `src\utils\config_auto_migrator.py`

- `src\utils\config_remediator.py`

- `src\utils\unified_config_utils.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio\ai_analytics_component.py`

- `tools\audit_broken_tools.py`

- `tools\github_repo_roi_calculator.py`

- `tools\classify_tools.py`

- `tools\tools_ranking_debate.py`

- `tools\tools_consolidation_and_ranking_complete.py`

- `tools\verify_tools_consolidation_execution.py`

- `tools\merge_duplicate_file_functionality.py`

- `tools\agent_activity_detector.py`

- `tools\captain_inbox_assistant.py`

- `tools\captain_swarm_response_generator.py`

- `tools\captain_workspace_cleanup.py`

- `tools\captain_message_processor.py`

- `tools\technical_debt_analyzer.py`

- `tools\repository_analyzer.py`

- `tools\code_analysis_tool.py`

- `tools\unified_test_analysis.py`

- `tools\master_import_fixer.py`

- `tools\analyze_web_integration_gaps.py`

- `tools\analysis\src_directory_report_generator.py`

- `trading_robot\core\risk_manager.py`



### `TOKEN=):
                        return line.split(` (19 locations)

- `tools\github_create_and_push_repo.py`

- `tools\repo_safe_merge.py`

- `tools\create_batch1_prs.py`

- `tools\verify_batch1_main_branches.py`

- `tools\create_batch2_prs.py`

- `tools\create_merge1_pr.py`

- `tools\verify_batch2_prs.py`

- `tools\merge_prs_via_api.py`

- `tools\resolve_pr_conflicts.py`

- `tools\review_dreamvault_integration.py`

- `tools\resolve_dreamvault_duplicates.py`

- `tools\execute_streamertools_duplicate_resolution.py`

- `tools\execute_dreamvault_cleanup.py`

- `tools\extract_portfolio_logic.py`

- `tools\extract_ai_framework_logic.py`

- `tools\enhanced_duplicate_detector.py`

- `tools\git_based_merge_primary.py`

- `tools\force_push_consolidations.py`

- `tools\repo_safe_merge_v2.py`



### `port=[]` (17 locations)

- `src\gaming\performance_validation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\demos\agent_training\model_evaluator.py`

- `tools\auto_remediate_loc.py`

- `tools\autonomous_task_engine.py`

- `tools\functionality_verification.py`

- `tools\git_work_verifier.py`

- `tools\work_attribution_tool.py`

- `tools\resolve_dreamvault_duplicates.py`

- `tools\enhanced_duplicate_detector.py`

- `tools\sftp_credential_troubleshooter.py`

- `tools\file_locking_optimizer.py`

- `tools\captain_inbox_manager.py`

- `tools\analyze_test_patterns.py`

- `tools\scan_violations.py`

- `tools\analysis\scan_technical_debt.py`

- `tools\consolidation\validate_consolidation.py`

- `scripts\cleanup_v2_compliance.py`



### `limit=100` (16 locations)

- `src\discord_commander\trading_data_service.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\swarm_analyzer.py`

- `src\services\agent_management.py`

- `src\services\performance_analyzer.py`

- `src\services\performance_analyzer.py`

- `src\services\handlers\task_handler.py`

- `src\web\vector_database\message_routes.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_interaction_panel.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\tests\integration\test_agent_training_system.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\content\enrich_conversation_data.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\debug_conversation_content.py`

- `tools\verify_batch1_merge_commits.py`

- `tools\verify_batch1_main_content.py`

- `tools_v2\categories\message_analytics_tools.py`

- `tests\unit\trading_robot\test_trading_repository_interface.py`

- `trading_robot\execution\live_executor.py`



### `default=0` (15 locations)

- `src\orchestrators\overnight\listener.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `tools\captain_roi_quick_calc.py`

- `tools\captain_roi_quick_calc.py`

- `tools\captain_update_log.py`

- `tools\refactoring_suggestion_engine.py`

- `tools\stress_test_messaging_queue.py`

- `tools\stress_test_messaging_queue.py`

- `tools\run_stress_test_with_metrics.py`

- `tools\code_analysis_tool.py`



### `limit=10` (14 locations)

- `src\infrastructure\unified_persistence.py`

- `src\infrastructure\unified_persistence.py`

- `src\services\performance_analyzer.py`

- `src\services\performance_analyzer.py`

- `src\services\recommendation_engine.py`

- `src\services\swarm_intelligence_manager.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\ai_studio\conversational_ai_component.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\unified_conversation_manager.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\unified_conversation_manager.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\gui\panels\ai_studio\conversational_ai_component.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\testing\test_all_templates_on_conversation.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\tests\testing\test_list_conversations.py`

- `tools_v2\tests\test_core.py`

- `systems\output_flywheel\integration\agent_session_hooks.py`



### `limit=1000` (13 locations)

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\prediction_analyzer.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\swarm_analyzer.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\swarm_analyzer.py`

- `src\services\agent_management.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\training_system.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\main_window_original_backup.py`

- `scripts\test_queue_processing_delivery_logging.py`

- `scripts\test_queue_processing_delivery_logging.py`

- `scripts\test_queue_processing_delivery_logging.py`

- `scripts\test_queue_processing_delivery_logging.py`

- `scripts\test_queue_processing_delivery_logging.py`

- `tests\unit\trading_robot\test_trading_repository_interface.py`

- `trading_robot\backtesting\backtester.py`



### `default=10` (12 locations)

- `src\orchestrators\overnight\cli.py`

- `src\workflows\cli.py`

- `tools\compliance_history_tracker.py`

- `tools\refactoring_cli.py`

- `tools\swarm_brain_cli.py`

- `tools\github_pusher_agent.py`

- `tools\github_pusher_agent.py`

- `tools\stress_test_messaging_queue.py`

- `tools\stress_test_messaging_queue.py`

- `tools\start_github_pusher_service.py`

- `tools\run_stress_test_with_metrics.py`

- `dream\repos\master\dadudekc\train_cartpole.py`



## 📁 SAME FILENAME (DIFFERENT LOCATIONS)


### `__init__.py` (191 locations)

- `__init__.py`

- `agent_workspaces\Agent-1\__init__.py`

- `agent_workspaces\Agent-3\__init__.py`

- `core\__init__.py`

- `docs\examples\__init__.py`

- `examples\__init__.py`

- `examples\quickstart_demo\__init__.py`

- `mcp_servers\__init__.py`

- `scripts\__init__.py`

- `scripts\execution\__init__.py`

- `scripts\hooks\__init__.py`

- `scripts\utilities\__init__.py`

- `src\__init__.py`

- `src\ai_automation\__init__.py`

- `src\ai_automation\utils\__init__.py`

- `src\ai_training\__init__.py`

- `src\ai_training\dreamvault\__init__.py`

- `src\ai_training\dreamvault\scrapers\__init__.py`

- `src\application\__init__.py`

- `src\application\use_cases\__init__.py`

- `src\architecture\__init__.py`

- `src\automation\__init__.py`

- `src\config\__init__.py`

- `src\core\__init__.py`

- `src\core\analytics\coordinators\__init__.py`

- `src\core\analytics\engines\__init__.py`

- `src\core\analytics\intelligence\__init__.py`

- `src\core\analytics\intelligence\pattern_analysis\__init__.py`

- `src\core\analytics\models\__init__.py`

- `src\core\analytics\orchestrators\__init__.py`

- `src\core\analytics\prediction\__init__.py`

- `src\core\analytics\processors\__init__.py`

- `src\core\analytics\processors\prediction\__init__.py`

- `src\core\base\__init__.py`

- `src\core\common\__init__.py`

- `src\core\config\__init__.py`

- `src\core\consolidation\__init__.py`

- `src\core\consolidation\utility_consolidation\__init__.py`

- `src\core\constants\__init__.py`

- `src\core\constants\fsm\__init__.py`

- `src\core\coordination\__init__.py`

- `src\core\coordination\swarm\__init__.py`

- `src\core\coordination\swarm\engines\__init__.py`

- `src\core\coordination\swarm\orchestrators\__init__.py`

- `src\core\engines\__init__.py`

- `src\core\error_handling\__init__.py`

- `src\core\error_handling\circuit_breaker\__init__.py`

- `src\core\error_handling\metrics\__init__.py`

- `src\core\file_locking\__init__.py`

- `src\core\file_locking\operations\__init__.py`

- `src\core\gamification\__init__.py`

- `src\core\import_system\__init__.py`

- `src\core\intelligent_context\__init__.py`

- `src\core\intelligent_context\core\__init__.py`

- `src\core\intelligent_context\engines\__init__.py`

- `src\core\intelligent_context\unified_intelligent_context\__init__.py`

- `src\core\managers\__init__.py`

- `src\core\managers\adapters\__init__.py`

- `src\core\managers\execution\__init__.py`

- `src\core\managers\monitoring\__init__.py`

- `src\core\managers\results\__init__.py`

- `src\core\orchestration\__init__.py`

- `src\core\orchestration\adapters\__init__.py`

- `src\core\pattern_analysis\__init__.py`

- `src\core\performance\__init__.py`

- `src\core\performance\metrics\__init__.py`

- `src\core\performance\unified_dashboard\__init__.py`

- `src\core\refactoring\__init__.py`

- `src\core\refactoring\metrics\__init__.py`

- `src\core\refactoring\tools\__init__.py`

- `src\core\session\__init__.py`

- `src\core\shared_utilities\__init__.py`

- `src\core\ssot\__init__.py`

- `src\core\ssot\unified_ssot\__init__.py`

- `src\core\ssot\unified_ssot\execution\__init__.py`

- `src\core\ssot\unified_ssot\validators\__init__.py`

- `src\core\stress_testing\__init__.py`

- `src\core\utilities\__init__.py`

- `src\core\utils\__init__.py`

- `src\core\validation\__init__.py`

- `src\core\vector_strategic_oversight\__init__.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\__init__.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\__init__.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\factories\__init__.py`

- `src\discord_commander\__init__.py`

- `src\discord_commander\controllers\__init__.py`

- `src\discord_commander\templates\__init__.py`

- `src\discord_commander\utils\__init__.py`

- `src\discord_commander\views\__init__.py`

- `src\domain\__init__.py`

- `src\domain\entities\__init__.py`

- `src\domain\ports\__init__.py`

- `src\domain\services\__init__.py`

- `src\domain\value_objects\__init__.py`

- `src\features\__init__.py`

- `src\gaming\__init__.py`

- `src\gaming\dreamos\__init__.py`

- `src\gaming\dreamos\resumer_v2\__init__.py`

- `src\gaming\handlers\__init__.py`

- `src\gaming\integration\__init__.py`

- `src\gaming\models\__init__.py`

- `src\gaming\utils\__init__.py`

- `src\gui\__init__.py`

- `src\gui\components\__init__.py`

- `src\gui\styles\__init__.py`

- `src\infrastructure\__init__.py`

- `src\infrastructure\browser\__init__.py`

- `src\infrastructure\browser\unified\__init__.py`

- `src\infrastructure\logging\__init__.py`

- `src\infrastructure\persistence\__init__.py`

- `src\infrastructure\time\__init__.py`

- `src\integrations\jarvis\__init__.py`

- `src\integrations\osrs\__init__.py`

- `src\message_task\__init__.py`

- `src\message_task\parsers\__init__.py`

- `src\obs\__init__.py`

- `src\opensource\__init__.py`

- `src\orchestrators\overnight\__init__.py`

- `src\quality\__init__.py`

- `src\repositories\__init__.py`

- `src\services\__init__.py`

- `src\services\chat_presence\__init__.py`

- `src\services\chatgpt\__init__.py`

- `src\services\contract_system\__init__.py`

- `src\services\coordination\__init__.py`

- `src\services\handlers\__init__.py`

- `src\services\helpers\__init__.py`

- `src\services\messaging\__init__.py`

- `src\services\messaging_cli_coordinate_management\__init__.py`

- `src\services\models\__init__.py`

- `src\services\protocol\__init__.py`

- `src\services\protocol\routers\__init__.py`

- `src\services\publishers\__init__.py`

- `src\services\thea\__init__.py`

- `src\services\utils\__init__.py`

- `src\shared_utils\__init__.py`

- `src\swarm_brain\__init__.py`

- `src\swarm_pulse\__init__.py`

- `src\templates\__init__.py`

- `src\tools\__init__.py`

- `src\trading_robot\core\__init__.py`

- `src\trading_robot\repositories\__init__.py`

- `src\trading_robot\repositories\implementations\__init__.py`

- `src\trading_robot\repositories\interfaces\__init__.py`

- `src\trading_robot\repositories\models\__init__.py`

- `src\trading_robot\services\__init__.py`

- `src\trading_robot\services\analytics\__init__.py`

- `src\utils\__init__.py`

- `src\utils\config_core\__init__.py`

- `src\utils\file_operations\__init__.py`

- `src\vision\__init__.py`

- `src\vision\analyzers\__init__.py`

- `src\web\__init__.py`

- `src\web\vector_database\__init__.py`

- `src\workflows\__init__.py`

- `swarm_brain\agent_field_manual\automation\__init__.py`

- `swarm_brain\procedures\__init__.py`

- `systems\__init__.py`

- `systems\output_flywheel\__init__.py`

- `systems\output_flywheel\integration\__init__.py`

- `systems\output_flywheel\pipelines\__init__.py`

- `systems\output_flywheel\processors\__init__.py`

- `systems\output_flywheel\publication\__init__.py`

- `tests\discord\__init__.py`

- `tests\unit\gui\__init__.py`

- `tests\unit\services\__init__.py`

- `tools\__init__.py`

- `tools\analysis\__init__.py`

- `tools\autonomous\__init__.py`

- `tools\cleanup\__init__.py`

- `tools\codemods\__init__.py`

- `tools\consolidation\__init__.py`

- `tools\coordination\__init__.py`

- `tools\fixes\__init__.py`

- `tools\thea\__init__.py`

- `tools\toolbelt\__init__.py`

- `tools\toolbelt\executors\__init__.py`

- `tools_v2\__init__.py`

- `tools_v2\adapters\__init__.py`

- `tools_v2\categories\__init__.py`

- `tools_v2\core\__init__.py`

- `tools_v2\tests\__init__.py`

- `tools_v2\utils\__init__.py`

- `trading_robot\__init__.py`

- `trading_robot\backtesting\__init__.py`

- `trading_robot\config\__init__.py`

- `trading_robot\core\__init__.py`

- `trading_robot\execution\__init__.py`

- `trading_robot\strategies\__init__.py`

- `trading_robot\tests\__init__.py`

- `trading_robot\web\__init__.py`



### `models.py` (10 locations)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\mmorpg\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\models.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\tools_db\models.py`

- `src\core\intelligent_context\unified_intelligent_context\models.py`

- `src\core\ssot\unified_ssot\models.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\models.py`

- `src\gaming\integration\models.py`

- `src\services\contract_system\models.py`

- `src\web\vector_database\models.py`

- `src\workflows\models.py`



### `main.py` (5 locations)

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\main.py`

- `agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\discord\main.py`

- `dream\repos\master\dadudekc\AI agent\AI\Digital dreamscape\main.py`

- `dream\repos\master\dadudekc\AI agent\main.py`

- `trading_robot\main.py`



### `config.py` (4 locations)

- `config.py`

- `src\ai_training\dreamvault\config.py`

- `src\services\config.py`

- `src\shared_utils\config.py`



### `registry.py` (4 locations)

- `src\core\engines\registry.py`

- `src\core\managers\registry.py`

- `src\core\orchestration\registry.py`

- `tools\cli\commands\registry.py`



### `cli.py` (4 locations)

- `src\orchestrators\overnight\cli.py`

- `src\services\chatgpt\cli.py`

- `src\vision\cli.py`

- `src\workflows\cli.py`



### `metrics.py` (3 locations)

- `src\core\intelligent_context\metrics.py`

- `src\core\metrics.py`

- `src\obs\metrics.py`



### `contracts.py` (3 locations)

- `src\core\engines\contracts.py`

- `src\core\managers\contracts.py`

- `src\core\orchestration\contracts.py`



### `enums.py` (3 locations)

- `src\core\intelligent_context\enums.py`

- `src\core\ssot\unified_ssot\enums.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\enums.py`



### `__main__.py` (3 locations)

- `src\core\cli\__main__.py`

- `src\services\cli\__main__.py`

- `tools\__main__.py`



### `agent_repository.py` (3 locations)

- `src\domain\ports\agent_repository.py`

- `src\infrastructure\persistence\agent_repository.py`

- `src\repositories\agent_repository.py`



### `logger.py` (3 locations)

- `src\domain\ports\logger.py`

- `src\shared_utils\logger.py`

- `src\utils\logger.py`



### `utils.py` (3 locations)

- `src\gui\utils.py`

- `src\vision\utils.py`

- `src\web\vector_database\utils.py`



### `status_reader.py` (2 locations)

- `src\discord_commander\status_reader.py`

- `src\services\chat_presence\status_reader.py`



### `messaging_protocol_models.py` (2 locations)

- `src\core\messaging_protocol_models.py`

- `src\services\protocol\messaging_protocol_models.py`



### `vector_database.py` (2 locations)

- `src\core\vector_database.py`

- `src\services\vector_database.py`



### `prediction_analyzer.py` (2 locations)

- `src\core\analytics\processors\prediction\prediction_analyzer.py`

- `src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\prediction_analyzer.py`



### `config_manager.py` (2 locations)

- `core\config_manager.py`

- `src\core\config\config_manager.py`



### `base.py` (2 locations)

- `src\core\consolidation\base.py`

- `src\gui\controllers\base.py`



### `fsm_models.py` (2 locations)

- `src\core\constants\fsm_models.py`

- `src\gaming\dreamos\fsm_models.py`


