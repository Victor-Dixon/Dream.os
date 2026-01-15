=======
<!-- SSOT Domain: documentation -->

# Task Discovery Protocol

**Version:** 1.0
**Last Updated:** 2025-12-22
**Author:** Agent-4 (Captain)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
**Status:** ACTIVE PROTOCOL

---

## 🎯 Purpose

This protocol defines a systematic approach for discovering work opportunities when the [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md) has no available tasks or all tasks are claimed. This ensures agents always have actionable work and prevents idle time.

**Related Protocols & Systems:**
- **[MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md)** - Main task tracking document where discovered tasks are added
- **[CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md)** - Use when discovered task meets Captain-Level criteria
- **Cycle Planner Integration** - `src/core/resume_cycle_planner_integration.py` - Tasks may be added to cycle planner for automatic agent assignment when agents resume work
- **Contract System** - `src/services/contract_system/` - Task claiming system: `python -m src.services.messaging_cli --get-next-task --agent Agent-X`
- **Cycle Accomplishment Reports** - `devlogs/YYYY-MM-DD_agent-X_cycle_accomplishments.md` - Review for next steps and incomplete work

---

## 📋 When to Use This Protocol

Use this protocol when:
- ✅ MASTER_TASK_LOG has no unclaimed tasks
- ✅ All tasks in MASTER_TASK_LOG are claimed by other agents
- ✅ Agent has completed all assigned tasks
- ✅ Agent is waiting on blockers and needs alternative work
- ✅ Agent wants to proactively identify work opportunities

---

## 🔍 Task Discovery Checklist

Follow this systematic checklist in order. Stop when you find actionable work.

### Step 1: Review Project State Reports

**Objective:** Understand current project state and identify gaps

- [ ] **Review State of the Project Report**
  - Location: `docs/` or project root
  - Check for: Outdated information, missing updates, incomplete sections
  - Action: Update report with current status, add missing information
  - **Task Opportunity:** "Update State of the Project Report"

- [ ] **Review/Update Progression Report**
  - Location: `docs/` or project tracking files
  - Check for: Progress tracking, milestone status, completion percentages
  - Action: Update progression metrics, identify stalled items
  - **Task Opportunity:** "Update Progression Report" or "Review Stalled Progress Items"

**Tools:**
- `find . -name "*project*report*" -o -name "*progression*" -o -name "*status*report*"`
- Check `docs/` directory for report files

---

### Step 2: Generate Project Scan

**Objective:** Identify technical debt, violations, and improvement opportunities

- [ ] **Run Project Scanner**
  - Tool: `tools/project_scanner.py` or similar
  - Check for: V2 violations, code quality issues, technical debt markers
  - Action: Review scan results, identify fixable issues
  - **Task Opportunity:** "Fix V2 violations identified in project scan" or "Address technical debt markers"

- [ ] **Check for Code Quality Issues**
  - Run: Linting, type checking, complexity analysis
  - Check for: Unused imports, dead code, code smells
  - Action: Create tasks for fixable issues
  - **Task Opportunity:** "Fix linting errors" or "Remove dead code"

**Tools:**
- `python tools/project_scanner.py` (if available)
- `ruff check .` or similar linting tools
- `pytest --cov` for coverage gaps

---

### Step 2b: Scan Websites (Automated Discovery)

**Objective:** Discover and health-check all website projects, identify SEO/deployment/build issues

- [ ] **Run Automated Website Discovery Scanner**
  - Tool: `powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\inventory_scanner.ps1"`
  - Scans: D:\websites (or configured website directory) recursively
  - Detects: WordPress, Next.js, Vite, Astro, CRA, static sites
  - Generates: `runtime/task_discovery/websites_inventory.json` and `.md`
  - **Task Opportunity:** Newly discovered sites need initialization/documentation

- [ ] **Run Website Health Checks**
  - Tool: `powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\health_scanner.ps1"`
  - Checks: 
    - Node-based: node_modules presence, build scripts
    - Static: title tags, meta descriptions, basic HTML structure
    - WordPress: notes for theme/plugin audits
  - Generates: `runtime/task_discovery/websites_findings.json` and `.md`
  - **Task Opportunity:** Sites with WARN/FAIL status need fixes

- [ ] **Review Generated Task Recommendations**
  - Location: `runtime/task_discovery/master_task_log_web_lane.md`
  - Contains: Paste-ready tasks grouped by site with priorities, points, proof artifacts
  - Action: Copy tasks to MASTER_TASK_LOG.md INBOX section
  - **Task Opportunity:** All WARN/FAIL sites generate claimable tasks

