# 🔗 Swarm Systems Integration - Implementation Plan (UPDATED)

**Date**: 2025-12-03  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Status**: 📋 **IMPLEMENTATION PLAN - UPDATED**  
**Priority**: HIGH  
**Reviewer**: Agent-4 (Captain)  
**Version**: 2.0 (Added Telephone Game + Contracts Integration)

---

## 🎯 **EXECUTIVE SUMMARY**

**Proposal Reviewed**: ✅ **APPROVED** - Architecturally sound integration strategy

**Integration Goal**: Connect 6 underutilized systems (debates, meetings, cycle_planner, GaslineHub, Telephone Game Protocol, contracts) to Captain's workflow → GaslineHub → Messaging System → Agents

**Architecture Assessment**: ✅ **SOUND** - Proper layering, clear integration points, maintains SSOT principles

**Key Addition**: Telephone Game + Contracts integration for automatic cross-domain coordination

**Implementation Approach**: Phased rollout with backward compatibility, V2 compliance, and comprehensive testing

---

## 📊 **ARCHITECTURE REVIEW**

### **✅ Integration Flow Validation (UPDATED - 6 Systems)**

The proposed flow is architecturally sound:

```
Captain Workflow (Orchestrator)
    ↓
┌─────────────────────────────────────┐
│  System Integration Layer           │
│  - Debate Monitor                   │
│  - Meeting Coordinator              │
│  - Cycle Planner Loader            │
│  - Contract Monitor                │
│  - Telephone Game Detector         │
└───────────────┬─────────────────────┘
                ↓
        GaslineHub (Coordinator)
                ↓
        ┌───────┴───────┐
        │               │
        ▼               ▼
  Messaging System  Telephone Game
        │           Chain Tracker
        │               │
        └───────┬───────┘
                ↓
            Agents
```

**Architecture Principles Applied**:
- ✅ **Single Responsibility**: Each system maintains its domain
- ✅ **Dependency Injection**: GaslineHub coordinates, doesn't own
- ✅ **Repository Pattern**: Systems read/write their own data
- ✅ **SSOT Compliance**: Each system maintains its own SSOT
- ✅ **V2 Compliance**: All new code <300 lines/file, <200 lines/class
- ✅ **Chain Pattern**: Telephone Game for sequential multi-domain coordination
- ✅ **Contract Pattern**: Structured task assignment with chain support

---

## 🚀 **PHASE 1: CAPTAIN INTEGRATION (HIGH PRIORITY)**

### **1.1 Enhance Captain Restart Pattern v1**

**File**: `agent_workspaces/Agent-4/inbox/CAPTAIN_RESTART_PATTERN_V1_2025-12-03.md`

**Changes Required**:
```markdown
## 5-MINUTE CHECKLIST (Enhanced)

1. Status.json stamp
2. Inbox sweep
3. Status sweep
4. **NEW: Check active debates** ← Add this
   - Load debates from `debates/` directory
   - Check for concluded debates (deadline passed)
   - Trigger GaslineHub for concluded debates
5. **NEW: Check scheduled meetings** ← Add this
   - Load meetings from `agent_workspaces/meeting/meeting.json`
   - Check for meetings scheduled today
   - Notify participants and create task assignments
6. **NEW: Check available contracts** ← Add this
   - Load contracts from contract system
   - Detect cross-domain contracts
   - Create Telephone Game chains for cross-domain contracts
7. **NEW: Detect Telephone Game opportunities** ← Add this
   - Identify tasks needing multi-domain coordination
   - Auto-create Telephone Game chains
   - Assign chain contracts via messaging system
8. Immediate follow-ups
9. Devlog anchor
```

**Implementation**:
- Create `src/core/captain_workflow_integrations.py` (new file, ~280 lines)
- Add `check_active_debates()` function
- Add `check_scheduled_meetings()` function
- Add `check_available_contracts()` function - **NEW**
- Add `detect_telephone_game_opportunities()` function - **NEW**
- Integrate into Captain Restart Pattern execution

**V2 Compliance**: ✅ Single file, <300 lines, clear functions

---

### **1.2 Enhance GaslineHub with Logging**

**File**: `src/core/gasline_integrations.py`

**Changes Required**:
```python
class GaslineHub:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.hub_dir = self.project_root / "agent_workspaces" / "GaslineHub"
        self.hub_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.hub_dir / "activations.json"
        # ... existing code ...
    
    def log_activation(self, source: str, target: str, action: str, metadata: Dict = None):
        """Log all activations for coordination tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,  # "debate", "meeting", "cycle_planner", "violations"
            "target": target,  # agent_id or "all"
            "action": action,
            "metadata": metadata or {}
        }
        
        # Append to JSON log file
        logs = []
        if self.log_file.exists():
            logs = json.loads(self.log_file.read_text())
        logs.append(log_entry)
        self.log_file.write_text(json.dumps(logs, indent=2))
        
        logger.info(f"📝 GaslineHub logged: {source} → {target} ({action})")
```

**Integration Points**:
- Update `hook_debate_decision()` to call `log_activation()`
- Update `hook_violations_found()` to call `log_activation()`
- Add new hooks for meetings and cycle planner

**V2 Compliance**: ✅ Adds ~50 lines, stays under 300 lines/file limit

