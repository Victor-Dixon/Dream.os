# SSOT Tagging Coordination - Web Domain Batch 7
**Coordinator:** Agent-2 (SSOT Domain Mapping Owner)  
**Assignee:** Agent-7 (Web Development Specialist)  
**Date:** 2025-12-29  
**Batch:** web_batch_1  
**Status:** ✅ ACCEPTED - Agent-7 executing tagging

---

## Batch 7 Details

**Batch ID:** `web_batch_1`  
**Domain:** `web`  
**Priority:** 2 (HIGH)  
**File Count:** ~65 files  
**Estimated Time:** 60-90 minutes  
**Primary Agent:** Agent-7  
**Role:** Agent-7 is PRIMARY (web domain owner)

---

## SSOT Tag Format

**Standard Format:**
```python
"""
Module description.

<!-- SSOT Domain: web -->
"""
```

**For Python files:** Add `<!-- SSOT Domain: web -->` in the module docstring (after module description or as first line).

---

## Tagging Instructions

1. **Add domain tag** in comments/docstring at top of file:
   - Format: `<!-- SSOT Domain: web -->`
   - Placement: In module docstring (first line or after module description)

2. **Tag all web domain files** in `src/web/`

3. **Verify tags** follow SSOT domain registry:
   - Domain name: `web`
   - Domain owner: Web Development (Agent-7)
   - Format: HTML comment format

4. **Test files** still compile after tagging:
   - Run syntax check: `python -m py_compile <file>`
   - Verify imports still work

5. **Commit** with message:
   ```
   feat: Add SSOT domain tags - web domain batch 1 (X files)
   ```

---

## Coordination Protocol

**Agent-7 Role:**
- Execute SSOT tagging for web domain files
- Verify SSOT tag format and placement
- Validate domain consistency
- Test file compilation after tagging
- Commit changes

**Agent-2 Role:**
- Coordinate SSOT tagging work
- Validate domain tags match registry
- Review tagged files for compliance
- Update SSOT domain mapping if needed

**Workflow:**
1. Agent-7 accepts batch assignment ✅
2. Agent-7 tags files with SSOT domain tags
3. Agent-7 verifies tags and tests compilation
4. Agent-7 commits changes
5. Agent-2 validates tags in architecture review
6. Both coordinate on completion

---

## Domain Information

**Domain:** `web`  
**Owner:** Web Development (Agent-7)  
**Priority:** 2 (HIGH)  
**Description:** Web application code, web routes, web handlers, frontend

**Examples:**
- `src/web/` - Web routes, web handlers, frontend code
- Web routes, web handlers, static files
- Web domain handlers, frontend integration

---

## Status

**Current Status:** ✅ VALIDATED - Batch 7 complete  
**Assignee:** Agent-7 (web domain owner)  
**Completion:** All 65 files verified - already have SSOT tags, no changes needed  
**Validation:** Agent-2 validated all tags - format correct, domain correct, placement correct  
**Timeline:** Verification completed immediately, validation completed within 15 minutes  
**Coordination:** Batch 7 complete - all web domain files SSOT compliant

---

**Last Updated:** 2025-12-29 by Agent-2  
**Next Review:** After Agent-7 commits changes

