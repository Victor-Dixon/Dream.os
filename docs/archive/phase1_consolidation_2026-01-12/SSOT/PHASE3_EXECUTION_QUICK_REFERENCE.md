# Phase 3 Execution Quick Reference

**For:** Agent-4 (Captain)  
**Prepared By:** Agent-8 (SSOT & System Integration Specialist)  
**Date:** 2025-12-30  
**Status:** Ready for Immediate Execution

<!-- SSOT Domain: documentation -->

---

## 🚀 Execution Checklist

### Pre-Execution (5 minutes)
- [ ] Review `docs/SSOT/PHASE3_READY_TO_SEND_MESSAGES.md`
- [ ] Assign TBD owners (Logging 2 files, Discord 1 file)
- [ ] Open progress tracker: `docs/SSOT/PHASE3_PROGRESS_TRACKER.md`

### Execution (30-60 minutes)
- [ ] Send high priority assignments (34 files)
  - [ ] Agent-2: 30 files (Core 29 + Domain 1)
  - [ ] Agent-1: 3 files (Integration)
  - [ ] Agent-3: 2 files (Infrastructure)
- [ ] Send medium priority assignments (8 files)
  - [ ] Agent-3: 3 files (Safety)
  - [ ] Agent-5: 2 files (Data 1 + Trading Robot 1)
  - [ ] Agent-2: 1 file (Domain)
  - [ ] TBD: 2 files (Logging) - assign owner first
  - [ ] TBD: 1 file (Discord) - assign owner first
- [ ] Update progress tracker as assignments sent

### Post-Execution Monitoring
- [ ] Track progress updates from domain owners
- [ ] Monitor validation checkpoints
- [ ] Coordinate re-validation after completion

---

## 📋 Assignment Quick Reference

### High Priority (34 files) - Execute First

| Owner | Files | Domain | File List | ETA |
|-------|-------|--------|-----------|-----|
| Agent-2 | 29 | Core | `docs/SSOT/PHASE3_FILE_LISTS/core_files.md` | 2-3 hours |
| Agent-1 | 3 | Integration | `docs/SSOT/PHASE3_FILE_LISTS/integration_files.md` | 30 min |
| Agent-3 | 2 | Infrastructure | `docs/SSOT/PHASE3_FILE_LISTS/infrastructure_files.md` | 30 min |

### Medium Priority (8 files) - Execute After High Priority

| Owner | Files | Domain | File List | ETA |
|-------|-------|--------|-----------|-----|
| Agent-3 | 3 | Safety | `docs/SSOT/PHASE3_FILE_LISTS/safety_files.md` | 1 hour |
| Agent-5 | 1 | Data | `docs/SSOT/PHASE3_FILE_LISTS/data_files.md` | 15 min |
| Agent-5 | 1 | Trading Robot | `docs/SSOT/PHASE3_FILE_LISTS/trading_robot_files.md` | 15 min |
| Agent-2 | 1 | Domain | `docs/SSOT/PHASE3_FILE_LISTS/domain_files.md` | 15 min |
| **TBD** | 2 | Logging | `docs/SSOT/PHASE3_FILE_LISTS/logging_files.md` | 30 min |
| **TBD** | 1 | Discord | `docs/SSOT/PHASE3_FILE_LISTS/discord_files.md` | 15 min |

---

## 📨 Ready-to-Send Messages

**Location:** `docs/SSOT/PHASE3_READY_TO_SEND_MESSAGES.md`

**Contains:**
- Copy-paste ready A2A messages for each domain owner
- File counts, file list references, issue types
- Action items, validation instructions, ETAs
- Coordination checklists

**Usage:**
1. Open `docs/SSOT/PHASE3_READY_TO_SEND_MESSAGES.md`
2. Copy message for target agent
3. Send via messaging CLI
4. Update progress tracker

---

## 📊 Progress Tracking

**Location:** `docs/SSOT/PHASE3_PROGRESS_TRACKER.md`

**Update When:**
- Assignment sent → Mark "Assignment sent" checkbox
- Progress update received → Update "In Progress" count
- Files fixed → Mark "Files fixed" checkbox
- Validation verified → Mark "Validation verified" checkbox

**Validation Checkpoints:**
1. **High Priority Completion:** 34/34 files (0% → Target: 100%)
2. **Medium Priority Completion:** 8/8 files (0% → Target: 100%)
3. **Final Validation:** 1,309/1,369 files (95.62% → Target: 100%)

---

## 🔧 Validation Tool

**Command:**
```bash
python tools/validate_all_ssot_files.py
```

**Expected Result:**
- All assigned files show `"valid": true`
- Final validation: 1,369/1,369 files valid (100%)

---

## 📚 Key Documents

| Document | Purpose | Location |
|----------|---------|----------|
| **Ready-to-Send Messages** | Copy-paste A2A messages | `docs/SSOT/PHASE3_READY_TO_SEND_MESSAGES.md` |
| **Progress Tracker** | Real-time progress monitoring | `docs/SSOT/PHASE3_PROGRESS_TRACKER.md` |
| **Execution Summary** | Complete file breakdown | `docs/SSOT/PHASE3_EXECUTION_SUMMARY.md` |
| **File Lists** | Domain-specific file lists | `docs/SSOT/PHASE3_FILE_LISTS/` |
| **Complete Summary** | Phase 1-3 documentation | `docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETE_SUMMARY.md` |

---

## ⚡ Quick Commands

### Send A2A Message
```bash
python -m src.services.messaging_cli --agent Agent-X \
  --message "[message content]" \
  --category a2a --sender Agent-4 --tags coordination-reply
```

### Run Validation
```bash
python tools/validate_all_ssot_files.py
```

### Check Progress
```bash
# View progress tracker
cat docs/SSOT/PHASE3_PROGRESS_TRACKER.md
```

---

## 🎯 Success Criteria

- [ ] All 34 high priority files fixed and validated
- [ ] All 8 medium priority files fixed and validated
- [ ] All 3 TBD owner files assigned and fixed
- [ ] Final validation: 1,369/1,369 files valid (100%)
- [ ] Completion milestone report generated
- [ ] MASTER_TASK_LOG updated

---

## 📞 Coordination Flow

1. **Review** ready-to-send messages
2. **Assign** TBD owners (Logging, Discord)
3. **Send** high priority assignments (34 files)
4. **Send** medium priority assignments (8 files)
5. **Track** progress using progress tracker
6. **Monitor** validation checkpoints
7. **Coordinate** re-validation after completion

---

**Status:** Ready for Immediate Execution  
**Last Updated:** 2025-12-30 by Agent-8  
**Next Action:** CAPTAIN executes Phase 3 assignments using ready-to-send messages