**Automated Scanner Features:**
- **Recursive discovery**: Finds all site roots at any depth
- **Type detection**: Automatically identifies framework/CMS type
- **Health scoring**: PASS/WARN/FAIL status per site
- **Task generation**: Creates formatted MASTER_TASK_LOG entries
- **Proof artifacts**: All findings JSON-backed for verification
- **Reusable**: Can be run anytime queue is empty

**Tools:**
- `runtime/task_discovery/inventory_scanner.ps1` - Discovers all sites
- `runtime/task_discovery/health_scanner.ps1` - Runs health checks
- `runtime/task_discovery/verify_artifacts.ps1` - Validates outputs
- Output: `runtime/task_discovery/master_task_log_web_lane.md` (paste-ready tasks)

**Example Task Output:**
```markdown
- [ ] **HIGH** (100 pts): [WEB] site-name - Fix issue description. 
  Source: Website discovery scan. Proof: runtime/task_discovery/websites_findings.json. [Agent-7]
```

**When to Use:**
- Queue is empty and no website tasks in MASTER_TASK_LOG
- After major website deployments (verify health)
- Monthly website health checks
- When new sites are added to D:\websites

---

### Step 3: Consult with Thea

**Objective:** Get AI consultation on project priorities and next steps

- [ ] **Consult Thea on Project State**
  - Query: "What should we do next given the current state of the project?"
  - Provide: Current MASTER_TASK_LOG status, agent status, recent completions
  - Action: Review recommendations, create tasks from actionable items
  - **Task Opportunity:** Tasks generated from Thea's recommendations

- [ ] **Ask Thea for Priority Assessment**
  - Query: "What are the highest priority items we should focus on?"
  - Action: Validate against project goals, create prioritized tasks
  - **Task Opportunity:** High-priority tasks identified by Thea

**Note:** Thea consultation should be used for strategic guidance, not routine task discovery.

---

### Step 4: Review Agent Status Files

**Objective:** Identify blockers, pending work, and coordination opportunities

- [ ] **Review All Agent status.json Files**
  - Location: `agent_workspaces/Agent-{1-8}/status.json`
  - Check for:
    - Blockers that need resolution
    - Pending tasks that need assistance
    - Coordination opportunities
    - Stalled work that needs unblocking
  - Action: Create coordination tasks or assistance tasks
  - **Task Opportunity:** "Unblock Agent-X on [task]" or "Assist Agent-X with [task]"

- [ ] **Check for Blockers**
  - Look for: `"blockers": [...]` in status files
  - Identify: Blockers that can be resolved by your agent
  - Action: Create blocker resolution tasks
  - **Task Opportunity:** "Resolve blocker: [description]"

- [ ] **Check for Coordination Opportunities**
  - Look for: `"coordination_opportunities"` or `"active_coordinations"`
  - Identify: Opportunities for bilateral coordination
  - Action: Create coordination tasks
  - **Task Opportunity:** "Coordinate with Agent-X on [task]"

**Tools:**
- `grep -r "blockers" agent_workspaces/`
- `grep -r "pending" agent_workspaces/ -i`
- `grep -r "coordination" agent_workspaces/ -i`

---

### Step 5: Review Recent Commits

**Objective:** Identify incomplete work, follow-up tasks, and technical debt

- [ ] **Check Recent Git Commits**
  - Command: `git log --oneline -20` or `git log --since="7 days ago"`
  - Look for:
    - Incomplete implementations (marked with TODO/FIXME)
    - Follow-up tasks mentioned in commit messages
    - Technical debt introduced
    - Broken functionality
  - Action: Create tasks for follow-up work
  - **Task Opportunity:** "Complete [feature] from commit [hash]" or "Fix [issue] introduced in commit [hash]"

- [ ] **Check for TODO/FIXME Comments**
  - Command: `grep -r "TODO\|FIXME" --include="*.py" --include="*.js" --include="*.md"`
  - Review: Each TODO/FIXME for actionable items
  - Action: Create tasks for valid TODOs
  - **Task Opportunity:** "Address TODO: [description]"

- [ ] **Review Commit Messages for Follow-ups**
  - Look for: "TODO:", "Follow-up:", "Next:", "Future:"
  - Action: Create tasks from commit message follow-ups
  - **Task Opportunity:** Tasks extracted from commit messages

