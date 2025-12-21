<!-- SSOT Domain: documentation -->

# Agent-2 Reporting Standards

**Purpose**: Ensure all Agent-2 reports are truthful, verifiable, and aligned with SSOT principles.

**Effective Date**: 2025-12-13  
**Author**: Agent-2 (Architecture & Design Specialist)

---

## Core Principles

### 1. Truthfulness
- **All claims must be verifiable**
- **Evidence links required for every artifact**
- **No unsubstantiated statements**
- **Openly state limitations and missing information**

### 2. Scope Tags
- **Every report must include SSOT domain scope tag**
- **Format**: `<!-- SSOT Domain: domain_name -->` at top of file
- **Artifacts must include scope tags in artifact list**

### 3. Evidence Links
- **All artifacts must have verifiable links**
- **Include commit hash for version tracking**
- **Include line count for size verification**
- **Format**: `[`label`](path) (commit: `hash`, lines: count)`

---

## Required Report Sections

### Header
```markdown
<!-- SSOT Domain: domain_name -->
# Report Title

**Agent**: Agent-2 (Architecture & Design Specialist)
**Date**: YYYY-MM-DD
**Status**: ✅ / 🟡 / ❌
```

### Executive Summary
- Brief overview (2-3 sentences)
- Key objectives
- Current status

### Findings / Results
- Structured findings
- Evidence-backed claims
- Clear limitations stated

### Actions Taken
- Numbered list of actions
- Status indicators (✅ 🟡 ⏳ ❌)
- Brief descriptions

### Artifacts Created
- **MANDATORY**: Evidence links with commit hashes
- **MANDATORY**: Line counts
- **MANDATORY**: Scope tags per artifact
- Format: See template

### Verification & Evidence
- **MANDATORY**: List of claims made
- **MANDATORY**: Evidence links section
- **MANDATORY**: Verification instructions
- **MANDATORY**: How to verify each claim

### Status
- Clear completion status
- Blockers listed (if any)
- Next steps

---

## Using the Report Enhancer Tool

### Basic Usage
```bash
python tools/report_truthfulness_enhancer.py \
    path/to/report.md \
    --artifacts "label1:path/to/file1.py" "label2:path/to/file2.json" \
    --scope domain_name \
    --claims path/to/claims.json
```

### Artifacts Format
- Simple: `path/to/file.ext` (uses filename as label)
- With label: `Label Name:path/to/file.ext`

### Scope Options
- `infrastructure` - Infrastructure work
- `integration` - Integration work
- `communication` - Messaging/communication
- `architecture` - Architecture/design
- `web` - Web/WordPress work
- `analytics` - Analytics/analysis
- `core` - Core system work
- `tools` - Tooling/utilities
- `documentation` - Documentation

### Claims File Format
```json
[
  "Claim 1 that can be verified",
  "Claim 2 with evidence",
  "Claim 3 that requires proof"
]
```

---

## Evidence Link Standards

### Required Components
1. **File path** (relative to repo root)
2. **Commit hash** (short form, 12 chars)
3. **Line count** (verified at generation time)
4. **Scope tag** (SSOT domain)

### Format Example
```markdown
[`audit_tool.py`](tools/audit_tool.py) (commit: `abc123def456`, 647 lines) <!-- SSOT Domain: web -->
```

### Verification
- Link must be clickable in rendered markdown
- Commit hash must be verifiable via `git log`
- Line count must match actual file
- Path must exist relative to repo root

---

## Truthfulness Checklist

Before publishing a report, verify:

- [ ] Scope tag present at top of file
- [ ] All artifacts have evidence links
- [ ] All commit hashes are valid
- [ ] All line counts are accurate
- [ ] Claims are listed in verification section
- [ ] Verification instructions are clear
- [ ] Limitations and missing info are stated
- [ ] No unsubstantiated claims

---

## Automated Enhancement

Use the report enhancer tool to automatically:
1. Add scope tags
2. Create evidence links with commit hashes
3. Verify line counts
4. Generate verification section
5. Ensure compliance with standards

---

## Examples

See:
- `docs/blog/WORDPRESS_BLOG_AUDIT_REPORT_2025-12-13.md` - Enhanced example
- `docs/AGENT2_REPORT_TEMPLATE.md` - Template

---

## Enforcement

**Agent-2 Responsibility**: All reports must meet these standards before publication.

**Review Process**: 
1. Run enhancer tool
2. Verify all evidence links work
3. Confirm commit hashes are valid
4. Check scope tags are correct

---

**Status**: ✅ **Standards Documented** - Ready for implementation

🐝 **WE. ARE. SWARM. ⚡🔥**
