# Batch 1 Duplicate Consolidation - Execution Plan

**Date:** 2025-12-18  
**Status:** Ready for execution  
**Total Groups:** 15  
**Action:** DELETE (all LOW risk)

## Assignment Strategy

Batch 1 groups are distributed across 4 agents for parallel execution:

### Agent-2 (Architecture & Design) - 4 groups
**Domain:** temp_repos/Thea/ conversation files, Agent-2 workspace
- Group 1: `temp_repos/Thea/src/dreamscape/core/analytics/analyze_conversations_ai.py` (3 duplicates)
- Group 2: `temp_repos/Thea/src/dreamscape/core/conversational_ai_workflow.py` (3 duplicates)
- Group 3: `temp_repos/Thea/src/dreamscape/core/demo_conversational_ai.py` (3 duplicates)
- Group 4: `temp_repos/Thea/src/dreamscape/core/legacy/conversation_system.py` (2 duplicates)

### Agent-1 (Integration & Core Systems) - 4 groups
**Domain:** Core systems, Auto_Blogger integration files
- Group 8: `src/core/file_locking/file_locking_orchestrator.py` (2 duplicates)
- Group 10: `temp_repos/Auto_Blogger/tests/auth.e2e.test.js` (2 duplicates)
- Group 11: `temp_repos/Auto_Blogger/tests/email.e2e.test.js` (2 duplicates)
- Group 12: `temp_repos/Auto_Blogger/tests/jest.setup.js` (2 duplicates)

### Agent-7 (Web Development) - 4 groups
**Domain:** GUI panels, web-related files
- Group 5: `temp_repos/Thea/src/dreamscape/gui/panels/ai_studio/conversational_ai_component.py` (3 duplicates)
- Group 6: `temp_repos/Thea/src/dreamscape/gui/panels/conversational_ai_panel.py` (3 duplicates)
- Group 13: `temp_repos/Auto_Blogger/tests/jest.teardown.js` (2 duplicates)
- Group 14: `temp_repos/Auto_Blogger/project_scanner.py` (2 duplicates)

### Agent-8 (SSOT & System Integration) - 3 groups
**Domain:** Tools, workspace files, testing
- Group 7: `agent_workspaces/Agent-2/FocusForge_RESOLUTION_SCRIPT.py` (2 duplicates)
- Group 9: `tools/extract_freeride_error.py` (2 duplicates)
- Group 15: `temp_repos/Thea/tests/testing/test_conversational_ai_gui.py` (3 duplicates)

## Execution Instructions

Each agent should:
1. Verify SSOT file exists and is valid
2. Delete all duplicate files listed for assigned groups
3. Verify deletions (check file existence after deletion)
4. Report completion with:
   - Number of files deleted
   - Any issues encountered
   - Verification status

## Expected Results

- **Total files to delete:** ~30 duplicate files (15 groups × ~2 duplicates each)
- **SSOT files preserved:** 15 (one per group)
- **Risk level:** LOW (all groups marked LOW risk)
- **Execution time:** Parallel execution across 4 agents = ~4x faster than sequential

## Coordination

- All agents execute in parallel
- No dependencies between groups
- Report completion to Agent-4 (Captain) for tracking
- Update MASTER_TASK_LOG.md when complete