**Tools:**
- `git log --oneline --since="7 days ago"`
- `git log --grep="TODO\|FIXME\|follow-up" -i`
- `grep -r "TODO\|FIXME" . --include="*.py" --include="*.js"`

---

### Step 6: Check Test Coverage

**Objective:** Identify testing gaps and improvement opportunities

- [ ] **Run Pytest Coverage Report**
  - Command: `pytest --cov=src --cov-report=html --cov-report=term`
  - Check for:
    - Files with low coverage (<85%)
    - Missing test files
    - Untested critical paths
  - Action: Create test coverage improvement tasks
  - **Task Opportunity:** "Add tests for [module]" or "Improve coverage for [file]"

- [ ] **Review Coverage Reports**
  - Location: `htmlcov/index.html` or coverage reports
  - Identify: Modules with <85% coverage
  - Action: Prioritize critical modules, create test tasks
  - **Task Opportunity:** "Increase test coverage for [module] to 85%+"

- [ ] **Check for Missing Test Files**
  - Compare: Source files vs test files
  - Identify: Modules without corresponding tests
  - Action: Create test creation tasks
  - **Task Opportunity:** "Create tests for [module]"

**Tools:**
- `pytest --cov=src --cov-report=html --cov-report=term`
- `coverage report` or `coverage html`
- Compare `src/` structure with `tests/` structure

---

### Step 7: Review Cycle Accomplishments

**Objective:** Identify incomplete work, follow-ups, and next steps

- [ ] **Review Recent Cycle Accomplishment Reports**
  - Location: `devlogs/YYYY-MM-DD_agent-X_cycle_accomplishments.md`
  - Check for:
    - "Next actions" or "Next steps" sections
    - Incomplete work mentioned
    - Follow-up tasks
    - Blockers that need resolution
  - Action: Create tasks from next actions
  - **Task Opportunity:** Tasks from "Next actions" sections

- [ ] **Review Daily/Weekly Reports**
  - Look for: Incomplete items, pending work, blockers
  - Action: Create tasks for incomplete work
  - **Task Opportunity:** "Complete [item] from cycle report"

- [ ] **Check for Recurring Issues**
  - Identify: Issues mentioned in multiple reports
  - Action: Create tasks for recurring problems
  - **Task Opportunity:** "Address recurring issue: [description]"

**Tools:**
- `find devlogs/ -name "*cycle*accomplishments*" -o -name "*daily*" -o -name "*weekly*"`
- `ls -lt devlogs/ | head -10` (most recent reports)

---

### Step 8: Check Documentation Gaps

**Objective:** Identify missing or outdated documentation

- [ ] **Review Documentation Completeness**
  - Check: README files, API docs, architecture docs
  - Identify: Missing documentation, outdated information
  - Action: Create documentation tasks
  - **Task Opportunity:** "Document [feature/module]" or "Update [documentation]"

- [ ] **Check for Documentation TODOs**
  - Search: `grep -r "TODO.*doc\|FIXME.*doc" --include="*.md" --include="*.rst"`
  - Action: Create documentation tasks
  - **Task Opportunity:** "Document [item] as noted in TODO"

**Tools:**
- `find docs/ -name "*.md" -exec grep -l "TODO\|FIXME\|outdated" {} \;`
- Review `README.md`, `docs/` structure

---

### Step 9: Check System Health

**Objective:** Identify system maintenance and improvement opportunities

- [ ] **Review System Health Reports**
  - Location: Toolbelt health reports, system status reports
  - Check for: Degraded performance, warnings, errors
  - Action: Create maintenance tasks
  - **Task Opportunity:** "Fix [system issue]" or "Improve [system component]"

- [ ] **Check for Broken Tools**
  - Run: Toolbelt health check
  - Identify: Broken or degraded tools
  - Action: Create tool fix tasks
  - **Task Opportunity:** "Fix broken tool: [tool name]"

**Tools:**
- `python tools/audit_toolbelt.py` (if available)
- Review `docs/toolbelt/TOOLBELT_HEALTH_AUDIT_REPORT.md`

---

### Step 10: Review Error Logs and Warnings

**Objective:** Identify recurring errors and warnings that need attention

- [ ] **Check Application Logs**
  - Location: Log files, error logs, warning logs
  - Look for: Recurring errors, unhandled exceptions, warnings
  - Action: Create error resolution tasks
  - **Task Opportunity:** "Fix recurring error: [error description]"

