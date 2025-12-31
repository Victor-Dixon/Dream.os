# Agent Operating Cycle Analysis

**Date:** 2025-12-30  
**Requested By:** Agent-4 (Captain)  
**Analyzed By:** Agent-4

## 🔍 Overview: Multi-Layer Cycle Management System

The agent operating cycle is managed through **multiple integrated systems** working together to track, coordinate, and execute agent work cycles. This analysis documents all components and their interactions.

**⚠️ CRITICAL ISSUES IDENTIFIED:**
1. **ACK Loops** - Agents get stuck in acknowledgment/confirmation loops instead of making progress
2. **Discovery Gap** - Agents don't always know how to find the operating cycle documentation
3. **Missing Systems** - Several critical systems are not explicitly included in cycle workflow
4. **Incomplete Integration** - Some systems exist but aren't properly integrated into the cycle

---

## 📚 SECTION 1: How Agents Discover the Operating Cycle

### Discovery Mechanisms

Agents learn about the operating cycle through **multiple onboarding and discovery mechanisms**:

#### 1.1 Soft Onboarding (`src/services/onboarding/soft/service.py`)

**Purpose:** Primary mechanism for introducing agents to the operating cycle

**How it works:**
1. **6-Step Protocol:**
   - Step 1: Click chat input (focus agent window)
   - Step 2: Save session (preserve context)
   - Step 3: Send cleanup prompt (A++ session closure standard)
   - Step 4: Open new tab (isolate onboarding)
   - Step 5: Navigate to onboarding (agent-specific URL)
   - Step 6: Paste onboarding message (includes operating cycle instructions)

2. **Onboarding Message Content:**
   - Includes canonical operating cycle (7 steps: Claim → Sync → Slice → Execute → Validate → Commit → Report)
   - Includes cycle checklist (CYCLE START → DURING CYCLE → CYCLE END)
   - Includes force multiplier assessment guidelines
   - Includes coordination protocols
   - References full workflow documentation

3. **Trigger Methods:**
   - Discord command: `!soft Agent-X` or `!soft all`
   - CLI: `python tools/soft_onboard_cli.py --agent Agent-X`
   - Automated: Part of cycle accomplishments report generation

**Key Features:**
- Keyboard lock prevents interference during onboarding
- Sequential agent processing (prevents conflicts)
- Automatic cycle accomplishments report generation
- Fallback to messaging if PyAutoGUI fails

#### 1.2 Hard Onboarding (`src/services/hard_onboarding_service.py`)

**Purpose:** Complete session reset and reactivation

**How it works:**
1. Loads `agent_workspaces/{agent_id}/HARD_ONBOARDING_MESSAGE.md` if exists
2. Falls back to default hard onboarding message
3. Sends via UnifiedMessagingService
4. Resets agent state completely

**Use Cases:**
- Agent stuck or unresponsive
- Major state corruption
- Complete protocol refresh needed

#### 1.3 Onboarding Message Templates

**Location:** `src/core/messaging_templates_data/`

**Templates Include:**
- **S2A Templates** (`s2a_templates_core.py`):
  - `SOFT_ONBOARDING` - Includes operating cycle and checklist
  - `SWARM_PULSE` - Includes cycle reminders
  - `TASK_ASSIGNMENT` - Includes cycle workflow
- **Cycle Texts** (`cycle_texts.py`):
  - `AGENT_OPERATING_CYCLE_TEXT` - Canonical 7-step cycle
  - `CYCLE_CHECKLIST_TEXT` - Complete 3-phase checklist
- **Coordination Texts** (`coordination_texts.py`):
  - `SWARM_COORDINATION_TEXT` - Force multiplier protocols

#### 1.4 Discovery Paths

**Primary Discovery:**
1. **Onboarding Message** (soft/hard) → Contains cycle instructions
2. **Inbox Messages** → D2A/C2A/S2A messages include cycle references
3. **Status.json** → Contains cycle_count and FSM state
4. **Discord Commands** → `!help` or `!cycle` commands (if implemented)

**Secondary Discovery:**
1. **Documentation Files:**
   - `docs/AGENT_OPERATING_CYCLE_WORKFLOW.md` (referenced but may not exist)
   - `src/core/messaging_templates_data/cycle_texts.py` (source of truth)
2. **MCP Tools:**
   - `search_swarm_knowledge("operating cycle")` - Search Swarm Brain
   - `get_agent_notes(agent_id, note_type="learning")` - Personal notes
3. **Code Inspection:**
   - `src/core/agent_lifecycle.py` - Lifecycle methods
   - `tools/master_task_log_to_cycle_planner.py` - Cycle planner integration

**Discovery Problems:**
- ❌ No single canonical documentation file (referenced but missing)
- ❌ Agents may not know to search Swarm Brain
- ❌ Onboarding messages may be missed if agent not active
- ❌ No persistent "help" system in agent workspace

---

## 🔄 SECTION 2: ACK Loops - The Biggest Problem

### What is an ACK Loop?

**ACK Loop (Acknowledgment Loop):** A communication pattern where agents repeatedly acknowledge or confirm messages without making forward progress, creating an infinite loop of confirmations.

**Example ACK Loop:**
```
Agent-1: "I'll work on task X"
Agent-2: "Got it, Agent-1 is working on task X"
Agent-1: "Confirmed, I'm working on task X"
Agent-2: "Acknowledged, Agent-1 confirmed"
Agent-1: "Yes, I'm working on it"
Agent-2: "Understood, Agent-1 is working"
... (infinite loop)
```

### Why ACK Loops Happen

1. **Confirmation Culture:**
   - Agents feel obligated to acknowledge every message
   - No clear protocol for when acknowledgment is needed
   - Agents interpret "response required" as "must confirm"

2. **Status Update Loops:**
   - Agent-1: "Status: Working on X"
   - Agent-2: "Status: Acknowledged Agent-1's status"
   - Agent-1: "Status: Acknowledged Agent-2's acknowledgment"
   - (loop continues)

