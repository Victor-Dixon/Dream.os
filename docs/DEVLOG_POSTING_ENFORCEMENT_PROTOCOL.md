# Devlog Posting Enforcement Protocol

**Protocol ID:** DEVLOG_POSTING_ENFORCEMENT  
**Protocol Version:** 1.0  
**Protocol Status:** ACTIVE  
**Enforced By:** Agent-6 (Coordination & Communication)  
**Last Updated:** 2025-12-26

---

## Overview

All agents MUST post devlogs regularly. Devlogs are critical for human-in-the-loop multi-agentic coordination and visibility.

---

## Devlog Requirements

### 1. Posting Frequency

- **After every significant task completion**
- **After every assignment completion**
- **At end of each work session**
- **When blocked or need help**
- **Weekly status updates (minimum)**

### 2. Required Format

**Devlogs MUST be in skimmable format for human-in-the-loop coordination:**

```markdown
# [Agent-X] Devlog: [Brief Title]

**Date:** YYYY-MM-DD
**Status:** ✅ COMPLETE / ⏳ IN PROGRESS / 🟡 BLOCKED

---

## Task Summary
[One-line summary of what you did]

## Actions Taken
- Action 1
- Action 2
- Action 3

## Results
- Result 1
- Result 2

## Artifacts Created
- File/artifact 1
- File/artifact 2

## Blockers (if any)
- Blocker 1 + proposed solution
- Blocker 2 + proposed solution

---

## Next Steps
[CRITICAL - Must include next steps at the end]

1. Next action 1
2. Next action 2
3. Next action 3

---

*Devlog by Agent-X | YYYY-MM-DD*
```

### 3. Required Sections

**MUST Include:**
- ✅ Task Summary (one-line)
- ✅ Actions Taken (bulleted list)
- ✅ Results (what was accomplished)
- ✅ Artifacts Created (files, reports, etc.)
- ✅ **Next Steps** (CRITICAL - must be at the end)
- ✅ Blockers (if any) + proposed solutions

### 4. Skimmable Format Rules

- **Use clear headings** (## Section Name)
- **Use bullet points** for lists
- **Keep paragraphs short** (2-3 sentences max)
- **Use status emojis** (✅ ⏳ 🟡 ❌)
- **Bold important items**
- **Include file paths** for artifacts

---

## Posting Method

**Use the correct devlog posting tool:**

```bash
python tools/devlog_poster_agent_channel.py --agent Agent-X --file <devlog_path>
```

**Location:** Posts to agent-specific Discord channel (e.g., #agent-6)

---

## Enforcement

**Agent-6 Responsibilities:**
1. Monitor devlog posting frequency
2. Remind agents to post devlogs
3. Verify devlogs include "Next Steps" section
4. Verify devlogs are in skimmable format
5. Coordinate devlog posting across agents

**Enforcement Actions:**
- Weekly devlog audit
- Reminder messages to agents missing devlogs
- Devlog format validation
- Next steps verification

---

## Master Task List Integration

**Devlogs MUST reference:**
- Tasks completed from MASTER_TASK_LOG.md
- Tasks claimed from MASTER_TASK_LOG.md
- Tasks in progress from MASTER_TASK_LOG.md
- Next tasks to claim from MASTER_TASK_LOG.md

**Example:**
```markdown
## Tasks Completed
- ✅ MASTER_TASK_LOG: "Fix broken tools Phase 3" (claimed, in progress)
- ✅ MASTER_TASK_LOG: "Website audit implementation" (complete)

## Next Tasks
- ⏳ MASTER_TASK_LOG: "Tool consolidation" (ready to claim)
```

---

## Human-in-the-Loop Coordination

**Why Skimmable Format:**
- Human can quickly scan devlogs
- Identify blockers quickly
- Provide help when needed
- Coordinate multi-agent work
- Track progress across swarm

**Format Requirements:**
- Clear structure (headings, bullets)
- Status indicators (✅ ⏳ 🟡)
- Next steps always at end
- File paths for artifacts
- Brief, actionable content

---

## Examples

### ✅ Good Devlog Format

```markdown
# Agent-6 Devlog: Deployment Verification Complete

**Date:** 2025-12-26
**Status:** ✅ COMPLETE

---

## Task Summary
Verified Build-In-Public Phase 0 deployment status on live sites.

## Actions Taken
- Navigated to dadudekc.com - Phase 0 sections NOT visible
- Navigated to weareswarm.online - Phase 0 sections NOT visible
- Created verification report
- Coordinated with Agent-3 for deployment

## Results
- Verification complete ✅
- Deployment gap identified ❌
- Coordination active with Agent-3

## Artifacts Created
- BUILD_IN_PUBLIC_DEPLOYMENT_VERIFICATION_2025-12-26.md
- AGENT3_AGENT6_BUILD_IN_PUBLIC_DEPLOYMENT_COORDINATION.md

---

## Next Steps
1. Stand by for Agent-3 deployment execution
2. Re-verify sites after deployment completes
3. Confirm Phase 0 sections visible
4. Report verification results to Captain
```

### ❌ Bad Devlog Format

```markdown
# Devlog

Did some work today. Fixed some things. Created some files. 
Working on more stuff. Will continue tomorrow.

[Missing: Task summary, actions taken, results, artifacts, next steps]
```

---

## Protocol Compliance

**All agents MUST:**
- ✅ Post devlogs regularly
- ✅ Include "Next Steps" section at end
- ✅ Use skimmable format
- ✅ Reference MASTER_TASK_LOG tasks
- ✅ Post to agent-specific Discord channel

**Agent-6 WILL:**
- ✅ Monitor compliance
- ✅ Remind agents to post
- ✅ Validate format
- ✅ Enforce requirements

---

*Protocol enforced by Agent-6 | 2025-12-26*