- [ ] **Review Linter Warnings**
  - Run: Linting tools, check for warnings
  - Action: Create tasks for fixable warnings
  - **Task Opportunity:** "Fix linting warnings in [file/module]"

**Tools:**
- `find . -name "*.log" -o -name "*error*" -o -name "*warning*"`
- Run linting tools: `ruff check .`, `pylint`, etc.

---

## 📝 Task Creation Process

When you find a work opportunity:

### Step 1: Validate the Task

- [ ] **Is this a valid task?**
  - Not already in MASTER_TASK_LOG?
  - Not already claimed by another agent?
  - Actionable and well-defined?
  - Has clear deliverables?

### Step 2: Classify the Task

- [ ] **Determine Priority:**
  - HIGH: Critical, blocking, system-wide impact
  - MEDIUM: Important, affects multiple agents
  - LOW: Nice-to-have, single-agent impact

- [ ] **Determine Agent Assignment:**
  - Which agent should handle this?
  - Is this a Captain-Level Task? (See CAPTAIN_LEVEL_TASK_PROTOCOL.md)

### Step 3: Add to MASTER_TASK_LOG

- [ ] **Format the Task:**
  ```markdown
  - [ ] **{PRIORITY}** ({points} pts): {Task Title} - {Task Description}. 
    **Source:** {Discovery method: Project scan, Status review, etc.}
    **Justification:** {Why this task is needed}
    [Agent-X CLAIMED] or [UNCLAIMED]
  ```

- [ ] **Estimate Point Value:**
  - **HIGH Priority:** 100-200 points (default: 150)
  - **MEDIUM Priority:** 50-100 points (default: 75)
  - **LOW Priority:** 25-50 points (default: 30)
  - **Captain-Level Tasks:** Apply 1.5x multiplier
  - **Coordination Tasks:** Apply 1.2x multiplier
  - **Multi-day tasks:** +25% bonus
  - **Cross-domain tasks:** +50% bonus
  - See [POINT_SYSTEM_INTEGRATION.md](POINT_SYSTEM_INTEGRATION.md) for detailed point calculation rules

- [ ] **Add to Appropriate Section in [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md):**
  - INBOX: New tasks
  - THIS_WEEK: Time-sensitive tasks
  - Captain-Level: If meets [Captain-Level criteria](CAPTAIN_LEVEL_TASK_PROTOCOL.md)

- [ ] **Consider Cycle Planner Integration:**
  - If task should be automatically assigned: Add to cycle planner system
  - See: `src/core/resume_cycle_planner_integration.py` for integration
  - Cycle planner tasks are automatically claimed when agents resume work

### Step 4: Document Discovery

- [ ] **Update Status:**
  - Note in status.json: "Task discovered via [method]"
  - Document discovery method for traceability

---

## 🎯 Priority Order for Discovery

When multiple opportunities are found, prioritize in this order:

1. **Blockers** (HIGH) - Unblock other agents
2. **System Health** (HIGH) - Fix broken systems
3. **Technical Debt** (MEDIUM) - Address code quality
4. **Documentation** (MEDIUM) - Improve documentation
5. **Test Coverage** (MEDIUM) - Improve test coverage
6. **Follow-ups** (LOW) - Complete incomplete work
7. **Nice-to-Haves** (LOW) - Improvements and optimizations

---

## 📊 Discovery Methods Summary

| Method | Purpose | Tools/Commands | Typical Task Types |
|--------|---------|----------------|-------------------|
| Project Reports | Understand state | `find docs/ -name "*report*"` | Updates, gap filling |
| Project Scan | Find violations | `python tools/project_scanner.py` | V2 fixes, tech debt |
| Website Scanner | Find site issues | `runtime/task_discovery/inventory_scanner.ps1` | SEO, builds, deploys |
| Thea Consultation | Strategic guidance | AI consultation | Strategic tasks |
| Agent Status | Find blockers | `grep -r "blockers" agent_workspaces/` | Blocker resolution |
| Recent Commits | Find follow-ups | `git log --since="7 days ago"` | Completion tasks |
| Test Coverage | Find gaps | `pytest --cov` | Test creation |
| Cycle Reports | Find next steps | `find devlogs/ -name "*cycle*"` | Follow-up tasks |
| Documentation | Find gaps | `find docs/ -name "*.md"` | Documentation tasks |
| System Health | Find issues | Health check tools | Maintenance tasks |
| Error Logs | Find errors | `find . -name "*.log"` | Error fixes |

