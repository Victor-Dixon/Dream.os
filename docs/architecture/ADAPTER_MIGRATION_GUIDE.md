<!-- SSOT Domain: architecture -->
# 📘 Adapter Migration Guide - tools/

> **📚 SSOT Reference**: For Adapter pattern implementation details, see [ARCHITECTURE_PATTERNS_DOCUMENTATION.md](./ARCHITECTURE_PATTERNS_DOCUMENTATION.md) (Adapter Pattern section)

**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-01-27  
**Priority:** HIGH  
**Status:** ARCHITECTURAL DOCUMENTATION

---

## 🎯 PURPOSE

This guide provides step-by-step instructions for migrating legacy tools from `tools/` to `tools/` using the IToolAdapter pattern.

---

## 📋 MIGRATION PROCESS

### **Step 1: Analyze Legacy Tool**

**Questions to Answer:**
1. What does the tool do?
2. What are its inputs/outputs?
3. Does it have dependencies on other tools?
4. Is there already an adapter in tools/?
5. What category should it belong to?

**Example:**
```python
# Legacy: tools/captain_message_all_agents.py → tools.toolbelt captain.message_all
def message_all_agents(message: str, priority: str = "regular", include_captain: bool = True):
    """Send message to all agents including Captain."""
    # Implementation
```

**Analysis:**
- Functionality: Broadcast messaging
- Inputs: message, priority, include_captain
- Outputs: Success/failure per agent
- Category: captain (messaging operations)
- Check: Already has `msg.broadcast` in messaging_tools.py

---

### **Step 2: Choose Migration Strategy**

**Strategy A: Direct Migration** (Most Common)
- Tool has unique functionality
- No equivalent in tools/
- Create new adapter

**Strategy B: Wrapper Migration**
- Tool already has equivalent in tools/
- Keep as wrapper, mark deprecated
- Delegate to tools adapter

**Strategy C: Consolidation Migration**
- Multiple similar tools exist
- Create unified adapter
- Deprecate all legacy versions

---

### **Step 3: Create Adapter**

**Template:**

```python
from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec
from ..adapters.error_types import ToolExecutionError

class ToolNameTool(IToolAdapter):
    """Tool description."""
    
    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="category.tool_name",
            version="1.0.0",
            category="category",
            summary="Brief tool description",
            required_params=["param1", "param2"],
            optional_params={"param3": "default_value"},
        )
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)
    
    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Execute tool."""
        try:
            # Validate params
            is_valid, missing = self.validate(params)
            if not is_valid:
                return ToolResult(
                    success=False,
                    output=None,
                    error_message=f"Missing params: {missing}",
                    exit_code=1,
                )
            
            # Extract params
            param1 = params["param1"]
            param2 = params["param2"]
            param3 = params.get("param3", "default_value")
            
            # Execute tool logic
            result = self._execute_tool_logic(param1, param2, param3)
            
            # Return result
            return ToolResult(
                success=True,
                output=result,
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            raise ToolExecutionError(str(e), tool_name="category.tool_name")
    
    def _execute_tool_logic(self, param1: str, param2: str, param3: str) -> dict:
        """Internal tool logic."""
        # Implementation here
        return {"result": "success"}
```

---

### **Step 4: Register Tool**

**Add to `tools/tool_registry.py`:**

```python
TOOL_REGISTRY = {
    # ... existing tools ...
    "category.tool_name": ("tools.categories.category_file", "ToolNameTool"),
}
```

**Naming Convention:**
- Use dot notation: `category.tool_name`
- Category matches file name (e.g., `captain`, `infra`, `msg`)
- Tool name is descriptive and concise

---

### **Step 5: Test Adapter**

**Test Checklist:**
- [ ] Tool can be imported
- [ ] get_spec() returns correct ToolSpec
- [ ] validate() works with valid params
- [ ] validate() rejects invalid params
- [ ] execute() works with valid params
- [ ] execute() handles errors gracefully
- [ ] Tool registered in tool_registry.py
- [ ] Tool accessible via toolbelt CLI

