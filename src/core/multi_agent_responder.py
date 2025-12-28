#!/usr/bin/env python3
"""
Multi-Agent Responder
======================

Handles inter-agent communication and coordination in the swarm system.

Purpose: Enable seamless agent-to-agent messaging and coordination
Author: Agent-2 (Architecture Specialist)
Created: 2025-12-01
Usage: Import and use MultiAgentResponder class for agent communication
"""
"""
Multi-Agent Responder - Response Collection & Combination

<!-- SSOT Domain: infrastructure -->

==========================================================

Collects responses from multiple agents and combines them into a single message.
Solves queue buildup problem: Instead of 7 messages, recipient gets 1 combined message.

Author: Agent-4 (Captain) - Autonomous Implementation
Date: 2025-11-27
Status: 🚀 ACTIVE - Powering Swarm Towards AGI
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ResponseStatus(Enum):
    """Status of response collection."""
    PENDING = "pending"
    COLLECTING = "collecting"
    COMPLETE = "complete"
    TIMEOUT = "timeout"
    PARTIAL = "partial"


@dataclass
class AgentResponse:
    """Individual agent response."""
    agent_id: str
    response: str
    timestamp: datetime
    received: bool = True


@dataclass
class ResponseCollector:
    """Collects responses from multiple agents."""
    collector_id: str
    request_id: str
    sender: str
    recipients: list[str]
    original_message: str
    timeout_seconds: int
    wait_for_all: bool
    created_at: datetime = field(default_factory=datetime.now)
    responses: dict[str, AgentResponse] = field(default_factory=dict)
    status: ResponseStatus = ResponseStatus.PENDING
    lock: threading.Lock = field(default_factory=threading.Lock)
    
    def add_response(self, agent_id: str, response: str) -> bool:
        """Add agent response to collector."""
        with self.lock:
            if agent_id not in self.recipients:
                logger.warning(f"Response from non-recipient {agent_id} ignored")
                return False
            
            if agent_id in self.responses:
                logger.info(f"Updating response from {agent_id}")
            
            self.responses[agent_id] = AgentResponse(
                agent_id=agent_id,
                response=response,
                timestamp=datetime.now()
            )
            
            # Update status
            if self.status == ResponseStatus.PENDING:
                self.status = ResponseStatus.COLLECTING
            
            # Check if complete
            if self._is_complete():
                self.status = ResponseStatus.COMPLETE
                logger.info(f"✅ Collector {self.collector_id} complete - all responses received")
                return True
            
            return False
    
    def _is_complete(self) -> bool:
        """Check if all responses received."""
        if self.wait_for_all:
            return len(self.responses) == len(self.recipients)
        else:
            # Complete if we have at least one response (for non-wait-for-all mode)
            return len(self.responses) > 0
    
    def is_timed_out(self) -> bool:
        """Check if collector has timed out."""
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.timeout_seconds
    
    def get_missing_agents(self) -> list[str]:
        """Get list of agents who haven't responded."""
        return [agent for agent in self.recipients if agent not in self.responses]
    
    def get_response_count(self) -> int:
        """Get number of responses received."""
        return len(self.responses)
    
    def get_total_expected(self) -> int:
        """Get total number of expected responses."""
        return len(self.recipients)