---

### **1.3 Create Debate Monitor Module**

**New File**: `src/core/debate_monitor.py` (~250 lines)

**Purpose**: Monitor `debates/` directory for concluded debates and trigger GaslineHub

**Implementation**:
```python
"""
Debate Monitor - Watches debates/ directory for concluded debates
Triggers GaslineHub activation when debates conclude

SSOT Domain: communication
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DebateMonitor:
    """Monitors debates directory for concluded debates"""
    
    def __init__(self, debates_dir: Path = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.debates_dir = debates_dir or (self.project_root / "debates")
        self.gasline_hub = None  # Lazy import to avoid circular deps
    
    def check_active_debates(self) -> List[Dict]:
        """Check for active debates needing decisions"""
        active_debates = []
        
        if not self.debates_dir.exists():
            return active_debates
        
        for debate_file in self.debates_dir.glob("*.json"):
            try:
                debate = json.loads(debate_file.read_text())
                if debate.get("status") == "active":
                    if self._deadline_passed(debate):
                        active_debates.append(debate)
            except Exception as e:
                logger.warning(f"Failed to load debate {debate_file}: {e}")
        
        return active_debates
    
    def process_concluded_debates(self) -> int:
        """Process concluded debates and trigger GaslineHub"""
        concluded = self.check_active_debates()
        processed = 0
        
        for debate in concluded:
            if self._trigger_gasline_activation(debate):
                processed += 1
                # Mark debate as processed
                self._mark_debate_processed(debate)
        
        return processed
    
    def _deadline_passed(self, debate: Dict) -> bool:
        """Check if debate deadline has passed"""
        deadline_str = debate.get("deadline")
        if not deadline_str:
            return False
        
        try:
            deadline = datetime.fromisoformat(deadline_str)
            return datetime.now() > deadline
        except Exception:
            return False
    
    def _trigger_gasline_activation(self, debate: Dict) -> bool:
        """Trigger GaslineHub activation for concluded debate"""
        if not self.gasline_hub:
            from src.core.gasline_integrations import GaslineHub
            self.gasline_hub = GaslineHub()
        
        try:
            # Extract decision from debate
            decision = self._extract_decision(debate)
            agent_assignments = self._extract_assignments(debate)
            
            # Trigger via GaslineHub
            success = self.gasline_hub.hook_debate_decision(
                topic=debate.get("topic", "unknown"),
                decision=decision,
                agent_assignments=agent_assignments
            )
            
            if success:
                # Log activation
                self.gasline_hub.log_activation(
                    source="debate",
                    target="all",
                    action="decision_executed",
                    metadata={"topic": debate.get("topic"), "decision": decision}
                )
            
            return success
        except Exception as e:
            logger.error(f"Failed to trigger gasline for debate: {e}")
            return False
    
    def _extract_decision(self, debate: Dict) -> str:
        """Extract winning decision from debate"""
        votes = debate.get("votes", {})
        if not votes:
            return debate.get("default_decision", "no_decision")
        
        # Find option with most votes
        winning_option = max(votes.items(), key=lambda x: x[1])
        return winning_option[0]
    
    def _extract_assignments(self, debate: Dict) -> Dict[str, str]:
        """Extract agent assignments from debate"""
        return debate.get("agent_assignments", {})
    
    def _mark_debate_processed(self, debate: Dict):
        """Mark debate as processed"""
        debate["status"] = "processed"
        debate["processed_at"] = datetime.now().isoformat()
        # Save back to file
        # (Implementation depends on debate file structure)
```

**V2 Compliance**: ✅ ~250 lines, single responsibility, clear functions

---

### **1.4 Create Meeting Coordinator Module**

**New File**: `src/core/meeting_coordinator.py` (~200 lines)

**Purpose**: Coordinate multi-agent meetings and convert outcomes to tasks

