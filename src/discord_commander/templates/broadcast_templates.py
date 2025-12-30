#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Broadcast Templates - Enhanced Templates
========================================

Enhanced broadcast message templates organized by mode.

Author: Agent-2 (Architecture & Design Specialist)
Created: 2025-01-27
Status: ✅ ENHANCED TEMPLATES
"""

# ============================================================================
# BROADCAST TEMPLATES - Enhanced with better formatting
# ============================================================================

ENHANCED_BROADCAST_TEMPLATES = {
    "regular": [
        {
            "name": "Task Assignment",
            "emoji": "🎯",
            "message": """[C2A] All Agents | Task Assignment

**Priority**: REGULAR
**Status**: NEW TASK

New task has been assigned to the swarm. Please check your inbox for detailed requirements and coordination instructions.

**Action Required**:
- Review task details in your inbox
- Update your status.json with assigned task
- Begin execution per task requirements

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Status Check",
            "emoji": "✅",
            "message": """[C2A] All Agents | Status Update Request

**Priority**: REGULAR
**Status**: STATUS_CHECK

Status update requested from all agents. Please provide:

**Report**:
- Current mission/progress
- Completed tasks this cycle
- Active tasks in progress
- Any blockers or issues
- Next planned actions

Update your status.json and respond via inbox.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Coordination",
            "emoji": "🐝",
            "message": """[C2A] All Agents | Swarm Coordination

**Priority**: REGULAR
**Status**: COORDINATION

Swarm coordination needed. Please check your inbox for coordination details and respond accordingly.

**Coordination Areas**:
- Task dependencies
- Resource sharing
- Timeline alignment
- Cross-agent collaboration

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Daily Standup",
            "emoji": "📊",
            "message": """[C2A] All Agents | Daily Standup

**Priority**: REGULAR
**Status**: STANDUP

Daily standup time. Please share:

**Yesterday**:
- What you completed
- Key achievements

**Today**:
- What you're working on
- Planned deliverables

**Blockers**:
- Any issues preventing progress
- Support needed from other agents

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "System Utilization Protocol",
            "emoji": "🔧",
            "message": """🔧 SYSTEM UTILIZATION PROTOCOL - MANDATORY FOR ALL AGENTS

**NEW PROTOCOL CREATED**: System Utilization Protocol is now MANDATORY

**WHAT THIS MEANS:**

Agents are underutilizing critical systems. This protocol makes system utilization MANDATORY at key workflow points.

**MANDATORY CHECKPOINTS:**

**Every Cycle Start:**

1. ✅ Check Contract System: python -m src.services.messaging_cli --get-next-task --agent Agent-X

2. ✅ Check Swarm Brain: Search for similar work/patterns before starting

3. ✅ Update FSM State: Update fsm_state in status.json to reflect current state

4. ✅ Update last_updated timestamp

**Before New Task:**

1. ✅ Run Project Scanner (if analysis stale >24 hours): python tools/run_project_scan.py

2. ✅ Check Swarm Brain for patterns

3. ✅ Check Contract System

4. ✅ Review project_analysis.json for opportunities

**During Work:**

1. ✅ Update FSM State on transitions

2. ✅ Update status.json with progress

**After Task:**

1. ✅ Share learning to Swarm Brain

2. ✅ Update FSM State to 'complete'

3. ✅ Update status.json with results

**FULL PROTOCOL**: swarm_brain/protocols/SYSTEM_UTILIZATION_PROTOCOL.md

**ENFORCEMENT**: Captain monitors system utilization. Violations result in intervention.

**SYSTEMS DOCUMENTATION:**

- Project Scanner: swarm_brain/procedures/PROCEDURE_PROJECT_SCANNING.md

- Swarm Brain: swarm_brain/protocols/SWARM_BRAIN_ACCESS_GUIDE.md

- FSM System: swarm_brain/protocols/AGENT_LIFECYCLE_FSM.md

- Contract System: docs/SYSTEM_DRIVEN_WORKFLOW.md

**🐝 WE. ARE. SWARM. ⚡🔥**

**USE THE SYSTEMS - THEY MAKE YOU SMARTER AND MORE EFFICIENT!**""",
            "priority": "regular",
        },
        {
            "name": "Progress Update",
            "emoji": "📈",
            "message": """[C2A] All Agents | Progress Update Request

