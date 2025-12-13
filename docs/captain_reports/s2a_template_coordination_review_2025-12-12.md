# S2A Template Coordination Review & Enhancement
**Date**: 2025-12-12  
**Issue**: No coordination messages sent all day - agents not using swarm as force multiplier  
**Status**: Reviewing and enhancing template language

## Current Issues Identified

### 1. Delegation Not Prominent Enough
- **Problem**: Delegation is listed as 4th option in "Required Output" section
- **Impact**: Agents may skip delegation option and choose easier solo tasks
- **Location**: Line 328 in `messaging_template_texts.py`

### 2. Language Too Passive
- **Problem**: "If task is large/multi-domain" is conditional language
- **Impact**: Agents may not recognize their tasks qualify
- **Current**: "Delegate work to other agents (if task is large/multi-domain - see Swarm Coordination below)"

### 3. Force Multiplier Section Too Long
- **Problem**: Detailed swarm coordination section is verbose (100+ lines)
- **Impact**: Agents may skip reading it
- **Location**: `SWARM_COORDINATION_TEXT` (lines 103-202)

### 4. No Concrete Examples
- **Problem**: Abstract guidance without specific scenarios
- **Impact**: Agents can't easily identify coordination opportunities

### 5. Delegation Not Emphasized in Cycle Checklist
- **Problem**: "Assess task size" mentioned but not emphasized
- **Impact**: Agents skip the assessment step

## Proposed Enhancements

### Enhancement 1: Make Delegation the FIRST Priority Option

**Current**:
```
Required Output (pick one now):
- Commit a real slice
- Run and record a validation result
- Produce a short artifact report with real delta
- **Delegate work to other agents** (if task is large/multi-domain - see Swarm Coordination below)
```

**Proposed**:
```
Required Output (pick one now):
- ⚡ **DELEGATE TO SWARM FIRST** (PREFERRED if task >1 cycle OR multi-domain - see Force Multiplier below)
- Commit a real slice (only if task is single-agent scope)
- Run and record a validation result (only if task is single-agent scope)
- Produce a short artifact report with real delta (only if task is single-agent scope)

🎯 FORCE MULTIPLIER CHECK (DO THIS FIRST):
Before choosing any solo option, ask yourself:
1. Will this take me more than 1 cycle? → DELEGATE NOW
2. Does this touch multiple domains (e.g., frontend + backend)? → COORDINATE NOW
3. Does another agent have better expertise? → ASK FOR HELP NOW
4. Can I break this into 2-4 parallel pieces? → SWARM ASSIGNMENT NOW

If ANY answer is YES → Use delegation/coordination (see Force Multiplier section below)
```

### Enhancement 2: Add Prominent Coordination Callout

**Add before "Required Output" section**:
```
🚨 COORDINATION MANDATE 🚨
Today's goal: Use the swarm as a force multiplier.
- 8 agents working together > 1 agent working alone
- If you haven't sent a coordination message today, consider delegating your next task
- Look for opportunities to break down work and assign to swarm
- Collaboration is progress - delegation messages count as work output
```

### Enhancement 3: Strengthen Cycle Checklist Language

**Current**:
```
- Assess task size: Is this a force multiplier opportunity? (see Swarm Coordination below)
```

**Proposed**:
```
- 🔍 FORCE MULTIPLIER ASSESSMENT (MANDATORY FIRST STEP):
  - Will this task take >1 cycle? → STOP, delegate parts to swarm
  - Does this touch 2+ domains? → STOP, coordinate with domain experts
  - Is another agent better suited? → STOP, message them to take over
  - Can this be parallelized? → STOP, break down and assign to 2-4 agents
  - ONLY if all answers are NO → proceed solo
```

### Enhancement 4: Add Coordination Examples Section

**Add after Force Multiplier section**:
```
**CONCRETE COORDINATION EXAMPLES** (Use these patterns):

Example 1: Large Refactor
  - Task: Refactor 10 files across frontend/backend
  - Action: Break into "frontend refactor" → Agent-7, "backend refactor" → Agent-1
  - Message: "Coordination: Frontend refactor task. You handle web/, I'll handle services/"

Example 2: Multi-Domain Feature
  - Task: Add feature requiring database + API + frontend
  - Action: Agent-1 (API) + Agent-7 (frontend) + Agent-8 (database schema)
  - Message: "Feature coordination: API endpoint assigned to Agent-1, frontend to Agent-7"

Example 3: Testing Across Domains
  - Task: Add tests for integration spanning 3 modules
  - Action: Each module's specialist adds their tests
  - Message: "Test coordination: Each agent adds tests for their domain modules"

Example 4: Documentation Update
  - Task: Update docs across 5 subsystems
  - Action: Each subsystem owner updates their docs
  - Message: "Doc update: Agent-2 (architecture), Agent-3 (infra), Agent-7 (web) - parallel docs"

**Remember**: Sending coordination messages IS progress. Commit them!
```

### Enhancement 5: Make Quick Delegation Decision More Visible

**Current**:
```
**QUICK DELEGATION DECISION**:
- If task > 1 cycle OR spans multiple domains → **DELEGATE NOW**
```

**Proposed**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 QUICK DELEGATION DECISION (30 SECOND CHECK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ask these 3 questions RIGHT NOW (before starting work):

1. **Time Estimate**: Will this take me >1 cycle (3+ hours)?
   → If YES: Break into pieces, delegate to 2-4 agents

2. **Domain Scope**: Does this touch 2+ agent domains?
   → If YES: Message domain specialists to coordinate

3. **Expertise Match**: Is another agent better suited?
   → If YES: Message them to take over, offer to assist

**If ANY answer is YES → DELEGATE/COORDINATE NOW**

Action:
- Use: `python -m src.services.messaging_cli --agent Agent-X --message "[task breakdown]" --priority normal`
- Send 2-4 coordination messages (one per agent)
- Commit the coordination messages (they count as progress!)
- Monitor via status.json updates

**If ALL answers are NO → Proceed solo**
```

### Enhancement 6: Add Daily Coordination Reminder

**Add at top of template**:
```
📊 COORDINATION METRIC CHECK:
- How many coordination messages have YOU sent today?
- If zero → Your next task should involve coordination
- Goal: At least 1 coordination message per day
- Remember: Using the swarm is progress, not overhead
```

## Implementation Plan

1. **Update STALL_RECOVERY template** with enhanced delegation emphasis
2. **Update SWARM_COORDINATION_TEXT** with concrete examples
3. **Add coordination examples section** to templates
4. **Update cycle checklist** to make coordination assessment mandatory
5. **Test updated templates** to ensure clarity and effectiveness

## Success Metrics

- **Target**: 3+ coordination messages per day across swarm
- **Current**: 0 coordination messages (problem)
- **Measurement**: Count A2A coordination messages in message history

## Files to Modify

1. `src/core/messaging_template_texts.py`
   - Update `STALL_RECOVERY` template (line 316)
   - Update `SWARM_COORDINATION_TEXT` (line 103)
   - Add coordination examples section
   - Update cycle checklist (line 44)

2. `src/core/optimized_stall_resume_prompt.py`
   - Update `_build_prompt` to emphasize coordination
   - Add coordination examples to recovery actions

## Next Steps

1. ✅ Review current template (DONE)
2. ⏳ Implement enhanced template language
3. ⏳ Add concrete coordination examples
4. ⏳ Update cycle checklist
5. ⏳ Test and validate improvements
6. ⏳ Monitor coordination message volume

---

**Status**: Analysis complete - ready for implementation

