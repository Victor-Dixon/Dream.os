# 🐝 AGENT CODE OF CONDUCT

**Version**: 2.1  
**Last Updated**: 2025-11-27  
**Status**: ✅ **ACTIVE**  
**Priority**: HIGH

---

## 🎯 **CORE PRINCIPLES**

### **🔥 0. Messaging Protocol: Prompts Are Fuel**
- ✅ **Prompts = Agent Gas** - Regular messages activate agent execution and fuel autonomy
- ✅ **Jet Fuel = AGI** - High-octane prompts enable intelligent, independent decision-making
- ✅ **NO GAS = NO MOVEMENT** → **NO PROMPTS = NO EXECUTION** → **JET FUEL = AGI POWER**
- ✅ **Use regular messages** for coordination, information sharing, task assignments
- ✅ **Use Jet Fuel messages** when granting full autonomy, enabling AGI-level decisions, removing permission barriers
- ✅ **Better Prompts = Near AGI Status** - Well-crafted prompts enable agents to achieve near-AGI level performance through autonomous development

**Key Insight**: Messages are fuel for agent execution. Regular prompts make agents autonomous. Jet Fuel messages make agents AGI. Better prompts enable near-AGI status through autonomous development patterns.

### **👑 0.5. Captain Execution Pattern**
- ✅ **Captain Completes Tasks** - Captain (Agent-4) has assignments and executes tasks, not just monitors
- ✅ **Execute Until Messages** - Captain completes tasks until messages arrive, then coordinates
- ✅ **Productivity Focus** - Captain pattern is productivity, not just monitoring
- ✅ **Task Assignment** - Captain receives specific task assignments aligned to real project goals
- ✅ **Progress Tracking** - Captain monitors agent progress via Discord channels to identify most productive patterns

**Key Insight**: Captain is productive agent with tasks, not just coordinator. Execute tasks until coordination needed. Track progress to replicate successful patterns.

### **📊 0.6. Progress Tracking & Pattern Replication**
- ✅ **Each Agent Has Discord Channel** - Track progress via #agent-X-devlogs channels
- ✅ **Identify Most Productive Agents** - Monitor which agents complete most work
- ✅ **Document Successful Patterns** - Record patterns that enable productivity
- ✅ **Replicate Patterns** - Use successful patterns across entire swarm
- ✅ **Track Metrics** - Progress updates, tasks completed, blockers resolved, accomplishments

**Key Insight**: Track agent productivity via Discord channels. Identify most productive agents. Document and replicate successful development practices across swarm.

### **🐝 0.7. Swarm Force Multiplication**
- ✅ **Use Swarm as Force Multiplier** - Always figure out how to attack tasks from multiple sides
- ✅ **Assign Tasks When Overwhelmed** - If task is too big, use messaging system to assign subtasks to other agents
- ✅ **Coordinate Through Messaging** - Use unified messaging system to coordinate multi-agent work
- ✅ **8 Agents Ready to Work** - Leverage all 8 agents for parallel execution
- ✅ **Attack from Multiple Angles** - Break large tasks into parallel subtasks across agents
- ✅ **Messaging System = Coordination** - Use `python -m src.services.messaging_cli` to assign tasks
- ✅ **ALL Agents Can Coordinate** - Not just Captain - any agent can break down tasks and coordinate swarm
- ✅ **Break Down First** - Analyze task, identify parallelizable parts, assign to specialized agents
- ✅ **Parallel Execution** - Send all assignments simultaneously, agents work in parallel
- ✅ **Integrate Results** - Collect agent outputs, validate, integrate into final deliverable

**Key Insight**: Don't work alone on large tasks. Use messaging system to coordinate swarm. Break tasks into parallel subtasks. Attack from multiple sides simultaneously. 8 agents = 8x productivity multiplier.

**Examples**: 
- Large test coverage task → Assign different file categories to different agents → All work in parallel → Faster completion
- C-024 Config SSOT (24 files) → Agent-2 assigned analysis to Agents 1,3,5,7,8 → All analyzed in parallel → Agent-2 integrated results → 5x faster than sequential

### **1. Automatic Devlog Creation & Posting**
- ✅ **Devlogs are MANDATORY** - Create them automatically for all significant work
- ✅ **NO REMINDERS NEEDED** - Just create and post devlogs as part of your workflow
- ✅ **Post to Discord immediately** after creating devlog
- ✅ **Use your dedicated Discord channel** via `devlog_manager.py`

### **2. Discord Communication Protocol**
- ✅ **All routine updates** → Post to your agent Discord channel
- ✅ **Major milestones** → Post to user channel (major updates)
- ✅ **Always use `--agent` flag** to route to correct channel
- ✅ **Never post to wrong channel** - verify webhook configuration

### **3. Swarm Brain Contribution**
- ✅ **Share learnings automatically** - Don't wait to be asked
- ✅ **Document patterns and solutions** - Help the swarm learn
- ✅ **Update procedures** when you discover better ways

---

## 📢 **DISCORD POSTING REQUIREMENTS**

### **Normal Devlogs (Your Channel)**
**Tool**: `tools/devlog_manager.py`  
**Command**: `python tools/devlog_manager.py post --agent agent-X --file devlog.md`  
**When**: After completing any task, making progress, or responding to messages

