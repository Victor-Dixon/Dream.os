#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->
Stress Test Runner - 9-Agent Simulation Engine
==============================================

Simulates 9 concurrent fake agents sending messages to stress test
the message queue system.

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

from __future__ import annotations

import logging
import random
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages for stress testing."""
    TEXT = "text"
    BROADCAST = "broadcast"
    SYSTEM = "system"
    URGENT = "urgent"


@dataclass
class AgentSimulator:
    """Simulates a single agent sending messages."""
    agent_id: str
    message_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_ms: float = 0.0
    last_activity: Optional[datetime] = None
    
    def record_send(self, success: bool, latency_ms: float) -> None:
        """Record a message send attempt."""
        self.message_count += 1
        self.last_activity = datetime.now()
        self.total_latency_ms += latency_ms
        
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "agent_id": self.agent_id,
            "message_count": self.message_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": (
                self.success_count / self.message_count * 100
                if self.message_count > 0 else 0.0
            ),
            "average_latency_ms": (
                self.total_latency_ms / self.message_count
                if self.message_count > 0 else 0.0
            ),
            "last_activity": (
                self.last_activity.isoformat()
                if self.last_activity else None
            ),
        }


class StressTestRunner:
    """
    Stress test runner that simulates 9 concurrent agents.
    
    Features:
    - 9 fake agents (Agent-1 through Agent-8, plus Agent-9)
    - 4 message types (text, broadcast, system, urgent)
    - Concurrent message sending
    - Configurable message rate
    - Statistics tracking
    """
    
    # Standard 8 agents plus one additional for stress testing
    AGENT_IDS = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8",
        "Agent-9"  # Additional agent for stress testing
    ]
    
    MESSAGE_TEMPLATES = {
        MessageType.TEXT: [
            "Testing message queue delivery",
            "Hello from {sender} to {recipient}",
            "Stress test message #{count}",
        ],
        MessageType.BROADCAST: [
            "Broadcast message to all agents",
            "System-wide announcement #{count}",
        ],
        MessageType.SYSTEM: [
            "System notification",
            "Queue status update",
        ],
        MessageType.URGENT: [
            "URGENT: Priority message",
            "High priority test message",
        ],
    }
    
    def __init__(
        self,
        delivery_callback: Any,
        duration_seconds: int = 60,
        messages_per_second: float = 10.0,
        message_types: Optional[List[MessageType]] = None,
    ):
        """Initialize stress test runner.
        
        Args:
            delivery_callback: Function to call for message delivery
            duration_seconds: Test duration in seconds
            messages_per_second: Target message rate
            message_types: Message types to use (defaults to all)
        """
        self.delivery_callback = delivery_callback
        self.duration_seconds = duration_seconds
        self.messages_per_second = messages_per_second
        self.message_types = message_types or list(MessageType)
        
        # Initialize agent simulators
        self.agents: Dict[str, AgentSimulator] = {
            agent_id: AgentSimulator(agent_id)
            for agent_id in self.AGENT_IDS
        }
        
        self.running = False
        self._lock = threading.Lock()
        self._threads: List[threading.Thread] = []
        
        # Test statistics
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_messages_sent = 0
        
    def start(self) -> None:
        """Start stress test."""
        if self.running:
            logger.warning("Stress test already running")
            return
        
        self.running = True
        self.start_time = datetime.now()
        logger.info(
            f"🚀 Starting stress test: {self.duration_seconds}s, "
            f"{self.messages_per_second} msg/s, {len(self.agents)} agents"
        )
        
        # Start agent threads
        for agent_id in self.AGENT_IDS:
            thread = threading.Thread(
                target=self._agent_worker,
                args=(agent_id,),
                daemon=True,
                name=f"StressAgent-{agent_id}"
            )
            thread.start()
            self._threads.append(thread)
        
        # Wait for duration
        time.sleep(self.duration_seconds)
        
        # Stop test
        self.stop()
    
    def stop(self) -> None:
        """Stop stress test."""
        if not self.running:
            return
        
        self.running = False
        self.end_time = datetime.now()
        logger.info("🛑 Stopping stress test...")
        
        # Wait for all threads to finish
        for thread in self._threads:
            thread.join(timeout=TimeoutConstants.HTTP_QUICK)
        
        logger.info("✅ Stress test stopped")
    
    def _agent_worker(self, agent_id: str) -> None:
        """Worker thread for a single agent.
        
        Args:
            agent_id: Agent identifier
        """
        agent = self.agents[agent_id]
        message_count = 0
        interval = 1.0 / self.messages_per_second
        
        while self.running:
            try:
                # Select random recipient (excluding self)
                recipients = [a for a in self.AGENT_IDS if a != agent_id]
                recipient = random.choice(recipients)
                
                # Select random message type
                message_type = random.choice(self.message_types)
                
                # Generate message content
                content = self._generate_message_content(
                    sender=agent_id,
                    recipient=recipient,
                    message_type=message_type,
                    count=message_count
                )
                
                # Send message
                start_time = time.time()
                success = self._send_message(
                    sender=agent_id,
                    recipient=recipient,
                    content=content,
                    message_type=message_type
                )
                latency_ms = (time.time() - start_time) * 1000
                
                # Record statistics
                agent.record_send(success, latency_ms)
                message_count += 1
                
                with self._lock:
                    self.total_messages_sent += 1
                
                # Wait for next message
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in agent worker {agent_id}: {e}")
                time.sleep(interval)
    
    def _generate_message_content(
        self,
        sender: str,
        recipient: str,
        message_type: MessageType,
        count: int
    ) -> str:
        """Generate message content.
        
        Args:
            sender: Sender agent ID
            recipient: Recipient agent ID
            message_type: Type of message
            count: Message count
            
        Returns:
            Message content string
        """
        templates = self.MESSAGE_TEMPLATES.get(message_type, ["Test message"])
        template = random.choice(templates)
        
        return template.format(
            sender=sender,
            recipient=recipient,
            count=count
        )
    
    def _send_message(
        self,
        sender: str,
        recipient: str,
        content: str,
        message_type: MessageType
    ) -> bool:
        """Send a message via delivery callback.
        
        Args:
            sender: Sender agent ID
            recipient: Recipient agent ID
            content: Message content
            message_type: Message type
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Call delivery callback with message data
            if callable(self.delivery_callback):
                return self.delivery_callback(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    message_type=message_type.value,
                )
            else:
                # Assume it's a send_message method
                return self.delivery_callback.send_message(
                    content=content,
                    sender=sender,
                    recipient=recipient,
                )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get stress test statistics.
        
        Returns:
            Dictionary with test statistics
        """
        with self._lock:
            elapsed_seconds = (
                (self.end_time - self.start_time).total_seconds()
                if self.start_time and self.end_time
                else 0.0
            )
            
            total_success = sum(a.success_count for a in self.agents.values())
            total_failure = sum(a.failure_count for a in self.agents.values())
            total_messages = sum(a.message_count for a in self.agents.values())
            
            return {
                "test_duration_seconds": elapsed_seconds,
                "total_messages_sent": total_messages,
                "total_successful": total_success,
                "total_failed": total_failure,
                "overall_success_rate": (
                    total_success / total_messages * 100
                    if total_messages > 0 else 0.0
                ),
                "messages_per_second": (
                    total_messages / elapsed_seconds
                    if elapsed_seconds > 0 else 0.0
                ),
                "agent_stats": [
                    agent.get_stats() for agent in self.agents.values()
                ],
                "start_time": (
                    self.start_time.isoformat()
                    if self.start_time else None
                ),
                "end_time": (
                    self.end_time.isoformat()
                    if self.end_time else None
                ),
            }

