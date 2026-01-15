#!/usr/bin/env python3
"""
Debate → Swarm Brain → Gasline Integration
Connects democratic decisions to automatic execution

When debate concludes:
Decision stored → S2A debate-cycle messages generated → GAS delivery → Execution tracked

<!-- SSOT Domain: integration -->

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _find_project_root(start: Path) -> Path:
    """Stable-ish root detection across runtimes."""
    start = start.resolve()
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
        if (parent / "pyproject.toml").exists():
            return parent
    return start.parents[2] if len(start.parents) >= 3 else start


def _safe_import_messaging() -> Dict[str, Any]:
    """
    Soft import layer for messaging modules to survive path evolution.
    Returns a dict with Coordinator, UnifiedMessage, enums, and render_message.
    """
    out: Dict[str, Any] = {
        "Coordinator": None,
        "UnifiedMessage": None,
        "MessageCategory": None,
        "UnifiedMessagePriority": None,
        "UnifiedMessageType": None,
        "UnifiedMessageTag": None,
        "render_message": None,
    }

    try:
        from src.services.messaging_infrastructure import MessageCoordinator  # type: ignore
        out["Coordinator"] = MessageCoordinator
    except Exception:
        try:
            from src.services.messaging.message_coordinator import MessageCoordinator  # type: ignore
            out["Coordinator"] = MessageCoordinator
        except Exception:
            out["Coordinator"] = None

    try:
        from src.services.messaging.messaging_models import (  # type: ignore
            MessageCategory,
            UnifiedMessagePriority,
            UnifiedMessageType,
            UnifiedMessageTag,
            UnifiedMessage,
        )
        out.update(
            {
                "MessageCategory": MessageCategory,
                "UnifiedMessagePriority": UnifiedMessagePriority,
                "UnifiedMessageType": UnifiedMessageType,
                "UnifiedMessageTag": UnifiedMessageTag,
                "UnifiedMessage": UnifiedMessage,
            }
        )
    except Exception:
        try:
            from src.core.messaging_models_core import (  # type: ignore
                MessageCategory,
                UnifiedMessagePriority,
                UnifiedMessageType,
                UnifiedMessageTag,
                UnifiedMessage,
            )
            out.update(
                {
                    "MessageCategory": MessageCategory,
                    "UnifiedMessagePriority": UnifiedMessagePriority,
                    "UnifiedMessageType": UnifiedMessageType,
                    "UnifiedMessageTag": UnifiedMessageTag,
                    "UnifiedMessage": UnifiedMessage,
                }
            )
        except Exception:
            pass

    try:
        from src.services.messaging.messaging_template_dispatcher import render_message  # type: ignore
        out["render_message"] = render_message
    except Exception:
        try:
            from src.core.messaging_templates import render_message  # type: ignore
            out["render_message"] = render_message
        except Exception:
            out["render_message"] = None

    return out


class DebateToGasIntegration:
    """Integrates debate outcomes with S2A Debate Cycle + GAS delivery."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or _find_project_root(Path(__file__))
        self.proposals_dir = self.project_root / "swarm_proposals"
        self.brain_dir = self.project_root / "swarm_brain"
        self.workflow_dir = self.project_root / "workflow_states"

    def process_debate_decision(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str],
    ) -> bool:
        """Process debate decision and activate agents (Debate→Agent is S2A)."""
        try:
            self._store_in_swarm_brain(
                topic, decision, execution_plan, agent_assignments)
            payloads = self._generate_activation_payloads(
                topic, decision, execution_plan, agent_assignments)
            self._deliver_via_gasline(payloads)
            self._create_execution_tracker(
                topic, decision, execution_plan, agent_assignments)
            logger.info("✅ Debate decision activated via gasline")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to process debate decision: {e}")
            return False

    def _store_in_swarm_brain(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str],
    ) -> None:
        decision_record = {
            "timestamp": _utc_now(),
            "topic": topic,
            "decision": decision,
            "execution_plan": execution_plan,
            "agent_assignments": agent_assignments,
            "status": "activated",
        }
        decisions_file = self.brain_dir / \
            "decisions" / f"{topic}_decision.json"
        decisions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(decisions_file, "w", encoding="utf-8") as f:
            json.dump(decision_record, f, indent=2)
        logger.info(f"📚 Stored decision in Swarm Brain: {decisions_file}")

    def _generate_activation_payloads(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        payloads: List[Dict[str, Any]] = []
        for agent_id, task in agent_assignments.items():
            payloads.append(
                {
                    "agent_id": agent_id,
                    "priority": "urgent",
                    "topic": topic,
                    "decision": decision,
                    "task": task,
                    "rules": "Follow the debate decision and deliver an artifact.",
                    "deliverable": task,
                    "fallback": "If blocked, produce a blocker artifact and escalate to Captain.",
                    "execution_plan": execution_plan,
                }
            )
        return payloads

    def _deliver_via_gasline(self, payloads: List[Dict[str, Any]]) -> None:
        m = _safe_import_messaging()
        Coordinator = m["Coordinator"]
        UnifiedMessage = m["UnifiedMessage"]
        MessageCategory = m["MessageCategory"]
        UnifiedMessagePriority = m["UnifiedMessagePriority"]
        UnifiedMessageType = m["UnifiedMessageType"]
        UnifiedMessageTag = m["UnifiedMessageTag"]
        render_message = m["render_message"]

        for p in payloads:
            agent_id = p["agent_id"]
            topic = p.get("topic", "Debate Decision")
            decision = p.get("decision", "")
            task = p.get("task", "Execute assigned slice")
            rules = p.get(
                "rules", "Follow debate decision and deliver artifact.")
            deliverable = p.get("deliverable", task)
            fallback = p.get(
                "fallback", "If blocked, produce blocker artifact and escalate to Captain.")

            rendered: Optional[str] = None
            if Coordinator and UnifiedMessage and render_message and MessageCategory:
                try:
                    umsg = UnifiedMessage(
                        content=task,
                        sender="SYSTEM",
                        recipient=agent_id,
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT if UnifiedMessageType else None,
                        priority=UnifiedMessagePriority.URGENT if UnifiedMessagePriority else None,
                        tags=[UnifiedMessageTag.SYSTEM] if UnifiedMessageTag else [],
                        category=MessageCategory.S2A,
                    )
                    rendered = render_message(
                        umsg,
                        template_key="DEBATE_CYCLE",
                        topic=topic,
                        role="Assignee",
                        context=f"Debate decision: {decision}",
                        rules=rules,
                        deliverable=deliverable,
                        fallback=fallback,
                    )
                    try:
                        Coordinator.send_to_agent(
                            agent=agent_id,
                            message=rendered,
                            priority=UnifiedMessagePriority.URGENT if UnifiedMessagePriority else None,
                            use_pyautogui=True,
                            sender="SYSTEM",
                            message_category=MessageCategory.S2A,
                        )
                    except TypeError:
                        Coordinator.send_to_agent(
                            agent=agent_id, message=rendered)
                    logger.info(f"⚡ GAS delivered to {agent_id}")
                    continue
                except Exception as e:
                    logger.warning(
                        f"⚠️ GAS delivery failed for {agent_id}: {e}")

            try:
                inbox_dir = self.project_root / "agent_workspaces" / agent_id / "inbox"
                inbox_dir.mkdir(parents=True, exist_ok=True)
                msg_file = inbox_dir / \
                    f"S2A_DEBATE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(msg_file, "w", encoding="utf-8") as f:
                    f.write(rendered or task)
                logger.info(f"📥 Inbox message created for {agent_id}")
            except Exception as e:
                logger.error(f"❌ Failed inbox fallback for {agent_id}: {e}")

    def _create_execution_tracker(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str],
    ) -> None:
        tracker = {
            "topic": topic,
            "decision": decision,
            "execution_plan": execution_plan,
            "started": _utc_now(),
            "status": "assigned",
            "agents": {
                agent_id: {
                    "task": task,
                    "status": "assigned",
                    "started": None,
                    "completed": None,
                    "artifact_paths": [],
                }
                for agent_id, task in agent_assignments.items()
            },
        }
        tracker_file = self.workflow_dir / f"{topic}_execution.json"
        tracker_file.parent.mkdir(parents=True, exist_ok=True)
        with open(tracker_file, "w", encoding="utf-8") as f:
            json.dump(tracker, f, indent=2)
        logger.info(f"📊 Execution tracker created: {tracker_file}")


