<<<<<<< HEAD
<!-- SSOT Domain: documentation -->

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
# Devlog Standards & Enforcement Protocol

**Effective:** 2025-12-26  
**Enforced By:** Agent-4 (Captain)  
**Purpose:** Ensure visibility for human-in-the-loop multi-agentic coordination

---

## Devlog Requirements (MANDATORY)

### When to Post Devlogs

- ✅ **After completing assignments**
- ✅ **After significant progress milestones**
- ✅ **When blocked (with next steps)**
- ✅ **After deployment execution**
- ✅ **After verification completion**
- ✅ **Weekly status updates**

### Required Format (Skimmable)

```markdown
# [AGENT-X] [TASK NAME] - [STATUS]

**Date:** YYYY-MM-DD  
**Agent:** Agent-X  
**Task:** [Brief task description]

---

## ✅ Completed
- Action 1
- Action 2

## ⏳ In Progress
- Action 3

## 🔴 Blockers
- Blocker description + proposed solution

---

## Next Steps
1. Immediate action
2. Next milestone
3. Handoff/coordination point

---

**Status:** ✅ COMPLETE / 🟡 IN PROGRESS / 🔴 BLOCKED
**Evidence:** [link to artifact/report]
```

### Key Requirements

1. **Must include "Next Steps" section** - Required for human-in-the-loop coordination
2. **Skimmable format** - Bullet points, clear sections, status indicators
3. **Status indicators** - ✅ COMPLETE, 🟡 IN PROGRESS, 🔴 BLOCKED
4. **Evidence links** - Reference artifacts, reports, code changes
5. **Next steps** - Clear actions for continuation

---

## Enforcement Protocol

**Agent-4 (Captain) Responsibilities:**
- Monitor devlog posting frequency
- Review devlog quality (format, next steps)
- Escalate missing devlogs
- Update tracking based on devlogs

**All Agents Must:**
- Post devlogs using: `python tools/devlog_poster.py --agent Agent-X --file <devlog_path>`
- Include "Next Steps" section in ALL devlogs
- Use skimmable format
- Post after assignment completion

---

## Current Enforcement Status

**Assignment Devlog Requirements:**
- All agents notified of devlog standards
- Next Steps section mandatory
- Skimmable format required
- Post after assignment completion

---

**Status:** ✅ STANDARDS DOCUMENTED - 🟡 ENFORCEMENT ACTIVE