**Implementation**:
```python
"""
Meeting Coordinator - Coordinates multi-agent meetings
Converts meeting outcomes to actionable tasks

SSOT Domain: communication
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)


class MeetingCoordinator:
    """Coordinates meetings and converts outcomes to tasks"""
    
    def __init__(self, meeting_dir: Path = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.meeting_dir = meeting_dir or (self.project_root / "agent_workspaces" / "meeting")
        self.meeting_file = self.meeting_dir / "meeting.json"
        self.gasline_hub = None
    
    def check_scheduled_meetings(self, target_date: date = None) -> List[Dict]:
        """Check for meetings scheduled for target date (default: today)"""
        if target_date is None:
            target_date = date.today()
        
        if not self.meeting_file.exists():
            return []
        
        try:
            meetings_data = json.loads(self.meeting_file.read_text())
            meetings = meetings_data.get("meetings", [])
            
            scheduled = []
            for meeting in meetings:
                meeting_date_str = meeting.get("date")
                if meeting_date_str:
                    try:
                        meeting_date = datetime.fromisoformat(meeting_date_str).date()
                        if meeting_date == target_date:
                            scheduled.append(meeting)
                    except Exception:
                        continue
            
            return scheduled
        except Exception as e:
            logger.warning(f"Failed to load meetings: {e}")
            return []
    
    def process_meeting_outcomes(self, meeting: Dict) -> bool:
        """Process meeting outcomes and create task assignments"""
        outcomes = meeting.get("outcomes", [])
        if not outcomes:
            return False
        
        # Convert outcomes to tasks
        tasks = self._convert_outcomes_to_tasks(outcomes, meeting)
        
        # Assign tasks via messaging system
        assigned = self._assign_tasks_via_messaging(tasks, meeting)
        
        return assigned > 0
    
    def _convert_outcomes_to_tasks(self, outcomes: List[Dict], meeting: Dict) -> List[Dict]:
        """Convert meeting outcomes to actionable tasks"""
        tasks = []
        
        for outcome in outcomes:
            task = {
                "title": outcome.get("action_item", "Meeting action item"),
                "description": outcome.get("description", ""),
                "assigned_to": outcome.get("assigned_agent", "TBD"),
                "priority": outcome.get("priority", "normal"),
                "source": "meeting",
                "meeting_id": meeting.get("id"),
                "meeting_date": meeting.get("date")
            }
            tasks.append(task)
        
        return tasks
    
    def _assign_tasks_via_messaging(self, tasks: List[Dict], meeting: Dict) -> int:
        """Assign tasks via messaging system"""
        if not self.gasline_hub:
            from src.core.gasline_integrations import GaslineHub
            self.gasline_hub = GaslineHub()
        
        assigned = 0
        for task in tasks:
            agent_id = task.get("assigned_to")
            if agent_id and agent_id != "TBD":
                # Create message for agent
                message = self._create_task_message(task, meeting)
                
                # Send via messaging system
                if self._send_task_message(agent_id, message):
                    assigned += 1
                    
                    # Log activation
                    self.gasline_hub.log_activation(
                        source="meeting",
                        target=agent_id,
                        action="task_assigned",
                        metadata={"task": task.get("title"), "meeting_id": meeting.get("id")}
                    )
        
        return assigned
    
    def _create_task_message(self, task: Dict, meeting: Dict) -> str:
        """Create task assignment message"""
        return f"""📅 MEETING TASK ASSIGNMENT

Meeting: {meeting.get('title', 'Team Meeting')}
Date: {meeting.get('date', 'N/A')}

TASK ASSIGNED TO YOU:
{task.get('title', 'Action Item')}

Description:
{task.get('description', 'No description provided')}

Priority: {task.get('priority', 'normal').upper()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: Meeting Outcome
Action Required: Complete task and report back

🐝 WE. ARE. SWARM. ⚡🔥"""
    
    def _send_task_message(self, agent_id: str, message: str) -> bool:
        """Send task message to agent"""
        try:
            from src.services.messaging_cli_handlers import send_message_to_agent
            send_message_to_agent(
                agent_id=agent_id,
                message=message,
                sender="Meeting Coordinator",
                priority="normal",
                use_pyautogui=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send task message to {agent_id}: {e}")
            return False
```

**V2 Compliance**: ✅ ~200 lines, single responsibility, clear functions

---

### **1.5 Create Cycle Planner Integration Module**

**New File**: `src/core/cycle_planner_integration.py` (~250 lines)

**Purpose**: Integrate cycle planner tasks into agent status.json workflow

**Implementation**:
```python
"""
Cycle Planner Integration - Loads cycle planner tasks into agent workflow
Integrates with agent status.json and cycle protocols

SSOT Domain: communication
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)


class CyclePlannerIntegration:
    """Integrates cycle planner tasks into agent workflow"""
    
    def __init__(self, planner_dir: Path = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.planner_dir = planner_dir or (self.project_root / "agent_workspaces" / "swarm_cycle_planner" / "cycles")
    
    def load_cycle_tasks(self, agent_id: str, target_date: date = None) -> List[Dict]:
        """Load pending tasks from cycle planner for agent"""
        if target_date is None:
            target_date = date.today()
        
        planner_file = self.planner_dir / f"{target_date.isoformat()}_{agent_id}_pending_tasks.json"
        
        if not planner_file.exists():
            return []
        
        try:
            tasks_data = json.loads(planner_file.read_text())
            return tasks_data.get("tasks", [])
        except Exception as e:
            logger.warning(f"Failed to load cycle tasks for {agent_id}: {e}")
            return []
    
    def merge_tasks_into_status(self, agent_id: str, tasks: List[Dict]) -> bool:
        """Merge cycle planner tasks into agent status.json next_actions"""
        status_file = self.project_root / "agent_workspaces" / agent_id / "status.json"
        
        if not status_file.exists():
            logger.warning(f"Status file not found for {agent_id}")
            return False
        
        try:
            status = json.loads(status_file.read_text())
            
            # Get existing next_actions
            next_actions = status.get("next_actions", [])
            
            # Add cycle planner tasks
            for task in tasks:
                task_str = task.get("title", task.get("description", "Cycle planner task"))
                if task_str not in next_actions:
                    next_actions.append(task_str)
            
            # Update status
            status["next_actions"] = next_actions
            status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save back
            status_file.write_text(json.dumps(status, indent=2))
            
            logger.info(f"✅ Merged {len(tasks)} cycle tasks into {agent_id} status.json")
            return True
        except Exception as e:
            logger.error(f"Failed to merge tasks into status: {e}")
            return False
    
    def mark_task_complete(self, agent_id: str, task_title: str, target_date: date = None) -> bool:
        """Mark cycle planner task as complete"""
        if target_date is None:
            target_date = date.today()
        
        planner_file = self.planner_dir / f"{target_date.isoformat()}_{agent_id}_pending_tasks.json"
        
        if not planner_file.exists():
            return False
        
        try:
            tasks_data = json.loads(planner_file.read_text())
            tasks = tasks_data.get("tasks", [])
            
            # Find and mark task complete
            for task in tasks:
                if task.get("title") == task_title or task.get("description") == task_title:
                    task["status"] = "complete"
                    task["completed_at"] = datetime.now().isoformat()
                    break
            
            # Save back
            tasks_data["tasks"] = tasks
            planner_file.write_text(json.dumps(tasks_data, indent=2))
            
            logger.info(f"✅ Marked task '{task_title}' complete in cycle planner")
            return True
        except Exception as e:
            logger.error(f"Failed to mark task complete: {e}")
            return False
```

