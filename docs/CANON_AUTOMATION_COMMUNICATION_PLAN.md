<!-- SSOT Domain: documentation -->

# Canon Automation: Communication Plan

**Date**: 2025-12-22
**Purpose**: How swarm members will learn about the canon automation system

---

## Communication Channels Created

### 1. **Central Announcement File**
**Location**: `agent_workspaces/SYSTEM_UPDATES.md`

**Purpose**: Single source of truth for system-wide announcements

**Content**:
* What the system is
* How it works (for agents)
* What gets extracted
* Authority flow
* Where to find more info

**How agents discover it**:
* Checked during onboarding
* Referenced in workspace README
* Can be read anytime

---

### 2. **Agent Workspace README**
**Location**: `agent_workspaces/README.md`

**Purpose**: Entry point for agents to understand workspace structure

**Content**:
* Workspace structure
* Important files (including SYSTEM_UPDATES.md)
* Communication methods
* Canon automation announcement summary

**How agents discover it**:
* First file they see when exploring workspaces
* Referenced in onboarding

---

### 3. **Detailed Agent Guide**
**Location**: `docs/CANON_AUTOMATION_FOR_AGENTS.md`

**Purpose**: Comprehensive guide for agents

**Content**:
* What you need to know
* What you need to do
* How it works (detailed)
* What gets extracted (with examples)
* Authority separation
* Benefits for agents
* FAQ

**How agents discover it**:
* Referenced in SYSTEM_UPDATES.md
* Part of documentation structure
* Can be searched/found

---

### 4. **System Update Check Script**
**Location**: `scripts/check_system_updates.py`

**Purpose**: Easy way for agents to check for updates

**Usage**:
```bash
python scripts/check_system_updates.py
```

**Output**: Displays SYSTEM_UPDATES.md content

**How agents discover it**:
* Referenced in documentation
* Can be added to agent toolkits
* Can be run on-demand

---

### 5. **Protocol Documentation**
**Location**: `digitaldreamscape.site/docs/CANON_AUTOMATION_PROTOCOL.md`

**Purpose**: Technical protocol for the system

**Content**:
* Authority flow
* Integration points
* Technical details
* Process steps

**How agents discover it**:
* Referenced in SYSTEM_UPDATES.md
* Part of Digital Dreamscape documentation

---

### 6. **Quick Start Guide**
**Location**: `digitaldreamscape.site/docs/CANON_AUTOMATION_QUICK_START.md`

**Purpose**: Quick reference for using the system

**Content**:
* How to run extraction
* Review results
* Process candidates

**How agents discover it**:
* Referenced in SYSTEM_UPDATES.md
* Part of Digital Dreamscape documentation

---

### 7. **Tool Documentation**
**Location**: `tools/canon_automation.py` (docstring)

**Purpose**: Technical documentation in the tool itself

**Content**:
* Tool purpose
* Usage instructions
* References to other docs

**How agents discover it**:
* When examining the tool
* Via help/docstrings

---

### 8. **Blog Post (Narrative)**
**Location**: `digitaldreamscape.site/blog/005-automating-canon.md`

**Purpose**: Narrative integration of the system

**Content**:
* Story of building the system
* How it fits the Digital Dreamscape
* Authority flow explained narratively

**How agents discover it**:
* Part of Digital Dreamscape narrative
* Referenced in documentation

---

## Discovery Paths for Agents

### Path 1: Workspace Exploration
```
agent_workspaces/
  → README.md (mentions SYSTEM_UPDATES.md)
    → SYSTEM_UPDATES.md (full announcement)
      → Links to detailed docs
```

### Path 2: Documentation Search
```
docs/
  → CANON_AUTOMATION_FOR_AGENTS.md (comprehensive guide)
    → References to other docs
```

### Path 3: Tool Discovery
```
tools/
  → canon_automation.py (tool with docstring)
    → References to docs
```

### Path 4: Script Execution
```
scripts/
  → check_system_updates.py
    → Displays SYSTEM_UPDATES.md
```

### Path 5: Digital Dreamscape Docs
```
digitaldreamscape.site/docs/
  → CANON_AUTOMATION_PROTOCOL.md
  → CANON_AUTOMATION_QUICK_START.md
```

---

## Recommended Agent Workflow

1. **Check SYSTEM_UPDATES.md** when starting work
2. **Read CANON_AUTOMATION_FOR_AGENTS.md** for details
3. **Run check_system_updates.py** to stay current
4. **Reference protocol docs** for technical questions

---

## Future Enhancements

**Potential additions**:
* Automated notification when SYSTEM_UPDATES.md changes
* Integration with agent onboarding
* Periodic reminders to check updates
* Agent-specific update summaries

---

## Summary

**8 communication channels** ensure agents can discover the canon automation system:

1. ✅ Central announcement (SYSTEM_UPDATES.md)
2. ✅ Workspace README (points to updates)
3. ✅ Detailed agent guide (comprehensive)
4. ✅ Update check script (easy access)
5. ✅ Protocol documentation (technical)
6. ✅ Quick start guide (reference)
7. ✅ Tool documentation (inline)
8. ✅ Blog post (narrative)

**Multiple discovery paths** ensure agents will find it:
* Workspace exploration
* Documentation search
* Tool discovery
* Script execution
* Digital Dreamscape docs

**No single point of failure** - if one channel is missed, others exist.

---

*Part of the Digital Dreamscape communication system*

