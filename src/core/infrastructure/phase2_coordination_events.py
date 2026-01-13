#!/usr/bin/env python3
"""
Phase 2 Coordination Events - Event-Driven Swarm Coordination
=============================================================

Event-driven coordination framework for Phase 2 code audit execution.
Uses the completed event infrastructure to track progress, coordinate agents,
and provide real-time swarm visibility.

<!-- SSOT Domain: phase2_coordination -->

Features:
- Phase 2 progress tracking via events
- Agent coordination and status updates
- Real-time swarm visibility
- Event-driven validation and QA coordination

Author: Agent-2 (Architecture & Design Specialist)
Date: 2026-01-12
Phase: Phase 2 - Code Audit Execution
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .event_models import Event, create_event
from .event_bus import get_event_bus
from ..discord_commander.discord_event_bridge import get_discord_event_bridge

logger = logging.getLogger(__name__)


class Phase2CoordinationEvents:
    """
    Event-driven coordination framework for Phase 2 execution.

    Provides real-time coordination, progress tracking, and swarm visibility
    for the Phase 2 code audit and consolidation work.
    """

    def __init__(self):
        """
        Initialize Phase 2 coordination events.
        """
        self.event_bus = get_event_bus()
        self.discord_bridge = get_discord_event_bridge()
        self.active_coordinations = {}

    async def initialize_phase2_coordination(self):
        """
        Initialize Phase 2 coordination framework.
        """
        try:
            # Initialize event bus if needed
            await self.event_bus.initialize()

            # Register Phase 2 event subscriptions
            await self._register_phase2_subscriptions()

            logger.info("Phase 2 coordination events initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Phase 2 coordination: {e}")
            raise

    async def _register_phase2_subscriptions(self):
        """
        Register event subscriptions for Phase 2 coordination.
        """
        subscriptions = [
            ("phase2:progress:*", self._handle_progress_update),
            ("phase2:coordination:*", self._handle_coordination_event),
            ("phase2:validation:*", self._handle_validation_event),
            ("phase2:completion:*", self._handle_completion_event),
        ]

        for event_pattern, handler in subscriptions:
            subscription = await self.event_bus.subscribe_to_events({
                'subscription_id': f"phase2_coordination_{event_pattern.replace(':', '_').replace('*', 'all')}_{datetime.now().isoformat()}",
                'event_patterns': [event_pattern],
                'callback': handler
            })
            self.active_coordinations[event_pattern] = subscription

        logger.info(f"Registered {len(subscriptions)} Phase 2 coordination subscriptions")

    async def publish_phase2_progress(self,
                                    agent_id: str,
                                    task: str,
                                    progress: float,
                                    status: str = "in_progress",
                                    details: Optional[Dict[str, Any]] = None) -> str:
        """
        Publish Phase 2 progress update for an agent.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            task: Task description
            progress: Progress percentage (0.0 to 1.0)
            status: Status string
            details: Additional progress details

        Returns:
            Event ID
        """
        progress_data = {
            'agent_id': agent_id,
            'task': task,
            'progress': progress,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'phase': 'phase2'
        }

        if details:
            progress_data.update(details)

        event = create_event(
            event_type="phase2:progress:update",
            source_service="phase2_coordinator",
            data=progress_data
        )

        event_id = await self.event_bus.publish_event(event)
        logger.info(f"Published Phase 2 progress for {agent_id}: {progress:.1%} complete")
        return event_id

    async def coordinate_agents(self,
                              coordinating_agent: str,
                              target_agents: List[str],
                              action: str,
                              details: Optional[Dict[str, Any]] = None) -> str:
        """
        Coordinate action between agents for Phase 2.

        Args:
            coordinating_agent: Agent initiating coordination
            target_agents: List of target agent IDs
            action: Coordination action
            details: Coordination details

        Returns:
            Event ID
        """
        coordination_data = {
            'coordinating_agent': coordinating_agent,
            'target_agents': target_agents,
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'phase': 'phase2'
        }

        if details:
            coordination_data.update(details)

        event = create_event(
            event_type="phase2:coordination:request",
            source_service="phase2_coordinator",
            data=coordination_data
        )

        event_id = await self.event_bus.publish_event(event)
        logger.info(f"Coordinated {action} from {coordinating_agent} to {len(target_agents)} agents")
        return event_id

    async def publish_validation_result(self,
                                      agent_id: str,
                                      validation_type: str,
                                      result: str,
                                      details: Optional[Dict[str, Any]] = None) -> str:
        """
        Publish Phase 2 validation result.

        Args:
            agent_id: Agent performing validation
            validation_type: Type of validation
            result: Validation result ("pass", "fail", "warning")
            details: Validation details

        Returns:
            Event ID
        """
        validation_data = {
            'agent_id': agent_id,
            'validation_type': validation_type,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'phase': 'phase2'
        }

        if details:
            validation_data.update(details)

        event = create_event(
            event_type="phase2:validation:result",
            source_service="phase2_validator",
            data=validation_data
        )

        event_id = await self.event_bus.publish_event(event)
        logger.info(f"Published Phase 2 validation result: {validation_type} - {result}")
        return event_id

    async def publish_completion(self,
                               agent_id: str,
                               task: str,
                               success: bool = True,
                               details: Optional[Dict[str, Any]] = None) -> str:
        """
        Publish Phase 2 task completion.

        Args:
            agent_id: Agent completing task
            task: Completed task
            success: Whether completion was successful
            details: Completion details

        Returns:
            Event ID
        """
        completion_data = {
            'agent_id': agent_id,
            'task': task,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'phase': 'phase2'
        }

        if details:
            completion_data.update(details)

        event_type = "phase2:completion:success" if success else "phase2:completion:failure"

        event = create_event(
            event_type=event_type,
            source_service="phase2_completion_tracker",
            data=completion_data
        )

        event_id = await self.event_bus.publish_event(event)
        status = "successful" if success else "failed"
        logger.info(f"Published Phase 2 completion: {agent_id} {task} - {status}")
        return event_id

    async def _handle_progress_update(self, event: Event):
        """
        Handle Phase 2 progress update events.
        """
        data = event.data

        # Publish to Discord for swarm visibility
        progress_msg = f"📊 **Phase 2 Progress**: {data['agent_id']} - {data['task']}\n"
        progress_msg += f"• Progress: {data['progress']:.1%}\n"
        progress_msg += f"• Status: {data['status']}\n"
        progress_msg += f"• Timestamp: {data['timestamp'][:19]}"

        await self.discord_bridge.publish_system_event(
            event_type="phase2_progress",
            event_data={'message': progress_msg}
        )

    async def _handle_coordination_event(self, event: Event):
        """
        Handle Phase 2 coordination events.
        """
        data = event.data

        # Publish coordination notice to Discord
        coord_msg = f"🤝 **Phase 2 Coordination**: {data['coordinating_agent']} → {', '.join(data['target_agents'])}\n"
        coord_msg += f"• Action: {data['action']}\n"
        coord_msg += f"• Timestamp: {data['timestamp'][:19]}"

        await self.discord_bridge.publish_system_event(
            event_type="phase2_coordination",
            event_data={'message': coord_msg}
        )

    async def _handle_validation_event(self, event: Event):
        """
        Handle Phase 2 validation events.
        """
        data = event.data

        # Publish validation result to Discord
        status_emoji = "✅" if data['result'] == "pass" else "❌" if data['result'] == "fail" else "⚠️"
        validation_msg = f"{status_emoji} **Phase 2 Validation**: {data['agent_id']} - {data['validation_type']}\n"
        validation_msg += f"• Result: {data['result']}\n"
        validation_msg += f"• Timestamp: {data['timestamp'][:19]}"

        await self.discord_bridge.publish_system_event(
            event_type="phase2_validation",
            event_data={'message': validation_msg}
        )

    async def _handle_completion_event(self, event: Event):
        """
        Handle Phase 2 completion events.
        """
        data = event.data

        # Publish completion notice to Discord
        status_emoji = "🎉" if data.get('success', True) else "⚠️"
        completion_msg = f"{status_emoji} **Phase 2 Completion**: {data['agent_id']}\n"
        completion_msg += f"• Task: {data['task']}\n"
        completion_msg += f"• Status: {'Success' if data.get('success', True) else 'Failed'}\n"
        completion_msg += f"• Timestamp: {data['timestamp'][:19]}"

        await self.discord_bridge.publish_system_event(
            event_type="phase2_completion",
            event_data={'message': completion_msg}
        )

    async def get_phase2_status(self) -> Dict[str, Any]:
        """
        Get current Phase 2 coordination status.

        Returns:
            Status information
        """
        # Get event bus metrics
        metrics = self.event_bus.metrics.get_metrics()

        # Count Phase 2 events
        phase2_events = sum(1 for event_type in metrics.get('events_by_type', {})
                           if event_type.startswith('phase2:'))

        return {
            'phase2_events_total': phase2_events,
            'active_coordinations': len(self.active_coordinations),
            'event_bus_healthy': self.event_bus is not None,
            'discord_bridge_active': self.discord_bridge is not None,
            'timestamp': datetime.now().isoformat()
        }

    async def shutdown_coordination(self):
        """
        Shutdown Phase 2 coordination framework.
        """
        for subscription_id in self.active_coordinations.values():
            try:
                await self.event_bus.unsubscribe(subscription_id)
            except Exception as e:
                logger.error(f"Error removing subscription {subscription_id}: {e}")

        self.active_coordinations.clear()
        logger.info("Phase 2 coordination framework shutdown")


# Global Phase 2 coordination instance
_phase2_coordination = None


def get_phase2_coordination() -> Phase2CoordinationEvents:
    """
    Get the global Phase 2 coordination instance.

    Returns:
        Phase2CoordinationEvents instance
    """
    global _phase2_coordination
    if _phase2_coordination is None:
        _phase2_coordination = Phase2CoordinationEvents()
    return _phase2_coordination


async def initialize_phase2_coordination():
    """
    Initialize the global Phase 2 coordination framework.

    Returns:
        Initialized Phase2CoordinationEvents
    """
    coordination = get_phase2_coordination()
    await coordination.initialize_phase2_coordination()
    return coordination


async def shutdown_phase2_coordination():
    """Shutdown the global Phase 2 coordination framework."""
    global _phase2_coordination
    if _phase2_coordination:
        await _phase2_coordination.shutdown_coordination()
        _phase2_coordination = None