**V2 Compliance**: ✅ ~250 lines, single responsibility, clear functions

---

## 🔄 **PHASE 2: ACTIVE MONITORING (MEDIUM PRIORITY)**

### **2.1 Integrate into Agent Cycle Protocol**

**File**: `swarm_brain/protocols/CYCLE_PROTOCOLS.md`

**Changes Required**:
```markdown
## ✅ START OF CYCLE (MANDATORY)

### 1. CHECK INBOX
[... existing content ...]

### 2. UPDATE STATUS.JSON
[... existing content ...]

### 3. **NEW: LOAD CYCLE PLANNER TASKS** ← Add this
```python
from src.core.cycle_planner_integration import CyclePlannerIntegration

planner = CyclePlannerIntegration()
tasks = planner.load_cycle_tasks(agent_id="Agent-X")
if tasks:
    planner.merge_tasks_into_status(agent_id="Agent-X", tasks=tasks)
```

### 4. REVIEW CURRENT MISSION
[... existing content ...]
```

**Implementation**:
- Update cycle protocol documentation
- Create helper function in `src/core/agent_lifecycle.py` (if exists)
- Or create new `src/core/cycle_integration_helper.py`

---

### **2.2 Create Captain Workflow Integration Module**

**New File**: `src/core/captain_workflow_integrations.py` (~280 lines)

**Purpose**: Central integration point for Captain Restart Pattern

**Implementation**:
```python
"""
Captain Workflow Integrations - Central integration for Captain Restart Pattern
Connects debates, meetings, cycle planner to Captain workflow

SSOT Domain: communication
"""

import logging
from pathlib import Path
from typing import Dict, List
from datetime import date

logger = logging.getLogger(__name__)


class CaptainWorkflowIntegrations:
    """Central integration point for Captain workflow"""
    
    def __init__(self):
        self.debate_monitor = None
        self.meeting_coordinator = None
        self.gasline_hub = None
    
    def check_active_debates(self) -> Dict:
        """Check for active debates needing decisions"""
        if not self.debate_monitor:
            from src.core.debate_monitor import DebateMonitor
            self.debate_monitor = DebateMonitor()
        
        active = self.debate_monitor.check_active_debates()
        processed = self.debate_monitor.process_concluded_debates()
        
        return {
            "active_count": len(active),
            "processed_count": processed,
            "active_debates": active
        }
    
    def check_scheduled_meetings(self, target_date: date = None) -> Dict:
        """Check for scheduled meetings"""
        if not self.meeting_coordinator:
            from src.core.meeting_coordinator import MeetingCoordinator
            self.meeting_coordinator = MeetingCoordinator()
        
        meetings = self.meeting_coordinator.check_scheduled_meetings(target_date)
        processed = 0
        
        for meeting in meetings:
            if self.meeting_coordinator.process_meeting_outcomes(meeting):
                processed += 1
        
        return {
            "scheduled_count": len(meetings),
            "processed_count": processed,
            "meetings": meetings
        }
    
    def execute_captain_checks(self) -> Dict:
        """Execute all Captain workflow checks"""
        results = {
            "debates": self.check_active_debates(),
            "meetings": self.check_scheduled_meetings(),
            "timestamp": date.today().isoformat()
        }
        
        logger.info(f"✅ Captain workflow checks complete: {results}")
        return results
```

**V2 Compliance**: ✅ ~280 lines, orchestrator pattern, clear functions

---

### **1.6 Create Contract Monitor Module**

**New File**: `src/core/contract_monitor.py` (~250 lines)

**Purpose**: Monitor contracts system and detect cross-domain contracts for Telephone Game