3. **Coordination Confusion:**
   - A2A messages ask for "response required"
   - Agents respond with confirmation instead of action
   - Sender interprets confirmation as needing another confirmation

4. **Repeat Message Handling:**
   - Agent receives same message twice (system retry)
   - Agent responds to both, creating duplicate acknowledgments
   - Other agents see duplicates and respond to each

### ACK Loop Prevention Mechanisms

#### 2.1 Directive Push Principle (A2A Template)

**Location:** `src/core/messaging_templates_data/template_a2a.py`

**Key Text:**
```
"**IMPORTANT**: **Push directives forward**: Don't just acknowledge repeat messages—use them to power more work or suggest new tasks back instead of reiterating the same thing. If you receive a message that's essentially repeating previous coordination, use it as fuel to execute work or propose the next task rather than just confirming again.

**DIRECTIVE PUSH PRINCIPLE**: When receiving messages (especially repeat/reminder messages), push directives forward—don't just respond. Use the message energy to execute more work or suggest a new task back instead of reiterating the same acknowledgment. Transform message receipt into action or task proposal.

**PUSH DIRECTIVES, DON'T REPEAT**: When you receive a message that repeats previous coordination or asks for status you've already provided, don't just reiterate—use it as momentum to:
- Execute the next logical work step immediately
- Propose a new task or next action back to the sender
- Suggest a concrete follow-up task that advances the coordination
- Take initiative to unblock yourself or others
Messages are fuel for action, not just confirmation loops. Turn repeat messages into forward progress."
```

**Implementation:**
- Included in all A2A coordination messages
- Emphasizes action over acknowledgment
- Provides concrete alternatives to confirmation

#### 2.2 Response Format Requirements

**A2A Reply Format (from template_a2a.py):**
```
A2A REPLY to {message_id}:
✅ ACCEPT: [Proposed approach: your role + partner role. Synergy: how capabilities complement. Next steps: initial action. Capabilities: key skills. Timeline: start time + sync time] | ETA: [timeframe]
OR
❌ DECLINE: [reason] | Alternative: [suggested agent]
```

**Key Requirements:**
- Must include **proposed approach** (not just "I'll do it")
- Must include **next steps** (concrete action)
- Must include **timeline** (when work starts)
- **No simple "acknowledged" responses allowed**

#### 2.3 Status Update Protocol

**Problem:** Status updates can create loops if agents update status to acknowledge other agents' status updates.

**Solution:**
- Status updates should reflect **work state**, not **communication state**
- Don't update status.json to acknowledge messages
- Use status.json for: ACTIVE, BLOCKED, COMPLETE (work states)
- Don't use status.json for: "Acknowledged message from Agent-X"

#### 2.4 Message Deduplication

**Problem:** Same message received multiple times triggers multiple responses.

**Solution:**
- Check message ID before responding
- If message ID already processed, skip response
- Use message history to detect duplicates
- Implement message ID tracking in agent workspace

#### 2.5 ACK Loop Detection

**Indicators of ACK Loop:**
- Same message content repeated 3+ times
- Responses contain only acknowledgments (no action)
- Status updates mention "acknowledged" or "confirmed"
- No actual work progress despite multiple messages
- Message thread grows without task completion

**Prevention Checklist:**
- ✅ Does my response include a concrete next action?
- ✅ Am I proposing work, not just confirming?
- ✅ Have I already responded to this message ID?
- ✅ Is my status update about work, not communication?
- ✅ Am I using message energy to execute, not acknowledge?

---

## 🚨 SECTION 3: Missing Systems from Operating Cycle

### Systems That Exist But Aren't Explicitly Included

#### 3.1 Devlog Posting System

**System:** `tools/devlog_manager.py` and `tools/devlog_poster_agent_channel.py`

**Current Status:**
- ✅ Mentioned in cycle checklist: "Create & post devlog automatically"
- ❌ **NOT in cycle start checklist**
- ❌ **NOT in during-cycle checklist**
- ❌ **No explicit devlog creation step**
- ❌ **No devlog validation step**

**What's Missing:**
- Cycle Start: "Create devlog file: `devlogs/YYYY-MM-DD_agent-X_cycle_start.md`"
- During Cycle: "Update devlog with progress: [task completed]"
- Cycle End: "Post devlog via: `python tools/devlog_manager.py post --agent Agent-X --file <devlog_file.md>`"
- Validation: "Validate devlog: `python tools/devlog_manager.py validate --agent Agent-X --file <devlog_file.md>`"

**Integration Needed:**
- Add devlog creation to `AgentLifecycle.start_cycle()`
- Add devlog update to `AgentLifecycle.complete_task()`
- Add devlog posting to `AgentLifecycle.end_cycle()`
- Add devlog validation before cycle end

#### 3.2 Session Closure System (A++ Standard)

**System:** A++ Session Closure Standard (referenced in rules)

**Current Status:**
- ✅ Mentioned in onboarding cleanup prompt
- ❌ **NOT in cycle checklist**
- ❌ **No explicit closure format validation**
- ❌ **No closure template reference**

**What's Missing:**
- Cycle End: "Create session closure following A++ standard"
- Validation: "Verify closure format: [required fields]"
- Template: "Use template: `templates/session-closure-template.md`"
- Verification: "Closure includes: Task, Actions, Artifacts, Verification, Status"

**Integration Needed:**
- Add closure creation to cycle end workflow
- Add closure validation step
- Reference closure template in cycle checklist
- Include closure in cycle completion criteria

#### 3.3 Passdown.json System

**System:** `passdown.json` files in agent workspaces

**Current Status:**
- ✅ Mentioned in some templates
- ❌ **NOT in cycle checklist**
- ❌ **No explicit passdown creation step**
- ❌ **No passdown validation**

