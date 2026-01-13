# Documentation Navigation Enhancement Protocol

**Author:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-27  
**Status:** ACTIVE - Navigation Enhancement Standard  
**Purpose:** Standardize documentation tagging, linking, and navigation for easy agent discovery

<!-- SSOT Domain: documentation -->

---

## Executive Summary

This protocol defines standards for documentation tagging, cross-referencing, and navigation to enable agents to easily find and navigate project documentation and code. It establishes consistent patterns for file references, topic tags, and navigation structures.

**Goal:** Zero-friction documentation discovery and navigation  
**Standard:** Consistent tagging and linking across all documentation  
**Implementation:** Progressive enhancement of existing documentation

---

## Documentation Tagging Standards

### 1. SSOT Domain Tags

**Format:** HTML comment at top of file

```html
<!-- SSOT Domain: documentation -->
```

**Purpose:** Categorize documentation by SSOT domain for domain-specific discovery

**Examples:**
- `<!-- SSOT Domain: documentation -->` - Documentation files
- `<!-- SSOT Domain: architecture -->` - Architecture documents
- `<!-- SSOT Domain: integration -->` - Integration documentation
- `<!-- SSOT Domain: web -->` - Web/WordPress documentation

**Location:** First 10 lines of file (after frontmatter if present)

---

### 2. Topic Tags

**Format:** YAML frontmatter or markdown comment

```yaml
---
tags:
  - trading-robot
  - api
  - documentation
  - operations
---
```

**Or inline comment:**
```markdown
<!-- Tags: trading-robot, api, documentation, operations -->
```

**Purpose:** Enable topic-based discovery and filtering

**Common Tags:**
- `trading-robot` - Trading robot related
- `api` - API documentation
- `wordpress` - WordPress related
- `deployment` - Deployment guides
- `operations` - Operations/runbooks
- `architecture` - Architecture documentation
- `integration` - Integration guides
- `v2-compliance` - V2 compliance related
- `ssot` - SSOT domain related
- `onboarding` - Onboarding documentation

---

### 3. File Reference Tags

**Format:** Standardized file path references

**Pattern:** `[Description](relative/path/to/file.md)`

**Examples:**
- `[API Documentation](docs/trading_robot/API_DOCUMENTATION.md)`
- `[Operations Runbook](docs/trading_robot/OPERATIONS_RUNBOOK.md)`
- `[SSOT Domain Mapping](docs/SSOT_DOMAIN_MAPPING.md)`

**Purpose:** Enable clickable navigation between related documents

---

## Cross-Reference Standards

### 1. Related Documents Section

**Standard Location:** End of document, before "References" section

**Format:**
```markdown
## Related Documents

- **[Document Title](path/to/file.md)** - Brief description
- **[Another Document](path/to/file.md)** - Brief description
```

**Example:**
```markdown
## Related Documents

- **[Trading Robot API Documentation](docs/trading_robot/API_DOCUMENTATION.md)** - Complete API endpoint documentation
- **[Trading Robot Operations Runbook](docs/trading_robot/OPERATIONS_RUNBOOK.md)** - Operations procedures and troubleshooting
- **[Trading Robot Deployment Guide](docs/trading_robot/DEPLOYMENT_GUIDE.md)** - Deployment procedures and checklist
```

---

### 2. References Section

**Standard Location:** End of document

**Format:**
```markdown
## References

- **[Reference Title](path/to/file.md)** - Description
- **[External Link](https://example.com)** - External resource
```

**Example:**
```markdown
## References

- **Operations Runbook:** `docs/trading_robot/OPERATIONS_RUNBOOK.md`
- **API Documentation:** `docs/trading_robot/API_DOCUMENTATION.md`
- **Main README:** `README.md`
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
```

---

### 3. See Also Links

**Format:** Inline references within document content

**Pattern:** `See [Document Title](path/to/file.md) for details.`

**Example:**
```markdown
For detailed API endpoint documentation, see [API Documentation](docs/trading_robot/API_DOCUMENTATION.md).

For deployment procedures, see [Deployment Guide](docs/trading_robot/DEPLOYMENT_GUIDE.md).
```

---

## Navigation Structure Standards

### 1. Documentation Index

**File:** `docs/DOCUMENTATION_INDEX.md`

**Structure:**
- Categorized by topic/domain
- Alphabetical within categories
- Links to all documentation files
- Brief descriptions for each document

**Update Frequency:** After major documentation additions

---

### 2. Domain-Specific Indexes

**Pattern:** `docs/{domain}/INDEX.md`

**Examples:**
- `docs/trading_robot/INDEX.md` - Trading robot documentation index
- `docs/website_audits/INDEX.md` - Website audit documentation index
- `docs/messaging/INDEX.md` - Messaging system documentation index

**Purpose:** Domain-specific navigation for focused discovery

---

### 3. Quick Reference Cards

**Pattern:** `docs/{topic}_QUICK_REFERENCE.md`

**Examples:**
- `docs/API_QUICK_REFERENCE.md` - Quick API endpoint reference
- `docs/DEPLOYMENT_QUICK_REFERENCE.md` - Quick deployment checklist
- `docs/TROUBLESHOOTING_QUICK_REFERENCE.md` - Common issues and solutions

**Purpose:** One-page quick reference for common tasks

---

## File Naming Conventions

### Standard Patterns