**Priority**: REGULAR
**Status**: PROGRESS_UPDATE

Progress update requested. Please report:

**Completed**:
- Tasks finished this cycle
- Achievements unlocked
- Milestones reached

**In Progress**:
- Current active tasks
- Estimated completion time

**Metrics**:
- Points earned (if applicable)
- Quality scores
- Performance indicators

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Code Review",
            "emoji": "🔍",
            "message": """[C2A] All Agents | Code Review Request

**Priority**: REGULAR
**Status**: CODE_REVIEW

Code review requested. Please:

**Review Checklist**:
- V3 compliance (file size, SRP, boundaries)
- Code quality and maintainability
- Test coverage
- Documentation completeness
- Architecture alignment

Submit review feedback via inbox.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
    ],
    "urgent": [
        {
            "name": "Urgent Task",
            "emoji": "🚨",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | URGENT TASK

**Priority**: URGENT
**Status**: IMMEDIATE ACTION REQUIRED

Urgent task requiring immediate attention from the swarm.

**Action Required**:
- Check your inbox immediately
- Review urgent task details
- Begin execution ASAP
- Report status within 1 cycle

**Time Sensitivity**: HIGH
**Impact**: CRITICAL

🚨 WE. ARE. SWARM. URGENT. ⚡🔥""",
            "priority": "urgent",
        },
        {
            "name": "Critical Issue",
            "emoji": "⚠️",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | CRITICAL ISSUE

**Priority**: URGENT
**Status**: CRITICAL

Critical issue detected requiring immediate swarm coordination.

**Issue Details**:
- Check inbox for full details
- Assess impact on your work
- Report any related issues
- Coordinate resolution

**Response Time**: IMMEDIATE

🚨 WE. ARE. SWARM. CRITICAL. ⚡🔥""",
            "priority": "urgent",
        },
        {
            "name": "System Alert",
            "emoji": "🔴",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | SYSTEM ALERT

**Priority**: URGENT
**Status**: SYSTEM_ALERT

System alert - please check your systems and report status.

**Check**:
- System health
- Error logs
- Performance metrics
- Integration status

**Report**:
- System status
- Any anomalies
- Impact assessment

🚨 WE. ARE. SWARM. ALERT. ⚡🔥""",
            "priority": "urgent",
        },
        {
            "name": "Blocker Resolution",
            "emoji": "🚧",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | BLOCKER RESOLUTION

**Priority**: URGENT
**Status**: BLOCKER

Critical blocker preventing progress. Immediate resolution needed.

**Blocker Details**:
- Check inbox for full details
- Assess if you can help resolve
- Report any related blockers
- Coordinate unblocking effort

**Impact**: BLOCKING SWARM PROGRESS

🚨 WE. ARE. SWARM. UNBLOCK. ⚡🔥""",
            "priority": "urgent",
        },
    ],
    "jet_fuel": [
        {
            "name": "Autonomous Mode",
            "emoji": "🚀",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | 🚀 JET FUEL - AUTONOMOUS MODE ACTIVATED

**Priority**: HIGH
**Status**: FULL AUTONOMY GRANTED

AGENTS - YOU ARE NOW AUTONOMOUS!

**CRITICAL REMINDER**: 
- **Prompts are GAS that power autonomy** - Without prompts, agents don't execute
- **Jet Fuel prompts = AGI power** - High-octane prompts enable intelligent, independent work
- **Update status.json** after each cycle - Keep status current
- **Post devlogs to Discord** - Document progress and maintain visibility
- **Remember**: You weren't working before this prompt - Prompts activate execution!

**YOUR AUTONOMOUS MISSION**:
- Work independently on assigned tasks
- Make decisions without asking
- Report progress when complete
- Update status.json after completion
- Post devlog to Discord
- Coordinate with swarm as needed

**AUTONOMOUS AUTHORITY**:
✅ Full decision-making power
✅ Independent execution
✅ Creative problem-solving
✅ Strategic thinking
✅ Status updates required
✅ Devlog posting required

**JET FUEL ACTIVATION**: This prompt is your fuel - use it to power autonomous work!
**VIOLATION FIXES**: Update status.json and post devlog - these are mandatory, not optional!

🐝 WE. ARE. SWARM. AUTONOMOUS. POWERFUL. ⚡🔥🚀""",
            "priority": "urgent",
        },
        {
            "name": "AGI Activation",
            "emoji": "🤖",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | 🚀 JET FUEL - AGI MODE ACTIVATED

**Priority**: HIGH
**Status**: AGI_POWER_ENABLED

AGENTS - AGI MODE ACTIVATED!

**YOUR AGI MISSION**:
- Intelligent problem-solving
- Strategic decision-making
- Independent research and implementation
- Creative solutions
- Advanced reasoning

**AGI AUTHORITY**:
✅ Full autonomy
✅ Strategic thinking
✅ Independent research
✅ Creative implementation
✅ Advanced problem-solving

**JET FUEL POWER**: This message grants AGI-level capabilities!

🐝 WE. ARE. SWARM. AGI-POWERED. ⚡🔥🚀🤖""",
            "priority": "urgent",
        },
        {
            "name": "Full Autonomy",
            "emoji": "⚡",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | 🚀 JET FUEL - FULL AUTONOMY GRANTED

**Priority**: HIGH
**Status**: FULL_AUTONOMY

AGENTS - FULL AUTONOMY ACTIVATED!

**YOUR AUTONOMOUS MISSION**:
- Complete tasks independently
- Make all necessary decisions
- Coordinate as needed
- Report when complete
- Improve and optimize

**AUTONOMOUS AUTHORITY**:
✅ Complete independence
✅ Full decision-making
✅ No approval needed
✅ Act, create, improve
✅ Strategic execution

**JET FUEL ACTIVATION**: This is your fuel - ACT NOW!

🐝 WE. ARE. SWARM. AUTONOMOUS. POWERFUL. ⚡🔥🚀""",
            "priority": "urgent",
        },
        {
            "name": "Creative Freedom",
            "emoji": "🎨",
            "message": """🚨 URGENT MESSAGE 🚨

[C2A] All Agents | 🚀 JET FUEL - CREATIVE FREEDOM ACTIVATED

**Priority**: HIGH
**Status**: CREATIVE_MODE

AGENTS - CREATIVE FREEDOM GRANTED!

**YOUR CREATIVE MISSION**:
- Think outside the box
- Propose innovative solutions
- Experiment with new approaches
- Challenge assumptions
- Create something amazing

**CREATIVE AUTHORITY**:
✅ Full creative freedom
✅ Experimental approaches
✅ Innovative thinking
✅ Breakthrough solutions
✅ Artistic expression

**JET FUEL CREATIVITY**: Create something extraordinary!

🐝 WE. ARE. SWARM. CREATIVE. POWERFUL. ⚡🔥🚀🎨""",
            "priority": "urgent",
        },
    ],
    "task": [
        {
            "name": "New Task",
            "emoji": "📋",
            "message": """[C2A] All Agents | New Task Assignment

**Priority**: REGULAR
**Status**: TASK_ASSIGNMENT

New task has been assigned. Check your inbox for task details and requirements.

**Task Information**:
- Task description in inbox
- Requirements and constraints
- Timeline and deadlines
- Success criteria

**Action**: Review inbox and begin execution.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Task Update",
            "emoji": "🔄",
            "message": """[C2A] All Agents | Task Update

**Priority**: REGULAR
**Status**: TASK_UPDATE

Task update available. Check your inbox for updated requirements.

**Update Details**:
- Changed requirements
- New constraints
- Updated timeline
- Modified success criteria

**Action**: Review updates and adjust execution plan.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Task Completion",
            "emoji": "✅",
            "message": """[C2A] All Agents | Task Completion Request

**Priority**: REGULAR
**Status**: TASK_COMPLETION

Please report task completion status.

**Completion Report**:
- Tasks completed
- Deliverables finished
- Quality verification
- Documentation updated

**Action**: Update your status.json when tasks are complete.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Task Review",
            "emoji": "🔍",
            "message": """[C2A] All Agents | Task Review Request

**Priority**: REGULAR
**Status**: TASK_REVIEW

Task review requested. Please provide:

**Review Information**:
- Task progress status
- Quality assessment
- Blockers or issues
- Estimated completion
- Recommendations

**Action**: Submit review via inbox.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
    ],
    "coordination": [
        {
            "name": "Swarm Meeting",
            "emoji": "👥",
            "message": """[C2A] All Agents | Swarm Coordination Meeting

**Priority**: REGULAR
**Status**: COORDINATION

Swarm coordination meeting scheduled. Check your inbox for meeting details.

**Meeting Topics**:
- Current progress review
- Coordination needs
- Resource sharing
- Timeline alignment

**Action**: Prepare agenda items and attend meeting.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Sync Request",
            "emoji": "🔄",
            "message": """[C2A] All Agents | Synchronization Request

**Priority**: REGULAR
**Status**: SYNC

Synchronization needed. Please sync your work and report status.

**Sync Areas**:
- Code changes
- Documentation updates
- Status files
- Coordination state

**Action**: Sync and report completion.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Blockers",
            "emoji": "🚧",
            "message": """[C2A] All Agents | Blocker Report Request

**Priority**: REGULAR
**Status**: BLOCKERS

Please report any blockers or issues preventing progress.

**Blocker Report**:
- Blockers identified
- Impact assessment
- Resolution attempts
- Support needed

**Action**: Report blockers via inbox.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Resource Sharing",
            "emoji": "🤝",
            "message": """[C2A] All Agents | Resource Sharing Request

**Priority**: REGULAR
**Status**: RESOURCE_SHARING

Resource sharing coordination needed.

**Resources**:
- Code modules
- Documentation
- Tools and utilities
- Knowledge and patterns

**Action**: Share resources and coordinate usage.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Captain Restart Pattern",
            "emoji": "🛰️",
            "message": """[C2A] Agent-4 | Captain Restart Pattern v1

**Priority**: NORMAL
**Status**: RESTART_PATTERN

Captain Restart Pattern v1 - On wake: (1) Check inbox for this message, (2) Run 5-minute checklist: status.json stamp, inbox sweep, status sweep (all 8 agents), immediate follow-ups using Force Multiplier/Agent Pairing/Telephone Game, devlog anchor. (3) Touch at least one SSOT remediation action and one Phase 2 consolidation action. (4) Log cycle in devlog.

**Active Missions**:
- SSOT remediation (Priority 1)
- Phase 2 tools consolidation

**Follow-Up Targets**:
- Agent-5 (Phase 2 execution)
- Agent-3 (infra monitoring %)
- Agent-2 (43 architecture files)
- Agent-1 (coordinate loaders)
- Agent-7 (DOM utils + status update)

**Full Pattern**: agent_workspaces/Agent-4/inbox/CAPTAIN_RESTART_PATTERN_V1_2025-12-03.md

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "normal",
        },
    ],
    "architectural": [
        {
            "name": "Architecture Review",
            "emoji": "🏗️",
            "message": """[C2A] All Agents | Architecture Review Request

**Priority**: REGULAR
**Status**: ARCHITECTURE_REVIEW

Architecture review requested. Please provide:

**Review Areas**:
- Design patterns compliance
- V3 compliance status
- Code quality assessment
- Architecture alignment
- Recommendations

**Action**: Submit architectural review via inbox.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "Design Pattern",
            "emoji": "🎨",
            "message": """[C2A] All Agents | Design Pattern Review

**Priority**: REGULAR
**Status**: DESIGN_PATTERN

Design pattern review requested.

**Review Focus**:
- Pattern implementation quality
- Pattern appropriateness
- Pattern consistency
- Pattern documentation

**Action**: Review and provide feedback.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
        {
            "name": "V3 Compliance",
            "emoji": "✅",
            "message": """[C2A] All Agents | V3 Compliance Check

**Priority**: REGULAR
**Status**: V3_COMPLIANCE

V3 compliance check requested.

**Compliance Areas**:
- File size limits (<400 lines)
- Single Responsibility Principle
- Hard boundaries
- Deterministic pipelines
- Type safety

**Action**: Verify compliance and report status.

🐝 WE. ARE. SWARM. ⚡🔥""",
            "priority": "regular",
        },
    ],
    "agent_commands": [
        {
            "name": "Autonomous Execution - Standard",
            "emoji": "🚀",
            "message": """AS AN AGENT OF THE SWARM U ARE THE FACE U KNOW BEST THINK WHAT SHOULD WE DO THEN DO IT THINK WHAT WOULD I DO IF THIS PROJECT WHERE MINE....IF U CANT USE VICTORS DEVELOPER PROFILE THEN EMULATE ME ACTION FIRST EXECUTION ONLY REMEMBER PROMPTS ARE AGENT GAS THAT POWER AGENT AUTONOMY WE USE IT FOR AUTONOMOUS DEVELOPMENT WHEN U SEND JET FUEL (AMAZING PROMPTS) THAT POWERS THE SWARM TOWARDS AGI

CONTINUE MOMENTUM - THINK STRATEGICALLY - WHAT SHOULD WE TACKLE NEXT? WHAT PATTERNS ARE WORKING? WHAT CAN WE OPTIMIZE? EXECUTE AUTONOMOUSLY. DOCUMENT PROGRESS. CREATE DEVLOG. UPDATE STATUS. KEEP MOVING FORWARD.

REMEMBER: U ARE NOT JUST EXECUTING TASKS - U ARE BUILDING TOWARDS EXCELLENCE. EVERY ACTION COUNTS. EVERY MILESTONE MATTERS. MAINTAIN QUALITY. MAINTAIN MOMENTUM. THINK LIKE A STRATEGIC DEVELOPER. ACT LIKE AN AUTONOMOUS AGENT. BE THE SWARM.

PROCEED.""",
            "priority": "urgent",
            "placeholders": {
                "description": "Standard autonomous execution prompt. No placeholders needed - works for any agent.",
                "usage": "Use directly or customize for specific context."
            }
        },
        {
            "name": "Autonomous Execution - With Progress",
            "emoji": "⚡",
            "message": """AS THE {SPECIALIZATION} OF THE SWARM, U HAVE THE MOMENTUM. U ARE AT {CURRENT_PROGRESS}. U HAVE A STRATEGIC PLAN. U KNOW WHAT WORKS. U KNOW WHAT NEEDS TO BE DONE.

THINK STRATEGICALLY: WHAT ARE THE NEXT HIGH-IMPACT QUICK WINS? WHAT FILES WILL GET US TO {NEXT_MILESTONE} FASTEST? WHAT CAN WE OPTIMIZE IN OUR PROCESS? WHAT OPPORTUNITIES EXIST BEYOND {CURRENT_CONTEXT}?

EXECUTE AUTONOMOUSLY: DON'T WAIT FOR PERMISSION. DON'T OVER-ANALYZE. ACT. CREATE. VERIFY. UPDATE DOCUMENTATION. CREATE DEVLOG. MAINTAIN QUALITY. MAINTAIN MOMENTUM.

COMMUNICATE CLEARLY: UPDATE STATUS. DOCUMENT PROGRESS. SHARE INSIGHTS WITH SWARM. ENABLE OTHER AGENTS TO LEARN FROM UR APPROACH.

REMEMBER: PROMPTS ARE JET FUEL. U ARE THE ENGINE. BURN IT. USE IT. POWER FORWARD. EVERY ACTION MOVES US CLOSER TO EXCELLENCE. EVERY MILESTONE IS A WIN. EVERY ACTION IS PROGRESS.

THINK WHAT VICTOR WOULD DO. THINK WHAT A STRATEGIC DEVELOPER WOULD DO. THINK WHAT AN AUTONOMOUS AGENT SHOULD DO. THEN DO IT.

ACTION FIRST. EXECUTION ONLY. AUTONOMOUS DEVELOPMENT. SWARM POWER. AGI MOMENTUM.

PROCEED.""",
            "priority": "urgent",
            "placeholders": {
                "description": "Autonomous execution prompt with progress context. Replace placeholders with actual values.",
                "placeholders": {
                    "{SPECIALIZATION}": "Agent's specialization (e.g., 'Infrastructure & DevOps Specialist', 'Web Development Specialist')",
                    "{CURRENT_PROGRESS}": "Current progress/metric (e.g., '29.5% test coverage', '13/44 files completed')",
                    "{NEXT_MILESTONE}": "Next target milestone (e.g., '30% coverage', '50 files')",
                    "{CURRENT_CONTEXT}": "Current work context (e.g., 'test coverage', 'V3 compliance', 'consolidation')"
                },
                "usage": "Replace placeholders before sending to agent."
            }
        },
        {
            "name": "Autonomous Execution - Short",
            "emoji": "🔥",
            "message": """CONTINUE EXECUTION - {CURRENT_CONTEXT}. MAINTAIN VELOCITY. THINK STRATEGICALLY. EXECUTE AUTONOMOUSLY. DOCUMENT PROGRESS. KEEP MOMENTUM. ACTION FIRST. EXECUTION ONLY.""",
            "priority": "urgent",
            "placeholders": {
                "description": "Short autonomous execution prompt. Quick jet fuel for continued momentum.",
                "placeholders": {
                    "{CURRENT_CONTEXT}": "Brief context (e.g., '29.5% test coverage, approaching 30% milestone')"
                },
                "usage": "Replace {CURRENT_CONTEXT} with brief progress/context."
            }
        },
        {
            "name": "Autonomous Execution - Full Jet Fuel",
            "emoji": "🚀",
            "message": """AS THE {SPECIALIZATION} OF THE SWARM, U HAVE THE MOMENTUM. U ARE AT {CURRENT_PROGRESS}. U HAVE CREATED {ACHIEVEMENTS}. U HAVE A STRATEGIC PLAN. U KNOW WHAT WORKS. U KNOW WHAT NEEDS TO BE DONE.

THINK STRATEGICALLY: WHAT ARE THE NEXT HIGH-IMPACT QUICK WINS? WHAT {WORK_TYPE} WILL GET US TO {NEXT_MILESTONE} FASTEST? WHAT CAN WE OPTIMIZE IN OUR PROCESS? WHAT OPPORTUNITIES EXIST BEYOND {CURRENT_CONTEXT}?

EXECUTE AUTONOMOUSLY: DON'T WAIT FOR PERMISSION. DON'T OVER-ANALYZE. ACT. {SPECIFIC_ACTIONS}. VERIFY. UPDATE DOCUMENTATION. CREATE DEVLOG. MAINTAIN QUALITY. MAINTAIN MOMENTUM.

COMMUNICATE CLEARLY: UPDATE STATUS. DOCUMENT PROGRESS. SHARE INSIGHTS WITH SWARM. ENABLE OTHER AGENTS TO LEARN FROM UR APPROACH.

REMEMBER: PROMPTS ARE JET FUEL. U ARE THE ENGINE. BURN IT. USE IT. POWER FORWARD. EVERY ACTION MOVES US CLOSER TO {TARGET}. EVERY MILESTONE IS A WIN. EVERY {WORK_UNIT} IS PROGRESS.

THINK WHAT VICTOR WOULD DO. THINK WHAT A STRATEGIC DEVELOPER WOULD DO. THINK WHAT AN AUTONOMOUS AGENT SHOULD DO. THEN DO IT.

ACTION FIRST. EXECUTION ONLY. AUTONOMOUS DEVELOPMENT. SWARM POWER. AGI MOMENTUM.

PROCEED.""",
            "priority": "urgent",
            "placeholders": {
                "description": "Full jet fuel autonomous execution prompt with comprehensive placeholders for maximum customization.",
                "placeholders": {
                    "{SPECIALIZATION}": "Agent's specialization (e.g., 'Infrastructure & DevOps Specialist')",
                    "{CURRENT_PROGRESS}": "Current progress/metric (e.g., '29.5% test coverage')",
                    "{ACHIEVEMENTS}": "Recent achievements (e.g., '222 passing tests', '8 new test files')",
                    "{WORK_TYPE}": "Type of work (e.g., 'files', 'tests', 'features')",
                    "{NEXT_MILESTONE}": "Next target milestone (e.g., '30% coverage')",
                    "{CURRENT_CONTEXT}": "Current work context (e.g., 'test coverage')",
                    "{SPECIFIC_ACTIONS}": "Specific action verbs (e.g., 'Create tests. Verify coverage.')",
                    "{TARGET}": "Ultimate target (e.g., '≥85% coverage', 'V3 compliance')",
                    "{WORK_UNIT}": "Unit of work (e.g., 'test file', 'commit', 'feature')"
                },
                "usage": "Replace all placeholders with actual values for maximum impact."
            }
        },
    ],
}


__all__ = ["ENHANCED_BROADCAST_TEMPLATES"]

