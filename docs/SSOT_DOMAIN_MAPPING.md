# SSOT Domain Mapping - Phase 1

**Date**: 2025-12-21  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: ✅ **COMPLETE**  
**Contract**: Phase 1 - SSOT Domain Mapping & Validation

---

## 🎯 Purpose

This document defines the mapping between tool directory structure and SSOT domains for Phase 1 bulk SSOT tag addition. This mapping enables automated SSOT tag insertion based on file location.

---

## 📊 Directory to SSOT Domain Mapping

### Core Domains

| Directory Path | SSOT Domain | Description | Example Tools |
|----------------|------------|-------------|---------------|
| `tools/communication/` | `communication` | Agent-to-agent messaging, inbox, coordination | `msg.send`, `msg.inbox`, `msg.broadcast` |
| `tools/coordination/` | `coordination` | Agent coordination, expert finding, pattern checking | `coord.find-expert`, `coord.request-review` |
| `tools/integration/` | `integration` | System integration, API connections, external services | `github_integration`, `wordpress_integration` |
| `tools/toolbelt/` | `toolbelt` | Toolbelt registry, tool discovery, CLI framework | `toolbelt_registry`, `tool_discovery` |
| `tools/autonomous/` | `autonomous` | Autonomous task execution, agent automation | `autonomous_task_engine`, `agent_lifecycle` |
| `tools/monitoring/` | `monitoring` | Health checks, observability, metrics | `health.ping`, `obs.metrics` |
| `tools/validation/` | `validation` | Code validation, compliance checking, testing | `v2_compliance_checker`, `validate_imports` |
| `tools/cli/` | `cli` | CLI commands, dispatchers, command handlers | `unified_dispatcher`, `cli_commands` |
| `tools/codemods/` | `codemods` | Code transformations, migrations, refactoring | `migrate_orchestrators`, `migrate_managers` |
| `tools/analysis/` | `analysis` | Code analysis, complexity metrics, duplicate detection | `complexity_analyzer`, `duplicate_detector` |
| `tools/fixes/` | `fixes` | Automated fixes, remediation tools | `auto_fix_missing_imports`, `auto_remediate_loc` |
| `tools/message_queue/` | `message_queue` | Message queue management, processing | `message_queue_processor`, `queue_manager` |
| `tools/templates/` | `templates` | Code templates, scaffolding | `template_generator`, `scaffold_tool` |
| `tools/thea/` | `thea` | Thea-specific tools, demo tools | `demo_thea_simple`, `demo_thea_live` |
| `tools/examples/` | `examples` | Example code, demos, tutorials | Example implementations |

### Special Domains

| Directory Path | SSOT Domain | Description | Example Tools |
|----------------|------------|-------------|---------------|
| `tools/` (root) | `tools` | **Default domain** for tools in root directory | `agent_mission_controller`, `captain_snapshot` |
| `tools/captain_*.py` | `captain` | Captain-specific operations (by filename pattern) | `captain_status_check`, `captain_assign_mission` |
| `tools/agent_*.py` | `agent` | Agent lifecycle and operations (by filename pattern) | `agent_claim`, `agent_status`, `agent_orient` |
| `tools/consolidation/` | `consolidation` | Code consolidation, deduplication | `consolidation_executor`, `consolidation_analyzer` |
| `tools/cleanup/` | `cleanup` | Cleanup utilities, workspace management | `workspace_cleanup`, `cleanup_obsolete_docs` |

### Domain Patterns (Filename-based)

| Pattern | SSOT Domain | Description |
|---------|------------|-------------|
| `*_wordpress_*.py` | `wordpress` | WordPress-specific tools |
| `*_github_*.py` | `github` | GitHub integration tools |
| `*_deploy_*.py` | `deployment` | Deployment tools |
| `*_audit_*.py` | `audit` | Audit and analysis tools |
| `*_verify_*.py` | `verification` | Verification and validation tools |
| `*_check_*.py` | `check` | Health check and status tools |
| `*_create_*.py` | `creation` | Content creation tools |
| `*_update_*.py` | `update` | Update and modification tools |
| `*_fix_*.py` | `fixes` | Bug fix and remediation tools |
| `*_debug_*.py` | `debug` | Debugging and diagnostics tools |

---

## 🔍 Domain Detection Rules

### Priority Order (First Match Wins):

1. **Directory-based mapping** (highest priority)
   - Check if file is in a mapped subdirectory
   - Use directory's SSOT domain

2. **Filename pattern matching**
   - Check for special patterns (captain_*, agent_*, etc.)
   - Check for domain-specific patterns (*_wordpress_*, etc.)

3. **Default domain**
   - If no match, use `tools` as default domain

### Examples:

