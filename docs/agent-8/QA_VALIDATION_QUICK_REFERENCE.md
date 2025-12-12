# QA Validation Quick Reference Guide

**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Purpose**: Quick reference for QA validation workflow  
**Date**: 2025-12-12

## Quick Commands

### Run Full Codebase Validation
```bash
python scripts/validate_v2_compliance.py --rules config/v2_rules.yaml
```

### Validate Specific Refactored Files
```bash
python scripts/validate_refactored_files.py file1.py file2.py --output-format text
```

### Validate with JSON Output
```bash
python scripts/validate_refactored_files.py file1.py --output-format json
```

### Run Test Suite
```bash
python -m pytest tests/tools/test_validate_refactored_files.py -v
```

## Validation Checklist (Quick)

### Pre-Validation
- [ ] Baseline established (107 violations)
- [ ] Priority files identified
- [ ] Refactoring strategies documented

### During Validation
- [ ] File size ≤300 LOC
- [ ] Function count reasonable
- [ ] Class count reasonable
- [ ] SSOT compliance verified
- [ ] Architecture patterns followed
- [ ] No breaking changes

### Post-Validation
- [ ] Compliance rate calculated
- [ ] Violations documented
- [ ] Findings reported
- [ ] Approval/change requests sent

## Key Metrics

### Baseline (2025-12-12)
- **Total Violations**: 107
- **Critical**: 2 files (>1000 LOC)
- **Major**: 2 files (500-1000 LOC)
- **Moderate**: 2 files (350-500 LOC)
- **Minor**: 4 files (300-350 LOC)
- **Additional**: 97 files

### Target (Post-Refactoring)
- **Violations Reduced**: 10 files (top priority)
- **New Compliant Files**: 32-48 files
- **Compliance Improvement**: ~9.3% reduction

## Top 10 Priority Files

1. `unified_discord_bot.py` - 2,692 lines (8.97x)
2. `github_book_viewer.py` - 1,164 lines (3.88x)
3. `status_change_monitor.py` - 811 lines (2.70x)
4. `swarm_showcase_commands.py` - 650 lines (2.17x)
5. `discord_gui_modals.py` - 600 lines (2.00x)
6. `messaging_commands.py` - 425 lines (1.42x)
7. `discord_service.py` - 386 lines (1.29x)
8. `systems_inventory_commands.py` - 353 lines (1.18x)
9. `discord_embeds.py` - 340 lines (1.13x)
10. `intelligence.py` - 339 lines (1.13x)

## Coordination Points

### Agent-2 (Large Files)
- unified_discord_bot.py
- github_book_viewer.py
- status_change_monitor.py
- swarm_showcase_commands.py

### Agent-7 (Medium Files)
- discord_gui_modals.py
- messaging_commands.py
- discord_service.py
- systems_inventory_commands.py
- discord_embeds.py
- intelligence.py

## Validation Workflow

1. **Initial Review**: Run validation on refactored files
2. **Compliance Check**: Verify ≤300 LOC, function/class counts
3. **SSOT Check**: Validate domain boundaries, configuration
4. **Integration Test**: Coordinate with Agent-1 for testing
5. **Final Validation**: Complete QA checklist, document findings
6. **Report**: Approve or request changes, report to Captain

## File Locations

### Validation Tools
- `scripts/validate_v2_compliance.py` - Full codebase validation
- `scripts/validate_refactored_files.py` - Refactored files validation
- `tests/tools/test_validate_refactored_files.py` - Test suite

### Documentation
- `docs/agent-8/QA_VALIDATION_CHECKLIST_2025-12-12.md` - Full checklist
- `docs/agent-8/V2_COMPLIANCE_VALIDATION_2025-12-12.md` - Baseline
- `docs/agent-8/REFACTORING_READINESS_ASSESSMENT_2025-12-12.md` - Strategies
- `docs/agent-8/COORDINATION_STATUS_REPORT_2025-12-12.md` - Status
- `docs/agent-8/AGENT8_PROGRESS_REPORT_2025-12-12.md` - Progress

### Results
- `validation_results_2025-12-12.txt` - Baseline results
- `validation_run_2025-12-12_15-13.txt` - Progress checkpoint

## V2 Compliance Rules

- **File Size**: Maximum 300 lines
- **Function Size**: Maximum 30 lines
- **Class Size**: Maximum 200 lines
- **Complexity**: Maximum 10 cyclomatic
- **Nesting**: Maximum 3 levels
- **Parameters**: Maximum 5 per function

## Status

✅ **Ready** - All tools and documentation prepared

---

**Quick Access**: Keep this guide handy for fast reference during validation workflow.

