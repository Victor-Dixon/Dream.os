# Phase 5: StatusChangeMonitor Migration Plan

**Date:** 2025-12-31  
**Coordinated By:** Agent-3 (Implementation) + Agent-4 (Validation)  
**Priority:** CRITICAL (Highest Risk - Touches Discord Bot Integration)  
**Status:** Design Review Phase

---

## 🎯 Mission

Migrate `StatusChangeMonitor` to use unified status reading library (`src/core/agent_status/`) while maintaining zero Discord bot disruption.

---

## 🚨 CRITICAL CONSTRAINTS

**StatusChangeMonitor is INTEGRATED with Discord bot lifecycle:**
- Uses `discord.ext.tasks` for async monitoring loop
- Starts automatically with bot (`setup_status_monitor()`)
- Posts real-time updates to Discord channels
- **ANY BREAKING CHANGES WILL DISABLE STATUS UPDATES**

**Safety Requirements:**
1. ✅ **Backward Compatibility:** Must continue working during migration
2. ✅ **Zero Downtime:** Changes must be additive, not replacement
3. ✅ **Async Compatibility:** Library is sync, must wrap for async use
4. ✅ **Discord Bot Testing:** Extensive validation after migration

---

## 📋 Current Implementation Analysis

### StatusChangeMonitor Integration Points:

1. **File Reading (Lines 123-159):**
   - Direct file reading in `_check_files()` method
   - Uses `asyncio.to_thread()` for non-blocking stat
   - Calls `_read_json_with_retry()` for JSON reading

2. **File Change Detection (Lines 134-156):**
   - Manual `mtime` comparison
   - Stores `last_modified` and `last_status` in memory
   - Detects changes via `_detect_changes()` method

3. **JSON Reading (Lines 161-177):**
   - `_read_json_with_retry()` with 3 retry attempts
   - Uses `asyncio.to_thread()` for async compatibility
   - Handles JSON decode errors

4. **Bot Lifecycle Integration:**
   - `setup_status_monitor()` function called during bot startup
   - `start_monitoring()` starts `@tasks.loop` decorator
   - `before_monitor()` waits for bot readiness

---

## 🔄 Migration Strategy

### Step 1: Add Unified Library Imports (Additive)
- Import `AgentStatusReader` from `src.core.agent_status.reader`
- Import `StatusFileWatcher` from `src.core.agent_status.watcher`
- Keep existing code intact (backward compatible)

### Step 2: Create Async Wrapper for Unified Library
- Create `_async_read_status()` method that wraps `AgentStatusReader.read_status()`
- Use `asyncio.to_thread()` to make sync library async-compatible
- Maintain retry logic compatibility

### Step 3: Replace File Reading Logic
- Replace `_read_json_with_retry()` calls with unified library
- Use `AgentStatusReader.read_status()` instead of direct JSON reading
- Maintain error handling and retry logic