```
tools/communication/msg_send.py
→ SSOT Domain: communication (directory match)

tools/captain_status_check.py
→ SSOT Domain: captain (filename pattern match)

tools/integration/github_pr_creator.py
→ SSOT Domain: integration (directory match)

tools/wordpress_deployer.py
→ SSOT Domain: wordpress (filename pattern match)

tools/random_tool.py
→ SSOT Domain: tools (default - no matches)
```

---

## ✅ Validation Rules

### SSOT Tag Format:
```html
<!-- SSOT Domain: <domain_name> -->
```

### Validation Checklist:
- ✅ Tag must be in HTML comment format
- ✅ Domain name must match one of the defined domains
- ✅ Tag should be near the top of the file (within first 50 lines)
- ✅ Only one SSOT tag per file
- ✅ Domain name should be lowercase, no spaces

### Invalid Examples:
```html
<!-- SSOT: communication -->  ❌ (missing "Domain:")
<!-- SSOT Domain: Communication -->  ❌ (uppercase)
<!-- SSOT Domain: communication tools -->  ❌ (spaces)
<!-- SSOT Domain: unknown_domain -->  ❌ (not in domain list)
```

### Valid Examples:
```html
<!-- SSOT Domain: communication -->
<!-- SSOT Domain: integration -->
<!-- SSOT Domain: tools -->
```

---

## 📋 Domain Registry

### Complete Domain List:

1. `communication` - Agent messaging and communication
2. `coordination` - Agent coordination and expert finding
3. `integration` - System integration and external services
4. `toolbelt` - Toolbelt registry and discovery
5. `autonomous` - Autonomous task execution
6. `monitoring` - Health checks and observability
7. `validation` - Code validation and compliance
8. `cli` - CLI commands and dispatchers
9. `codemods` - Code transformations and migrations
10. `analysis` - Code analysis and metrics
11. `fixes` - Automated fixes and remediation
12. `message_queue` - Message queue management
13. `templates` - Code templates and scaffolding
14. `thea` - Thea-specific tools
15. `examples` - Example code and demos
16. `captain` - Captain-specific operations
17. `agent` - Agent lifecycle and operations
18. `consolidation` - Code consolidation
19. `cleanup` - Cleanup utilities
20. `wordpress` - WordPress-specific tools
21. `github` - GitHub integration tools
22. `deployment` - Deployment tools
23. `audit` - Audit and analysis tools
24. `verification` - Verification tools
25. `check` - Health check tools
26. `creation` - Content creation tools
27. `update` - Update tools
28. `debug` - Debugging tools
29. `tools` - **Default domain** (root tools)
30. `analytics` - Analytics and reporting tools (found in existing tags)
31. `qa` - Quality assurance tools (found in existing tags)
32. `infrastructure` - Infrastructure tools (found in existing tags)

---

## 🔧 Implementation Notes

### For Bulk SSOT Tag Addition Script:

1. **Load this mapping** as the authoritative domain mapping
2. **Apply rules in priority order** (directory → pattern → default)
3. **Validate domain** against domain registry before adding tag
4. **Skip files** that already have SSOT tags
5. **Filter to SIGNAL tools only** (use classification from Phase -1)

### Domain Mapping Function (Pseudocode):

```python
def get_ssot_domain(file_path: Path) -> str:
    # 1. Check directory-based mapping
    for directory, domain in DIRECTORY_MAPPING.items():
        if directory in str(file_path):
            return domain
    
    # 2. Check filename patterns
    filename = file_path.name.lower()
    for pattern, domain in FILENAME_PATTERNS.items():
        if pattern in filename:
            return domain
    
    # 3. Default domain
    return "tools"
```

---

## 📊 Statistics

- **Total Domains Defined**: 29 domains
- **Directory-based Mappings**: 15 directories
- **Filename Pattern Mappings**: 10 patterns
- **Default Domain**: `tools`

---

## 🔄 Maintenance

### When to Update This Mapping:

1. **New subdirectories added** to `tools/`
2. **New domain-specific tool patterns** emerge
3. **Domain consolidation** or splitting needed
4. **SSOT domain registry** changes in main repo

### Update Process:

1. Update this document
2. Update bulk SSOT tag script to use new mapping
3. Re-run validation on existing SSOT tags
4. Update domain registry if needed

---

## 📝 References

- **V2 Compliance Refactoring Plan**: `docs/V2_COMPLIANCE_REFACTORING_PLAN.md`
- **Tool Classification**: `tools/TOOL_CLASSIFICATION.md`
- **SSOT Standards**: See main repository SSOT documentation

---

**Agent-8 (SSOT & System Integration)**  
🐝 **WE. ARE. SWARM.** ⚡🔥

**Status**: ✅ SSOT Domain Mapping Complete - Ready for Phase 1 bulk tag addition