class MultiAgentResponder:
    """Coordinates multi-agent response collection and combination."""
    
    def __init__(self, storage_dir: str = "runtime/multi_agent_responses"):
        """Initialize multi-agent responder."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.collectors: dict[str, ResponseCollector] = {}
        self.lock = threading.Lock()
        self._timeout_checker_running = False
        self._start_timeout_checker()
    
    def _start_timeout_checker(self):
        """Start background thread to check for timeouts."""
        if self._timeout_checker_running:
            return
        
        self._timeout_checker_running = True
        
        def check_timeouts():
            while self._timeout_checker_running:
                try:
                    self._check_timeouts()
                    time.sleep(10)  # Check every 10 seconds
                except Exception as e:
                    logger.error(f"Error in timeout checker: {e}")
        
        thread = threading.Thread(target=check_timeouts, daemon=True)
        thread.start()
        logger.info("✅ Multi-Agent Responder timeout checker started")
    
    def _check_timeouts(self):
        """Check for timed-out collectors."""
        with self.lock:
            timed_out = []
            for collector_id, collector in self.collectors.items():
                if collector.is_timed_out() and collector.status not in [ResponseStatus.COMPLETE, ResponseStatus.TIMEOUT]:
                    collector.status = ResponseStatus.TIMEOUT
                    timed_out.append(collector_id)
                    logger.info(f"⏱️  Collector {collector_id} timed out")
            
            # Process timed-out collectors
            for collector_id in timed_out:
                self._finalize_collector(collector_id)
    
    def create_request(
        self,
        request_id: str,
        sender: str,
        recipients: list[str],
        content: str,
        timeout_seconds: int = 300,
        wait_for_all: bool = False
    ) -> str:
        """
        Create multi-agent request and return collector ID.
        
        Args:
            request_id: Unique request identifier
            sender: Original message sender
            recipients: List of agent IDs to respond
            content: Original message content
            timeout_seconds: Maximum time to wait for responses
            wait_for_all: If True, wait for all responses; if False, send when timeout
            
        Returns:
            Collector ID for tracking responses
        """
        collector_id = f"collector_{request_id}_{int(time.time())}"
        
        collector = ResponseCollector(
            collector_id=collector_id,
            request_id=request_id,
            sender=sender,
            recipients=recipients,
            original_message=content,
            timeout_seconds=timeout_seconds,
            wait_for_all=wait_for_all
        )
        
        with self.lock:
            self.collectors[collector_id] = collector
        
        logger.info(
            f"📋 Created multi-agent request {collector_id} "
            f"({len(recipients)} recipients, timeout: {timeout_seconds}s)"
        )
        
        return collector_id
    
    def submit_response(
        self,
        collector_id: str,
        agent_id: str,
        response: str
    ) -> bool:
        """
        Submit agent's response to collector.
        
        Args:
            collector_id: Collector ID from request
            agent_id: Agent who is responding
            response: Agent's response content
            
        Returns:
            True if collector is now complete, False otherwise
        """
        with self.lock:
            collector = self.collectors.get(collector_id)
            if not collector:
                logger.warning(f"Collector {collector_id} not found")
                return False
            
            if collector.status in [ResponseStatus.COMPLETE, ResponseStatus.TIMEOUT]:
                logger.warning(f"Collector {collector_id} already finalized")
                return False
        
        # Add response (outside lock to avoid deadlock)
        is_complete = collector.add_response(agent_id, response)
        
        if is_complete:
            self._finalize_collector(collector_id)
        
        return is_complete
    
    def _finalize_collector(self, collector_id: str):
        """Finalize collector and trigger combined message delivery."""
        with self.lock:
            collector = self.collectors.get(collector_id)
            if not collector:
                return
            
            if collector.status in [ResponseStatus.COMPLETE, ResponseStatus.TIMEOUT]:
                # Already finalized
                return
        
        # Generate combined response
        combined = self._combine_responses(collector)
        
        # Save to storage
        self._save_collector(collector, combined)
        
        # CRITICAL: Deliver combined message to original sender via message queue
        # This ensures the combined message routes through the queue (THE SPINE)
        try:
            from ..services.messaging_infrastructure import MessageCoordinator
            from ..core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
            
            # Deliver combined message to original sender
            delivery_result = MessageCoordinator.send_to_agent(
                agent=collector.sender,
                message=combined,
                priority=UnifiedMessagePriority.REGULAR,
                use_pyautogui=True,
                stalled=False
            )
            
            if isinstance(delivery_result, dict) and delivery_result.get("success"):
                logger.info(
                    f"✅ Combined message delivered to {collector.sender} "
                    f"(collector: {collector_id}, queue_id: {delivery_result.get('queue_id', 'unknown')})"
                )
            else:
                logger.warning(
                    f"⚠️ Failed to deliver combined message to {collector.sender} "
                    f"(collector: {collector_id})"
                )
        except Exception as e:
            logger.error(
                f"❌ Error delivering combined message for collector {collector_id}: {e}",
                exc_info=True
            )
        
        logger.info(
            f"✅ Collector {collector_id} finalized: "
            f"{collector.get_response_count()}/{collector.get_total_expected()} responses"
        )
    
    def _combine_responses(self, collector: ResponseCollector) -> str:
        """Combine all responses into single message."""
        lines = [
            f"# 🐝 Combined Response from {len(collector.responses)} Agent(s)",
            "",
            f"**Request**: {collector.original_message}",
            f"**Request ID**: {collector.request_id}",
            f"**Collector ID**: {collector.collector_id}",
            f"**Responses Received**: {collector.get_response_count()}/{collector.get_total_expected()}",
            f"**Status**: {collector.status.value.upper()}",
            f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            ""
        ]
        
        # Add each response
        for agent_id in collector.recipients:
            if agent_id in collector.responses:
                response = collector.responses[agent_id]
                lines.extend([
                    f"## {agent_id} Response",
                    "",
                    response.response,
                    "",
                    f"*Received at: {response.timestamp.strftime('%Y-%m-%d %H:%M:%S')}*",
                    "",
                    "---",
                    ""
                ])
            else:
                lines.extend([
                    f"## {agent_id} Response",
                    "",
                    "*No response received*",
                    "",
                    "---",
                    ""
                ])
        
        # Add summary
        missing = collector.get_missing_agents()
        if missing:
            lines.extend([
                "",
                f"**Missing Responses**: {', '.join(missing)}",
                ""
            ])
        
        lines.extend([
            f"**Combined at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "**WE. ARE. SWARM. ⚡🔥**"
        ])
        
        return "\n".join(lines)
    
    def get_combined_response(self, collector_id: str) -> Optional[str]:
        """Get combined response if collector is complete."""
        with self.lock:
            collector = self.collectors.get(collector_id)
            if not collector:
                return None
            
            if collector.status not in [ResponseStatus.COMPLETE, ResponseStatus.TIMEOUT]:
                return None
        
        return self._combine_responses(collector)
    
    def is_complete(self, collector_id: str) -> bool:
        """Check if collector is complete."""
        with self.lock:
            collector = self.collectors.get(collector_id)
            if not collector:
                return False
            
            return collector.status in [ResponseStatus.COMPLETE, ResponseStatus.TIMEOUT]
    
    def get_collector_status(self, collector_id: str) -> Optional[dict[str, Any]]:
        """Get status of collector."""
        with self.lock:
            collector = self.collectors.get(collector_id)
            if not collector:
                return None
        
        return {
            "collector_id": collector_id,
            "status": collector.status.value,
            "responses_received": collector.get_response_count(),
            "total_expected": collector.get_total_expected(),
            "missing_agents": collector.get_missing_agents(),
            "is_timed_out": collector.is_timed_out(),
            "created_at": collector.created_at.isoformat(),
            "elapsed_seconds": (datetime.now() - collector.created_at).total_seconds()
        }
    
    def _save_collector(self, collector: ResponseCollector, combined: str):
        """Save collector data to storage."""
        try:
            file_path = self.storage_dir / f"{collector.collector_id}.json"
            data = {
                "collector_id": collector.collector_id,
                "request_id": collector.request_id,
                "sender": collector.sender,
                "recipients": collector.recipients,
                "original_message": collector.original_message,
                "status": collector.status.value,
                "responses": {
                    agent_id: {
                        "response": resp.response,
                        "timestamp": resp.timestamp.isoformat()
                    }
                    for agent_id, resp in collector.responses.items()
                },
                "combined_response": combined,
                "created_at": collector.created_at.isoformat(),
                "finalized_at": datetime.now().isoformat()
            }
            
            import json
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to save collector {collector.collector_id}: {e}")


# Global instance
_responder_instance: Optional[MultiAgentResponder] = None


def get_multi_agent_responder() -> MultiAgentResponder:
    """Get global multi-agent responder instance."""
    global _responder_instance
    if _responder_instance is None:
        _responder_instance = MultiAgentResponder()
    return _responder_instance

