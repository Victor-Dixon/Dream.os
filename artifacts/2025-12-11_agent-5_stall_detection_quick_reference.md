# Stall Detection Enhancement - Quick Reference

**Date**: 2025-12-11  
**Agent**: Agent-5 (Business Intelligence Specialist)  
**Type**: Quick Reference  
**Status**: ✅ Complete

## Current System: 11 Activity Sources

✅ status.json, inbox, devlogs, reports, message queue, workspace files, git commits, Discord posts, tool execution, Swarm Brain, agent lifecycle

## Additional Indicators: 8 New Sources

### Phase 1 (High Priority - 30-40% reduction)
1. **Artifacts Directory** - `artifacts/YYYY-MM-DD_agent-X_*.md`
2. **Contract System** - Task claims/completions via ContractManager
3. **Inbox Processing** - Message read/processed indicators

### Phase 2 (Medium Priority - 20-30% reduction)
4. **Documentation** - `docs/AGENTX_*.md`
5. **Cycle Planner** - `cycle_planner_tasks_*.json`
6. **Passdown.json** - Session status updates
7. **Code Modifications** - Git commits with agent attribution

### Phase 3 (Low Priority - 5-10% reduction)
8. **Test Execution** - Pytest cache/test results

## Expected Results

- **Current**: 10-20% false positive rate
- **After All Phases**: 2-5% false positive rate
- **Total Activity Sources**: 19 (11 current + 8 new)

## Implementation

Add to: `src/orchestrators/overnight/enhanced_agent_activity_detector.py`

**Pattern**: Each check returns `{"source": str, "timestamp": float, "age_seconds": float}` or `None`

## Status

✅ **Analysis Complete** - Ready for implementation.

---

**Full Analysis**: `artifacts/2025-12-11_agent-5_stall_detection_enhancement_analysis.md`
