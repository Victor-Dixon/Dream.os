# Documentation Tagging and Navigation Protocol

<!-- SSOT Domain: documentation -->

**Purpose:** Standardize tagging and linking practices to enable agents to easily find and navigate project documentation and code.

**Scope:** All documentation files, code files, and related artifacts across the codebase.

**Status:** Draft Protocol (2025-12-27)  
**Author:** Agent-3 (Infrastructure & DevOps Specialist)

---

## Overview

This protocol establishes standards for:
- **SSOT Domain Tags** - Categorizing files by domain ownership
- **Navigation Links** - Cross-referencing related files and documentation
- **File Organization** - Logical grouping and discoverability
- **Documentation Indexing** - Centralized navigation structures

---

## 1. SSOT Domain Tags

### Format
```html
<!-- SSOT Domain: domain-name -->
```

### Placement
- **Code files:** Top of file, after shebang/docstring
- **Documentation files:** Top of file, after title/metadata

### Examples
```python
#!/usr/bin/env python3
"""
Service for message delivery.

<!-- SSOT Domain: communication -->
"""
```

```markdown
# Messaging Service Documentation

<!-- SSOT Domain: communication -->
```

### Domain List
See `docs/SSOT_DOMAIN_MAPPING.md` for complete domain list.

**Common Domains:**
- `communication` - Messaging, notifications, routing
- `infrastructure` - DevOps, deployment, CI/CD
- `integration` - API integrations, external services
- `analytics` - Metrics, tracking, business intelligence
- `core` - Core utilities, base classes, shared components
- `governance` - Policies, standards, protocols

---

## 2. Navigation Links in Documentation

### Internal Links (Markdown)
Use relative paths for files within repository:

```markdown
See [Protocol Document](docs/PROTOCOL_NAME.md) for details.
Reference [Service Implementation](src/services/service_name.py).
Check [Status File](agent_workspaces/Agent-X/status.json).
```

### Cross-References
Link related files explicitly:

```markdown
**Related Files:**
- Implementation: `src/services/messaging_service.py`
- Protocol: `docs/MESSAGING_PROTOCOL.md`
- Status: `agent_workspaces/Agent-1/status.json`
```

### Section Links
Link to specific sections within documents:

```markdown
See [Deployment Steps](#deployment-steps) below.
Reference [Architecture Overview](docs/ARCHITECTURE.md#overview).
```

---

## 3. Code File Cross-References

### Docstring Links
Include links to related code and documentation:

```python
"""
Message Delivery Service

See also:
- Protocol: docs/MESSAGING_PROTOCOL.md
- Related: src/core/messaging_core.py
- Tests: tests/test_messaging_service.py
"""
```

### Import Comments
Document key dependencies:

```python
# Key dependencies:
# - src/core/messaging_models.py (UnifiedMessage)
# - src/utils/logger.py (Logging utilities)
# - docs/MESSAGING_ARCHITECTURE.md (Architecture overview)
```

---

## 4. Documentation Index Standards

### Central Index File
`docs/DOCUMENTATION_INDEX.md` should include:
- Categorized lists of documentation
- Quick links to common protocols
- Navigation by domain
- Agent workspace references

### Protocol Index
Maintain protocol-specific index with:
- Protocol name and purpose
- Related protocols
- Implementation locations
- Usage examples

---

## 5. File Organization Tags

### Status Tags
For tracking files:
```markdown
**Status:** Active | Deprecated | Draft
**Last Updated:** 2025-12-27
**Owner:** Agent-X
```

### Task References
Link to task tracking:
```markdown
**Related Task:** MASTER_TASK_LOG.md - Task ID/Description
**Issue:** #123 or docs/issues/issue-name.md
```

---

## 6. Agent Workspace Links

### Status File Links
Link from documentation to agent workspaces:

```markdown
**Agent Status:**
- Agent-3: `agent_workspaces/Agent-3/status.json`
- Current Mission: See status.json for latest
- Coordination: See docs/COORDINATION_PROTOCOL.md
```

### Devlog References
Link to agent devlogs:

```markdown
**Recent Work:**
- Agent-3 Devlog: `agent_workspaces/Agent-3/devlogs/2025-12-27_work.md`
- See agent workspace for complete history
```

---

## 7. Implementation Guidelines

### For New Files
1. Add SSOT domain tag at top
2. Include cross-references to related files
3. Link to relevant protocols
4. Update documentation index if needed

### For Existing Files
1. Audit for missing SSOT tags
2. Add navigation links where helpful
3. Cross-reference related documentation
4. Update indices as needed

### For Documentation
1. Start with clear title and SSOT tag
2. Include "Related Files" or "See Also" section
3. Link to protocols and standards
4. Reference agent workspaces when relevant

---

## 8. Discovery Tools

### Search Strategies
Agents should use:
- **Codebase Search:** Semantic search for finding related code
- **Grep:** Exact string/pattern matching
- **File Search:** Glob patterns for file discovery
- **Documentation Index:** Centralized navigation

### Tag-Based Discovery
Search by SSOT domain:
```bash
grep -r "SSOT Domain: communication" src/
grep -r "SSOT Domain: infrastructure" docs/
```

---

## 9. Validation Checklist

When reviewing files, check:
- [ ] SSOT domain tag present and correct
- [ ] Navigation links to related files included
- [ ] Cross-references to protocols/standards
- [ ] Links to agent workspaces (if relevant)
- [ ] Documentation index updated (if new file)
- [ ] File paths are correct and relative

---

## 10. Examples

### Good Documentation File
```markdown
# Messaging Service Documentation

<!-- SSOT Domain: communication -->

## Overview

Service for delivering messages to agents via multiple channels.

**Related Files:**
- Implementation: `src/services/messaging_service.py`
- Protocol: `docs/MESSAGING_PROTOCOL.md`
- Models: `src/core/messaging_models.py`
- Status: `agent_workspaces/Agent-1/status.json`

**See Also:**
- [Architecture Overview](docs/MESSAGING_ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md#messaging)
```

### Good Code File
```python
#!/usr/bin/env python3
"""
Messaging Service Implementation

<!-- SSOT Domain: communication -->

See also:
- Protocol: docs/MESSAGING_PROTOCOL.md
- Models: src/core/messaging_models.py
- Tests: tests/test_messaging_service.py
"""

from .messaging_models import UnifiedMessage
# ...
```

---

## 11. Maintenance

### Regular Audits
- Review files for missing tags (quarterly)
- Validate navigation links (after major refactors)
- Update documentation indices (monthly)
- Check broken links (as part of CI/CD)

### Agent Responsibilities
- Add tags when creating new files
- Update links when refactoring
- Report broken links or missing navigation
- Maintain workspace documentation links

---

## 12. Integration with Existing Protocols

This protocol complements:
- **SSOT_DOMAIN_COORDINATION_PROTOCOL.md** - Domain tagging standards
- **DOCUMENTATION_INDEX.md** - Centralized navigation
- **TASK_DISCOVERY_PROTOCOL.md** - Finding work opportunities
- **V2_COMPLIANCE_GUIDELINES** - Code quality standards

---

## Status

**Version:** 1.0 (Draft)  
**Created:** 2025-12-27  
**Author:** Agent-3  
**Review Status:** Draft - Pending agent review

**Next Steps:**
1. Review with Agent-2 (Architecture) for validation
2. Test with sample files to validate approach
3. Create tooling for automated tag/link validation
4. Integrate into V2 compliance guidelines

