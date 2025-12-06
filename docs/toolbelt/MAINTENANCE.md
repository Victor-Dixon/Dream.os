# Agent Toolbelt - Maintenance Rules (SSOT)

**Last Updated**: 2025-12-04  
**SSOT Domain**: Communication  
**Maintainer**: Agent-6 (Coordination & Communication Specialist)

---

## 🎯 Purpose

This document defines **enforceable rules** for keeping the toolbelt registry current and preventing SSOT drift.

---

## 📋 Maintenance Rules

### **Rule 1: New Tool Registration**

**When**: Adding a new tool to the toolbelt  
**Action**: MUST update BOTH:
1. `tools/toolbelt_registry.py` - Add tool to `TOOLS_REGISTRY` dict
2. `docs/toolbelt/TOOL_REGISTRY.md` - Add tool entry to appropriate category table

**Required Fields**:
- Tool ID (key in registry)
- Name (human-readable)
- Module path
- Main function name
- Description (one-line)
- Flags (array)
- Args passthrough (boolean)

**Example**:
```python
# tools/toolbelt_registry.py
"new-tool": {
    "name": "New Tool Name",
    "module": "tools.new_tool_cli",
    "main_function": "main",
    "description": "One-line description",
    "flags": ["--new-tool", "-nt"],
    "args_passthrough": True,
}
```

```markdown
# docs/toolbelt/TOOL_REGISTRY.md
| New Tool Name | `--new-tool`, `-nt` | `tools.new_tool_cli` | One-line description |
```

---

### **Rule 2: Tool Removal**

**When**: Removing or deprecating a tool  
**Action**: MUST update BOTH:
1. `tools/toolbelt_registry.py` - Remove tool entry
2. `docs/toolbelt/TOOL_REGISTRY.md` - Remove tool entry
3. Add deprecation note if tool is deprecated (not removed)

---

### **Rule 3: Tool Modification**

**When**: Changing tool flags, module, or description  
**Action**: MUST update BOTH:
1. `tools/toolbelt_registry.py` - Update tool entry
2. `docs/toolbelt/TOOL_REGISTRY.md` - Update tool entry

**Verification**: Run `python -m tools.toolbelt --list` to verify changes

---

### **Rule 4: Registry Verification**

**When**: Before committing toolbelt changes  
**Action**: MUST run:
```bash
python -m tools.toolbelt --list
python -m tools.toolbelt --help
```

**Check**:
- All tools in registry appear in `--list` output
- All flags work correctly
- No duplicate flags (unless intentional)
- Module paths are correct

---

### **Rule 5: Documentation Sync**

**When**: Any registry change  
**Action**: Update `docs/toolbelt/TOOL_REGISTRY.md` within same commit

**Enforcement**: Pre-commit hook (future) or code review requirement

---

## 🔍 Verification Checklist

Before committing toolbelt changes:

- [ ] Tool added to `tools/toolbelt_registry.py`
- [ ] Tool added to `docs/toolbelt/TOOL_REGISTRY.md`
- [ ] Tool appears in `python -m tools.toolbelt --list`
- [ ] Tool flags work: `python -m tools.toolbelt --<flag>`
- [ ] Module path is correct
- [ ] Description is accurate
- [ ] Category assignment is correct

---

## ⚠️ SSOT Drift Prevention

### **Known Risk**: Tool names/flags drifting from actual modules

**Mitigation**:
1. **Automated Verification**: Run `--list` and `--help` before commits
2. **Documentation Sync**: Registry and docs updated together
3. **Code Review**: Verify registry matches actual implementation

### **Drift Detection**:
- Compare `tools/toolbelt_registry.py` with `python -m tools.toolbelt --list`
- Compare `docs/toolbelt/TOOL_REGISTRY.md` with actual CLI output
- Document discrepancies in `docs/toolbelt/TOOL_REGISTRY.md` "Known Drift" section

---

## 📊 Maintenance Workflow

### **Adding a New Tool**:

1. **Create Tool Module**: `tools/new_tool_cli.py` with `main()` function
2. **Register Tool**: Add to `tools/toolbelt_registry.py`
3. **Document Tool**: Add to `docs/toolbelt/TOOL_REGISTRY.md`
4. **Verify**: Run `python -m tools.toolbelt --list` and test flags
5. **Commit**: Include both registry and docs in same commit

### **Updating Existing Tool**:

1. **Update Registry**: Modify entry in `tools/toolbelt_registry.py`
2. **Update Docs**: Modify entry in `docs/toolbelt/TOOL_REGISTRY.md`
3. **Verify**: Test flags and functionality
4. **Commit**: Include both changes in same commit

### **Removing Tool**:

1. **Deprecate** (if needed): Add deprecation notice
2. **Remove Registry**: Remove from `tools/toolbelt_registry.py`
3. **Remove Docs**: Remove from `docs/toolbelt/TOOL_REGISTRY.md`
4. **Verify**: Confirm tool no longer appears in `--list`
5. **Commit**: Document removal reason

---

## 🎯 Enforcement

### **Current**:
- Manual verification before commits
- Code review requirement for registry changes

### **Future** (Recommended):
- Pre-commit hook to verify registry matches CLI
- Automated test comparing registry with `--list` output
- CI check for registry/docs sync

---

## 📝 Change Log

**2025-12-04**: Initial SSOT maintenance rules established  
**Next Review**: When registry structure changes

---

**SSOT Maintenance Rules** ✅  
**Enforcement**: Manual (current), Automated (future)  
**Maintained by**: Agent-6

🐝 **WE. ARE. SWARM. ⚡🔥**