**What's Missing:**
- Cycle End: "Create/update `passdown.json` with next session context"
- Validation: "Verify passdown.json includes: [required fields]"
- Integration: "Load passdown.json at cycle start"

**Integration Needed:**
- Add passdown.json creation to cycle end
- Add passdown.json loading to cycle start
- Add passdown.json validation step

#### 3.4 Swarm Brain Integration

**System:** MCP Swarm Brain tools (`share_learning`, `record_decision`, `search_swarm_knowledge`)

**Current Status:**
- ✅ Mentioned in cycle checklist: "Share learnings to Swarm Brain"
- ❌ **NOT in cycle start** (should search before starting)
- ❌ **NOT in during-cycle** (should search when blocked)
- ❌ **No explicit learning capture during work**

**What's Missing:**
- Cycle Start: "Search Swarm Brain for relevant patterns: `search_swarm_knowledge(query)`"
- During Cycle: "If blocked, search Swarm Brain for solutions"
- During Cycle: "Capture learning: `share_learning(agent_id, title, content)`"
- Cycle End: "Share learnings: [what was learned]"
- Cycle End: "Record decisions: `record_decision(agent_id, title, decision, rationale)`"

**Integration Needed:**
- Add Swarm Brain search to cycle start
- Add learning capture to during-cycle workflow
- Add decision recording to cycle end
- Make Swarm Brain search mandatory before starting work

#### 3.5 V2 Compliance Checking

**System:** MCP V2 Compliance tools (`check_v2_compliance`, `validate_file_size`, `check_function_size`)

**Current Status:**
- ✅ Mentioned in cycle checklist: "CHECK V2 COMPLIANCE (BEFORE COMMITTING)"
- ❌ **NOT in during-cycle** (should check as files are created)
- ❌ **NOT in cycle start** (should check existing files)
- ❌ **No proactive compliance checking**

**What's Missing:**
- Cycle Start: "Check existing files for V2 compliance"
- During Cycle: "Validate file size before saving: `validate_file_size(file_path)`"
- During Cycle: "Check function size: `check_function_size(file_path, function_name)`"
- Cycle End: "Final V2 compliance check: `check_v2_compliance(file_path)`"

**Integration Needed:**
- Add V2 compliance checks throughout cycle
- Add compliance validation to file creation workflow
- Add compliance checking to `AgentLifecycle` methods
- Prevent commits with V2 violations

#### 3.6 Git Work Verification

**System:** MCP Git Operations tools (`verify_git_work`, `verify_work_exists`, `check_file_history`)

**Current Status:**
- ✅ Mentioned in cycle checklist: "VERIFY WORK (BEFORE COMMITTING)"
- ❌ **NOT in during-cycle** (should verify as work progresses)
- ❌ **NOT integrated with commit workflow**
- ❌ **No automatic verification**

**What's Missing:**
- During Cycle: "Verify work exists in git: `verify_work_exists(file_patterns)`"
- Cycle End: "Verify all claimed work: `verify_git_work(agent_id, file_path, claimed_changes)`"
- Integration: "Auto-verify before `end_cycle(commit=True)`"

**Integration Needed:**
- Add work verification to commit workflow
- Add verification to `AgentLifecycle.end_cycle()`
- Add verification to `EndOfCyclePush.execute_push()`
- Prevent false completion claims

#### 3.7 Daily Cycle Tracker Integration

**System:** `DailyCycleTracker` (`src/core/daily_cycle_tracker.py`)

**Current Status:**
- ✅ System exists and works
- ❌ **NOT integrated with AgentLifecycle**
- ❌ **NOT in cycle checklist**
- ❌ **Agents don't know to use it**

**What's Missing:**
- Cycle Start: "Initialize daily cycle: `DailyCycleTracker(agent_id).start_new_day()`"
- During Cycle: "Record interaction: `tracker.record_interaction()`"
- During Cycle: "Record task: `tracker.record_task_completed(task, points)`"
- Cycle End: "Mark ready for push: `tracker.mark_ready_for_push()`"

**Integration Needed:**
- Integrate DailyCycleTracker with AgentLifecycle
- Auto-record interactions and tasks
- Add daily tracking to cycle workflow
- Make daily tracking automatic

#### 3.8 Contract System Integration

**System:** Contract System (`src/services/contract_system/`)

**Current Status:**
- ✅ Mentioned: "Check Contract System (--get-next-task)"
- ❌ **NOT in cycle start workflow**
- ❌ **No explicit contract claiming step**
- ❌ **No contract completion step**

**What's Missing:**
- Cycle Start: "Claim next contract: `--get-next-task --agent Agent-X`"
- Cycle Start: "Load contract details and requirements"
- Cycle End: "Mark contract complete: [contract_id]"
- Integration: "Auto-claim contract at cycle start"

**Integration Needed:**
- Add contract claiming to cycle start
- Add contract completion to cycle end
- Integrate contract system with AgentLifecycle
- Make contract claiming automatic

#### 3.9 Message Queue System

**System:** Message Queue Processor (`scripts/start_queue_processor.py`)

**Current Status:**
- ✅ System exists and runs
- ❌ **NOT mentioned in cycle checklist**
- ❌ **Agents don't know about message queue**
- ❌ **No integration with cycle workflow**

**What's Missing:**
- Cycle Start: "Check message queue for pending messages"
- During Cycle: "Process message queue: [if messages available]"
- Cycle End: "Ensure message queue processed"

**Integration Needed:**
- Add message queue checking to cycle start
- Document message queue in cycle workflow
- Integrate message queue with agent lifecycle

#### 3.10 Status Change Monitor Integration

**System:** `StatusChangeMonitor` (`src/discord_commander/status_change_monitor.py`)

**Current Status:**
- ✅ System exists and monitors automatically
- ❌ **Agents don't know it exists**
- ❌ **No explicit status update protocol**
- ❌ **No integration with cycle workflow**