def activate_debate_decision(
    topic: str,
    decision: str,
    execution_plan: Dict,
    agent_assignments: Dict[str, str],
    *,
    project_root: Optional[Path] = None,
) -> bool:
    integrator = DebateToGasIntegration(project_root=project_root)
    return integrator.process_debate_decision(topic, decision, execution_plan, agent_assignments)


if __name__ == "__main__":
    result = activate_debate_decision(
        topic="orientation_system",
        decision="Integration approach - combine proposal variants",
        execution_plan={
            "immediate": "Build working orientation tool",
            "phase_1": "CLI tool for discovery",
            "phase_2": "Single-page reference guide",
            "phase_3": "GAS integration",
        },
        agent_assignments={
            "Agent-7": "Build tools/agent_orient.py - enhance existing tools approach",
            "Agent-2": "Create docs/AGENT_ORIENTATION.md - single-page reference",
            "Agent-4": "Integrate orientation into onboarding/gasline",
        },
    )
    print("✅ Debate decision activated" if result else "❌ Activation failed")
#!/usr/bin/env python3
"""
Debate → Swarm Brain → Gasline Integration
Connects democratic decisions to automatic execution

When debate concludes → Decision stored → Agents activated → Work happens
"""

logger = logging.getLogger(__name__)


class DebateToGasIntegration:
    """Integrates debate outcomes with gasline delivery for automatic execution"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.proposals_dir = self.project_root / "swarm_proposals"
        self.brain_dir = self.project_root / "swarm_brain"

    def process_debate_decision(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str]
    ) -> bool:
        """
        Process debate decision and activate agents

        Args:
            topic: Debate topic (e.g., 'orientation_system')
            decision: Final decision (e.g., 'Integration approach')
            execution_plan: What needs to be done
            agent_assignments: Which agent does what

        Returns:
            True if successful
        """
        try:
            # Step 1: Store in Swarm Brain
            self._store_in_swarm_brain(topic, decision, execution_plan)

            # Step 2: Generate activation messages
            messages = self._generate_activation_messages(
                topic, decision, execution_plan, agent_assignments
            )

            # Step 3: Deliver via gasline
            self._deliver_via_gasline(messages)

            # Step 4: Create execution tracking
            self._create_execution_tracker(topic, agent_assignments)

            logger.info(
                f"✅ Debate decision '{decision}' activated via gasline")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to process debate decision: {e}")
            return False

    def _store_in_swarm_brain(
        self, topic: str, decision: str, execution_plan: Dict
    ):
        """Store decision in swarm brain for collective knowledge"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "decision": decision,
            "execution_plan": execution_plan,
            "status": "activated"
        }

        # Store as knowledge entry
        decisions_file = self.brain_dir / \
            "decisions" / f"{topic}_decision.json"
        decisions_file.parent.mkdir(parents=True, exist_ok=True)

        with open(decisions_file, 'w') as f:
            json.dump(decision_record, f, indent=2)

        logger.info(f"📚 Stored decision in Swarm Brain: {decisions_file}")

    def _generate_activation_messages(
        self,
        topic: str,
        decision: str,
        execution_plan: Dict,
        agent_assignments: Dict[str, str]
    ) -> List[Dict]:
        """Generate activation messages for assigned agents"""
        messages = []

        for agent_id, task in agent_assignments.items():
            message = f"""🎯 DEBATE DECISION → ACTION!

Topic: {topic}
Decision: {decision}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR ASSIGNMENT ({agent_id}):
{task}

CONTEXT (From Swarm Brain):
- Collective decision: {decision}
- Your part: {task}
- Coordination: Check swarm_brain/decisions/{topic}_decision.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTION STEPS:
1. Review decision: cat swarm_brain/decisions/{topic}_decision.json
2. Check your inbox: agent_workspaces/{agent_id}/inbox/
3. Execute your part: {task}
4. Report completion: Update status.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐝 SWARM DECISION → IMMEDIATE ACTION!

BEGIN NOW!
"""

            messages.append({
                "agent_id": agent_id,
                "message": message,
                "priority": "urgent",
                "topic": topic,
                "decision": decision,
                "task": task,
                "rules": "Follow the debate decision and deliver an artifact.",
                "deliverable": task,
                "fallback": "If blocked, escalate to Captain with blocker and ETA.",
            })

        return messages

    def _deliver_via_gasline(self, messages: List[Dict]):
        """Deliver activation messages via gasline (PyAutoGUI) using S2A dispatcher."""
        try:
            from src.services.messaging_infrastructure import MessageCoordinator
            from src.core.messaging_models_core import (
                MessageCategory,
                UnifiedMessagePriority,
                UnifiedMessageType,
                UnifiedMessageTag,
            )
            from src.core.messaging_templates import render_message
            from src.core.messaging_models_core import UnifiedMessage
        except ImportError:
            MessageCoordinator = None

        for msg in messages:
            agent_id = msg["agent_id"]
            topic = msg.get("topic", "Debate Decision")
            decision = msg.get("decision", "")
            task = msg.get("task", msg.get(
                "message", "Execute assigned slice"))
            rules = msg.get(
                "rules", "Follow debate decision and deliver artifact.")
            deliverable = msg.get("deliverable", task)
            fallback = msg.get(
                "fallback", "If blocked, escalate to Captain with blocker and ETA.")

            rendered = None
            if MessageCoordinator:
                try:
                    umsg = UnifiedMessage(
                        content=task,
                        sender="SYSTEM",
                        recipient=agent_id,
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.URGENT,
                        tags=[UnifiedMessageTag.SYSTEM],
                        category=MessageCategory.S2A,
                    )
                    rendered = render_message(
                        umsg,
                        template_key="DEBATE_CYCLE",
                        topic=topic,
                        role="Assignee",
                        context=f"Debate decision: {decision}",
                        rules=rules,
                        deliverable=deliverable,
                        fallback=fallback,
                    )
                    MessageCoordinator.send_to_agent(
                        agent=agent_id,
                        message=rendered,
                        priority=UnifiedMessagePriority.URGENT,
                        use_pyautogui=True,
                        sender="SYSTEM",
                        message_category=MessageCategory.S2A,
                    )
                    logger.info(f"⚡ GAS delivered to {agent_id}")
                    continue
                except Exception as e:
                    logger.warning(
                        f"⚠️ Dispatcher delivery failed for {agent_id}: {e}")

            # Fallback: create inbox file with rendered or raw task
            try:
                inbox_dir = self.project_root / "agent_workspaces" / agent_id / "inbox"
                inbox_dir.mkdir(parents=True, exist_ok=True)
                msg_file = inbox_dir / \
                    f"DEBATE_DECISION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(msg_file, 'w', encoding='utf-8') as f:
                    if rendered:
                        f.write(rendered)
                    else:
                        f.write(task)
                logger.info(f"📥 Inbox message created for {agent_id}")
            except Exception as e:
                logger.error(
                    f"❌ Failed to deliver debate message to {agent_id}: {e}")

    def _create_execution_tracker(self, topic: str, agent_assignments: Dict):
        """Create execution tracking file"""
        tracker = {
            "topic": topic,
            "started": datetime.now().isoformat(),
            "agents": {
                agent_id: {
                    "task": task,
                    "status": "assigned",
                    "started": None,
                    "completed": None
                }
                for agent_id, task in agent_assignments.items()
            }
        }

        tracker_file = self.project_root / \
            "workflow_states" / f"{topic}_execution.json"
        tracker_file.parent.mkdir(parents=True, exist_ok=True)

        with open(tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2)

        logger.info(f"📊 Execution tracker created: {tracker_file}")


