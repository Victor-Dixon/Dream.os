#!/usr/bin/env python3
"""
Agent Consolidation Coordinator

This script coordinates consolidation tasks across the 8-agent team, ensuring
that consolidation operations are properly distributed and tracked. It handles:

1. Task assignment based on agent capabilities
2. Progress tracking and status updates
3. Conflict prevention during multi-agent operations
4. Consolidation result aggregation

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class ConsolidationPhase(Enum):
    PHASE1 = "phase1"
    PHASE2 = "phase2"
    PHASE3 = "phase3"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"

@dataclass
class ConsolidationTask:
    """Represents a consolidation task assigned to an agent"""
    task_id: str
    phase: ConsolidationPhase
    operation: str
    agent_id: str
    description: str
    priority: str  # "high", "medium", "low"
    estimated_effort: str  # "small", "medium", "large"
    dependencies: List[str]  # Task IDs this task depends on
    status: TaskStatus
    assigned_at: str
    completed_at: str = ""
    result: Optional[Dict[str, Any]] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self):
        data = asdict(self)
        data['phase'] = self.phase.value
        data['status'] = self.status.value
        return data

    @staticmethod
    def from_dict(task_data: Dict[str, Any]) -> "ConsolidationTask":
        """
        Robust loader for tasks persisted as JSON.
        Accepts both enum objects and legacy string values for phase/status.
        """
        phase_val = task_data.get("phase")
        status_val = task_data.get("status")

        # Normalize phase/status (strings → enums)
        if isinstance(phase_val, str):
            phase = ConsolidationPhase(phase_val)
        elif isinstance(phase_val, ConsolidationPhase):
            phase = phase_val
        else:
            raise ValueError(f"Invalid phase value: {phase_val!r}")

        if isinstance(status_val, str):
            status = TaskStatus(status_val)
        elif isinstance(status_val, TaskStatus):
            status = status_val
        else:
            raise ValueError(f"Invalid status value: {status_val!r}")

        # Notes/result normalization
        notes = task_data.get("notes") or []
        if not isinstance(notes, list):
            notes = [str(notes)]

        result = task_data.get("result", None)
        if result is not None and not isinstance(result, dict):
            # Keep it safe: store as dict wrapper
            result = {"value": result}

        return ConsolidationTask(
            task_id=task_data["task_id"],
            phase=phase,
            operation=task_data["operation"],
            agent_id=task_data.get("agent_id", ""),
            description=task_data["description"],
            priority=task_data["priority"],
            estimated_effort=task_data["estimated_effort"],
            dependencies=task_data.get("dependencies", []),
            status=status,
            assigned_at=task_data.get("assigned_at", ""),
            completed_at=task_data.get("completed_at", ""),
            result=result,
            notes=notes,
        )

@dataclass
class AgentCapability:
    """Defines an agent's capabilities for consolidation tasks"""
    agent_id: str
    role: str
    specializations: List[str]
    current_workload: int  # Number of active tasks
    available: bool

