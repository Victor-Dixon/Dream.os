# Cycle Snapshot System - Code Review Checklist

**Date:** 2025-12-31  
**For:** Agent-2 (Architecture & Design Specialist)  
**Coordinated With:** Agent-3 (Infrastructure & DevOps Specialist)  
**Status:** Active - Use at Each Checkpoint

---

## 🎯 Code Review Purpose

**Ensure:**
- V2 compliance (file size, function size, type hints)
- Architecture alignment (modular design, separation of concerns)
- Safety (error handling, validation, logging)
- Code quality (readability, maintainability, documentation)

---

## 📋 Checkpoint 1: After Module 2 (Core Models)

**File:** `tools/cycle_snapshots/core/snapshot_models.py`

### Architecture Review
- [ ] Dataclasses properly defined
- [ ] Type hints on all fields
- [ ] Clear separation of concerns
- [ ] Models match architecture design

### V2 Compliance
- [ ] File <400 lines
- [ ] All functions <30 lines
- [ ] Type hints on all functions
- [ ] Proper docstrings

### Code Quality
- [ ] Clear naming conventions
- [ ] Proper imports
- [ ] No circular dependencies
- [ ] Documentation complete

### Safety
- [ ] Error handling for invalid data
- [ ] Validation logic (if applicable)
- [ ] Logging (if applicable)

**Review Notes:**
```
[Agent-2 fills in here]
```

**Status:** ⬜ Pending | ✅ Approved | 🟡 Needs Changes | ❌ Rejected

---

## 📋 Checkpoint 2: After Modules 3-5 (Data Collectors)

**Files:**
- `tools/cycle_snapshots/data_collectors/agent_status_collector.py`
- `tools/cycle_snapshots/data_collectors/task_log_collector.py`
- `tools/cycle_snapshots/data_collectors/git_collector.py`

