# Code-Comment Mismatch Analysis Report

**Date**: 2025-12-12
**Agent**: Agent-2 (Architecture & Design Specialist)
**Status**: ✅ **ANALYSIS COMPLETE**

---

## Summary

- **Files Scanned**: 945
- **Total Issues Found**: 961
- **High Severity**: 0
- **Medium Severity**: 63
- **Low Severity**: 898

---

## 🟡 Medium Severity Issues

### src\discord_commander\status_reader.py:67
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: File not modified, return cache

### src\discord_commander\tools_commands.py:252
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Return None if Discord not available (cog won't lo

### src\ai_training\dreamvault\database.py:26
- **Type**: method_mismatch
- **Function/Class**: DatabaseConnection
- **Message**: Docstring mentions method 'cursor()' but class doesn't have it

### src\ai_training\dreamvault\database.py:26
- **Type**: method_mismatch
- **Function/Class**: DatabaseConnection
- **Message**: Docstring mentions method 'DatabaseConnection()' but class doesn't have it

### src\ai_training\dreamvault\database.py:147
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: For INSERT/UPDATE/DELETE, commit and return affect

### src\architecture\design_patterns.py:74
- **Type**: method_mismatch
- **Function/Class**: Factory
- **Message**: Docstring mentions method 'Type1Class()' but class doesn't have it

### src\architecture\design_patterns.py:122
- **Type**: method_mismatch
- **Function/Class**: Subject
- **Message**: Docstring mentions method 'MyObserver()' but class doesn't have it

### src\architecture\design_patterns.py:122
- **Type**: method_mismatch
- **Function/Class**: Subject
- **Message**: Docstring mentions method 'Subject()' but class doesn't have it

### src\core\agent_documentation_service.py:140
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Final fallback: Return empty results with warning

### src\core\agent_documentation_service.py:236
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Final fallback: Return None (document not found)

### src\core\auto_gas_pipeline_system.py:453
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: (Simplified for now - return default)

### src\core\deferred_push_queue.py:152
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Return oldest pending entry

### src\core\in_memory_message_queue.py:246
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: In-memory queue doesn't track expiration, so retur

### src\core\in_memory_message_queue.py:271
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: In-memory queue doesn't track expiration, so retur

### src\core\message_queue_persistence.py:165
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: All recovery strategies failed - backup and return

### src\core\smart_assignment_optimizer.py:120
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Return agent with highest score

### src\core\engines\communication_core_engine.py:82
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Simplified receive logic - return last message

### src\core\error_handling\component_management.py:263
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Type variable for generic return types

### src\core\error_handling\error_execution.py:33
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Type variable for generic return types

### src\core\error_handling\circuit_breaker\protocol.py:33
- **Type**: parameter_mismatch
- **Function/Class**: call
- **Message**: Docstring documents parameter 'kwargs' but function doesn't have it

### src\core\intelligent_context\unified_intelligent_context\search_operations.py:90
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: If vector DB search returns results, use them

### src\core\intelligent_context\unified_intelligent_context\search_operations.py:94
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Fallback to mock results if vector DB unavailable 

### src\core\orchestration\base_orchestrator.py:26
- **Type**: method_mismatch
- **Function/Class**: BaseOrchestrator
- **Message**: Docstring mentions method 'super()' but class doesn't have it

### src\core\refactoring\optimization_helpers.py:140
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: For now, return original content

### src\core\refactoring\optimization_helpers.py:142
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: For this placeholder implementation, we return the

### src\core\refactoring\optimization_helpers.py:145
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Could add comments with suggestions, but for now j

### src\core\refactoring\tools\optimization_tools.py:146
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Return content as-is - optimizations should be app

### src\core\session\base_session_manager.py:78
- **Type**: parameter_mismatch
- **Function/Class**: create_session
- **Message**: Docstring documents parameter 'Returns' but function doesn't have it

### src\core\session\rate_limited_session_manager.py:69
- **Type**: parameter_mismatch
- **Function/Class**: create_session
- **Message**: Docstring documents parameter 'Returns' but function doesn't have it

### src\core\utils\simple_utils.py:97
- **Type**: return_mismatch
- **Function/Class**: N/A
- **Message**: Comment says 'returns' but next line doesn't return: Return 0 instead of None for backward compatibilit

## Issue Types Summary

- **missing_documentation**: 856
- **return_mismatch**: 46
- **assignment_mismatch**: 29
- **method_mismatch**: 10
- **call_mismatch**: 9
- **parameter_mismatch**: 7
- **deprecated_marker**: 4

---

*Analysis generated by code-comment mismatch detector*