class ConsolidationCoordinator:
    """Coordinates consolidation tasks across the 8-agent team"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.agent_workspaces = self.base_path / "agent_workspaces"
        self.coordination_file = self.agent_workspaces / "consolidation_coordination.json"
        self.tasks_file = self.agent_workspaces / "consolidation_tasks.json"
        self.agent_workspaces.mkdir(parents=True, exist_ok=True)

        # Define agent capabilities
        self.agent_capabilities = {
            "Agent-1": AgentCapability("Agent-1", "Integration & Core Systems",
                                     ["file_operations", "data_processing", "automation"], 0, True),
            "Agent-2": AgentCapability("Agent-2", "Architecture & Design",
                                     ["architecture", "design_patterns", "code_review"], 0, True),
            "Agent-3": AgentCapability("Agent-3", "Infrastructure & DevOps",
                                     ["infrastructure", "deployment", "monitoring"], 0, True),
            "Agent-4": AgentCapability("Agent-4", "Captain (Strategic Oversight)",
                                     ["coordination", "planning", "oversight"], 0, True),
            "Agent-5": AgentCapability("Agent-5", "Business Intelligence",
                                     ["analytics", "reporting", "data_analysis"], 0, True),
            "Agent-6": AgentCapability("Agent-6", "Coordination & Communication",
                                     ["communication", "messaging", "coordination"], 0, True),
            "Agent-7": AgentCapability("Agent-7", "Web Development",
                                     ["web_development", "frontend", "automation"], 0, True),
            "Agent-8": AgentCapability("Agent-8", "SSOT & System Integration",
                                     ["integration", "data_consistency", "system_design"], 0, True)
        }

        self.tasks: Dict[str, ConsolidationTask] = {}
        self.load_existing_tasks()

    def load_existing_tasks(self):
        """Load existing consolidation tasks from file"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    for task_data in data.get('tasks', []):
                        try:
                            task = ConsolidationTask.from_dict(task_data)
                            self.tasks[task.task_id] = task
                        except Exception as task_err:
                            print(f"Warning: Skipping invalid task record: {task_err}")
            except Exception as e:
                print(f"Warning: Could not load existing tasks: {e}")

    def save_tasks(self):
        """Save current tasks to file"""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'tasks': [task.to_dict() for task in self.tasks.values()]
            }
            with open(self.tasks_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def create_phase1_tasks(self) -> List[ConsolidationTask]:
        """Create Phase 1 consolidation tasks"""
        tasks = []

        # Phase 1 Task 1: Agent Workspace Cleanup (QUICK_START.md deduplication)
        task1 = ConsolidationTask(
            task_id="phase1_quickstart_dedup",
            phase=ConsolidationPhase.PHASE1,
            operation="quickstart_deduplication",
            agent_id="",  # Will be assigned
            description="Deduplicate QUICK_START.md files across all agent workspaces",
            priority="high",
            estimated_effort="small",
            dependencies=[],
            status=TaskStatus.PENDING,
            assigned_at=""
        )
        tasks.append(task1)

        # Phase 1 Task 2: Cache file cleanup
        task2 = ConsolidationTask(
            task_id="phase1_cache_cleanup",
            phase=ConsolidationPhase.PHASE1,
            operation="cache_cleanup",
            agent_id="",
            description="Remove .pyc cache files and __pycache__ directories from agent workspaces",
            priority="medium",
            estimated_effort="small",
            dependencies=[],
            status=TaskStatus.PENDING,
            assigned_at=""
        )
        tasks.append(task2)

        # Phase 1 Task 3: Archive consolidation
        task3 = ConsolidationTask(
            task_id="phase1_archive_consolidation",
            phase=ConsolidationPhase.PHASE1,
            operation="archive_consolidation",
            agent_id="",
            description="Consolidate archive directories into centralized location",
            priority="medium",
            estimated_effort="medium",
            dependencies=[],
            status=TaskStatus.PENDING,
            assigned_at=""
        )
        tasks.append(task3)

        # Phase 1 Task 4: Status.json standardization
        task4 = ConsolidationTask(
            task_id="phase1_status_standardization",
            phase=ConsolidationPhase.PHASE1,
            operation="status_standardization",
            agent_id="",
            description="Ensure all status.json files have required fields and proper formatting",
            priority="high",
            estimated_effort="small",
            dependencies=[],
            status=TaskStatus.PENDING,
            assigned_at=""
        )
        tasks.append(task4)

        return tasks

    def assign_task_to_agent(self, task: ConsolidationTask) -> str:
        """Assign a task to the most suitable agent based on capabilities and workload"""
        best_agent = None
        lowest_workload = float('inf')

        # Define task requirements
        task_requirements = {
            "quickstart_deduplication": ["file_operations", "automation"],
            "cache_cleanup": ["file_operations", "automation"],
            "archive_consolidation": ["file_operations", "data_processing"],
            "status_standardization": ["data_processing", "automation"],
            "report_consolidation": ["analytics", "data_processing"],
            "documentation_cleanup": ["web_development", "automation"],
            "archive_optimization": ["infrastructure", "data_processing"],
            "monitoring_setup": ["infrastructure", "monitoring"]
        }

        required_skills = task_requirements.get(task.operation, ["automation"])

        for agent_id, capability in self.agent_capabilities.items():
            if not capability.available:
                continue

            # Check if agent has required skills
            has_required_skills = any(skill in capability.specializations for skill in required_skills)

            # Prefer agents with matching skills and lower workload
            if has_required_skills and capability.current_workload < lowest_workload:
                lowest_workload = capability.current_workload
                best_agent = agent_id

        # If no agent has perfect match, assign to lowest workload agent
        if not best_agent:
            for agent_id, capability in self.agent_capabilities.items():
                if capability.available and capability.current_workload < lowest_workload:
                    lowest_workload = capability.current_workload
                    best_agent = agent_id

        return best_agent

    def assign_tasks(self, tasks: List[ConsolidationTask]):
        """Assign tasks to agents and update coordination state"""
        for task in tasks:
            agent_id = self.assign_task_to_agent(task)
            if agent_id:
                task.agent_id = agent_id
                task.assigned_at = datetime.now().isoformat()
                task.status = TaskStatus.PENDING

                # Update agent workload
                self.agent_capabilities[agent_id].current_workload += 1

                self.tasks[task.task_id] = task
                print(f"Assigned {task.operation} to {agent_id}")

        self.save_tasks()

    def create_task_messages(self) -> List[Dict]:
        """Create messages for agents with their assigned tasks"""
        agent_tasks = {}

        # Group tasks by agent
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING and task.agent_id:
                if task.agent_id not in agent_tasks:
                    agent_tasks[task.agent_id] = []
                agent_tasks[task.agent_id].append(task)

        messages = []
        for agent_id, tasks in agent_tasks.items():
            message = {
                "to": agent_id,
                "from": "Agent-7",
                "type": "consolidation_task_assignment",
                "priority": "urgent",
                "tasks": [task.to_dict() for task in tasks],
                "instructions": "Execute the assigned consolidation tasks and update status upon completion."
            }
            messages.append(message)

        return messages

    def update_task_status(self, task_id: str, status: TaskStatus, result: Dict = None, notes: List[str] = None):
        """Update the status of a consolidation task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            old_status = task.status

            task.status = status
            if status == TaskStatus.COMPLETED:
                task.completed_at = datetime.now().isoformat()
            if result:
                task.result = result
            if notes:
                task.notes.extend(notes)

            # Update agent workload
            if old_status != TaskStatus.COMPLETED and status == TaskStatus.COMPLETED:
                if task.agent_id in self.agent_capabilities:
                    self.agent_capabilities[task.agent_id].current_workload = max(0,
                        self.agent_capabilities[task.agent_id].current_workload - 1)

            self.save_tasks()
            print(f"Updated task {task_id} status to {status.value}")

    def get_consolidation_status(self) -> Dict:
        """Get current consolidation status across all agents"""
        status_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "in_progress_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
            "pending_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
            "failed_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED]),
            "agent_workloads": {}
        }

        # Calculate agent workloads
        for agent_id, capability in self.agent_capabilities.items():
            agent_tasks = [t for t in self.tasks.values() if t.agent_id == agent_id]
            status_summary["agent_workloads"][agent_id] = {
                "total_tasks": len(agent_tasks),
                "completed": len([t for t in agent_tasks if t.status == TaskStatus.COMPLETED]),
                "in_progress": len([t for t in agent_tasks if t.status == TaskStatus.IN_PROGRESS]),
                "pending": len([t for t in agent_tasks if t.status == TaskStatus.PENDING]),
                "current_workload": capability.current_workload
            }

        return status_summary

    def save_status_report(self):
        """Save current consolidation status to file"""
        status = self.get_consolidation_status()
        status_file = self.agent_workspaces / "consolidation_status.json"

        try:
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
            print(f"Status report saved to {status_file}")
        except Exception as e:
            print(f"Error saving status report: {e}")

    def run_coordination_cycle(self):
        """Run a complete coordination cycle"""
        print("🔄 Starting Consolidation Coordination Cycle")
        print("=" * 50)

        # Create Phase 1 tasks
        print("📋 Creating Phase 1 consolidation tasks...")
        phase1_tasks = self.create_phase1_tasks()

        # Assign tasks to agents
        print("👥 Assigning tasks to agents...")
        self.assign_tasks(phase1_tasks)

        # Create task assignment messages
        print("📨 Creating task assignment messages...")
        messages = self.create_task_messages()

        # Save coordination state
        self.save_status_report()

        print("\n✅ Coordination cycle complete!")
        print(f"Created {len(phase1_tasks)} tasks")
        print(f"Generated {len(messages)} assignment messages")

        # Display agent workloads
        status = self.get_consolidation_status()
        print("\n📊 Current Agent Workloads:")
        for agent_id, workload in status["agent_workloads"].items():
            print(f"  {agent_id}: {workload['pending']} pending, {workload['in_progress']} in progress")

        return messages

    def simulate_task_completion(self, task_id: str, success: bool = True):
        """Simulate task completion for testing"""
        if task_id in self.tasks:
            status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            result = {
                "files_processed": 5,
                "files_removed": 3,
                "space_saved_mb": 1.2,
                "status": "success" if success else "error"
            }
            self.update_task_status(task_id, status, result)
            print(f"Simulated completion of task {task_id}")


def main():
    """Main entry point for consolidation coordination"""
    print("Agent Consolidation Coordinator")
    print("This script coordinates consolidation tasks across the 8-agent team.")
    print()

    coordinator = ConsolidationCoordinator()

    # Run coordination cycle
    messages = coordinator.run_coordination_cycle()

    print("\n📨 Task Assignment Messages:")
    print("-" * 30)
    for i, message in enumerate(messages, 1):
        print(f"{i}. To: {message['to']}")
        print(f"   Tasks: {len(message['tasks'])}")
        for task in message['tasks']:
            print(f"   - {task['operation']} ({task['priority']} priority)")
        print()

    # For testing: simulate some task completions
    print("🧪 Testing: Simulating task completions...")
    for task_id in list(coordinator.tasks.keys())[:2]:  # Complete first 2 tasks
        coordinator.simulate_task_completion(task_id, success=True)

    # Show updated status
    coordinator.save_status_report()

    print("\n✅ Coordination testing complete!")


if __name__ == "__main__":
    main()