---

### **Step 6: Deprecate Legacy Tool**

**Add deprecation notice:**

```python
"""
⚠️ DEPRECATED: This tool has been migrated to tools.
Use 'python -m tools.toolbelt category.tool_name' instead.
This file will be removed in future version.

Migrated to: tools/categories/category_file.py → ToolNameTool
Registry: category.tool_name
"""

import warnings

warnings.warn(
    "⚠️ DEPRECATED: This tool has been migrated to tools. "
    "Use 'python -m tools.toolbelt category.tool_name' instead. "
    "This file will be removed in future version.",
    DeprecationWarning,
    stacklevel=2
)
```

---

## 🎯 CATEGORY ASSIGNMENT GUIDE

### **Captain Tools** (`captain_*.py`)

**Categories:**
- `captain_tools.py` - Core operations (status, gas, leaderboard)
- `captain_tools_advanced.py` - Advanced operations (analysis, optimization)
- `captain_tools_extension.py` - Extended operations (progress, missions)
- `captain_coordination_tools.py` - Coordination (completion, task picking)

**Assignment Rules:**
- Core ops → `captain_tools.py`
- Analysis/validation → `captain_tools_advanced.py`
- Progress/missions → `captain_tools_extension.py`
- Workflow/coordination → `captain_coordination_tools.py`

### **Infrastructure Tools** (`infrastructure_tools.py`)

**Scope:**
- Workspace management
- System health
- Performance optimization
- Browser pool management

### **Messaging Tools** (`messaging_tools.py`)

**Scope:**
- Agent messaging
- Broadcast operations
- Inbox management

### **Analysis Tools** (`analysis_tools.py`)

**Scope:**
- Project scanning
- Complexity analysis
- Duplication detection

---

## ⚠️ COMMON PITFALLS

### **1. Duplicate Implementations**

**Problem:** Creating adapter when one already exists

**Solution:**
- Always check tool_registry.py first
- Search for similar functionality
- Consolidate if duplicates found

### **2. Legacy Dependencies**

**Problem:** Importing from `tools/` directory

**Solution:**
- Migrate dependencies to `tools/`
- Or refactor to be self-contained
- Never create circular dependencies

### **3. V2 Compliance Violations**

**Problem:** File exceeds 400 line limit

**Solution:**
- Split into multiple category files
- Extract helper functions to utilities
- Keep each file focused

### **4. Inconsistent Patterns**

**Problem:** Not following IToolAdapter pattern

**Solution:**
- Always implement all 3 required methods
- Use ToolSpec and ToolResult
- Follow error handling patterns

---

## 📊 MIGRATION CHECKLIST

**Pre-Migration:**
- [ ] Analyze legacy tool functionality
- [ ] Check for existing adapters
- [ ] Determine appropriate category
- [ ] Review similar tools for patterns

**Migration:**
- [ ] Create adapter class
- [ ] Implement get_spec()
- [ ] Implement validate()
- [ ] Implement execute()
- [ ] Add error handling
- [ ] Add logging

**Post-Migration:**
- [ ] Register in tool_registry.py
- [ ] Test adapter functionality
- [ ] Add deprecation notice to legacy tool
- [ ] Update documentation
- [ ] Verify V2 compliance

---

## 🎯 SUCCESS METRICS

**Quality:**
- ✅ Adapter follows IToolAdapter pattern
- ✅ All required methods implemented
- ✅ Proper error handling
- ✅ Type hints complete
- ✅ Logging implemented

**Compliance:**
- ✅ File ≤400 lines
- ✅ No legacy dependencies
- ✅ Registered correctly
- ✅ No duplicates

**Functionality:**
- ✅ Tool works correctly
- ✅ Handles edge cases
- ✅ Returns proper ToolResult
- ✅ Accessible via toolbelt

---

**WE. ARE. SWARM.** 🐝⚡🔥

**Agent-2:** Migration guide complete! Ready for autonomous tool migration.

**Status:** ✅ **DOCUMENTATION COMPLETE** | Patterns documented | Ready for use