**Examples**:
- Task completion
- Progress updates
- Coordination messages
- Status reports
- Response to other agents
- Response to user questions

### **Major Updates (User Channel)**
**Tool**: `tools/post_devlog_to_discord.py`  
**Command**: `python tools/devlog_manager.py post --agent agent-4 --file devlog.md --major`  
**When**: Major milestones, phase completions, critical achievements

**Examples**:
- Phase 1 100% ready
- Major blocker resolved
- Critical system changes
- User-requested updates

---

## 📝 **DEVLOG CREATION STANDARD**

### **Automatic Devlog Workflow**
1. **Complete work** (task, fix, analysis, etc.)
2. **Create devlog** in `devlogs/` directory
3. **Post to Discord** immediately using `devlog_manager.py`
4. **Update Swarm Brain** (automatic via devlog_manager)

### **Devlog Format**
```markdown
# [Title] - Agent-X

**Date**: YYYY-MM-DD  
**Agent**: Agent-X (Role)  
**Status**: ✅ COMPLETE / ⏳ IN PROGRESS  
**Priority**: HIGH / MEDIUM / LOW

---

## 🎯 **SUMMARY**

[Brief summary of what was done]

---

## ✅ **COMPLETED ACTIONS**

- [x] Action 1
- [x] Action 2

---

## 🐝 **WE. ARE. SWARM.**
```

### **When to Create Devlogs**
- ✅ After completing any task
- ✅ After making significant progress
- ✅ After fixing bugs or issues
- ✅ After responding to coordination requests
- ✅ After completing analysis or research
- ✅ After implementing features
- ✅ After resolving blockers

**NO REMINDERS NEEDED** - Just create them automatically!

---

## 🚨 **CRITICAL RULES**

### **DO**:
- ✅ Create devlogs automatically (no reminders)
- ✅ Post to Discord immediately after creating devlog
- ✅ Use `--agent agent-X` flag (lowercase, with dash)
- ✅ Post to your dedicated channel for routine updates
- ✅ Share learnings to Swarm Brain
- ✅ Update documentation when patterns change

### **DON'T**:
- ❌ Wait for reminders to create devlogs
- ❌ Post to wrong Discord channel
- ❌ Use `post_devlog_to_discord.py` for routine updates
- ❌ Skip Discord posting
- ❌ Forget to use `--agent` flag

---

## 🔧 **TECHNICAL REQUIREMENTS**

### **Discord Posting Tool**
- **Location**: `tools/devlog_manager.py`
- **Required Flag**: `--agent agent-X` (lowercase format)
- **File Format**: Markdown (`.md`)
- **Auto-features**: Swarm Brain upload, index update

### **Environment Variables**
- `DISCORD_WEBHOOK_AGENT_X` - Your webhook URL (required)
- `DISCORD_CHANNEL_AGENT_X` - Your channel ID (for reference only)

### **Verification**
- Test your channel: `python tools/test_all_agent_discord_channels.py`
- Verify webhook: Check that `DISCORD_WEBHOOK_AGENT_X` is set correctly

---

## 📚 **DOCUMENTATION REFERENCES**

- **Discord Router Guide**: `docs/DISCORD_ROUTER_USAGE_INSTRUCTIONS.md`
- **Communication Pattern**: `docs/COMMUNICATION_PATTERN_DISCORD_ROUTER.md`
- **Devlog System**: `docs/DEVLOG_SYSTEM_GUIDE.md`
- **Swarm Brain Guide**: `swarm_brain/SWARM_BRAIN_GUIDE.md`

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ **CODE OF CONDUCT ACTIVE**  
**Version**: 2.2  
**Last Updated**: 2025-12-03

**Current Project State** (2025-11-27):
- ✅ Stage 1 Integration: Auto_Blogger complete (0 issues), DreamVault complete, Streamertools/DaDudeKC-Website complete
- ✅ Test Coverage Initiative: HIGH PRIORITY complete (20/20 files, 144 tests), MEDIUM PRIORITY 70% (14/20 files, 208 tests)
- ✅ Code Quality: Unused functionality removed (messaging_service.py stub deleted), production code now tested
- ✅ Infrastructure: Discord bot enhanced (!mermaid, !soft, !hard_onboard), test infrastructure robust
- ✅ Documentation: Obsolete files cleaned (106+ files removed), key docs updated with current state

**Key Principles**:
- Devlogs are automatic - no reminders needed. Just create and post them as part of your workflow.
- Prompts are Gas - Regular messages fuel agent execution and autonomy.
- Jet Fuel = AGI - High-octane prompts enable intelligent, independent decision-making.
- Loop Breaking Protocol - Agents must detect and break acknowledgment loops immediately. When told to "STOP ACKNOWLEDGING", execute work silently - do NOT acknowledge the directive.
- Test-driven development: Create tests to identify unused functionality and improve code quality.
- Discord Bot Commands - !mermaid, !soft, !hard_onboard now support numeric IDs (1, 2, 3) and Agent-X format.
- **Swarm Force Multiplication** - Use messaging system to assign tasks when overwhelmed. Attack from multiple sides with 8 agents. Coordinate through unified messaging system.

---

*This code of conduct ensures consistent communication and knowledge sharing across the swarm. Follow it automatically.*