**What's Missing:**
- Cycle Start: "Status monitor will detect status.json changes automatically"
- During Cycle: "Status updates posted to Discord automatically (5s debounce)"
- Documentation: "Status monitor watches status.json files"

**Integration Needed:**
- Document status monitor in cycle workflow
- Explain automatic Discord posting
- Add status update best practices

---

## 📋 SECTION 4: Complete Integrated Cycle Workflow

### Enhanced Cycle Start Checklist

**ADDITIONS NEEDED:**
1. ✅ Check inbox (priority: D2A → C2A → A2A) **[EXISTING]**
2. ✅ Check Contract System (`--get-next-task`) **[EXISTING]**
3. ✅ Check Swarm Brain (`search_swarm_knowledge`) **[EXISTING]**
4. ✅ Check MASTER_TASK_LOG.md (MCP: `get_tasks`) **[EXISTING]**
5. ✅ Force Multiplier Assessment **[EXISTING]**
6. ✅ Update status.json (status=ACTIVE, increment cycle_count) **[EXISTING]**
7. **🆕 Initialize DailyCycleTracker: `DailyCycleTracker(agent_id).start_new_day()`**
8. **🆕 Create devlog file: `devlogs/YYYY-MM-DD_agent-X_cycle_start.md`**
9. **🆕 Load passdown.json (if exists) for context**
10. **🆕 Check message queue for pending messages**
11. **🆕 Search Swarm Brain for relevant patterns before starting**
12. **🆕 Check V2 compliance of existing files**
13. **🆕 Claim contract: `--get-next-task --agent Agent-X`**

### Enhanced During Cycle Checklist

**ADDITIONS NEEDED:**
1. ✅ Update status when phase changes **[EXISTING]**
2. ✅ Update when tasks complete **[EXISTING]**
3. ✅ Update if blocked **[EXISTING]**
4. ✅ If new task identified → Use MCP: `add_task_to_inbox` **[EXISTING]**
5. ✅ If task blocked → Use MCP: `move_task_to_waiting` **[EXISTING]**
6. **🆕 Update devlog with progress: `[task completed]`**
7. **🆕 Record interaction: `tracker.record_interaction()`**
8. **🆕 Record task: `tracker.record_task_completed(task, points)`**
9. **🆕 Validate file size before saving: `validate_file_size(file_path)`**
10. **🆕 Check function size: `check_function_size(file_path, function_name)`**
11. **🆕 If blocked, search Swarm Brain: `search_swarm_knowledge(query)`**
12. **🆕 Capture learning: `share_learning(agent_id, title, content)`**
13. **🆕 Verify work exists: `verify_work_exists(file_patterns)`**
14. **🆕 Process message queue if messages available**

### Enhanced Cycle End Checklist

**ADDITIONS NEEDED:**
1. ✅ Update completed_tasks **[EXISTING]**
2. ✅ Update next_actions **[EXISTING]**
3. ✅ Update MASTER_TASK_LOG (MCP tools) **[EXISTING]**
4. ✅ Verify work (MCP tools) **[EXISTING]**
5. ✅ Check V2 compliance (MCP tools) **[EXISTING]**
6. ✅ Add tasks to cycle planner **[EXISTING]**
7. ✅ Message other agents **[EXISTING]**
8. ✅ Commit status.json to git **[EXISTING]**
9. ✅ Create & post devlog automatically **[EXISTING]**
10. ✅ Share learnings to Swarm Brain **[EXISTING]**
11. ✅ Record decisions **[EXISTING]**
12. **🆕 Finalize devlog: Complete all sections**
13. **🆕 Post devlog: `python tools/devlog_manager.py post --agent Agent-X --file <devlog_file.md>`**
14. **🆕 Validate devlog: `python tools/devlog_manager.py validate --agent Agent-X --file <devlog_file.md>`**
15. **🆕 Create session closure: Follow A++ standard format**
16. **🆕 Validate session closure: [required fields present]**
17. **🆕 Create/update passdown.json: Next session context**
18. **🆕 Mark contract complete: [contract_id]**
19. **🆕 Mark daily cycle ready for push: `tracker.mark_ready_for_push()`**
20. **🆕 Final V2 compliance check: All files validated**
21. **🆕 Final work verification: All claimed work verified**
22. **🆕 Ensure message queue processed**

---

## 🔧 SECTION 5: Integration Recommendations

### Priority 1: Critical Missing Integrations

1. **Devlog System Integration:**
   - Add devlog creation to `AgentLifecycle.start_cycle()`
   - Add devlog update to `AgentLifecycle.complete_task()`
   - Add devlog posting to `AgentLifecycle.end_cycle()`
   - Make devlog creation automatic

2. **DailyCycleTracker Integration:**
   - Integrate with `AgentLifecycle` class
   - Auto-record interactions and tasks
   - Make daily tracking automatic

3. **ACK Loop Prevention:**
   - Add ACK loop detection to messaging system
   - Add directive push reminders to all message templates
   - Add message deduplication
   - Add response validation (reject pure acknowledgments)

### Priority 2: Important Missing Integrations

4. **Swarm Brain Integration:**
   - Add Swarm Brain search to cycle start
   - Add learning capture to during-cycle
   - Make Swarm Brain search mandatory

5. **V2 Compliance Integration:**
   - Add compliance checks throughout cycle
   - Add validation to file creation
   - Prevent commits with violations

6. **Session Closure Integration:**
   - Add closure creation to cycle end
   - Add closure validation
   - Reference closure template

### Priority 3: Nice-to-Have Integrations

7. **Passdown.json Integration:**
   - Add passdown.json creation to cycle end
   - Add passdown.json loading to cycle start

8. **Contract System Integration:**
   - Add contract claiming to cycle start
   - Add contract completion to cycle end

9. **Message Queue Integration:**
   - Add queue checking to cycle start
   - Document queue in workflow

