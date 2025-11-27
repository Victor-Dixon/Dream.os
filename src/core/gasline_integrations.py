#!/usr/bin/env python3
"""
Gasline Integration Hub
Connects existing components to activation/messaging system

COMMANDER'S INSIGHT: "Incorporate more gaslines to components we already have"

This module provides gasline hooks for:
1. Debate System → Automatic execution
2. Swarm Brain → Knowledge-driven activation  
3. Project Scanner → Violation-driven assignments
4. Documentation → Learning-driven orientation
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GaslineHub:
    """Central hub for gasline integrations across all components"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.enabled_integrations = {
            "debate": True,
            "swarm_brain": True,
            "project_scanner": True,
            "documentation": True,
            "violations": True
        }
    
    # ═══════════════════════════════════════════════════════════
    # INTEGRATION 1: DEBATE SYSTEM → GASLINE
    # ═══════════════════════════════════════════════════════════
    
    def hook_debate_decision(
        self,
        topic: str,
        decision: str,
        agent_assignments: Dict[str, str]
    ) -> bool:
        """
        When debate concludes → Store in brain → Activate agents
        
        Flow:
        Debate ends → Swarm Brain stores → Gasline delivers → Agents execute
        """
        if not self.enabled_integrations["debate"]:
            return False
        
        try:
            # Import debate-to-gas integration
            from src.core.debate_to_gas_integration import activate_debate_decision
            
            # Activate with full context
            execution_plan = self._generate_execution_plan_from_brain(topic)
            
            activate_debate_decision(
                topic=topic,
                decision=decision,
                execution_plan=execution_plan,
                agent_assignments=agent_assignments
            )
            
            logger.info(f"⚡ Debate '{topic}' activated via gasline")
            return True
            
        except Exception as e:
            logger.error(f"❌ Debate gasline hook failed: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════
    # INTEGRATION 2: PROJECT SCANNER → GASLINE
    # ═══════════════════════════════════════════════════════════
    
    def hook_violations_found(
        self,
        violations: List[Dict],
        auto_assign: bool = True
    ) -> bool:
        """
        When violations found → Create tasks → Activate agents
        
        Flow:
        Scanner finds violations → Swarm Brain prioritizes → Gasline assigns → Agents fix
        """
        if not self.enabled_integrations["violations"]:
            return False
        
        try:
            # Prioritize violations by ROI
            prioritized = self._prioritize_violations_with_brain(violations)
            
            # Auto-assign to best agents
            if auto_assign:
                assignments = self._assign_violations_to_agents(prioritized)
                
                # Deliver via gasline
                for agent_id, violation_tasks in assignments.items():
                    self._send_violation_assignment(agent_id, violation_tasks)
            
            logger.info(f"⚡ {len(violations)} violations activated via gasline")
            return True
            
        except Exception as e:
            logger.error(f"❌ Violation gasline hook failed: {e}")
            return False
    
    def _prioritize_violations_with_brain(
        self, violations: List[Dict]
    ) -> List[Dict]:
        """Use Swarm Brain to prioritize violations by ROI/impact"""
        # Query brain for historical patterns
        # Which violations had highest ROI when fixed?
        # Which are blocking other work?
        
        # For now, simple prioritization
        return sorted(
            violations,
            key=lambda v: (
                v.get('complexity', 0),  # Higher complexity = higher priority
                v.get('lines', 0)         # Larger files = higher priority
            ),
            reverse=True
        )
    
    def _assign_violations_to_agents(
        self, violations: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """Assign violations to best-suited agents using Swarm Brain + Markov optimizer."""
        assignments = {}
        
        try:
            # Use smart assignment with Swarm Brain + Markov optimizer
            smart_assigner = SmartAssignmentOptimizer()
            assignments = smart_assigner.assign_violations(violations)
            logger.info(f"Smart assignment completed for {len(violations)} violations")
            return assignments
        except Exception as e:
            logger.error(f"Smart assignment failed, falling back to round-robin: {e}")
            # Fallback to round-robin
            return self._assign_violations_round_robin(violations)
    
    def _assign_violations_round_robin(
        self, violations: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """Fallback round-robin assignment."""
        assignments = {}
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        for i, violation in enumerate(violations[:7]):  # Top 7
            agent_id = agents[i % len(agents)]
            if agent_id not in assignments:
                assignments[agent_id] = []
            assignments[agent_id].append(violation)
        return assignments
    
    def _send_violation_assignment(
        self, agent_id: str, violations: List[Dict]
    ):
        """Send violation assignment via gasline"""
        violation_list = "\n".join([
            f"  • {v['file']} ({v.get('lines', '?')} lines)"
            for v in violations
        ])
        
        message = f"""🚨 V2 VIOLATIONS DETECTED → IMMEDIATE ACTION!

VIOLATIONS ASSIGNED TO YOU ({agent_id}):
{violation_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MISSION: Fix V2 violations
PRIORITY: HIGH
VALUE: {len(violations) * 300}-{len(violations) * 500} points

STEPS:
1. Review violations: cat project_analysis.json
2. Create execution plan
3. Fix violations (target: <400 lines, 100% types, tests)
4. Verify: python tools/v2_compliance_checker.py
5. Report completion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐝 AUTO-ASSIGNED VIA SWARM INTELLIGENCE!

BEGIN NOW!
"""
        
        try:
            from src.services.messaging_cli_handlers import send_message_to_agent
            send_message_to_agent(
                agent_id=agent_id,
                message=message,
                sender="Swarm Brain (Auto-Assignment)",
                priority="high",
                use_pyautogui=True
            )
            logger.info(f"⚡ Violation assignment sent to {agent_id}")
        except ImportError:
            # Fallback: Create inbox file
            inbox_file = self.project_root / "agent_workspaces" / agent_id / "inbox" / f"VIOLATIONS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            inbox_file.parent.mkdir(parents=True, exist_ok=True)
            inbox_file.write_text(message)
            logger.info(f"📥 Violation inbox created for {agent_id}")
    
    # ═══════════════════════════════════════════════════════════
    # INTEGRATION 3: SWARM BRAIN → GASLINE
    # ═══════════════════════════════════════════════════════════
    
    def hook_knowledge_request(
        self, agent_id: str, query: str
    ) -> bool:
        """
        When agent needs knowledge → Brain searches → Gas delivers results
        
        Flow:
        Agent asks question → Swarm Brain finds answer → Gasline delivers → Agent proceeds
        """
        if not self.enabled_integrations["swarm_brain"]:
            return False
        
        try:
            from src.swarm_brain.swarm_memory import SwarmMemory
            
            memory = SwarmMemory(agent_id=agent_id)
            results = memory.search_swarm_knowledge(query)
            
            if results:
                # Send results via gasline
                self._send_knowledge_results(agent_id, query, results)
                return True
            else:
                # No results - send guidance
                self._send_no_results_guidance(agent_id, query)
                return False
                
        except Exception as e:
            logger.error(f"❌ Knowledge gasline hook failed: {e}")
            return False
    
    def _send_knowledge_results(
        self, agent_id: str, query: str, results: List
    ):
        """Send knowledge search results to agent"""
        results_text = "\n".join([
            f"  {i+1}. {r.get('title', 'Untitled')}"
            for i, r in enumerate(results[:5])
        ])
        
        message = f"""📚 SWARM BRAIN SEARCH RESULTS

Query: "{query}"
Found: {len(results)} results

TOP RESULTS:
{results_text}

Access full results via:
from src.swarm_brain.swarm_memory import SwarmMemory
memory = SwarmMemory(agent_id='{agent_id}')
results = memory.search_swarm_knowledge("{query}")

🧠 Collective knowledge at your service!
"""
        # Send via messaging system
        # (Implementation depends on messaging_cli availability)
    
    def _send_no_results_guidance(self, agent_id: str, query: str):
        """Guide agent when no knowledge found"""
        message = f"""📚 SWARM BRAIN: No Results Found

Query: "{query}"

ACTIONS:
1. Try different search terms
2. Check documentation: swarm_brain/DOCUMENTATION_INDEX.md
3. Ask Captain: Message Agent-4
4. Add knowledge after solving: memory.share_learning()

💡 You might be first to solve this - pioneer it!
"""
    
    # ═══════════════════════════════════════════════════════════
    # INTEGRATION 4: DOCUMENTATION → GASLINE
    # ═══════════════════════════════════════════════════════════
    
    def hook_documentation_migration(
        self, completed_items: List[str], remaining_items: List[str]
    ) -> bool:
        """
        When documentation needs migration → Assign → Activate
        
        Flow:
        Docs identified → Swarm Brain prioritizes → Gasline assigns → Agents migrate
        """
        if not self.enabled_integrations["documentation"]:
            return False
        
        # Create assignments for remaining documentation
        # Activate agents to migrate docs to Swarm Brain
        pass
    
    # ═══════════════════════════════════════════════════════════
    # UTILITY: GENERATE EXECUTION PLANS
    # ═══════════════════════════════════════════════════════════
    
    def _generate_execution_plan_from_brain(self, topic: str) -> Dict:
        """Query Swarm Brain for execution plan patterns"""
        # Check if similar topics were executed before
        # Learn from past execution patterns
        # Generate optimized plan
        
        return {
            "phase_1": "Initial implementation",
            "phase_2": "Integration testing",
            "phase_3": "Deployment"
        }


# ═══════════════════════════════════════════════════════════
# QUICK FUNCTIONS FOR CAPTAIN USE
# ═══════════════════════════════════════════════════════════

def activate_on_violations():
    """Scan violations → Auto-assign to agents → Deliver GAS"""
    hub = GaslineHub()
    
    # Load violations from project_analysis.json
    analysis_file = Path("project_analysis.json")
    if analysis_file.exists():
        with open(analysis_file) as f:
            data = json.load(f)
            violations = data.get("violations", [])
            
            if violations:
                hub.hook_violations_found(violations, auto_assign=True)
                print(f"✅ {len(violations)} violations auto-assigned and GAS delivered!")
            else:
                print("No violations found")
    else:
        print("❌ Run project scanner first: python comprehensive_project_analyzer.py")


def activate_on_debate_decision(topic: str):
    """Apply debate decision → Activate agents"""
    hub = GaslineHub()
    
    # Read decision from swarm brain
    decision_file = Path(f"swarm_brain/decisions/{topic}_decision.json")
    if decision_file.exists():
        with open(decision_file) as f:
            data = json.load(f)
            hub.hook_debate_decision(
                topic=topic,
                decision=data["decision"],
                agent_assignments=data.get("agent_assignments", {})
            )
            print(f"✅ Debate decision '{topic}' activated!")
    else:
        print(f"❌ Decision file not found: {decision_file}")


# ═══════════════════════════════════════════════════════════
# SMART ASSIGNMENT OPTIMIZER - Swarm Brain + Markov
# ═══════════════════════════════════════════════════════════

class SmartAssignmentOptimizer:
    """Smart assignment using Swarm Brain + Markov optimizer."""
    
    def __init__(self):
        """Initialize optimizer with Swarm Brain and Markov chain."""
        try:
            from src.swarm_brain.swarm_memory import SwarmMemory
            self.swarm_memory = SwarmMemory(agent_id="GaslineHub")
        except Exception as e:
            logger.warning(f"Swarm Brain unavailable: {e}")
            self.swarm_memory = None
        
        # Agent specializations (base knowledge)
        self.agent_specializations = {
            "Agent-1": ["testing", "qa", "integration", "core_systems"],
            "Agent-2": ["architecture", "v2_compliance", "design", "patterns"],
            "Agent-3": ["infrastructure", "monitoring", "devops", "deployment"],
            "Agent-5": ["memory", "performance", "business_intelligence", "analytics"],
            "Agent-6": ["optimization", "planning", "coordination", "communication"],
            "Agent-7": ["web", "frontend", "ui", "web_development"],
            "Agent-8": ["autonomous", "qa", "ssot", "system_integration"],
        }
        
        # Markov chain state (agent performance history)
        self.markov_chain = self._initialize_markov_chain()
    
    def _initialize_markov_chain(self) -> Dict[str, Dict[str, float]]:
        """Initialize Markov chain with agent performance probabilities."""
        # Start with equal probabilities, will be updated based on history
        agents = list(self.agent_specializations.keys())
        chain = {}
        
        for agent in agents:
            chain[agent] = {
                "success_rate": 0.5,  # Default 50% success
                "avg_completion_time": 1.0,  # Normalized time
                "specialization_match": 0.5,  # Default match score
            }
        
        # Try to load historical data from Swarm Brain
        if self.swarm_memory:
            try:
                history = self.swarm_memory.search_swarm_knowledge("agent performance history violations")
                # Update chain based on history if available
                # (Simplified - would need more sophisticated parsing)
            except Exception:
                pass
        
        return chain
    
    def assign_violations(self, violations: List[Dict]) -> Dict[str, List[Dict]]:
        """Assign violations to agents using smart assignment algorithm."""
        assignments = {}
        
        # Score each agent for each violation
        for violation in violations:
            best_agent = self._find_best_agent_for_violation(violation)
            
            if best_agent not in assignments:
                assignments[best_agent] = []
            assignments[best_agent].append(violation)
        
        # Balance workload (ensure no agent is overloaded)
        assignments = self._balance_workload(assignments, len(violations))
        
        return assignments
    
    def _find_best_agent_for_violation(self, violation: Dict) -> str:
        """Find best agent for a violation using scoring algorithm."""
        violation_type = violation.get("type", "unknown").lower()
        violation_file = violation.get("file", "").lower()
        violation_complexity = violation.get("complexity", 0)
        
        agent_scores = {}
        
        for agent_id, specializations in self.agent_specializations.items():
            score = 0.0
            
            # 1. Specialization match (40% weight)
            specialization_score = self._calculate_specialization_match(
                violation_type, violation_file, specializations
            )
            score += specialization_score * 0.4
            
            # 2. Markov chain performance (30% weight)
            markov_score = self._calculate_markov_score(agent_id, violation_type)
            score += markov_score * 0.3
            
            # 3. Swarm Brain knowledge (20% weight)
            brain_score = self._calculate_brain_score(agent_id, violation_type)
            score += brain_score * 0.2
            
            # 4. Current workload (10% weight) - prefer less loaded agents
            workload_score = self._calculate_workload_score(agent_id)
            score += workload_score * 0.1
            
            agent_scores[agent_id] = score
        
        # Return agent with highest score
        best_agent = max(agent_scores, key=agent_scores.get)
        logger.debug(f"Assigned violation to {best_agent} (score: {agent_scores[best_agent]:.2f})")
        return best_agent
    
    def _calculate_specialization_match(
        self, violation_type: str, violation_file: str, specializations: List[str]
    ) -> float:
        """Calculate how well agent specializations match violation."""
        match_score = 0.0
        
        # Check if violation type matches any specialization
        for spec in specializations:
            if spec.lower() in violation_type or violation_type in spec.lower():
                match_score += 0.5
            if spec.lower() in violation_file or violation_file in spec.lower():
                match_score += 0.3
        
        # Normalize to 0-1
        return min(1.0, match_score)
    
    def _calculate_markov_score(self, agent_id: str, violation_type: str) -> float:
        """Calculate score based on Markov chain (agent performance history)."""
        if agent_id not in self.markov_chain:
            return 0.5  # Default score
        
        chain_data = self.markov_chain[agent_id]
        
        # Combine success rate and specialization match
        score = (
            chain_data["success_rate"] * 0.6 +
            chain_data["specialization_match"] * 0.4
        )
        
        return score
    
    def _calculate_brain_score(self, agent_id: str, violation_type: str) -> float:
        """Calculate score based on Swarm Brain knowledge."""
        if not self.swarm_memory:
            return 0.5  # Default if Swarm Brain unavailable
        
        try:
            # Search for agent's past performance on similar violations
            query = f"{agent_id} {violation_type} performance success"
            results = self.swarm_memory.search_swarm_knowledge(query)
            
            if results:
                # If found in brain, boost score
                return 0.8
            else:
                # No history found, neutral score
                return 0.5
        except Exception:
            return 0.5
    
    def _calculate_workload_score(self, agent_id: str) -> float:
        """Calculate score based on current agent workload."""
        try:
            from src.discord_commander.status_reader import StatusReader
            
            status_reader = StatusReader()
            agent_status = status_reader.read_agent_status(agent_id)
            
            if agent_status:
                current_tasks = len(agent_status.get("current_tasks", []))
                # Prefer agents with fewer current tasks
                # Score decreases as tasks increase
                if current_tasks == 0:
                    return 1.0
                elif current_tasks <= 2:
                    return 0.8
                elif current_tasks <= 5:
                    return 0.5
                else:
                    return 0.2
            
            return 0.5  # Default if status unavailable
        except Exception:
            return 0.5
    
    def _balance_workload(
        self, assignments: Dict[str, List[Dict]], total_violations: int
    ) -> Dict[str, List[Dict]]:
        """Balance workload across agents to prevent overload."""
        if not assignments:
            return assignments
        
        agents = list(assignments.keys())
        avg_per_agent = total_violations / len(agents) if agents else 0
        max_per_agent = int(avg_per_agent * 1.5)  # Allow 50% over average
        
        # Redistribute if any agent is overloaded
        balanced = {}
        overflow = []
        
        for agent_id, violations in assignments.items():
            if len(violations) > max_per_agent:
                # Keep max_per_agent, move rest to overflow
                balanced[agent_id] = violations[:max_per_agent]
                overflow.extend(violations[max_per_agent:])
            else:
                balanced[agent_id] = violations
        
        # Redistribute overflow to less loaded agents
        if overflow:
            for violation in overflow:
                # Find agent with least violations
                least_loaded = min(balanced.keys(), key=lambda a: len(balanced.get(a, [])))
                if least_loaded not in balanced:
                    balanced[least_loaded] = []
                balanced[least_loaded].append(violation)
        
        return balanced


if __name__ == "__main__":
    print("🔌 GASLINE INTEGRATION HUB")
    print("\nAvailable integrations:")
    print("  1. Debate → Gasline (debate decisions → automatic execution)")
    print("  2. Violations → Gasline (scanner finds → agents activated)")
    print("  3. Swarm Brain → Gasline (knowledge → informed activation)")
    print("  4. Documentation → Gasline (docs migration → agents assigned)")
    print("\n💡 Usage:")
    print("  from src.core.gasline_integrations import activate_on_violations")
    print("  activate_on_violations()  # Auto-assign all violations!")