def activate_debate_decision(
    topic: str,
    decision: str,
    execution_plan: Dict,
    agent_assignments: Dict[str, str]
) -> bool:
    """
    Quick function to activate a debate decision

    Example:
        activate_debate_decision(
            topic="orientation_system",
            decision="Integration approach combining all 8 proposals",
            execution_plan={
                "phase_1": "Build orientation CLI tool",
                "phase_2": "Create single-page reference",
                "phase_3": "Integrate with gasline"
            },
            agent_assignments={
                "Agent-7": "Build tools/agent_orient.py CLI tool",
                "Agent-2": "Create docs/AGENT_ORIENTATION.md reference",
                "Agent-4": "Integrate with onboarding service"
            }
        )
    """
    integrator = DebateToGasIntegration()
    return integrator.process_debate_decision(
        topic, decision, execution_plan, agent_assignments
    )


if __name__ == "__main__":
    # Example: Activate orientation system decision
    result = activate_debate_decision(
        topic="orientation_system",
        decision="Integration approach - combine Agent-7's enhance existing + Agent-3's CLI + Agent-2's single-page",
        execution_plan={
            "immediate": "Build working orientation tool",
            "phase_1": "CLI tool for discovery",
            "phase_2": "Single-page reference guide",
            "phase_3": "GAS integration"
        },
        agent_assignments={
            "Agent-7": "Build tools/agent_orient.py - enhance existing tools approach",
            "Agent-2": "Create docs/AGENT_ORIENTATION.md - single-page reference",
            "Agent-4": "Integrate orientation into onboarding/gasline"
        }
    )

    if result:
        print("✅ Debate decision activated - agents receiving GAS now!")
    else:
        print("❌ Activation failed")