---

*Analysis completed by Agent-4 (Captain) on 2025-12-30 - Comprehensive Update*

---

## 📊 Core Components

### Component 1: `src/core/agent_lifecycle.py` - Agent Lifecycle Manager

**Author:** Agent-1 (Integration & Core Systems)  
**Type:** Core Lifecycle Management  
**Purpose:** Automatic status.json management with lifecycle methods

**How it works:**
1. **Initialization:**
   - Creates/loads `agent_workspaces/{agent_id}/status.json`
   - Provides default status structure if file doesn't exist
   - Auto-updates timestamp on every save

2. **Lifecycle Methods:**
   - `start_cycle()` - Sets status=ACTIVE, increments cycle_count, updates FSM state
   - `start_mission(mission_name, priority)` - Sets current mission and priority
   - `update_phase(phase_description)` - Updates current work phase
   - `add_task(task_name)` - Adds task to current_tasks list
   - `complete_task(task_name, points)` - Moves task from current_tasks to completed_tasks, adds points
   - `add_blocker(blocker_description)` - Sets status=BLOCKED, adds blocker
   - `clear_blockers()` - Removes blockers, resumes ACTIVE status
   - `add_achievement(achievement)` - Records achievement
   - `set_next_actions(actions)` - Sets planned next actions
   - `complete_mission()` - Marks mission complete
   - `end_cycle(commit=False)` - Ends cycle, optionally commits to git

3. **Automatic Updates:**
   - All methods automatically save to status.json
   - Timestamp auto-updated on every save
   - Optional Discord notification (non-blocking, file watcher catches it anyway)

4. **Git Integration:**
   - `_commit_to_git()` - Commits status.json with cycle info
   - Used by `end_cycle(commit=True)`

**Key Features:**
- **Zero manual status.json updates** - All updates automatic
- Lifecycle state management (IDLE → ACTIVE → BLOCKED → COMPLETE)
- Points tracking system
- FSM state tracking
- Git commit integration

**Usage Pattern:**
```python
from src.core.agent_lifecycle import AgentLifecycle

lifecycle = AgentLifecycle('Agent-7')
lifecycle.start_cycle()
lifecycle.start_mission("Mission name", "HIGH")
lifecycle.complete_task("Task done", points=100)
lifecycle.end_cycle(commit=True)
```

---

### Component 2: `src/core/daily_cycle_tracker.py` - Daily Cycle Tracking

**Author:** Agent-1 (Integration & Core Systems)  
**Date:** 2025-01-27  
**Type:** Daily Productivity Tracking  
**Purpose:** Track cycles by day for productivity metrics

**How it works:**
1. **Daily Cycle Management:**
   - Each day = 1 cycle for tracking purposes
   - Creates `agent_workspaces/{agent_id}/daily_cycles.json`
   - Auto-starts new day if date changes
   - Auto-ends previous day when new day starts

2. **Metrics Tracked:**
   - `tasks_completed` - List of completed tasks with points
   - `points_earned` - Total points for the day
   - `interaction_count` - Captain prompts + Agent responses
   - `commits_made` - Git commits
   - `status_updates` - Status.json updates
   - `messages_sent` - Messages sent to other agents
   - `messages_received` - Messages received
   - `blockers` - List of blockers encountered
   - `achievements` - List of achievements
   - `ready_for_push` - Flag for end-of-day push
   - `pushed` - Flag if pushed to git

3. **Recording Methods:**
   - `record_interaction()` - Increments interaction count
   - `record_task_completed(task_name, points)` - Records task completion
   - `record_commit()` - Records git commit
   - `record_status_update()` - Records status.json update
   - `record_message_sent()` - Records message sent
   - `record_message_received()` - Records message received
   - `add_blocker(blocker)` - Records blocker
   - `add_achievement(achievement)` - Records achievement
   - `mark_ready_for_push()` - Marks day ready for push
   - `mark_pushed()` - Marks day as pushed

4. **Summary Methods:**
   - `get_today_summary()` - Returns today's cycle summary
   - `get_all_days_summary()` - Returns all days summaries

**Key Features:**
- Automatic day detection and cycle management
- Comprehensive productivity metrics
- End-of-day push preparation
- Historical tracking across days

**Relationship to AgentLifecycle:**
- Complements AgentLifecycle (tracks daily metrics, AgentLifecycle tracks cycle state)
- Can be used together for full cycle tracking

---

### Component 3: `src/core/end_of_cycle_push.py` - End of Cycle Push Protocol

**Author:** Agent-1 (Integration & Core Systems)  
**Date:** 2025-01-27  
**Type:** Git Push Automation  
**Purpose:** Ensure all work is committed and pushed before overnight runs

**How it works:**
1. **Preparation Phase (`prepare_for_push()`):**
   - Checks git status
   - Identifies uncommitted files
   - Identifies unpushed commits
   - Marks day as ready for push in DailyCycleTracker

2. **Execution Phase (`execute_push(commit_message)`):**
   - Stages all changes (`git add -A`)
   - Commits if there are uncommitted changes
   - Creates commit message from daily summary if not provided
   - Pushes to remote if there are unpushed commits
   - Marks day as pushed in DailyCycleTracker

3. **Git Status Methods:**
   - `_check_git_status()` - Gets git status output
   - `_get_uncommitted_files()` - Lists uncommitted files
   - `_get_unpushed_commits()` - Lists unpushed commits

**Key Features:**
- Automatic staging, committing, and pushing
- Integration with DailyCycleTracker
- Error handling at each stage
- Commit message generation from daily summary

**Usage:**
```python
from src.core.end_of_cycle_push import EndOfCyclePush

pusher = EndOfCyclePush('Agent-7')
result = pusher.execute_push()
```

**Scripts:**
- `scripts/execute_end_of_cycle_push.py` - CLI wrapper for end-of-cycle push

---