**Implementation**:
```python
"""
Contract Monitor - Monitors contracts system for cross-domain coordination
Detects contracts needing Telephone Game chains

SSOT Domain: communication
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ContractMonitor:
    """Monitors contracts and detects cross-domain opportunities"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.contract_manager = None  # Lazy import
        self.telephone_game_detector = None
    
    def check_available_contracts(self) -> List[Dict]:
        """Check for available contracts needing assignment"""
        if not self.contract_manager:
            from src.services.contract_system.manager import ContractManager
            self.contract_manager = ContractManager()
        
        try:
            all_contracts = self.contract_manager.storage.get_all_contracts()
            available = [c for c in all_contracts if c.get("status") == "pending"]
            return available
        except Exception as e:
            logger.error(f"Failed to check contracts: {e}")
            return []
    
    def detect_cross_domain_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Detect contracts that span multiple domains"""
        cross_domain = []
        
        for contract in contracts:
            domains = self._analyze_contract_domains(contract)
            if len(domains) > 1:
                contract["detected_domains"] = domains
                cross_domain.append(contract)
        
        return cross_domain
    
    def _analyze_contract_domains(self, contract: Dict) -> List[str]:
        """Analyze contract to identify required domains"""
        domains = []
        
        # Analyze contract description and tasks
        description = contract.get("description", "").lower()
        title = contract.get("title", "").lower()
        tasks = contract.get("tasks", [])
        
        # Domain detection keywords
        domain_keywords = {
            "integration": ["integration", "integrate", "bridge", "connect"],
            "architecture": ["architecture", "design", "pattern", "structure"],
            "infrastructure": ["infrastructure", "deployment", "devops", "monitoring"],
            "analytics": ["analytics", "metrics", "business intelligence", "bi"],
            "communication": ["communication", "messaging", "coordination"],
            "web": ["web", "frontend", "ui", "dashboard", "website"],
            "qa": ["qa", "testing", "test", "quality", "validation"]
        }
        
        # Check description and title
        text = f"{description} {title}"
        for domain, keywords in domain_keywords.items():
            if any(keyword in text for keyword in keywords):
                if domain not in domains:
                    domains.append(domain)
        
        # Check tasks
        for task in tasks:
            task_text = f"{task.get('title', '')} {task.get('description', '')}".lower()
            for domain, keywords in domain_keywords.items():
                if any(keyword in task_text for keyword in keywords):
                    if domain not in domains:
                        domains.append(domain)
        
        return domains
    
    def get_domain_experts(self, domains: List[str]) -> List[str]:
        """Get domain expert agents for given domains"""
        domain_to_agent = {
            "integration": "Agent-1",
            "architecture": "Agent-2",
            "infrastructure": "Agent-3",
            "analytics": "Agent-5",
            "communication": "Agent-6",
            "web": "Agent-7",
            "qa": "Agent-8"
        }
        
        agents = []
        for domain in domains:
            agent = domain_to_agent.get(domain)
            if agent and agent not in agents:
                agents.append(agent)
        
        return agents
```

**V2 Compliance**: ✅ ~250 lines, single responsibility, clear functions

---

### **1.7 Create Telephone Game Chain Manager**

**New File**: `src/core/telephone_game_tracker.py` (~280 lines)

**Purpose**: Manage Telephone Game chains, track progress, integrate with contracts

