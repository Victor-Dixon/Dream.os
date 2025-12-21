<!-- SSOT Domain: architecture -->
# Documentation Cleanup Candidates - Safe to Delete
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-14  
**Status**: 🟡 Analysis Complete - Ready for Review

---

## Executive Summary

**Analysis**: Reviewed `docs/` directory for obsolete, duplicate, or superseded documentation files.

**Candidates Identified**: 6 files that appear safe to delete

**Risk Level**: LOW - All candidates have enhanced/superseded versions

---

## Candidates for Deletion

### 1. ✅ **AGENT_ONBOARDING_GUIDE.md**
**Location**: `docs/AGENT_ONBOARDING_GUIDE.md`

**Reason**: 
- Superseded by `AGENT_ONBOARDING_GUIDE_ENHANCED.md`
- Enhanced version explicitly states: "PRIMARY ONBOARDING DOCUMENT" (Version 2.0)
- Enhanced version is 707 lines vs 155 lines (more comprehensive)

**Verification**:
- Enhanced version exists and is actively maintained
- Enhanced version contains all content from original + improvements

**Risk**: LOW - Enhanced version is primary document

---

### 2. ✅ **CYCLE_TIMELINE_IMPLEMENTATION.md**
**Location**: `docs/CYCLE_TIMELINE_IMPLEMENTATION.md`

**Reason**:
- Implementation summary of creating `CYCLE_TIMELINE.md`
- Historical record only, not a reference document
- `CYCLE_TIMELINE.md` is the actual timeline document (534 lines vs 266 lines summary)

**Verification**:
- Implementation doc is a meta-document about creating the timeline
- Actual timeline document `CYCLE_TIMELINE.md` exists and is current

**Risk**: LOW - Historical/implementation record, not actively referenced

---

### 3. ✅ **utils_function_catalog.md**
**Location**: `docs/utils_function_catalog.md`

**Reason**:
- Superseded by `utils_function_catalog_enhanced.md`
- Enhanced version is comprehensive (376 lines vs 135 lines)
- Enhanced version includes V2 compliance tracking and detailed statistics

**Verification**:
- Enhanced version exists with full catalog + compliance metrics
- Enhanced version is more up-to-date and comprehensive

**Risk**: LOW - Enhanced version contains all information

---

### 4. ⚠️ **ONBOARDING_GUIDE.md** (Check for uniqueness)
**Location**: `docs/ONBOARDING_GUIDE.md`

**Reason**: 
- Potential duplicate of `AGENT_ONBOARDING_GUIDE_ENHANCED.md`
- Need to verify if content is unique or duplicate

**Verification Required**:
- Compare content with `AGENT_ONBOARDING_GUIDE_ENHANCED.md`
- Check if this is a different onboarding context (human vs agent)

**Risk**: MEDIUM - Need content verification before deletion

---

### 5. ⚠️ **AGENT_ORIENTATION.md** (Check for uniqueness)
**Location**: `docs/AGENT_ORIENTATION.md`

**Reason**:
- Potential overlap with onboarding guides
- May be historical or replaced

**Verification Required**:
- Compare content with `AGENT_ONBOARDING_GUIDE_ENHANCED.md`
- Check if orientation is distinct from onboarding

**Risk**: MEDIUM - Need content verification before deletion

---

### 6. ✅ **Archive Folder Files** (Low Priority)
**Location**: `docs/archive/`

**Reason**:
- Already in archive folder (75 files)
- Historical records, not active documentation
- Can be moved to deeper archive or deleted if storage is concern

**Verification**:
- Archive folder contains historical/consolidation analysis files
- Some files may have value for reference

**Risk**: VERY LOW - Already archived, not active

**Recommendation**: Keep archive folder but could compress or move to external storage if needed

---

## Deletion Safety Checklist

### High Confidence Deletions (Can delete immediately):
- [x] `AGENT_ONBOARDING_GUIDE.md` - Enhanced version is primary
- [x] `CYCLE_TIMELINE_IMPLEMENTATION.md` - Implementation summary, not reference
- [x] `utils_function_catalog.md` - Enhanced version is comprehensive

### Medium Confidence (Verify before deletion):
- [ ] `ONBOARDING_GUIDE.md` - Verify uniqueness
- [ ] `AGENT_ORIENTATION.md` - Verify uniqueness

### Low Priority (Archive management):
- [ ] `docs/archive/` - Already archived, low priority cleanup

---

## Verification Steps Before Deletion

1. **Search for References**:
   ```bash
   grep -r "AGENT_ONBOARDING_GUIDE.md" .
   grep -r "CYCLE_TIMELINE_IMPLEMENTATION.md" .
   grep -r "utils_function_catalog.md" .
   ```

2. **Check Documentation Index**:
   - Verify `DOCUMENTATION_INDEX.md` doesn't reference these files
   - Update index if files are removed

3. **Git History**:
   - All files will remain in git history if needed for reference
   - No permanent data loss

---

## Recommended Action Plan

### Phase 1: Safe Deletions (High Confidence) - READY TO EXECUTE
1. Delete `AGENT_ONBOARDING_GUIDE.md` ✅ Safe - Enhanced version is primary
2. Delete `CYCLE_TIMELINE_IMPLEMENTATION.md` ✅ Safe - Implementation summary only
3. Delete `utils_function_catalog.md` ✅ Safe - Enhanced version is comprehensive
4. Commit with message: `docs: remove obsolete documentation files (superseded by enhanced versions)`

**Note**: Documentation index references `ONBOARDING_GUIDE.md` (different from `AGENT_ONBOARDING_GUIDE.md`) and `AGENT_ORIENTATION.md`, so these appear to be distinct and should be kept.

### Phase 2: Verification Deletions (After Review) - SKIP
- `ONBOARDING_GUIDE.md` - Listed in documentation index, appears to be distinct (human onboarding?)
- `AGENT_ORIENTATION.md` - Listed in documentation index, appears to be distinct from onboarding

**Decision**: Keep these files as they appear in the documentation index and may serve different purposes.

### Phase 3: Archive Management (Optional)
1. Consider compressing `docs/archive/` if storage is concern
2. Move to external archive location if needed

---

## Impact Assessment

**Files to Delete**: 3-5 files
**Space Saved**: ~50-100 KB (minimal, but reduces clutter)
**Risk**: LOW - All have enhanced/superseded versions
**Git History**: Preserved for historical reference

---

## Next Steps

1. ✅ Analysis complete
2. ⏳ Review by Captain/team (optional)
3. ⏳ Execute Phase 1 deletions (high confidence)
4. ⏳ Execute Phase 2 deletions (after verification)

---

**Status**: 🟡 Ready for execution - Phase 1 deletions are safe  
**Agent**: Agent-2 (Architecture & Design Specialist)