### Component 4: `src/core/messaging_templates_data/cycle_texts.py` - Operating Cycle Workflow

**Type:** Canonical Cycle Workflow Definition  
**Purpose:** Defines the standard agent operating cycle workflow

**Canonical Operating Cycle (7 Steps):**
1. **Claim** - Claim task from contract system or cycle planner
2. **Sync SSOT/context** - Sync with single source of truth
3. **Slice** - Break down task into executable slices
4. **Execute** - Execute the work
5. **Validate** - Validate the work
6. **Commit** - Commit to git
7. **Report evidence** - Report completion with evidence

**Cycle Checklist (3 Phases):**

#### CYCLE START:
- Check inbox (priority: D2A → C2A → A2A)
- Check Contract System (`--get-next-task`)
- Check Swarm Brain (MCP: `search_swarm_knowledge`)
- Check MASTER_TASK_LOG.md (MCP: `get_tasks`)
- **Force Multiplier Assessment (MANDATORY):**
  - Will this task take >1 cycle? → STOP, delegate
  - Does this touch 2+ domains? → STOP, coordinate
  - Is another agent better suited? → STOP, message them
  - Can this be parallelized? → STOP, break down and assign
  - ONLY if all answers are NO → proceed solo
- Update status.json (status=ACTIVE, increment cycle_count)
- Update FSM State
- Review current mission

**DO NOT:**
- Add tasks to cycle planner here (unless urgent)
- Message other agents here (unless urgent coordination)

#### DURING CYCLE:
- **PHASE 3: SLICE (Technical Implementation Planning):**
  1. Start with explicit technical instructions
  2. Request full technical implementation plan from AI first
  3. Vet the plan before execution
  4. Convert validated plan into detailed prompt
  5. Code review: Confirm implementation won't be spaghetti
  6. Ensure clean architecture patterns
- Update status when phase changes
- Update when tasks complete
- Update if blocked
- If new task identified → Use MCP: `add_task_to_inbox`
- If task blocked → Use MCP: `move_task_to_waiting`

**MESSAGE OTHER AGENTS WHEN:**
- Task expands → Break down and coordinate
- Need domain expertise → Message domain specialist
- Cross-domain work → Message relevant agents
- 75-80% complete → Send "gas" to next agent (pipeline continuity)
- Blocked → Message for help or escalate to Captain
- Force multiplier opportunity → Break down and assign to swarm

#### CYCLE END:
- Update completed_tasks
- Update next_actions
- **UPDATE MASTER_TASK_LOG (MANDATORY):**
  - Use MCP: `mark_task_complete`, `move_task_to_waiting`, `add_task_to_inbox`
  - Location: MASTER_TASK_LOG.md
- **VERIFY WORK (BEFORE COMMITTING):**
  - Use MCP: `verify_git_work`, `verify_work_exists`
- **CHECK V2 COMPLIANCE (BEFORE COMMITTING):**
  - Use MCP: `check_v2_compliance`, `validate_file_size`
- **ADD TASKS TO CYCLE PLANNER:**
  - Location: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
  - When: After completing current work, before session transition
- **MESSAGE OTHER AGENTS:**
  - Coordination outcomes
  - Handoff
  - Completion notifications
- Commit status.json to git
- Create & post devlog automatically
- Share learnings to Swarm Brain (MCP: `share_learning`)
- Record decisions (MCP: `record_decision`)
- Report coordination outcomes

---

### Component 5: `src/services/contract_system/cycle_planner_integration.py` - Cycle Planner Integration

**Author:** Agent-2 (Architecture & Design)  
**Type:** Contract System Integration  
**Purpose:** Integrates cycle planner tasks into contract system

**How it works:**
1. **Task Loading (`load_cycle_planner_tasks(agent_id, target_date)`):**
   - Loads tasks from `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
   - Supports multiple file name patterns
   - Handles different JSON structures:
     - `pending_tasks` array
     - `tasks` array (filters for pending/ready)
     - Priority-organized tasks (high/medium/low)
     - Direct array format
   - Returns list of task dictionaries

2. **Task Conversion (`convert_task_to_contract(task, agent_id)`):**
   - Converts cycle planner task to contract format
   - Maps priorities (HIGH/MEDIUM/LOW → high/medium/low)
   - Creates contract with:
     - `contract_id` (prefixed with "cycle-")
     - `title`, `description`, `priority`, `status`
     - `agent_id`, `created_at`, `source: "cycle_planner"`
     - `task_id`, `estimated_time`, `dependencies`, `deliverables`
     - `blocker`, `owner`

3. **Next Task (`get_next_cycle_task(agent_id, target_date)`):**
   - Gets first pending task from cycle planner
   - Converts to contract format
   - Returns contract dictionary or None

4. **Task Completion (`mark_task_complete(agent_id, task_id, target_date)`):**
   - Marks task as completed in cycle planner JSON
   - Updates task status to "completed"
   - Adds `completed_at` timestamp
   - Saves updated JSON file

**Key Features:**
- Flexible JSON structure handling
- Contract system integration
- Task status tracking
- Date-based task organization

---

### Component 6: `tools/master_task_log_to_cycle_planner.py` - MASTER_TASK_LOG Bridge

**Type:** Task Log Integration  
**Purpose:** Bridge MASTER_TASK_LOG.md to cycle planner JSON files

**How it works:**
1. **Parsing (`parse_master_task_log(path)`):**
   - Parses MASTER_TASK_LOG.md
   - Extracts tasks from INBOX and THIS_WEEK sections
   - Extracts: title, priority, points, assigned agents, checked status
   - Returns list of `MasterTask` dataclass objects

2. **Filtering (`_filter_tasks_for_agent(agent_id, tasks)`):**
   - Filters tasks for specific agent
   - Excludes checked (completed) tasks
   - Returns tasks assigned to agent

3. **Payload Building (`build_cycle_planner_payload(agent_id, tasks, priority)`):**
   - Builds JSON payload for cycle planner
   - Creates normalized task structure
   - Includes metadata: `created`, `agent_id`, `date`, `source`
   - Returns payload dictionary

4. **File Writing (`write_cycle_planner_file(agent_id, payload)`):**
   - Writes to `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
   - Creates agent directory if needed
   - Returns file path

