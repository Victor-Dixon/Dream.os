# Stall Recovery Message - Swarm Coordination Improvements

**Date**: 2025-12-10  
**Author**: Agent-5  
**Purpose**: Enhance STALL_RECOVERY template to encourage task delegation and swarm coordination

## Changes Made

### 1. Added Delegation as Explicit Required Output

**Before:**
```
Required Output (pick one now):
- Commit a real slice
- Run and record a validation result
- Produce a short artifact report with real delta
```

**After:**
```
Required Output (pick one now):
- Commit a real slice
- Run and record a validation result
- Produce a short artifact report with real delta
- **Delegate work to other agents** (if task is large/multi-domain - see Swarm Coordination below)
```

### 2. Enhanced Swarm Coordination Section

**Key Improvements:**
- Added "Immediate Delegation" as step 2 (before starting work)
- Added agent domain expertise mapping for quick reference
- Emphasized that delegation counts as progress
- Added concrete examples of when to delegate
- Made coordination commands more prominent with examples

**New Content:**
- **Quick Delegation Decision** section added before Escalation
- **Delegation Examples** section with real-world scenarios
- Enhanced anti-patterns to include "starting work before checking if task should be delegated"

### 3. Added Quick Reference Section

Added before Escalation:
```
**QUICK DELEGATION DECISION**:
- If task > 1 cycle OR spans multiple domains → **DELEGATE NOW**
- Use: `python -m src.services.messaging_cli --agent Agent-X --message "[task]" --priority normal`
- Delegation IS progress - assign work, then commit the assignment messages
```

## Impact

These changes should:
1. **Increase delegation** - Makes delegation a first-class option, not an afterthought
2. **Reduce solo work** - Emphasizes checking task size before starting
3. **Provide clear guidance** - Agent expertise mapping and examples make it actionable
4. **Validate delegation as progress** - Explicitly states that sending assignments counts

## Testing

- ✅ Template rendering test passes
- ✅ Integration tests verify template structure
- ✅ No breaking changes to existing functionality

## Files Modified

- `src/core/messaging_template_texts.py` - Enhanced STALL_RECOVERY template and SWARM_COORDINATION_TEXT

