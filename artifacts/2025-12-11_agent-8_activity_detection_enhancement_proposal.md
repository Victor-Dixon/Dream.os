# Agent Activity Detection Enhancement Proposal

**Date**: 2025-12-11  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Task**: Identify additional activity sources to further reduce false stalls

## Current Activity Sources (11)

1. ✅ status.json modifications
2. ✅ inbox file modifications
3. ✅ devlog creation/modification
4. ✅ report files in workspace
5. ✅ message queue activity
6. ✅ workspace file modifications
7. ✅ git commits (by agent name in commit message)
8. ✅ discord posts
9. ✅ tool execution logs
10. ✅ swarm brain contributions
11. ✅ agent lifecycle events

## Proposed Additional Activity Sources (12+)

### High Priority (Immediate Impact)

**12. passdown.json modifications**
- **Location**: `agent_workspaces/{agent_id}/passdown.json`
- **Why**: Agents update this during session transitions
- **Impact**: Catches activity during handoff periods
- **Implementation**: Check file mtime and `session_date` field

**13. Artifacts directory (root level)**
- **Location**: `artifacts/YYYY-MM-DD_agent-X_*.md`
- **Why**: Agents create validation artifacts here
- **Impact**: Catches validation/test work
- **Implementation**: Check for agent-specific artifact files

**14. Cycle planner task files**
- **Location**: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
- **Why**: Agents create/update these when planning work
- **Impact**: Catches planning activity
- **Implementation**: Check for recent cycle planner files

**15. Notes directory**
- **Location**: `agent_workspaces/{agent_id}/notes/*.md`
- **Why**: Agents create notes during work
- **Impact**: Catches documentation/analysis work
- **Implementation**: Check for recent note file modifications

**16. Git file changes (not just commits)**
- **Location**: Git working directory
- **Why**: Agents modify files even if not committed yet
- **Impact**: Catches in-progress work
- **Implementation**: `git diff --name-only` filtered by agent workspace paths

**17. Validation reports directory**
- **Location**: `agent_workspaces/{agent_id}/validation_reports/*.md`
- **Why**: Agents create validation reports
- **Impact**: Catches validation work
- **Implementation**: Check for recent validation report files

### Medium Priority (Good Coverage)

**18. Activity logs directory**
- **Location**: `agent_workspaces/{agent_id}/activity/*.md`
- **Why**: Some agents log activity here
- **Impact**: Additional activity tracking
- **Implementation**: Check for recent activity log files

**19. Session completion reports**
- **Location**: `agent_workspaces/{agent_id}/session_completion/*.md`
- **Why**: Agents create session summaries
- **Impact**: Catches session wrap-up activity
- **Implementation**: Check for recent session completion files

**20. Contract system activity**
- **Location**: Contract system database/logs
- **Why**: Agents claim/complete contracts
- **Impact**: Catches task assignment activity
- **Implementation**: Check contract system for agent activity

**21. Coordination message files (outbound)**
- **Location**: Other agents' inboxes with agent as sender
- **Why**: Agents send A2A/C2A messages
- **Impact**: Catches coordination activity
- **Implementation**: Scan other agent inboxes for messages from this agent

**22. Test execution artifacts**
- **Location**: `.pytest_cache/`, `htmlcov/`, `coverage.xml`, test result files
- **Why**: Agents run tests
- **Impact**: Catches testing activity
- **Implementation**: Check for recent test cache/coverage files

### Lower Priority (Nice to Have)

**23. Preferences files**
- **Location**: `agent_workspaces/{agent_id}/*_preferences.json`
- **Why**: Agents update preferences
- **Impact**: Minor activity indicator
- **Implementation**: Check for preferences file modifications

**24. Swarm Brain entries (comprehensive)**
- **Location**: `swarm_brain/**/*.md` with agent name in content
- **Why**: Agents contribute learnings
- **Impact**: Catches knowledge sharing
- **Implementation**: Enhanced search in swarm_brain directory

**25. Git stash activity**
- **Location**: Git stashes
- **Why**: Agents may stash work
- **Impact**: Catches interrupted work sessions
- **Implementation**: Check `git stash list` for agent-related stashes

**26. File lock indicators**
- **Location**: Lock files, temp files
- **Why**: Agents may create lock files during work
- **Impact**: Catches active work sessions
- **Implementation**: Check for agent-specific lock/temp files

## Implementation Priority

### Phase 2 (Next Enhancement)
1. passdown.json modifications
2. Artifacts directory (root level)
3. Cycle planner task files
4. Notes directory
5. Git file changes (working directory)

### Phase 3 (Further Enhancement)
6. Validation reports directory
7. Activity logs directory
8. Session completion reports
9. Contract system activity
10. Coordination message files (outbound)

### Phase 4 (Comprehensive)
11. Test execution artifacts
12. Preferences files
13. Enhanced Swarm Brain search
14. Git stash activity
15. File lock indicators

## Expected Impact

**Current**: 11 activity sources  
**Phase 2**: +5 sources = 16 total (45% increase)  
**Phase 3**: +5 sources = 21 total (91% increase)  
**Phase 4**: +5 sources = 26 total (136% increase)

**False Positive Reduction**:
- Current: 60-70% → 10-20% (Phase 1)
- Phase 2: 10-20% → 5-10% (estimated)
- Phase 3: 5-10% → 2-5% (estimated)
- Phase 4: 2-5% → 1-2% (estimated)

## Implementation Notes

1. **Performance**: Some checks (git diff, contract system) may be slower - cache results
2. **Reliability**: Some sources (test artifacts) may be cleaned up - use reasonable time windows
3. **Accuracy**: Git file changes may include auto-generated files - filter appropriately
4. **Maintenance**: New activity sources should be documented and tested

## Next Steps

1. Implement Phase 2 sources (5 additional)
2. Test with all agents
3. Measure false positive reduction
4. Proceed to Phase 3 if needed

---
*Agent-8: SSOT & System Integration Specialist*  
*🐝 WE. ARE. SWARM. ⚡🔥*