### Step 4: Replace File Change Detection
- Replace manual `mtime` comparison with `StatusFileWatcher`
- Use watcher's `check_changes()` method
- Maintain debouncing logic (watcher doesn't handle debouncing)

### Step 5: Maintain Existing Functionality
- Keep debouncing logic intact
- Keep dashboard update logic
- Keep inactivity check hooks
- Keep Discord posting logic

---

## 🛠️ Implementation Plan

### Phase 5a: Preparation (Agent-3)
**Duration:** 30 minutes

1. Review StatusChangeMonitor code structure
2. Identify all file reading locations
3. Create async wrapper functions for unified library
4. Test async wrapper in isolation

**Deliverables:**
- Async wrapper functions
- Unit tests for async wrappers

---

### Phase 5b: Migration - File Reading (Agent-3)
**Duration:** 1-2 hours

1. Add unified library imports
2. Replace `_read_json_with_retry()` with `AgentStatusReader`
3. Update `_check_files()` to use unified reader
4. Maintain async compatibility with `asyncio.to_thread()`
5. Test file reading functionality

**Safety Checkpoints:**
- ✅ Agent-4 validates: Discord bot starts correctly
- ✅ Agent-4 validates: Status updates still post
- ✅ Agent-4 validates: No performance degradation

**Deliverables:**
- Migrated file reading logic
- Validation test results

---

### Phase 5c: Migration - File Change Detection (Agent-3)
**Duration:** 1-2 hours

1. Replace manual `mtime` comparison with `StatusFileWatcher`
2. Integrate watcher's `check_changes()` method
3. Maintain debouncing logic (watcher doesn't debounce)
4. Test change detection accuracy

**Safety Checkpoints:**
- ✅ Agent-4 validates: Change detection works correctly
- ✅ Agent-4 validates: Debouncing still works
- ✅ Agent-4 validates: Status updates post correctly

**Deliverables:**
- Migrated change detection logic
- Validation test results

---

### Phase 5d: Extensive Validation (Agent-4)
**Duration:** 1-2 hours

1. Execute comprehensive validation suite:
   - Discord bot starts correctly
   - Status updates post to Discord
   - Debouncing works
   - Inactivity detection works
   - No performance degradation
   - Change detection accuracy
   - Error handling
   - Retry logic

2. Monitor Discord bot for 30 minutes
3. Verify all status updates post correctly
4. Check for any errors in logs

**Deliverables:**
- Extensive validation report
- Performance benchmarks
- Error log analysis

---

### Phase 5e: Code Review (Agent-2)
**Duration:** 30 minutes

1. Review migration code for safety
2. Validate architecture compliance
3. Check for potential issues
4. Approve or request changes

**Deliverables:**
- Code review report
- Approval or change requests

---

## 🔒 Safety Protocols

### Before Migration:
1. **Agent-4 validates:** Discord bot is running correctly
2. **Agent-4 validates:** StatusChangeMonitor is posting updates
3. **Agent-4 establishes:** Baseline metrics (update frequency, performance)
4. **Agent-2 reviews:** Migration plan for safety

### During Migration:
1. **Agent-3:** Create feature branch for Phase 5
2. **Agent-3:** Test changes in isolation
3. **Agent-3:** Run unit tests
4. **Agent-3:** Test async wrappers
5. **Agent-4:** Validate after each sub-phase (5b, 5c)

### After Migration:
1. **Agent-4:** Execute extensive validation suite
2. **Agent-4:** Monitor Discord bot for 30 minutes
3. **Agent-4:** Verify all status updates post correctly
4. **Agent-4:** Check for any errors in logs
5. **Agent-2:** Review code for safety
6. **All:** Approve before production deployment

### Rollback Plan:
- If Discord bot breaks: Immediately revert to previous working state
- If status updates stop: Revert StatusChangeMonitor changes
- If performance degrades: Revert and investigate
- If change detection fails: Revert and investigate

---

## 📊 Success Metrics

### Phase 5a (Preparation):
- ✅ Async wrapper functions created
- ✅ Unit tests pass
- ✅ No Discord bot disruption

### Phase 5b (File Reading Migration):
- ✅ File reading uses unified library
- ✅ Async compatibility maintained
- ✅ Status updates still post
- ✅ No performance degradation

### Phase 5c (Change Detection Migration):
- ✅ Change detection uses unified watcher
- ✅ Debouncing still works
- ✅ Status updates post correctly
- ✅ Change detection accuracy maintained

### Phase 5d (Extensive Validation):
- ✅ All validation checkpoints pass
- ✅ Discord bot works correctly
- ✅ Status updates post correctly
- ✅ No errors in logs
- ✅ Performance maintained or improved

### Phase 5e (Code Review):
- ✅ Code review approved
- ✅ Architecture compliance confirmed
- ✅ No safety concerns identified

---

## 🎯 Next Steps

1. **Agent-3 + Agent-4:** Coordinate Phase 5 design review (NOW)
2. **Agent-3:** Implement Phase 5a (Preparation) - 30 min
3. **Agent-3:** Implement Phase 5b (File Reading) - 1-2 hours
4. **Agent-4:** Validate Phase 5b - 15-30 min
5. **Agent-3:** Implement Phase 5c (Change Detection) - 1-2 hours
6. **Agent-4:** Validate Phase 5c - 15-30 min
7. **Agent-4:** Execute Phase 5d (Extensive Validation) - 1-2 hours
8. **Agent-2:** Execute Phase 5e (Code Review) - 30 min
9. **All:** Approve production deployment

---

## 📝 Notes

- **Async Compatibility:** Unified library is sync, must wrap with `asyncio.to_thread()` for async use
- **Debouncing:** Watcher doesn't handle debouncing - maintain existing debouncing logic
- **Error Handling:** Maintain existing retry logic and error handling
- **Performance:** Monitor performance closely - unified library may have different performance characteristics
- **Testing:** Extensive testing required - this is the highest risk phase

---

**Last Updated:** 2025-12-31 07:16 UTC  
**Status:** Design Review Phase - Awaiting Agent-3 + Agent-4 coordination