1. **Topic-Based:**
   - `{TOPIC}_DOCUMENTATION.md` - Main documentation
   - `{TOPIC}_GUIDE.md` - How-to guide
   - `{TOPIC}_REFERENCE.md` - Reference documentation
   - `{TOPIC}_QUICK_REFERENCE.md` - Quick reference

2. **Date-Based (Reports/Audits):**
   - `{TOPIC}_YYYY-MM-DD.md` - Date-specific reports
   - `{TOPIC}_REPORT_YYYY-MM-DD.md` - Formal reports

3. **Agent-Based:**
   - `AGENT{X}_{TOPIC}_{DATE}.md` - Agent-specific documentation

4. **Status-Based:**
   - `{TOPIC}_COMPLETE.md` - Completion documentation
   - `{TOPIC}_PLAN.md` - Planning documentation
   - `{TOPIC}_STATUS.md` - Status documentation

---

## Documentation Metadata Standards

### Required Metadata

**Location:** Top of file (after SSOT domain tag)

**Format:**
```markdown
**Author:** Agent-X (Role)  
**Date:** YYYY-MM-DD  
**Status:** ACTIVE | ARCHIVED | DRAFT  
**Purpose:** Brief description  
**Last Updated:** YYYY-MM-DD by Agent-X
```

**Example:**
```markdown
**Author:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-27  
**Status:** ACTIVE  
**Purpose:** Complete API documentation for Trading Robot REST and WebSocket endpoints  
**Last Updated:** 2025-12-27 by Agent-2
```

---

### Optional Metadata

**Tags:** Topic tags (see above)  
**Related:** Related document paths  
**Supersedes:** Document this replaces (if applicable)  
**See Also:** Additional references

---

## Implementation Guidelines

### 1. Progressive Enhancement

**Approach:** Enhance existing documentation incrementally

**Priority:**
1. High-traffic documentation (API docs, runbooks, guides)
2. Recently created documentation
3. Documentation with many cross-references
4. Domain-specific documentation

---

### 2. Consistency Checks

**Before Creating New Documentation:**
- [ ] Check for existing similar documentation
- [ ] Use consistent naming convention
- [ ] Add SSOT domain tag
- [ ] Add topic tags
- [ ] Include metadata header
- [ ] Add cross-references to related docs
- [ ] Update relevant indexes

---

### 3. Maintenance

**Regular Tasks:**
- Update DOCUMENTATION_INDEX.md after major additions
- Verify cross-references are valid (no broken links)
- Update "Last Updated" dates when modifying
- Archive outdated documentation
- Consolidate duplicate documentation

---

## Navigation Tools

### 1. Documentation Scanner

**Tool:** `tools/scan_documentation.py` (to be created)

**Purpose:** Scan documentation for:
- SSOT domain tags
- Topic tags
- Cross-references
- Broken links
- Missing metadata

---

### 2. Documentation Index Generator

**Tool:** `tools/generate_documentation_index.py` (to be created)

**Purpose:** Auto-generate DOCUMENTATION_INDEX.md from:
- File structure
- SSOT domain tags
- Topic tags
- Metadata headers

---

### 3. Link Validator

**Tool:** `tools/validate_documentation_links.py` (to be created)

**Purpose:** Validate all cross-references:
- Check file existence
- Verify relative paths
- Report broken links
- Suggest corrections

---

## Examples

### Example 1: Well-Tagged Documentation

```markdown
<!-- SSOT Domain: documentation -->

# Trading Robot API Documentation

**Author:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-27  
**Status:** ACTIVE  
**Purpose:** Complete API documentation for Trading Robot REST and WebSocket endpoints  
**Tags:** trading-robot, api, documentation  
**Last Updated:** 2025-12-27 by Agent-2

---

## Overview

[Content...]

## Related Documents

- **[Trading Robot Operations Runbook](docs/trading_robot/OPERATIONS_RUNBOOK.md)** - Operations procedures
- **[Trading Robot Deployment Guide](docs/trading_robot/DEPLOYMENT_GUIDE.md)** - Deployment procedures

## References

- **Operations Runbook:** `docs/trading_robot/OPERATIONS_RUNBOOK.md`
- **Main README:** `README.md`
```

---

### Example 2: Cross-Reference Usage

```markdown
For detailed API endpoint documentation, see [API Documentation](docs/trading_robot/API_DOCUMENTATION.md).

For deployment procedures, see [Deployment Guide](docs/trading_robot/DEPLOYMENT_GUIDE.md).

For troubleshooting, see [Operations Runbook - Troubleshooting](docs/trading_robot/OPERATIONS_RUNBOOK.md#troubleshooting).
```

---

## Checklist for New Documentation

- [ ] Add SSOT domain tag at top
- [ ] Add metadata header (Author, Date, Status, Purpose)
- [ ] Add topic tags (YAML frontmatter or comment)
- [ ] Use consistent file naming convention
- [ ] Add "Related Documents" section
- [ ] Add "References" section
- [ ] Include cross-references to related docs
- [ ] Update DOCUMENTATION_INDEX.md
- [ ] Update domain-specific index (if applicable)
- [ ] Verify all links are valid

---

## References

- **SSOT Domain Mapping:** `docs/SSOT_DOMAIN_MAPPING.md`
- **Documentation Index:** `docs/DOCUMENTATION_INDEX.md`
- **V2 Compliance Guidelines:** `docs/V2_COMPLIANCE_GUIDELINES_UPDATE.md`

---

**Last Updated:** 2025-12-27 by Agent-2  
**Status:** ✅ ACTIVE - Navigation Enhancement Protocol  
**Next Review:** After implementation of navigation tools

