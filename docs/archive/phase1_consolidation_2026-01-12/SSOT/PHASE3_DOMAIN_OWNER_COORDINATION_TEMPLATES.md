# Phase 3 Domain Owner Coordination Message Templates

**Prepared By:** Agent-8 (SSOT & System Integration Specialist)  
**For Use By:** Agent-4 (Captain)  
**Date:** 2025-12-30

<!-- SSOT Domain: documentation -->

---

## High Priority Domain Owner Coordination Messages

### Core Domain - Agent-2 (Architecture & Design)

**Subject:** SSOT Tag Remediation - Core Domain (33 files)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Core Domain

Agent-2 role: Review and fix SSOT tag format/placement issues in 33 core domain files identified in Phase 2 re-validation.

Files Affected: 33 files in core domain
Issue: Tag format, domain registry, or tag placement issues
Priority: HIGH
Action Required: Review invalid files and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tags in all 33 files
- Verification using tools/ssot_tagging_validator.py
- Completion report with file list

Timeline: [To be set after Phase 2 results]
```

### Integration Domain - Agent-1 (Integration)

**Subject:** SSOT Tag Remediation - Integration Domain (3 files)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Integration Domain

Agent-1 role: Review and fix SSOT tag format/placement issues in 3 integration domain files identified in Phase 2 re-validation.

Files Affected: 3 files in integration domain
Issue: Tag format, domain registry, or tag placement issues
Priority: HIGH
Action Required: Review invalid files and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tags in all 3 files
- Verification using tools/ssot_tagging_validator.py
- Completion report with file list

Timeline: [To be set after Phase 2 results]
```

### Infrastructure Domain - Agent-3 (Infrastructure)

**Subject:** SSOT Tag Remediation - Infrastructure Domain (1 file)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Infrastructure Domain

Agent-3 role: Review and fix SSOT tag format/placement issues in 1 infrastructure domain file identified in Phase 2 re-validation.

Files Affected: 1 file in infrastructure domain
Issue: Tag format, domain registry, or tag placement issues
Priority: HIGH
Action Required: Review invalid file and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tag in 1 file
- Verification using tools/ssot_tagging_validator.py
- Completion confirmation

Timeline: [To be set after Phase 2 results]
```

---

## Medium Priority Domain Owner Coordination Messages

### Gaming Domain - Agent-6 (Coordination) [Proposed]

**Subject:** SSOT Tag Remediation - Gaming Domain (4 files)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Gaming Domain

Agent-6 role: Review and fix SSOT tag format/placement issues in 4 gaming domain files identified in Phase 2 re-validation.

Files Affected: 4 files in gaming domain
Issue: Tag format, domain registry, or tag placement issues
Priority: MEDIUM
Action Required: Review invalid files and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tags in all 4 files
- Verification using tools/ssot_tagging_validator.py
- Completion report with file list

Timeline: [To be set after Phase 2 results]
```

### Logging Domain - Agent-3 (Infrastructure) [Proposed]

**Subject:** SSOT Tag Remediation - Logging Domain (2 files)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Logging Domain

Agent-3 role: Review and fix SSOT tag format/placement issues in 2 logging domain files identified in Phase 2 re-validation.

Files Affected: 2 files in logging domain
Issue: Tag format, domain registry, or tag placement issues
Priority: MEDIUM
Action Required: Review invalid files and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tags in all 2 files
- Verification using tools/ssot_tagging_validator.py
- Completion report with file list

Timeline: [To be set after Phase 2 results]
```

### Discord Domain - Agent-6 (Coordination) [Proposed]

**Subject:** SSOT Tag Remediation - Discord Domain (2 files)

**Message Template:**
```
A2A COORDINATION REQUEST: SSOT Tag Remediation - Discord Domain

Agent-6 role: Review and fix SSOT tag format/placement issues in 2 discord domain files identified in Phase 2 re-validation.

Files Affected: 2 files in discord domain
Issue: Tag format, domain registry, or tag placement issues
Priority: MEDIUM
Action Required: Review invalid files and fix SSOT tag format/placement

Expected Deliverables:
- Fixed SSOT tags in all 2 files
- Verification using tools/ssot_tagging_validator.py
- Completion report with file list

Timeline: [To be set after Phase 2 results]
```

---

## SSOT Tag Remediation Guidelines

### Standard Tag Format
```html
<!-- SSOT Domain: domain_name -->
```

### Common Issues and Fixes

1. **Missing Tag:**
   - **Fix:** Add `<!-- SSOT Domain: domain_name -->` to file header or module docstring
   - **Placement:** First line of file or first line of module docstring

2. **Incorrect Format:**
   - **Wrong:** `@domain domain_name` or `SSOT domain: domain_name`
   - **Fix:** Use HTML comment format: `<!-- SSOT Domain: domain_name -->`

3. **Wrong Domain:**
   - **Fix:** Verify domain matches file purpose using `docs/SSOT_DOMAIN_MAPPING.md`
   - **Update:** Change to correct domain if needed

4. **Tag Placement:**
   - **Fix:** Move tag to file header (first 20 lines) or module docstring

### Validation Tool

Use `tools/ssot_tagging_validator.py` to verify fixes:
```bash
python tools/ssot_tagging_validator.py --directory <directory> --output validation_report.json
```

---

## Coordination Checklist

### Pre-Coordination
- [x] Phase 2 re-validation executed
- [x] Validation results available
- [ ] Invalid files identified and categorized by domain
- [ ] Domain owners confirmed
- [ ] File lists prepared for each domain owner

### Coordination Execution
- [ ] High priority messages sent (core, integration, infrastructure)
- [ ] Medium priority messages sent (gaming, logging, discord)
- [ ] Owner confirmations received
- [ ] Task deadlines communicated
- [ ] Progress tracking setup

### Post-Coordination
- [ ] Remediation progress monitored
- [ ] Completion verified using validation tool
- [ ] Final validation executed
- [ ] Milestone closure completed

---

## References

- **Phase 3 Task Assignment Template:** `docs/SSOT/PHASE3_TASK_ASSIGNMENT_TEMPLATE.md`
- **SSOT Domain Mapping:** `docs/SSOT_DOMAIN_MAPPING.md`
- **Validation Tool:** `tools/ssot_tagging_validator.py`
- **Coordination Summary:** `docs/SSOT/COORDINATION_SUMMARY.md`

---

**Documentation Created:** 2025-12-30 by Agent-8  
**Status:** Ready for use after Phase 2 validation results