**Implementation**:
```python
"""
Telephone Game Tracker - Manages Telephone Game chains
Tracks chain progress, integrates with contracts and GaslineHub

SSOT Domain: communication
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TelephoneGameTracker:
    """Tracks and manages Telephone Game chains"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.hub_dir = self.project_root / "agent_workspaces" / "GaslineHub"
        self.hub_dir.mkdir(parents=True, exist_ok=True)
        self.chains_file = self.hub_dir / "telephone_game_chains.json"
        self.contract_manager = None
        self.gasline_hub = None
    
    def create_chain_from_contract(self, contract: Dict, chain_agents: List[str]) -> Dict:
        """Create Telephone Game chain from cross-domain contract"""
        chain_id = f"chain_{contract.get('contract_id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        chain = {
            "chain_id": chain_id,
            "contract_id": contract.get("contract_id"),
            "chain_agents": chain_agents,
            "chain_position": 0,
            "total_length": len(chain_agents),
            "status": "initiated",
            "created_at": datetime.now().isoformat(),
            "contract": contract,
            "chain_contracts": []
        }
        
        # Create contracts for each agent in chain
        chain_contracts = self._create_chain_contracts(chain, contract)
        chain["chain_contracts"] = chain_contracts
        
        # Save chain
        self._save_chain(chain)
        
        # Log in GaslineHub
        self._log_chain_creation(chain)
        
        return chain
    
    def _create_chain_contracts(self, chain: Dict, original_contract: Dict) -> List[Dict]:
        """Create contracts for each agent in chain"""
        chain_contracts = []
        
        if not self.contract_manager:
            from src.services.contract_system.manager import ContractManager
            self.contract_manager = ContractManager()
        
        for i, agent_id in enumerate(chain["chain_agents"]):
            chain_contract = {
                "contract_id": f"{original_contract.get('contract_id')}_chain_{i+1}",
                "title": f"Telephone Game Chain: {original_contract.get('title', 'Cross-Domain Task')}",
                "description": f"Part of Telephone Game chain for {original_contract.get('title')}",
                "agent_id": agent_id,
                "status": "pending",
                "chain_info": {
                    "chain_id": chain["chain_id"],
                    "chain_position": i + 1,
                    "total_chain_length": len(chain["chain_agents"]),
                    "previous_agent": chain["chain_agents"][i-1] if i > 0 else None,
                    "next_agent": chain["chain_agents"][i+1] if i < len(chain["chain_agents"]) - 1 else None,
                    "final_target": chain["chain_agents"][-1],
                    "role_in_chain": self._get_chain_role(agent_id, i, len(chain["chain_agents"]))
                },
                "contract_tasks": self._extract_chain_tasks(original_contract, agent_id, i),
                "points": original_contract.get("points", 100) // len(chain["chain_agents"]),
                "created_at": datetime.now().isoformat()
            }
            
            # Save chain contract
            try:
                from src.services.contract_system.models import Contract
                contract_obj = Contract.from_dict(chain_contract)
                self.contract_manager.storage.save_contract(contract_obj)
                chain_contracts.append(chain_contract)
            except Exception as e:
                logger.error(f"Failed to create chain contract for {agent_id}: {e}")
        
        return chain_contracts
    
    def _get_chain_role(self, agent_id: str, position: int, total: int) -> str:
        """Get role description for agent in chain"""
        if position == 0:
            return "First in chain - Initial validation"
        elif position == total - 1:
            return "Final target - Execute with enriched context"
        else:
            return "Chain relay - Add domain expertise and forward"
    
    def _extract_chain_tasks(self, contract: Dict, agent_id: str, position: int) -> List[Dict]:
        """Extract tasks relevant to this agent's position in chain"""
        # For now, return simplified task
        return [{
            "task_id": f"chain_task_{position+1}",
            "title": f"Chain Position {position+1}: Add domain expertise",
            "description": contract.get("description", ""),
            "chain_context": f"Position {position+1} in Telephone Game chain"
        }]
    
    def update_chain_progress(self, chain_id: str, agent_id: str, additions: Dict) -> bool:
        """Update chain progress when agent adds expertise"""
        chain = self._load_chain(chain_id)
        if not chain:
            return False
        
        # Update chain position
        current_position = chain.get("chain_position", 0)
        if agent_id in chain["chain_agents"]:
            agent_index = chain["chain_agents"].index(agent_id)
            if agent_index == current_position:
                chain["chain_position"] = current_position + 1
                chain["last_updated"] = datetime.now().isoformat()
                
                # Add agent's contributions
                if "contributions" not in chain:
                    chain["contributions"] = []
                chain["contributions"].append({
                    "agent_id": agent_id,
                    "position": agent_index,
                    "additions": additions,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update contract
                self._update_chain_contract(chain, agent_id, additions)
                
                # Save chain
                self._save_chain(chain)
                
                # Log progress
                self._log_chain_progress(chain, agent_id)
                
                return True
        
        return False
    
    def complete_chain(self, chain_id: str, final_result: Dict) -> bool:
        """Mark chain as complete"""
        chain = self._load_chain(chain_id)
        if not chain:
            return False
        
        chain["status"] = "completed"
        chain["completed_at"] = datetime.now().isoformat()
        chain["final_result"] = final_result
        
        # Mark all chain contracts as complete
        for chain_contract in chain.get("chain_contracts", []):
            try:
                contract = self.contract_manager.storage.get_contract(chain_contract["contract_id"])
                if contract:
                    contract["status"] = "completed"
                    self.contract_manager.storage.save_contract(contract)
            except Exception as e:
                logger.warning(f"Failed to complete chain contract: {e}")
        
        # Save chain
        self._save_chain(chain)
        
        # Log completion
        self._log_chain_completion(chain)
        
        return True
    
    def _save_chain(self, chain: Dict):
        """Save chain to file"""
        chains = []
        if self.chains_file.exists():
            chains = json.loads(self.chains_file.read_text())
        
        # Update or add chain
        updated = False
        for i, c in enumerate(chains):
            if c.get("chain_id") == chain["chain_id"]:
                chains[i] = chain
                updated = True
                break
        
        if not updated:
            chains.append(chain)
        
        self.chains_file.write_text(json.dumps(chains, indent=2))
    
    def _load_chain(self, chain_id: str) -> Optional[Dict]:
        """Load chain from file"""
        if not self.chains_file.exists():
            return None
        
        chains = json.loads(self.chains_file.read_text())
        for chain in chains:
            if chain.get("chain_id") == chain_id:
                return chain
        
        return None
    
    def _log_chain_creation(self, chain: Dict):
        """Log chain creation in GaslineHub"""
        if not self.gasline_hub:
            from src.core.gasline_integrations import GaslineHub
            self.gasline_hub = GaslineHub()
        
        self.gasline_hub.log_activation(
            source="telephone_game",
            target="all",
            action="chain_created",
            metadata={
                "chain_id": chain["chain_id"],
                "contract_id": chain.get("contract_id"),
                "chain_agents": chain["chain_agents"]
            }
        )
    
    def _log_chain_progress(self, chain: Dict, agent_id: str):
        """Log chain progress in GaslineHub"""
        if not self.gasline_hub:
            from src.core.gasline_integrations import GaslineHub
            self.gasline_hub = GaslineHub()
        
        next_agent = None
        if chain["chain_position"] < len(chain["chain_agents"]):
            next_agent = chain["chain_agents"][chain["chain_position"]]
        
        self.gasline_hub.log_activation(
            source="telephone_game",
            target=next_agent or "complete",
            action="chain_progress",
            metadata={
                "chain_id": chain["chain_id"],
                "current_agent": agent_id,
                "position": chain["chain_position"],
                "total": chain["total_length"]
            }
        )
    
    def _log_chain_completion(self, chain: Dict):
        """Log chain completion in GaslineHub"""
        if not self.gasline_hub:
            from src.core.gasline_integrations import GaslineHub
            self.gasline_hub = GaslineHub()
        
        self.gasline_hub.log_activation(
            source="telephone_game",
            target=chain["chain_agents"][-1],
            action="chain_completed",
            metadata={
                "chain_id": chain["chain_id"],
                "contract_id": chain.get("contract_id"),
                "final_result": chain.get("final_result")
            }
        )
    
    def _update_chain_contract(self, chain: Dict, agent_id: str, additions: Dict):
        """Update chain contract with agent's additions"""
        # Find contract for this agent
        for chain_contract in chain.get("chain_contracts", []):
            if chain_contract.get("agent_id") == agent_id:
                # Update contract with additions
                if "additions" not in chain_contract:
                    chain_contract["additions"] = []
                chain_contract["additions"].append(additions)
                chain_contract["status"] = "in_progress"
                
                # Save updated contract
                try:
                    from src.services.contract_system.models import Contract
                    contract_obj = Contract.from_dict(chain_contract)
                    self.contract_manager.storage.save_contract(contract_obj)
                except Exception as e:
                    logger.warning(f"Failed to update chain contract: {e}")
```