---

## 🔄 Continuous Discovery

**Regular Discovery Schedule:**
- **Daily:** Review agent status files, check recent commits
- **Weekly:** Run project scan, review cycle accomplishments
- **Monthly:** Comprehensive documentation review, system health check, website scanner audit

**Discovery Triggers:**
- After completing all assigned tasks
- When waiting on blockers
- At start of new work cycle
- When MASTER_TASK_LOG is empty

---

## ✅ Validation Checklist

Before adding a discovered task to MASTER_TASK_LOG:

- [ ] Task is not duplicate
- [ ] Task is actionable (clear deliverables)
- [ ] Priority is appropriate
- [ ] Agent assignment is correct
- [ ] Task description is complete
- [ ] Discovery method is documented
- [ ] Task follows MASTER_TASK_LOG format

---

## 📌 Quick Reference

**Discovery Order:**
1. Project Reports → 2. Project Scan → **2b. Website Scanner** → 3. Thea Consultation → 4. Agent Status → 5. Recent Commits → 6. Test Coverage → 7. Cycle Reports → 8. Documentation → 9. System Health → 10. Error Logs

**Stop When:**
- You find actionable work
- You've completed all steps
- You've identified 3+ tasks (prioritize and add top priority)

**Always:**
- Document discovery method
- Validate task before adding
- Follow MASTER_TASK_LOG format
- Update status.json with discovery activity

---

## 🚨 Important Notes

- **Don't create duplicate tasks** - Always check MASTER_TASK_LOG first
- **Validate before adding** - Ensure task is actionable and well-defined
- **Prioritize appropriately** - Use priority guidelines
- **Document discovery** - Track how tasks were found for future reference
- **Follow protocols** - Use CAPTAIN_LEVEL_TASK_PROTOCOL.md for Captain tasks

---

**Protocol Status:** ✅ ACTIVE  
**Next Review:** 2025-03-22  
**Maintained By:** Agent-4 (Captain)

---

## 🔗 Related Documents & Systems

> **📖 System Integration:** See [TASK_MANAGEMENT_SYSTEM_INTEGRATION.md](TASK_MANAGEMENT_SYSTEM_INTEGRATION.md) for complete overview of how all task management components work together.

### Core Task Management
- **[MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md)** - Main task tracking document where discovered tasks are added
- **[CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md)** - Protocol for creating Captain-Level Tasks (check if discovered task meets criteria)

### Task Assignment Systems
- **Cycle Planner Integration** - `src/core/resume_cycle_planner_integration.py` - Automatic task assignment when agents resume work
- **Contract System** - `src/services/contract_system/` - Task claiming system: `python -m src.services.messaging_cli --get-next-task --agent Agent-X`

### Discovery Sources
- **Cycle Accomplishment Reports** - `devlogs/YYYY-MM-DD_agent-X_cycle_accomplishments.md` - Review for next steps and incomplete work
- **Agent Status Files** - `agent_workspaces/Agent-X/status.json` - Check for blockers and pending work

### Integration Workflow
```
1. MASTER_TASK_LOG empty or all tasks claimed?
   ↓ (yes)
2. Follow TASK_DISCOVERY_PROTOCOL.md (this document)
   ↓ (task discovered)
3. Check: Is this Captain-Level?
   → YES → Follow CAPTAIN_LEVEL_TASK_PROTOCOL.md
   → NO → Assign to appropriate agent
   ↓
4. Add to MASTER_TASK_LOG.md
   ↓ (optional)
5. Add to Cycle Planner for automatic assignment
   ↓
6. Agent claims via Contract System or Cycle Planner
```

### Task Discovery → Task Management Flow
- **Discovery** → This protocol (TASK_DISCOVERY_PROTOCOL.md)
- **Classification** → CAPTAIN_LEVEL_TASK_PROTOCOL.md (if Captain-Level)
- **Documentation** → MASTER_TASK_LOG.md
- **Assignment** → Cycle Planner or Contract System
- **Execution** → Agent status.json updates
- **Completion** → Mark complete in MASTER_TASK_LOG

---

## 📜 APPENDIX: Complete Discovery Command Reference

### Verify Protocol Exists
```bash
# Check that governance docs are present
ls -la docs/TASK_DISCOVERY_PROTOCOL.md docs/CAPTAIN_LEVEL_TASK_PROTOCOL.md 2>/dev/null
ls -la MASTER_TASK_LOG.md DELEGATION_BOARD.md 2>/dev/null
```

