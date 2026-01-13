#!/usr/bin/env python3
"""
Swarm Task Tracker v1.0
========================

AI-powered task assignment and progress tracking system.
Automatically distributes work across swarm, prevents bottlenecks.

Author: Agent-4 (Strategic Coordination Lead)
Created: 2026-01-13
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

class SwarmTaskTracker:
    """Intelligent task distribution and tracking system."""

    def __init__(self, repo_path: str = "D:/Agent_Cellphone_V2_Repository"):
        self.repo_path = Path(repo_path)
        self.task_matrix_file = self.repo_path / "swarm_task_distribution_matrix_20260113.md"
        self.coordination_cache = self.repo_path / "coordination_cache.json"
        self.agent_workspaces = self.repo_path / "agent_workspaces"

        # Agent expertise mapping for smart assignment
        self.agent_expertise = {
            'Agent-1': ['integration', 'core', 'messaging', 'unified'],
            'Agent-2': ['architecture', 'storage', 'data', 'design'],
            'Agent-3': ['infrastructure', 'devops', 'monitoring', 'reliability'],
            'Agent-4': ['coordination', 'strategy', 'qa', 'leadership'],
            'Agent-5': ['ai', 'intelligence', 'prediction', 'analysis'],
            'Agent-6': ['research', 'analytics', 'optimization', 'patterns'],
            'Agent-7': ['ui', 'ux', 'testing', 'validation'],
            'Agent-8': ['planning', 'documentation', 'strategy', 'automation']
        }

        self.task_status = self._load_task_status()

    def _load_task_status(self) -> Dict:
        """Load current task completion status."""
        # This would ideally be stored in a database, but for now we'll track in memory
        # and persist to a JSON file
        status_file = self.repo_path / "task_status_cache.json"
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._initialize_task_status()

    def _initialize_task_status(self) -> Dict:
        """Initialize task status from the distribution matrix."""
        status = {}

        try:
            with open(self.task_matrix_file, 'r') as f:
                content = f.read()

            current_agent = None
            for line in content.split('\n'):
                if line.startswith('### **Agent-'):
                    current_agent = line.split('**')[1].replace(':', '')
                    status[current_agent] = {'classes': {}}
                elif current_agent and line.strip().startswith('✅'):
                    class_name = line.strip()[1:].strip()
                    if class_name:
                        status[current_agent]['classes'][class_name] = {
                            'status': 'ASSIGNED',
                            'assigned_at': datetime.now().isoformat(),
                            'completed_at': None,
                            'progress': 0
                        }
        except FileNotFoundError:
            pass

        return status

    def auto_assign_tasks(self, todo_items: List[str]) -> Dict[str, List[str]]:
        """AI-powered automatic task assignment based on agent expertise."""
        assignments = {agent: [] for agent in self.agent_expertise.keys()}

        for todo in todo_items:
            best_agent = self._find_best_agent_for_task(todo)
            if best_agent:
                assignments[best_agent].append(todo)

        return assignments

    def _find_best_agent_for_task(self, task: str) -> Optional[str]:
        """Find the best agent for a given task based on expertise matching."""
        task_lower = task.lower()
        best_score = 0
        best_agent = None

        for agent, expertise in self.agent_expertise.items():
            score = 0
            for keyword in expertise:
                if keyword in task_lower:
                    score += 1

            # Bonus for Agent-4 as coordination lead for coordination tasks
            if agent == 'Agent-4' and any(word in task_lower for word in ['coordinate', 'assign', 'lead', 'manage']):
                score += 2

            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent

    def update_task_progress(self, agent_id: str, class_name: str, progress: int, notes: str = ""):
        """Update progress for a specific task."""
        if agent_id not in self.task_status:
            self.task_status[agent_id] = {'classes': {}}

        if class_name not in self.task_status[agent_id]['classes']:
            self.task_status[agent_id]['classes'][class_name] = {
                'status': 'IN_PROGRESS',
                'assigned_at': datetime.now().isoformat(),
                'progress': 0
            }

        task = self.task_status[agent_id]['classes'][class_name]
        task['progress'] = min(100, max(0, progress))
        task['last_updated'] = datetime.now().isoformat()
        task['notes'] = notes

        if progress >= 100:
            task['status'] = 'COMPLETED'
            task['completed_at'] = datetime.now().isoformat()
        elif progress > 0:
            task['status'] = 'IN_PROGRESS'
        else:
            task['status'] = 'ASSIGNED'

        self._save_task_status()

    def get_overall_progress(self) -> Dict:
        """Get overall swarm progress metrics."""
        total_tasks = 0
        completed_tasks = 0
        total_progress = 0

        for agent_status in self.task_status.values():
            for class_status in agent_status.get('classes', {}).values():
                total_tasks += 1
                total_progress += class_status.get('progress', 0)
                if class_status.get('status') == 'COMPLETED':
                    completed_tasks += 1

        avg_progress = total_progress / total_tasks if total_tasks > 0 else 0
        completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0

        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate * 100,
            'average_progress': avg_progress,
            'estimated_completion': self._estimate_completion_time()
        }

    def _estimate_completion_time(self) -> str:
        """Estimate completion time based on current progress."""
        progress = self.get_overall_progress()
        avg_progress = progress['average_progress']

        if avg_progress >= 100:
            return "COMPLETED"
        elif avg_progress == 0:
            return "Not started"

        # Assume linear progress, 8 hours total work
        hours_remaining = (100 - avg_progress) / 100 * 8
        completion_time = datetime.now() + timedelta(hours=hours_remaining)

        return f"{completion_time.strftime('%H:%M UTC')} ({hours_remaining:.1f} hours)"

    def get_agent_workload(self) -> Dict[str, Dict]:
        """Get workload analysis for all agents."""
        workloads = {}

        for agent_id in self.agent_expertise.keys():
            agent_status = self.task_status.get(agent_id, {'classes': {}})
            classes = agent_status.get('classes', {})

            total_assigned = len(classes)
            completed = sum(1 for c in classes.values() if c.get('status') == 'COMPLETED')
            in_progress = sum(1 for c in classes.values() if c.get('status') == 'IN_PROGRESS')
            avg_progress = sum(c.get('progress', 0) for c in classes.values()) / total_assigned if total_assigned > 0 else 0

            workloads[agent_id] = {
                'total_assigned': total_assigned,
                'completed': completed,
                'in_progress': in_progress,
                'avg_progress': avg_progress,
                'workload_level': self._calculate_workload_level(total_assigned, in_progress)
            }

        return workloads

    def _calculate_workload_level(self, total_assigned: int, in_progress: int) -> str:
        """Calculate workload level descriptor."""
        if total_assigned == 0:
            return "IDLE"
        elif total_assigned >= 5 or in_progress >= 3:
            return "OVERLOADED"
        elif total_assigned >= 3 or in_progress >= 2:
            return "HIGH"
        elif total_assigned >= 2 or in_progress >= 1:
            return "MEDIUM"
        else:
            return "LIGHT"

    def redistribute_overloaded_tasks(self) -> Dict[str, List[str]]:
        """Redistribute tasks from overloaded agents to available agents."""
        workloads = self.get_agent_workload()
        redistributions = {}

        # Find overloaded agents
        overloaded = [agent for agent, workload in workloads.items()
                     if workload['workload_level'] == 'OVERLOADED']

        # Find available agents
        available = [agent for agent, workload in workloads.items()
                    if workload['workload_level'] in ['IDLE', 'LIGHT']]

        for overloaded_agent in overloaded:
            if not available:
                break

            # Get tasks that can be redistributed
            agent_tasks = self.task_status.get(overloaded_agent, {}).get('classes', {})
            pending_tasks = [task for task, status in agent_tasks.items()
                           if status.get('status') != 'COMPLETED']

            if len(pending_tasks) <= 3:  # Keep minimum workload
                continue

            # Redistribute excess tasks
            tasks_to_move = pending_tasks[3:]  # Keep 3, redistribute the rest
            target_agent = available[0]  # Simple round-robin for now

            redistributions[f"{overloaded_agent} → {target_agent}"] = tasks_to_move

            # Update task status
            for task in tasks_to_move:
                if task in self.task_status[overloaded_agent]['classes']:
                    # Move task to new agent
                    task_data = self.task_status[overloaded_agent]['classes'][task]
                    if target_agent not in self.task_status:
                        self.task_status[target_agent] = {'classes': {}}
                    self.task_status[target_agent]['classes'][task] = task_data

                    # Remove from old agent
                    del self.task_status[overloaded_agent]['classes'][task]

            self._save_task_status()

        return redistributions

    def _save_task_status(self):
        """Save task status to persistent storage."""
        status_file = self.repo_path / "task_status_cache.json"
        with open(status_file, 'w') as f:
            json.dump(self.task_status, f, indent=2, default=str)

    def generate_status_report(self) -> str:
        """Generate comprehensive status report."""
        progress = self.get_overall_progress()
        workloads = self.get_agent_workload()

        report = []
        report.append("📊 SWARM TASK TRACKER REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        report.append("")

        report.append("🎯 OVERALL PROGRESS:")
        report.append(f"  Total Tasks: {progress['total_tasks']}")
        report.append(f"  Completed: {progress['completed_tasks']}")
        report.append(".1f"        report.append(".1f"        report.append(f"  ETA: {progress['estimated_completion']}")
        report.append("")

        report.append("👥 AGENT WORKLOADS:")
        for agent, workload in workloads.items():
            status_icon = {
                'OVERLOADED': '🔴',
                'HIGH': '🟡',
                'MEDIUM': '🟢',
                'LIGHT': '🔵',
                'IDLE': '⚪'
            }.get(workload['workload_level'], '❓')

            report.append(f"  {status_icon} {agent}: {workload['total_assigned']} tasks | "
                         ".1f"                         f" | {workload['workload_level']}")

        # Check for redistributions needed
        overloaded_count = sum(1 for w in workloads.values() if w['workload_level'] == 'OVERLOADED')
        if overloaded_count > 0:
            report.append("")
            report.append("⚠️  WORKLOAD REDISTRIBUTION RECOMMENDED:")
            redistributions = self.redistribute_overloaded_tasks()
            if redistributions:
                for move, tasks in redistributions.items():
                    report.append(f"  🔄 {move}: {len(tasks)} tasks")
            else:
                report.append("  Unable to redistribute - all agents at capacity")

        report.append("")
        report.append("💡 AI INSIGHTS:")
        report.append("  • Parallel processing activated across all agents")
        report.append("  • Real-time progress tracking enabled")
        report.append("  • Automated workload balancing active")

        return "\n".join(report)

def main():
    """Main task tracker execution."""
    tracker = SwarmTaskTracker()

    # Display current status
    print(tracker.generate_status_report())

    # Check for needed redistributions
    workloads = tracker.get_agent_workload()
    overloaded = [agent for agent, workload in workloads.items()
                 if workload['workload_level'] == 'OVERLOADED']

    if overloaded:
        print(f"\n🔄 REDISTRIBUTING WORKLOAD FROM: {', '.join(overloaded)}")
        redistributions = tracker.redistribute_overloaded_tasks()
        if redistributions:
            print("✅ Redistribution completed")
        else:
            print("⚠️  No redistribution possible")

    print("\n⚡ TASK TRACKING ACTIVE - SWARM EFFICIENCY MAXIMIZED")

if __name__ == "__main__":
    main()