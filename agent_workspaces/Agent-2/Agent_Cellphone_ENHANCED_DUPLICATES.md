============================================================
📋 ENHANCED DUPLICATE DETECTION REPORT
============================================================

🔍 Exact Duplicates (Content-Based):
   Total Groups: 20
   Total Files: 64

   Top 10 Exact Duplicate Groups:
      sample_task.json: 8 locations
         SSOT: agent_workspaces\Agent-1\inbox\sample_task.json
         Remove: agent_workspaces\Agent-2\inbox\sample_task.json
         Remove: agent_workspaces\Agent-3\inbox\sample_task.json
         ... and 5 more
      sample_task.json: 8 locations
         SSOT: agent_workspaces\Agent-1\inbox\tasks\sample_task.json
         Remove: agent_workspaces\Agent-2\inbox\tasks\sample_task.json
         Remove: agent_workspaces\Agent-3\inbox\tasks\sample_task.json
         ... and 5 more
      sample_result.json: 8 locations
         SSOT: agent_workspaces\Agent-1\outbox\sample_result.json
         Remove: agent_workspaces\Agent-2\outbox\sample_result.json
         Remove: agent_workspaces\Agent-3\outbox\sample_result.json
         ... and 5 more
      task_list.json: 6 locations
         SSOT: agent_workspaces\Agent-3\task_list.json
         Remove: agent_workspaces\Agent-4\task_list.json
         Remove: agent_workspaces\Agent-5\task_list.json
         ... and 3 more
      sync_20250811_075422.json: 3 locations
         SSOT: agent_workspaces\Agent-3\inbox\sync_20250811_075422.json
         Remove: agent_workspaces\Agent-3\inbox\sync_20250811_075852.json
         Remove: agent_workspaces\Agent-3\inbox\sync_20250811_084354.json
      response_1755343361038_Agent-2.json: 3 locations
         SSOT: runtime\agent_comms\inbox\response_1755343361038_Agent-2.json
         Remove: runtime\collaborative_tasks\reports\collaboration_report_20250816_141740.md
         Remove: src\collaborative\communication_hub\secure_hub.py
      task_list.json: 2 locations
         SSOT: agent_workspaces\Agent-1\task_list.json
         Remove: agent_workspaces\Agent-2\task_list.json
      2025-07-02T07-50-01_agent-2_to_agent-1.json: 2 locations
         SSOT: agent_workspaces\Agent-1\inbox\2025-07-02T07-50-01_agent-2_to_agent-1.json
         Remove: agent_workspaces\queue\completed\2025-07-02T07-50-01_agent-2_to_agent-1.json
      2025-07-02T07-50-02_agent-2_to_agent-1.json: 2 locations
         SSOT: agent_workspaces\Agent-1\inbox\2025-07-02T07-50-02_agent-2_to_agent-1.json
         Remove: agent_workspaces\queue\completed\2025-07-02T07-50-02_agent-2_to_agent-1.json
      2025-07-02T07-51-14_agent-2_to_agent-1.json: 2 locations
         SSOT: agent_workspaces\Agent-1\inbox\2025-07-02T07-51-14_agent-2_to_agent-1.json
         Remove: agent_workspaces\queue\completed\2025-07-02T07-51-14_agent-2_to_agent-1.json

📋 Name-Based Duplicates:
   Total Groups: 12
   Total Files: 48

   Top 10 Name-Based Duplicate Groups:
      __init__.py: 26 locations
         SSOT: overnight_runner\__init__.py
      agent_cell_phone.py: 2 locations
         SSOT: CORE\agent_cell_phone.py
      inter_agent_framework.py: 2 locations
         SSOT: CORE\inter_agent_framework.py
      main.py: 2 locations
         SSOT: CORE\main.py
      fsm_orchestrator.py: 2 locations
         SSOT: dreamos\core\fsm_orchestrator.py
      inbox_consumer.py: 2 locations
         SSOT: overnight_runner\inbox_consumer.py
      onboarding_utils.py: 2 locations
         SSOT: scripts\onboarding_utils.py
      overnight_runner.py: 2 locations
         SSOT: scripts\overnight_runner.py
      utils.py: 2 locations
         SSOT: src\utils.py
      enhanced_response_capture.py: 2 locations
         SSOT: src\agent_cell_phone\enhanced_response_capture.py

🔧 Recommendations:
   1. Remove exact duplicates (keep SSOT versions)
   2. Review name-based duplicates (may have different content)
   3. Update imports if needed
   4. Test functionality after cleanup