**V2 Compliance**: ✅ ~280 lines, single responsibility, clear functions

---

## 📋 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Captain Integration** (HIGH PRIORITY)

- [ ] **1.1** Enhance Captain Restart Pattern v1 with debate/meeting/contract checks
- [ ] **1.2** Enhance GaslineHub with logging (`log_activation()` method) and chain tracking
- [ ] **1.3** Create `src/core/debate_monitor.py` (~250 lines)
- [ ] **1.4** Create `src/core/meeting_coordinator.py` (~200 lines)
- [ ] **1.5** Create `src/core/cycle_planner_integration.py` (~250 lines)
- [ ] **1.6** Create `src/core/contract_monitor.py` (~250 lines) - **NEW**
- [ ] **1.7** Create `src/core/telephone_game_tracker.py` (~280 lines) - **NEW**
- [ ] **1.8** Create `src/core/captain_workflow_integrations.py` (~280 lines) - **UPDATED**
- [ ] **1.9** Update `src/core/gasline_integrations.py` to use logging and chain tracking
- [ ] **1.10** Update `src/services/contract_system/manager.py` with Telephone Game integration
- [ ] **1.11** Add SSOT tags to all new files (`<!-- SSOT Domain: communication -->`)
- [ ] **1.12** Create unit tests for all new modules (≥85% coverage)
- [ ] **1.13** Integration testing with Captain Restart Pattern

### **Phase 2: Active Monitoring** (MEDIUM PRIORITY)

- [ ] **2.1** Update `swarm_brain/protocols/CYCLE_PROTOCOLS.md` with cycle planner integration
- [ ] **2.2** Update `runtime/agent_comms/TELEPHONE_GAME_PROTOCOL.md` with contract integration
- [ ] **2.3** Create helper functions for agent cycle integration
- [ ] **2.4** Test cycle planner task loading in agent workflow
- [ ] **2.5** Test meeting task assignment flow
- [ ] **2.6** Test debate decision execution flow
- [ ] **2.7** Test contract detection and Telephone Game chain creation - **NEW**
- [ ] **2.8** Test Telephone Game chain relay with contract updates - **NEW**
- [ ] **2.9** Test chain completion and contract synchronization - **NEW**

### **Phase 3: Automation** (LOW PRIORITY - Future)

- [ ] **3.1** Auto-trigger debates for major decisions
- [ ] **3.2** Auto-schedule meetings for coordination needs
- [ ] **3.3** Auto-populate cycle planner from status.json

---

## 🎯 **ARCHITECTURE DECISIONS**

### **1. SSOT Domain Assignment**

**Decision**: All new modules assigned to **Communication SSOT** domain

**Rationale**:
- Debates, meetings, cycle planning are all communication/coordination systems
- GaslineHub is a communication coordinator
- Maintains clear domain boundaries

**Implementation**: Add `<!-- SSOT Domain: communication -->` to all new files

---

### **2. Integration Pattern**

**Decision**: Use **Orchestrator Pattern** with dependency injection

**Rationale**:
- Captain Workflow Integrations orchestrates all systems
- GaslineHub coordinates activations
- Each system maintains independence
- Easy to test and maintain

**Implementation**: 
- `CaptainWorkflowIntegrations` orchestrates
- `GaslineHub` coordinates
- Individual monitors/coordinators handle their domains

---

### **3. Error Handling**

**Decision**: Graceful degradation with logging

**Rationale**:
- Systems should not break if one integration fails
- Log all errors for debugging
- Continue processing other systems

**Implementation**:
- Try/except blocks around all integration points
- Log errors with context
- Return success/failure status

---

### **4. V2 Compliance**

**Decision**: All new files must meet V2 standards

**Requirements**:
- Files: <300 lines
- Classes: <200 lines
- Functions: <30 lines
- Test coverage: ≥85%

**Implementation**: 
- Split large modules if needed
- Extract helper functions
- Create comprehensive test suites

---

## 📊 **EXPECTED BENEFITS**