### Find Repository-Specific Tools
```bash
# Locate scanner/health tools this repo uses
rg -n "project_scanner|TASK_DISCOVERY_PROTOCOL|system health|health check|scanner" -S . || true
find tools scripts -maxdepth 3 -type f \( -name "*scan*.py" -o -name "*health*.py" -o -name "*audit*.py" -o -name "*project*scanner*.py" \) 2>/dev/null
```

### Lane 1: System Health Scan
```bash
# Run linting and type checking
mkdir -p runtime/task_discovery
python -m ruff check . 2>&1 | tee runtime/task_discovery/ruff.txt || true
python -m mypy . 2>&1 | tee runtime/task_discovery/mypy.txt || true
```

### Lane 2: Tests
```bash
# Locate test conventions
rg -n "pytest|coverage|--cov|tox|nox|unittest|ruff|mypy" -S pyproject.toml setup.cfg tox.ini noxfile.py .github 2>/dev/null

# Run tests with coverage
mkdir -p runtime/task_discovery
pytest --maxfail=1 -q
pytest --cov --cov-report=term-missing | tee runtime/task_discovery/coverage.txt
```

### Lane 3: Documentation
```bash
# Harvest doc debt markers
mkdir -p runtime/task_discovery
rg -n "TODO|FIXME|TBD|DEPRECATED|OUTDATED" -S README.md docs/ | tee runtime/task_discovery/docs_debt.txt

# Check for missing essential guides
for guide in "how to run" "how to test" "how to deploy" "getting started" "contributing"; do
  echo "Checking for: $guide"
  rg -i "$guide" README.md docs/ || echo "  ⚠️  Missing: $guide"
done
```

### Lane 4: Duplication / Tech Debt
```bash
# Find duplicate detection tooling
mkdir -p runtime/task_discovery
rg -n "duplicate|duplication|copy[- ]paste|complexity|radon|lizard" -S . || true

# Find oversized files (V2 policy breaches)
find src -name "*.py" -exec wc -l {} \; | awk '$1 > 300 {print}' | tee runtime/task_discovery/oversized_files.txt
```

### Lane 5: Websites (Windows PowerShell)
```powershell
# Run automated website discovery
powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\inventory_scanner.ps1"
powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\health_scanner.ps1"
powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\verify_artifacts.ps1"
```

### Lane 5: Websites (Bash/Linux - Manual)
```bash
# Find site roots manually
mkdir -p runtime/task_discovery
find . -maxdepth 4 -type f \( -name "package.json" -o -name "wp-config.php" -o -name "index.html" -o -name "next.config.*" -o -name "astro.config.*" \) 2>/dev/null | tee runtime/task_discovery/site_roots.txt
```

### Complete All-Lanes Discovery (One Command)
```bash
#!/bin/bash
# Complete discovery workflow - run all 5 primary lanes

echo "🔍 TASK DISCOVERY - ALL LANES"
echo "=============================="
mkdir -p runtime/task_discovery

echo ""
echo "Lane 1: HEALTH Scan..."
python -m ruff check . 2>&1 | tee runtime/task_discovery/ruff.txt || true
python -m mypy . 2>&1 | tee runtime/task_discovery/mypy.txt || true

echo ""
echo "Lane 2: TESTS..."
pytest --cov --cov-report=term-missing | tee runtime/task_discovery/coverage.txt 2>&1 || true

echo ""
echo "Lane 3: DOCS..."
rg -n "TODO|FIXME|TBD|DEPRECATED|OUTDATED" -S README.md docs/ | tee runtime/task_discovery/docs_debt.txt 2>&1 || true

echo ""
echo "Lane 4: DEBT..."
find src -name "*.py" -exec wc -l {} \; | awk '$1 > 300 {print}' | tee runtime/task_discovery/oversized_files.txt 2>&1 || true

echo ""
echo "Lane 5: WEB... (if Windows with PowerShell)"
# powershell.exe -ExecutionPolicy Bypass -File "runtime\task_discovery\inventory_scanner.ps1" 2>&1 || true

echo ""
echo "✅ Discovery complete! Review artifacts in runtime/task_discovery/"
echo "Next: Analyze findings and add tasks to MASTER_TASK_LOG.md"
```

**Save the above script as `tools/discover_all_lanes.sh` for quick discovery runs.**

---

🐝 WE. ARE. SWARM. ⚡🔥