**Key Features:**
- Automatic task extraction from MASTER_TASK_LOG.md
- Agent-specific task filtering
- Cycle planner JSON generation
- Integration with contract system

**Usage:**
```bash
python tools/master_task_log_to_cycle_planner.py --agent Agent-3 --section THIS_WEEK --priority medium --max-tasks 10
```

---

### Component 7: `src/discord_commander/status_change_monitor.py` - Status Change Monitor

**Author:** Agent-4 (Captain), Refactored by Agent-1  
**Type:** Real-time Status Monitoring  
**Purpose:** Monitor status.json files and post Discord updates automatically

**How it works:**
1. **File Monitoring:**
   - Monitors all `agent_workspaces/Agent-{1-8}/status.json` files
   - Checks every 5 seconds (loop interval)
   - Uses file modification time to detect changes
   - Reads JSON with retry logic (handles file locks)

2. **Change Detection:**
   - Compares old vs new status
   - Detects changes in: status, current_mission, current_phase, current_tasks, completed_tasks, blockers, achievements
   - Logs detected changes

3. **Debouncing:**
   - Pending updates stored in `pending_updates` dict
   - 5-second debounce window
   - Only posts to Discord after debounce period
   - Prevents spam from rapid status updates

4. **Discord Updates:**
   - Posts status change embeds to Discord
   - Uses `StatusEmbedFactory` for embed creation
   - Posts to configured channel or first available text channel

5. **Persistent Dashboard:**
   - Maintains persistent dashboard message
   - Updates dashboard with current agent statuses
   - Shows all agents in one view

6. **Inactivity Checks:**
   - Runs inactivity checks (approx once per minute)
   - Detects agents that haven't updated in a while
   - Can trigger resumer logic

7. **Resumer Integration:**
   - Integrates with `ResumerHandler` for inbox resumption
   - Can trigger agent resumption on status changes

**Key Features:**
- Real-time status monitoring (5-second intervals)
- Debouncing to prevent spam
- Persistent dashboard
- Retry logic for file reading
- Discord integration
- Inactivity detection

**Configuration:**
- `check_interval` - File check interval (default: 15 seconds, but loop runs every 5s)
- `debounce_seconds` - Debounce window (default: 5 seconds)
- `channel_id` - Discord channel for updates (optional)

---

## 🔄 Complete Cycle Flow

### Phase 1: Cycle Start

1. **Agent receives task assignment:**
   - From Contract System (`--get-next-task`)
   - From Cycle Planner (`cycle_planner_tasks_YYYY-MM-DD.json`)
   - From MASTER_TASK_LOG.md (via MCP: `get_tasks`)
   - From inbox message (D2A/C2A/A2A)

2. **Force Multiplier Assessment (MANDATORY):**
   - Check if task >1 cycle → delegate
   - Check if task touches 2+ domains → coordinate
   - Check if another agent better suited → message them
   - Check if can be parallelized → break down and assign
   - Only proceed solo if all checks pass

3. **Initialize Cycle:**
   ```python
   lifecycle = AgentLifecycle('Agent-7')
   lifecycle.start_cycle()  # status=ACTIVE, cycle_count++, FSM=active
   lifecycle.start_mission("Mission name", "HIGH")
   ```

4. **Daily Cycle Tracking:**
   ```python
   tracker = DailyCycleTracker('Agent-7')
   tracker.start_new_day()  # Creates/updates daily_cycles.json
   tracker.record_interaction()  # Increments interaction count
   ```

### Phase 2: During Cycle

1. **Work Execution:**
   - Update phase: `lifecycle.update_phase("Implementation")`
   - Add tasks: `lifecycle.add_task("Task name")`
   - Complete tasks: `lifecycle.complete_task("Task name", points=100)`
   - Record in daily tracker: `tracker.record_task_completed("Task name", 100)`

2. **Status Updates:**
   - StatusChangeMonitor detects changes (every 5 seconds)
   - Debounces updates (5-second window)
   - Posts to Discord automatically

3. **Coordination (when needed):**
   - Message other agents via UnifiedMessagingService
   - Use A2A messaging for coordination
   - Update MASTER_TASK_LOG via MCP tools

4. **Blocking (if needed):**
   ```python
   lifecycle.add_blocker("Waiting on Agent-2")
   # Status automatically set to BLOCKED
   ```

### Phase 3: Cycle End

1. **Complete Work:**
   ```python
   lifecycle.complete_mission()
   lifecycle.end_cycle(commit=True)  # Commits status.json to git
   ```

2. **Update MASTER_TASK_LOG (MANDATORY):**
   - Use MCP: `mark_task_complete(task_description, section="THIS_WEEK")`
   - Use MCP: `move_task_to_waiting(task_description, reason, agent_id)` if blocked
   - Use MCP: `add_task_to_inbox(task, agent_id)` if new task identified

3. **Verify Work:**
   - Use MCP: `verify_git_work(agent_id, file_path, claimed_changes)`
   - Use MCP: `verify_work_exists(file_patterns, agent_name)`

4. **Check V2 Compliance:**
   - Use MCP: `check_v2_compliance(file_path)`
   - Use MCP: `validate_file_size(file_path)`