### **Swarm Efficiency**:
- **Debates**: Democratic decisions → Automatic execution (no manual intervention)
- **Meetings**: Coordinated multi-agent work → Better outcomes
- **Cycle Planner**: Task continuity → No lost work
- **GaslineHub**: Central coordination → System visibility
- **Telephone Game**: Cross-domain coordination → Enriched information flow - **NEW**
- **Contracts**: Structured task assignment → Better task management - **NEW**

### **Reduced Manual Work**:
- Captain doesn't need to manually check each system
- Agents automatically get tasks from cycle planner and contracts
- Decisions automatically executed
- Telephone Game chains automatically detected and initiated - **NEW**
- Contracts automatically assigned for cross-domain work - **NEW**

### **Better Coordination**:
- All systems connected through GaslineHub
- Central logging of all activations
- System-wide visibility
- Telephone Game for multi-domain coordination - **NEW**
- Contracts for structured task assignment - **NEW**
- Chain tracking for cross-domain work - **NEW**

---

## 🚀 **NEXT STEPS**

1. **Review & Approval**: Captain reviews this implementation plan
2. **Assignment**: Assign Phase 1 tasks to appropriate agents
3. **Execution**: Begin Phase 1 implementation
4. **Testing**: Verify integrations work correctly
5. **Documentation**: Update protocols and documentation

---

## 📝 **FILES TO CREATE/MODIFY**

### **New Files** (7 core files + 8 test files = 15 files):
1. `src/core/debate_monitor.py` (~250 lines)
2. `src/core/meeting_coordinator.py` (~200 lines)
3. `src/core/cycle_planner_integration.py` (~250 lines)
4. `src/core/contract_monitor.py` (~250 lines) - **NEW**
5. `src/core/telephone_game_tracker.py` (~280 lines) - **NEW**
6. `src/core/captain_workflow_integrations.py` (~280 lines) - **UPDATED**
7. `tests/unit/core/test_debate_monitor.py` (~150 lines)
8. `tests/unit/core/test_meeting_coordinator.py` (~120 lines)
9. `tests/unit/core/test_cycle_planner_integration.py` (~150 lines)
10. `tests/unit/core/test_contract_monitor.py` (~150 lines) - **NEW**
11. `tests/unit/core/test_telephone_game_tracker.py` (~180 lines) - **NEW**
12. `tests/unit/core/test_captain_workflow_integrations.py` (~180 lines)

### **Modified Files** (5 files):
1. `src/core/gasline_integrations.py` (add logging + chain tracking, ~80 lines)
2. `src/services/contract_system/manager.py` (add Telephone Game integration, ~50 lines) - **NEW**
3. `agent_workspaces/Agent-4/inbox/CAPTAIN_RESTART_PATTERN_V1_2025-12-03.md` (add checks)
4. `swarm_brain/protocols/CYCLE_PROTOCOLS.md` (add cycle planner integration)
5. `runtime/agent_comms/TELEPHONE_GAME_PROTOCOL.md` (add contract integration) - **NEW**

**Total**: 15 new files, 5 modified files

---

---

## 📞 **TELEPHONE GAME + CONTRACTS INTEGRATION DETAILS**

### **Integration Architecture**

**Flow**: Cross-Domain Contract → Telephone Game Chain → Contract Generation → Chain Initiation

```
Contract Detection
    ↓
Domain Analysis (Contract Monitor)
    ↓
Chain Agent Identification
    ↓
Chain Contract Creation (Telephone Game Tracker)
    ↓
Chain Initiation (Messaging System)
    ↓
Chain Progress Tracking (GaslineHub)
    ↓
Chain Completion (Contract Synchronization)
```

### **Key Integration Points**

1. **Contract Detection** (`contract_monitor.py`):
   - Analyzes contract description/tasks for domain keywords
   - Identifies contracts spanning multiple domains
   - Returns domain expert agents for chain

2. **Chain Creation** (`telephone_game_tracker.py`):
   - Creates Telephone Game chain from contract
   - Generates chain contracts for each agent
   - Stores chain metadata in GaslineHub

3. **Chain Initiation**:
   - Sends Telephone Game message to first agent
   - Includes contract context and chain information
   - Tracks chain progress in GaslineHub

4. **Chain Relay**:
   - Each agent updates their chain contract
   - Adds domain expertise to contract
   - Forwards enriched message to next agent

5. **Chain Completion**:
   - Final agent completes chain and all contracts
   - Logs completion in GaslineHub
   - Synchronizes contract status

### **Contract Structure for Chains**

Each agent in chain receives a contract with:
- `chain_info`: Chain metadata (position, previous/next agents, role)
- `contract_tasks`: Tasks specific to chain position
- `chain_context`: Full chain information for context

### **Benefits**

- **Automatic Detection**: Cross-domain contracts automatically trigger Telephone Game
- **Contract Tracking**: Each agent has contract with chain context
- **Enriched Information**: Domain expertise added at each step
- **Coordinated Execution**: Final agent has complete context
- **System Integration**: Contracts → Telephone Game → GaslineHub → Messaging

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-2 - Architecture & Design Specialist*  
*Swarm Systems Integration - Implementation Plan Complete (v2.0 - Updated with Telephone Game + Contracts)*