### Architecture Review
- [ ] Modular design (each collector independent)
- [ ] Clear separation of concerns
- [ ] Proper integration patterns (MCP fallback)
- [ ] Error isolation (one collector failure doesn't break others)

### V2 Compliance
- [ ] Each file <400 lines
- [ ] All functions <30 lines
- [ ] Type hints on all functions
- [ ] Proper docstrings

### Integration Patterns
- [ ] MCP integration with graceful degradation
- [ ] File system integration (fallback)
- [ ] Error handling for missing dependencies
- [ ] Logging for integration failures

### Code Quality
- [ ] Clear naming conventions
- [ ] Proper error messages
- [ ] Consistent return types
- [ ] Documentation complete

### Safety
- [ ] Error handling for missing files
- [ ] Error handling for invalid JSON
- [ ] Error handling for git failures
- [ ] Logging for all errors

**Review Notes:**
```
[Agent-2 fills in here]
```

**Status:** ⬜ Pending | ✅ Approved | 🟡 Needs Changes | ❌ Rejected

---

## 📋 Checkpoint 3: After Modules 6-7 (Aggregation & Reports)

**Files:**
- `tools/cycle_snapshots/aggregators/snapshot_aggregator.py`
- `tools/cycle_snapshots/processors/report_generator.py`

### Architecture Review
- [ ] Aggregator properly combines data
- [ ] Report generator uses aggregated data
- [ ] Clear separation of concerns
- [ ] Proper data flow

### V2 Compliance
- [ ] Each file <400 lines
- [ ] Functions <30 lines (where possible)
- [ ] Type hints on all functions
- [ ] Proper docstrings

### Code Quality
- [ ] Clear naming conventions
- [ ] Proper error handling
- [ ] Consistent formatting
- [ ] Documentation complete

### Safety
- [ ] Error handling for missing data
- [ ] Error handling for invalid data
- [ ] Validation of aggregated data
- [ ] Logging for errors

### Report Quality
- [ ] Markdown format correct
- [ ] All sections included
- [ ] Proper formatting
- [ ] Readable output

**Review Notes:**
```
[Agent-2 fills in here]
```

**Status:** ⬜ Pending | ✅ Approved | 🟡 Needs Changes | ❌ Rejected

---

## 📋 Checkpoint 4: After Module 8 (CLI)

**File:** `tools/cycle_snapshots/main.py`

### Architecture Review
- [ ] Proper CLI argument parsing
- [ ] Clear integration flow
- [ ] Proper error handling
- [ ] Clean exit codes

### V2 Compliance
- [ ] File <400 lines
- [ ] Functions <30 lines (where possible)
- [ ] Type hints on all functions
- [ ] Proper docstrings

### CLI Quality
- [ ] Clear argument names
- [ ] Helpful help text
- [ ] Proper error messages
- [ ] Consistent output format

### Integration Flow
- [ ] Data collectors called correctly
- [ ] Aggregator called correctly
- [ ] Report generator called correctly
- [ ] Files saved correctly

### Safety
- [ ] Error handling for all operations
- [ ] Proper logging
- [ ] Clean error messages
- [ ] Exit codes correct

**Review Notes:**
```
[Agent-2 fills in here]
```

**Status:** ⬜ Pending | ✅ Approved | 🟡 Needs Changes | ❌ Rejected

---

## 📋 Checkpoint 5: After Module 9 (Tests)

**File:** `tests/unit/test_cycle_snapshots_phase1.py`

### Test Coverage
- [ ] All modules tested
- [ ] Edge cases covered
- [ ] Error cases covered
- [ ] Integration tests included

### Test Quality
- [ ] Clear test names
- [ ] Proper test structure
- [ ] Good assertions
- [ ] Proper fixtures/mocks

### Test Execution
- [ ] All tests pass
- [ ] Tests run quickly
- [ ] Tests are isolated
- [ ] No flaky tests

**Review Notes:**
```
[Agent-2 fills in here]
```

**Status:** ⬜ Pending | ✅ Approved | 🟡 Needs Changes | ❌ Rejected

---

## 🔄 Review Process

### Step 1: Agent-3 Requests Review
Agent-3 completes module(s) and requests review:
```
"Checkpoint X complete - ready for review: [list of files]"
```

### Step 2: Agent-2 Reviews
Agent-2 reviews code using this checklist:
- Read all files
- Check V2 compliance
- Check architecture alignment
- Check safety measures
- Fill in review notes

### Step 3: Agent-2 Provides Feedback
Agent-2 provides feedback:
- ✅ Approved: Continue to next module
- 🟡 Needs Changes: Specific changes required
- ❌ Rejected: Major issues, needs redesign

### Step 4: Agent-3 Addresses Feedback
Agent-3 addresses feedback and resubmits if needed.

### Step 5: Continue to Next Checkpoint
Once approved, continue to next module/checkpoint.

---

## 📊 Review Status Tracking

**Checkpoint 1 (Core Models):** ⬜ Pending  
**Checkpoint 2 (Data Collectors):** ⬜ Pending  
**Checkpoint 3 (Aggregation & Reports):** ⬜ Pending  
**Checkpoint 4 (CLI):** ⬜ Pending  
**Checkpoint 5 (Tests):** ⬜ Pending  

**Phase 1 Status:** 🟡 In Progress (2/10 modules complete)

---

## 🎯 Review Principles

### Focus Areas
1. **V2 Compliance:** File size, function size, type hints
2. **Architecture:** Modular design, separation of concerns
3. **Safety:** Error handling, validation, logging
4. **Code Quality:** Readability, maintainability, documentation

### Review Style
- **Constructive:** Focus on improvements, not just problems
- **Specific:** Provide concrete examples and suggestions
- **Timely:** Review within 24 hours of request
- **Thorough:** Check all aspects, not just one

### Approval Criteria
- ✅ All checklist items pass
- ✅ V2 compliance verified
- ✅ Architecture aligned
- ✅ Safety measures in place
- ✅ Code quality acceptable

---

**Status:** Ready for Use  
**Next:** Agent-3 requests Checkpoint 1 review after Module 2 complete