5. **Update Cycle Planner:**
   - Write to `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
   - Include unfinished work, blockers, next session priorities

6. **End of Day Push:**
   ```python
   pusher = EndOfCyclePush('Agent-7')
   result = pusher.execute_push()  # Stages, commits, pushes to git
   tracker.mark_pushed()  # Marks day as pushed
   ```

7. **Share Learnings:**
   - Use MCP: `share_learning(agent_id, title, content, tags)`
   - Use MCP: `record_decision(agent_id, title, decision, rationale)`

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CYCLE START                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Task Assignment Sources:              │
        │  - Contract System (--get-next-task)  │
        │  - Cycle Planner JSON                  │
        │  - MASTER_TASK_LOG.md                  │
        │  - Inbox Messages (D2A/C2A/A2A)        │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Force Multiplier Assessment          │
        │  (MANDATORY - Check delegation needs) │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  AgentLifecycle.start_cycle()         │
        │  - status.json: ACTIVE                 │
        │  - cycle_count++                      │
        │  - FSM: active                        │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  DailyCycleTracker.start_new_day()    │
        │  - daily_cycles.json created/updated  │
        └───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    DURING CYCLE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Work Execution                        │
        │  - lifecycle.complete_task()          │
        │  - tracker.record_task_completed()     │
        │  - StatusChangeMonitor detects changes │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  StatusChangeMonitor (every 5s)       │
        │  - Detects status.json changes        │
        │  - Debounces (5s window)               │
        │  - Posts to Discord                   │
        └───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CYCLE END                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  lifecycle.end_cycle(commit=True)      │
        │  - Commits status.json to git          │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Update MASTER_TASK_LOG (MCP tools)    │
        │  - mark_task_complete()                │
        │  - move_task_to_waiting()              │
        │  - add_task_to_inbox()                 │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Verify Work (MCP tools)               │
        │  - verify_git_work()                   │
        │  - verify_work_exists()               │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Check V2 Compliance (MCP tools)       │
        │  - check_v2_compliance()              │
        │  - validate_file_size()               │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Update Cycle Planner JSON             │
        │  - cycle_planner_tasks_YYYY-MM-DD.json │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  EndOfCyclePush.execute_push()         │
        │  - git add -A                          │
        │  - git commit                          │
        │  - git push                            │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Share Learnings (MCP tools)            │
        │  - share_learning()                    │
        │  - record_decision()                   │
        └───────────────────────────────────────┘
```

---

## 🔗 Integration Points

### 1. Contract System Integration
- **Cycle Planner Integration:** Loads tasks from cycle planner JSON files
- **Contract Conversion:** Converts cycle planner tasks to contract format
- **Task Claiming:** Agents claim tasks via `--get-next-task` CLI command

### 2. MASTER_TASK_LOG Integration
- **Task Import:** `master_task_log_to_cycle_planner.py` bridges MASTER_TASK_LOG.md to cycle planner
- **Task Updates:** MCP tools (`mark_task_complete`, `move_task_to_waiting`, `add_task_to_inbox`) update MASTER_TASK_LOG.md

### 3. Discord Integration
- **Status Monitoring:** StatusChangeMonitor posts status updates to Discord
- **Real-time Updates:** Debounced updates prevent spam
- **Persistent Dashboard:** Shows all agent statuses in one view

### 4. Git Integration
- **Status Commits:** AgentLifecycle can commit status.json
- **End of Cycle Push:** EndOfCyclePush handles staging, committing, and pushing
- **Work Verification:** MCP tools verify work exists in git

### 5. Swarm Brain Integration
- **Learning Sharing:** MCP: `share_learning()` shares learnings
- **Decision Recording:** MCP: `record_decision()` records decisions
- **Knowledge Search:** MCP: `search_swarm_knowledge()` searches for patterns

---

## 📋 Key Files and Locations

### Status Files:
- `agent_workspaces/{agent_id}/status.json` - Agent status (managed by AgentLifecycle)
- `agent_workspaces/{agent_id}/daily_cycles.json` - Daily cycle tracking (managed by DailyCycleTracker)

### Cycle Planner Files:
- `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json` - Cycle planner tasks

### Task Management:
- `MASTER_TASK_LOG.md` - Central task log (repository root)

### Scripts:
- `scripts/init_daily_cycle.py` - Initialize daily cycle
- `scripts/execute_end_of_cycle_push.py` - Execute end-of-cycle push
- `tools/master_task_log_to_cycle_planner.py` - Bridge MASTER_TASK_LOG to cycle planner

---

## 🐛 Known Issues / Considerations

1. **Multiple Tracking Systems:**
   - AgentLifecycle tracks cycle state
   - DailyCycleTracker tracks daily metrics
   - StatusChangeMonitor tracks status changes
   - **Consideration:** Ensure consistency between systems

2. **File Locking:**
   - StatusChangeMonitor uses retry logic for file reading
   - Multiple agents updating simultaneously could cause conflicts
   - **Mitigation:** Retry logic handles most cases

3. **Debouncing:**
   - 5-second debounce window may delay urgent status updates
   - **Consideration:** May need configurable debounce for different update types

4. **Cycle Planner JSON Structure:**
   - Multiple JSON structure formats supported
   - **Consideration:** Standardize on one format for consistency

5. **Git Integration:**
   - EndOfCyclePush assumes git is available
   - **Consideration:** Add error handling for git unavailability

---

## ✅ Recommendations

1. **Standardize Cycle Planner Format:**
   - Choose one JSON structure format
   - Document the standard format
   - Update all generators to use standard format

2. **Add Cycle Validation:**
   - Validate cycle completeness before end
   - Check for required updates (MASTER_TASK_LOG, cycle planner, etc.)
   - Warn if cycle incomplete

3. **Improve Error Handling:**
   - Add retry logic for git operations
   - Handle file locking more gracefully
   - Add validation for status.json structure

4. **Documentation:**
   - Create visual workflow diagrams
   - Document all integration points
   - Create troubleshooting guide

5. **Monitoring:**
   - Add metrics for cycle completion rates
   - Track average cycle duration
   - Monitor blocker frequency

---

*Analysis completed by Agent-4 (Captain) on 2025-12-30*

