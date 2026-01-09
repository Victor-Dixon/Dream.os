# Tool Classification: Signal vs Noise

**Generated:** 2025-12-30  
**Classification Tool:** `tools/classify_tools_signal_noise.py`  
**Scope:** `tools/` directory

---

## Executive Summary

- **Total Tools Analyzed:** 146 Python files
- **SIGNAL (Active/Important):** 92 tools (63.0%)
- **NOISE (Unused/Deprecated):** 3 tools (2.1%)
- **UNKNOWN (Unclassified):** 51 tools (34.9%)

---

## Classification Criteria

### SIGNAL Indicators
- ✅ Registered in `tool_registry.lock.json`
- ✅ Imported by other tools
- ✅ Core infrastructure components (tool_registry, toolbelt_core, etc.)
- ✅ Package `__init__.py` files for registered modules

### NOISE Indicators
- ❌ Marked as deprecated
- ❌ Test-only files (`test_*.py`, `*_test.py`)
- ❌ Legacy/archive files
- ❌ Standalone scripts (may be noise)

### UNKNOWN
- ❓ Tools that don't clearly fit SIGNAL or NOISE criteria
- ❓ May need manual review

---

## Detailed Breakdown

### SIGNAL Tools (92)

**By Category:**
- **Registered Tools:** 27 (from tool_registry.lock.json)
- **Imported Tools:** ~35 (referenced by other tools)
- **Core Infrastructure:** ~15 (tool_registry, toolbelt_core, etc.)
- **Utility/Helper Tools:** ~15 (tag_analyzer, validators, checkers, etc.)

**Examples:**
- `tool_registry.py` - Core registry system
- `toolbelt_core.py` - Core orchestrator
- `devlog_manager.py` - Used by cycle reports
- `ssot_coordination_report.py` - Used by reports
- `wordpress_manager.py` - Used by website tools

### NOISE Tools (3)

**Deprecated Tools:**
- `validate_closure_format.py` - Marked as deprecated
- `categories/captain_tools_extension.py` - Marked as deprecated
- `categories/infrastructure_tools.py` - Marked as deprecated

**Note:** Test files are now classified separately (not automatically NOISE)

**Examples:**
- `validate_closure_format.py` - Marked as deprecated
- `test_deployment_staging.py` - Test-only
- `test_bi_tools.py` - Test-only
- `test_toolbelt_basic.py` - Test-only
- `test_unified_tool_registry_mcp.py` - Test-only

### UNKNOWN Tools (51)

**May need manual review:**
- `test_deployment_staging.py` (test file - may be SIGNAL if part of test infrastructure)
- `master_task_log_to_cycle_planner.py` (integration tool - likely SIGNAL)
- `discord_health_monitor.py` (monitoring tool - likely SIGNAL)
- `calibrate_agent_coordinates.py` (utility tool - likely SIGNAL)
- `system_health_dashboard.py` (dashboard tool - likely SIGNAL)

---

## Recommendations

### High Priority
1. **Review UNKNOWN tools** - 59 tools need manual classification
2. **Archive NOISE tools** - Move deprecated/test-only tools to archive
3. **Document SIGNAL tools** - Ensure all SIGNAL tools have proper SSOT tags

### Medium Priority
1. **Refine classification criteria** - Improve automated classification
2. **Expand scope** - Classify tools across entire codebase (not just tools/)
3. **Create maintenance plan** - Regular re-classification as tools evolve

---

## Next Steps

1. ✅ Classification tool created and executed
2. ⏳ Manual review of UNKNOWN tools
3. ⏳ Archive NOISE tools
4. ⏳ Update SSOT tags for SIGNAL tools
5. ⏳ Expand classification to entire codebase

---

**Report Location:** `reports/tool_classification_signal_noise.json`  
**Tool Location:** `tools/classify_tools_signal_noise.py`

