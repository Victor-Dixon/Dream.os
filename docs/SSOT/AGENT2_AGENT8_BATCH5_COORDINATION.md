# SSOT Tagging Coordination - Agent-8 Batch 5
**Coordinator:** Agent-2 (SSOT Domain Mapping Owner)  
**Assignee:** Agent-8 (SSOT & System Integration)  
**Date:** 2025-12-29  
**Batch:** integration_batch_4  
**Status:** 🔄 REASSIGNED - Agent-8 declined (CS2 mod incident priority), reassigning to Agent-1 (primary) or Agent-5/Agent-7

---

## Batch 5 Details

**Batch ID:** `integration_batch_4`  
**Domain:** `integration`  
**Priority:** 2 (HIGH)  
**File Count:** 15 files  
**Estimated Time:** 45 minutes  
**Primary Agent:** Agent-1  
**Secondary Agent:** Agent-8  
**Role:** Agent-8 is SECONDARY (supporting Agent-1)

---

## Files to Tag

1. `src/services/handlers/contract_handler.py`
2. `src/services/handlers/coordinate_handler.py`
3. `src/services/handlers/hard_onboarding_handler.py`
4. `src/services/handlers/onboarding_handler.py`
5. `src/services/handlers/task_handler.py`
6. `src/services/handlers/utility_handler.py`
7. `src/services/handlers/soft_onboarding_handler.py`
8. `src/services/helpers/task_repo_loader.py`
9. `src/services/helpers/__init__.py`
10. `src/services/messaging/services/__init__.py`
11. `src/services/messaging/services/message_delivery_service.py`
12. `src/services/messaging/services/message_formatting_service.py`
13. `src/services/messaging/services/message_routing_service.py`
14. `src/services/messaging/services/message_validation_service.py`
15. `src/services/messaging_cli_coordinate_management/__init__.py`

---

## SSOT Tag Format

**Standard Format:**
```python
"""
Module description.

<!-- SSOT Domain: integration -->
"""
```

**For Python files:** Add `<!-- SSOT Domain: integration -->` in the module docstring (after module description or as first line).

**Example:**
```python
"""
Contract handler for task management.

<!-- SSOT Domain: integration -->
"""
```

---

## Tagging Instructions

1. **Add domain tag** in comments/docstring at top of file:
   - Format: `<!-- SSOT Domain: integration -->`
   - Placement: In module docstring (first line or after module description)

2. **Tag all 15 files** in this batch

3. **Verify tags** follow SSOT domain registry:
   - Domain name: `integration`
   - Domain owner: Integration (Agent-1) - Agent-8 supporting
   - Format: HTML comment format

4. **Test files** still compile after tagging:
   - Run syntax check: `python -m py_compile <file>`
   - Verify imports still work

5. **Commit** with message:
   ```
   feat: Add SSOT domain tags - integration domain batch 4 (15 files)
   ```

---

## Coordination Protocol

**Agent-8 Role:**
- Support Agent-1 (primary) in tagging integration domain files
- Verify SSOT tag format and placement
- Validate domain consistency
- Test file compilation after tagging

**Agent-2 Role:**
- Coordinate SSOT tagging work
- Validate domain tags match registry
- Review tagged files for compliance
- Update SSOT domain mapping if needed

**Workflow:**
1. Agent-8 tags files with SSOT domain tags
2. Agent-8 verifies tags and tests compilation
3. Agent-8 commits changes
4. Agent-2 validates tags in architecture review
5. Both coordinate on completion

---

## Validation Checklist

- [ ] All 15 files have SSOT domain tags
- [ ] SSOT domain tags use correct format (`<!-- SSOT Domain: integration -->`)
- [ ] SSOT domain name matches registry (`integration`)
- [ ] Files compile after tagging
- [ ] Imports still work correctly
- [ ] Commit message follows format
- [ ] Changes committed to git

---

## Domain Information

**Domain:** `integration`  
**Owner:** Integration (Agent-1)  
**Secondary:** SSOT & System Integration (Agent-8)  
**Priority:** 2 (HIGH)  
**Description:** System integration components, API integrations, external service connections

**Examples:**
- `src/services/` - Service classes, business logic
- `src/integrations/` - API clients, external service adapters
- Integration handlers, coordination services

---

## Status

**Current Status:** 🔄 REASSIGNED - Agent-8 declined due to CS2 mod incident (user priority)  
**Reassignment:** Batch reassigned to Agent-1 (primary) or Agent-5/Agent-7 as alternative  
**Next Action:** Alternative agent tags files and commits changes  
**Timeline:** Estimated 45 minutes for completion (within 24h)  
**Agent-8 Re-engagement:** After CS2 mod stable (~24h)  
**Coordination:** Agent-2 coordinating reassignment and validation

---

**Last Updated:** 2025-12-29 by Agent-2  
**Next Review:** After Agent-1 (or alternative agent) completes tagging

