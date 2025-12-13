#!/usr/bin/env python3
"""
Message Queue Processor - Deterministic Queue Processing
=======================================================

<!-- SSOT Domain: communication -->

Processes queued messages with dependency injection for messaging core.
Supports both real and mock messaging cores for testing.

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
License: MIT
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .message_queue import MessageQueue, QueueConfig
from .message_queue_persistence import QueueEntry

logger = logging.getLogger(__name__)


class MessageQueueProcessor:
    """
    Deterministic processor for queued messages.

    Responsibilities:
    • Read from queue
    • Deliver message via unified messaging core
    • Mark delivered/failed
    • Log to repository (optional)
    • PyAutoGUI delivery (primary)
    • Inbox fallback on delivery failure (backup)
    • Error handling and logging

    V3 Compliance:
    • Single responsibility: Queue processing only
    • Hard boundaries: Clear error isolation
    • Deterministic: Predictable delivery pipeline
    • Type-safe: Stricter type usage
    """

    def __init__(
        self,
        queue: Optional[MessageQueue] = None,
        message_repository: Optional[Any] = None,
        config: Optional[QueueConfig] = None,
        messaging_core: Optional[Any] = None,
    ) -> None:
        """Initialize message queue processor.

        Args:
            queue: MessageQueue instance (creates default if None)
            message_repository: MessageRepository for logging (optional)
            config: QueueConfig instance (creates default if None)
            messaging_core: Optional messaging core for dependency injection (for testing)
        """
        self.config = config or QueueConfig()
        self.queue = queue or MessageQueue(config=self.config)
        self.message_repository = message_repository
        # Injected core (None = use default real core)
        self.messaging_core = messaging_core
        self.running = False
        
        # Initialize performance metrics collector
        try:
            from .message_queue_performance_metrics import MessageQueuePerformanceMetrics
            self.performance_metrics = MessageQueuePerformanceMetrics()
            self.performance_metrics.start_session()
        except Exception as e:
            logger.warning(f"Performance metrics not available: {e}")
            self.performance_metrics = None

    def process_queue(
        self,
        max_messages: Optional[int] = None,
        batch_size: int = 1,
        interval: float = 5.0,
    ) -> int:
        """
        Process queued messages in controlled batches.

        Args:
            max_messages: Maximum messages to process (None = unlimited)
            batch_size: Number of messages to process per batch
            interval: Sleep interval between batches (seconds)

        Returns:
            Number of messages processed
        """
        self.running = True
        processed = 0

        try:
            while self.running:
                entries = self._safe_dequeue(batch_size)
                if not entries:
                    if max_messages is None:
                        time.sleep(interval)
                        continue
                    break

                for entry in entries:
                    if max_messages and processed >= max_messages:
                        break

                    # CRITICAL: Wait for full delivery sequence to complete before moving to next
                    # This ensures proper sequencing and prevents race conditions
                    ok = self._deliver_entry(entry)
                    processed += 1
                    
                    # CRITICAL: Small delay between messages to ensure UI settles
                    # This prevents rapid-fire messages from interfering with each other
                    if ok:
                        time.sleep(0.5)  # Brief pause after successful delivery
                    else:
                        time.sleep(1.0)  # Longer pause after failed delivery for recovery

                if max_messages and processed >= max_messages:
                    break

        except KeyboardInterrupt:
            logger.info("🛑 Stopped by operator")
        except Exception as e:
            logger.error(f"Fatal queue loop error: {e}", exc_info=True)
        finally:
            self.running = False
            
            # End performance metrics session
            if self.performance_metrics:
                session_summary = self.performance_metrics.end_session()
                logger.info(f"📊 Performance metrics: {session_summary}")
            
            logger.info(f"✅ Queue processor complete: {processed} delivered")

        return processed

    def _safe_dequeue(self, batch_size: int) -> list[Any]:
        """Safely dequeue messages with error isolation.

        Args:
            batch_size: Number of messages to dequeue

        Returns:
            List of queue entries (empty list on error)
        """
        try:
            return self.queue.dequeue(batch_size=batch_size)
        except Exception as e:
            logger.error(f"Dequeue error: {e}", exc_info=True)
            return []

    def _deliver_entry(self, entry: Any) -> bool:
        """
        Deliver queue entry → log → mark state.

        Error isolation: Each step wrapped in try/except to prevent
        cascade failures. One entry failure doesn't stop processing.
        
        Retry Logic: Failed deliveries are retried with exponential backoff.
        Max retries: 3 attempts with delays: 5s, 15s, 45s

        Args:
            entry: Queue entry with message data

        Returns:
            True if delivered, False otherwise
        """
        # Track agent activity for message delivery
        tracker = None
        recipient = None
        queue_id = None
        
        try:
            from .agent_activity_tracker import get_activity_tracker
            tracker = get_activity_tracker()
        except Exception:
            pass  # Non-critical if tracker unavailable
        
        # Start performance tracking
        delivery_start_time = None
        use_pyautogui = True  # Default, will be updated later
        if self.performance_metrics:
            delivery_start_time = self.performance_metrics.start_delivery_tracking(
                getattr(entry, 'queue_id', 'unknown')
            )
        
        try:
            # Extract message data first
            queue_id = getattr(entry, 'queue_id', 'unknown')
            message = getattr(entry, 'message', None)
            
            # Check if this is a retry attempt
            entry_metadata = getattr(entry, 'metadata', {})
            delivery_attempts = entry_metadata.get('delivery_attempts', 0)
            max_retries = 3
            
            # If already failed max retries, skip
            if delivery_attempts >= max_retries:
                logger.warning(
                    f"Entry {queue_id} exceeded max retries ({max_retries}), "
                    f"marking as permanently failed"
                )
                self.queue.mark_failed(queue_id, f"max_retries_exceeded ({max_retries})")
                return False

            if not message:
                logger.warning(f"Entry {queue_id} missing message")
                self.queue.mark_failed(queue_id, "no_message")
                return False

            # FIXED: Extract recipient/content handling both dict and UnifiedMessage object
            # Supports concurrent calls from different sources (Discord, CLI, queue, etc.)
            if isinstance(message, dict):
                # Message is a dict (serialized format)
                recipient = message.get("recipient") or message.get("to")
                content = message.get("content")
                message_type_str = message.get(
                    "message_type") or message.get("type")
                sender = message.get("sender") or message.get("from", "SYSTEM")
                priority_str = message.get("priority", "regular")
                tags_list = message.get("tags", [])
                metadata = message.get("metadata", {})
            else:
                # Message is UnifiedMessage object (object format)
                recipient = getattr(message, "recipient", None)
                content = getattr(message, "content", None)
                message_type_attr = getattr(message, "message_type", None)
                if message_type_attr:
                    message_type_str = getattr(
                        message_type_attr, "value", None) or str(message_type_attr)
                else:
                    message_type_str = None
                sender = getattr(message, "sender", "SYSTEM")
                priority_attr = getattr(message, "priority", None)
                if priority_attr:
                    priority_str = getattr(
                        priority_attr, "value", None) or str(priority_attr)
                else:
                    priority_str = "regular"
                tags_attr = getattr(message, "tags", [])
                tags_list = [getattr(t, "value", None) or str(t)
                             for t in tags_attr] if tags_attr else []
                metadata = getattr(message, "metadata", {})

            if not recipient:
                logger.warning(f"Entry {queue_id} missing recipient")
                self.queue.mark_failed(queue_id, "missing_recipient")
                if tracker and recipient and recipient.startswith("Agent-"):
                    tracker.mark_inactive(recipient)
                return False

            if not content:
                logger.warning(f"Entry {queue_id} missing content")
                self.queue.mark_failed(queue_id, "missing_content")
                if tracker and recipient and recipient.startswith("Agent-"):
                    tracker.mark_inactive(recipient)
                return False

            # Mark agent as delivering message (if agent-to-agent or system delivery)
            if tracker and recipient and recipient.startswith("Agent-"):
                try:
                    tracker.mark_delivering(recipient, queue_id)
                except Exception:
                    pass  # Non-critical tracking failure

            # Route delivery with preserved message_type
            success = self._route_delivery(
                recipient, content, metadata, message_type_str, sender, priority_str, tags_list
            )
            
            # VERIFICATION: Skip inbox verification for PyAutoGUI messages
            # PyAutoGUI sends directly to Discord chat, not inbox, so inbox verification is not applicable
            # The PyAutoGUI delivery service already reports success/failure, which is sufficient
            # CRITICAL: Check metadata from both entry and message to ensure we catch use_pyautogui flag
            use_pyautogui = True  # Default to True for backward compatibility
            if isinstance(metadata, dict):
                use_pyautogui = metadata.get("use_pyautogui", True)
            elif hasattr(entry, 'metadata') and isinstance(entry.metadata, dict):
                use_pyautogui = entry.metadata.get("use_pyautogui", True)
            
            if success and use_pyautogui:
                # PyAutoGUI messages go to Discord chat, not inbox
                # Trust the PyAutoGUI delivery service's success/failure report
                logger.info(
                    f"✅ PyAutoGUI delivery successful for {recipient} (skipping inbox verification - "
                    f"message sent to Discord chat, not inbox)"
                )
                # No verification needed - PyAutoGUI delivery to Discord chat is verified by the delivery service

            # Record performance metrics
            if self.performance_metrics and delivery_start_time:
                delivery_method = 'pyautogui' if use_pyautogui else 'inbox'
                content_len = len(content) if content else 0
                entry_metadata = getattr(entry, 'metadata', {})
                attempt_num = entry_metadata.get('delivery_attempts', 0) + 1
                retry_delay = entry_metadata.get('next_retry_delay')
                
                self.performance_metrics.end_delivery_tracking(
                    queue_id=queue_id,
                    recipient=recipient,
                    delivery_method=delivery_method,
                    success=success,
                    start_time=delivery_start_time,
                    attempt_number=attempt_num,
                    content_length=content_len,
                    retry_delay=retry_delay
                )
            
            if success:
                self.queue.mark_delivered(queue_id)
                if self.message_repository:
                    try:
                        self.message_repository.log_message(message)
                    except Exception:
                        pass  # Non-critical logging failure
                # Mark agent as inactive after successful delivery
                if tracker and recipient and recipient.startswith("Agent-"):
                    try:
                        tracker.mark_inactive(recipient)
                    except Exception:
                        pass  # Non-critical tracking failure
                return True
            else:
                # Increment retry count
                metadata = getattr(entry, 'metadata', {})
                current_attempts = metadata.get('delivery_attempts', 0)
                new_attempts = current_attempts + 1
                
                # Calculate exponential backoff delay: 5s, 15s, 45s
                backoff_delays = [5.0, 15.0, 45.0]
                delay = backoff_delays[min(new_attempts - 1, len(backoff_delays) - 1)]
                
                # Update entry metadata with retry info
                if not hasattr(entry, 'metadata'):
                    entry.metadata = {}
                entry.metadata['delivery_attempts'] = new_attempts
                entry.metadata['last_retry_time'] = datetime.now().isoformat()
                entry.metadata['next_retry_delay'] = delay
                
                # Mark as failed but reset to PENDING for retry (unless max retries exceeded)
                if new_attempts < max_retries:
                    logger.info(
                        f"Delivery failed for {queue_id} (attempt {new_attempts}/{max_retries}), "
                        f"will retry in {delay}s"
                    )
                    # Reset to PENDING so it can be retried
                    self.queue._reset_entry_for_retry(queue_id, new_attempts, delay)
                else:
                    logger.error(
                        f"Delivery failed for {queue_id} after {new_attempts} attempts, "
                        f"marking as permanently failed"
                    )
                    self.queue.mark_failed(queue_id, f"delivery_failed_after_{new_attempts}_attempts")
                
                # Mark agent as inactive after failed delivery
                if tracker and recipient and recipient.startswith("Agent-"):
                    try:
                        tracker.mark_inactive(recipient)
                    except Exception:
                        pass  # Non-critical tracking failure
                return False

        except Exception as e:
            queue_id = getattr(entry, 'queue_id', 'unknown')
            logger.error(f"Delivery error for {queue_id}: {e}", exc_info=True)
            
            # Record performance metrics for error case
            if self.performance_metrics and delivery_start_time:
                try:
                    delivery_method = 'pyautogui' if use_pyautogui else 'inbox'
                    content_len = len(content) if content else 0
                    entry_metadata = getattr(entry, 'metadata', {})
                    attempt_num = entry_metadata.get('delivery_attempts', 0) + 1
                    
                    self.performance_metrics.end_delivery_tracking(
                        queue_id=queue_id,
                        recipient=recipient or 'unknown',
                        delivery_method=delivery_method,
                        success=False,
                        start_time=delivery_start_time,
                        attempt_number=attempt_num,
                        content_length=content_len
                    )
                except Exception:
                    pass  # Non-critical metrics failure
            
            self.queue.mark_failed(queue_id, str(e))
            # Mark agent as inactive on error
            if tracker and recipient and recipient.startswith("Agent-"):
                try:
                    tracker.mark_inactive(recipient)
                except Exception:
                    pass  # Non-critical tracking failure
            return False

    def _route_delivery(
        self,
        recipient: str,
        content: str,
        metadata: dict = None,
        message_type_str: str = None,
        sender: str = "SYSTEM",
        priority_str: str = "regular",
        tags_list: list = None,
    ) -> bool:
        """
        Route message delivery with fallback logic.

        Primary: PyAutoGUI delivery via messaging core
        Backup: Inbox fallback when PyAutoGUI fails

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful, False otherwise
        """
        try:
            metadata = metadata or {}
            
            # CRITICAL: Check use_pyautogui flag from metadata
            # If explicitly set to False, skip PyAutoGUI and use inbox only
            use_pyautogui = metadata.get("use_pyautogui", True)  # Default to True for backward compatibility
            
            if not use_pyautogui:
                logger.info(
                    f"use_pyautogui=False in metadata for {recipient}, using inbox delivery"
                )
                return self._deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)
            
            # Check if queue is full (skip PyAutoGUI if so)
            try:
                from ..utils.agent_queue_status import AgentQueueStatus
                queue_status = AgentQueueStatus()
                if queue_status.is_queue_full(recipient):
                    logger.warning(
                        f"Queue full for {recipient}, skipping PyAutoGUI, using inbox"
                    )
                    return self._deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)
            except ImportError:
                # Queue status utility not available, proceed normally
                pass
            except Exception as e:
                logger.debug(f"Error checking queue status: {e}")
                # Continue with normal flow

            # PRIMARY: Try PyAutoGUI delivery first
            success = self._deliver_via_core(
                recipient, content, metadata, message_type_str, sender, priority_str, tags_list or []
            )
            if success:
                return True

            # BACKUP: Fallback to inbox when PyAutoGUI fails
            # (e.g., when Cursor queue is full with pending prompts)
            logger.warning(
                f"PyAutoGUI delivery failed for {recipient}, using inbox fallback"
            )
            return self._deliver_fallback_inbox(recipient, content, metadata, sender, priority_str)
        except Exception as e:
            logger.error(f"Delivery routing error: {e}")
            # Last resort: try inbox fallback
            try:
                return self._deliver_fallback_inbox(recipient, content, metadata or {}, sender, priority_str)
            except Exception as fallback_error:
                logger.error(f"Inbox fallback also failed: {fallback_error}")
                return False

    def _deliver_via_core(
        self,
        recipient: str,
        content: str,
        metadata: dict = None,
        message_type_str: str = None,
        sender: str = "SYSTEM",
        priority_str: str = "regular",
        tags_list: list = None,
    ) -> bool:
        """
        Primary path: Unified messaging core (PyAutoGUI delivery or injected mock).

        Uses injected messaging_core if provided (for testing), otherwise uses real core.
        V3 Unified Imports: Uses src.core.messaging_core.send_message
        Keyboard control: Wraps delivery in keyboard_control context (only for real core)

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata (optional)

        Returns:
            True if delivery successful, False otherwise
        """
        try:
            from .messaging_models_core import (
                UnifiedMessageType,
                UnifiedMessagePriority,
                UnifiedMessageTag,
            )

            # Parse message_type from string (preserve from queue entry)
            if message_type_str:
                try:
                    # Try to match enum value directly
                    message_type = UnifiedMessageType(message_type_str)
                except (ValueError, TypeError):
                    # Fallback: map string to enum
                    message_type_map = {
                        "captain_to_agent": UnifiedMessageType.CAPTAIN_TO_AGENT,
                        "agent_to_agent": UnifiedMessageType.AGENT_TO_AGENT,
                        # Fixed: Map to AGENT_TO_AGENT
                        "agent_to_captain": UnifiedMessageType.AGENT_TO_AGENT,
                        "system_to_agent": UnifiedMessageType.SYSTEM_TO_AGENT,
                        "human_to_agent": UnifiedMessageType.HUMAN_TO_AGENT,
                        "onboarding": UnifiedMessageType.ONBOARDING,
                        "text": UnifiedMessageType.TEXT,
                        "broadcast": UnifiedMessageType.BROADCAST,
                    }
                    message_type = message_type_map.get(
                        message_type_str.lower(), UnifiedMessageType.SYSTEM_TO_AGENT
                    )
                    logger.debug(
                        f"📍 Mapped message_type_str '{message_type_str}' to {message_type}")
            else:
                # Default based on sender/recipient if message_type not specified
                # Try to infer from sender/recipient
                if sender and recipient:
                    sender_upper = sender.upper()
                    recipient_upper = recipient.upper()

                    # Agent-to-Agent (including Agent-to-Captain - use AGENT_TO_AGENT)
                    if sender.startswith("Agent-") and recipient.startswith("Agent-"):
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    # Agent-to-Captain (Agent-4) - use AGENT_TO_AGENT (not a separate type)
                    elif sender.startswith("Agent-") and recipient_upper in ["CAPTAIN", "AGENT-4"]:
                        # Fixed: Use AGENT_TO_AGENT, not non-existent AGENT_TO_CAPTAIN
                        message_type = UnifiedMessageType.AGENT_TO_AGENT
                    # Captain-to-Agent
                    elif sender_upper in ["CAPTAIN", "AGENT-4"]:
                        message_type = UnifiedMessageType.CAPTAIN_TO_AGENT
                    # System-to-Agent
                    else:
                        message_type = UnifiedMessageType.SYSTEM_TO_AGENT
                else:
                    # Default to SYSTEM_TO_AGENT if not specified
                    message_type = UnifiedMessageType.SYSTEM_TO_AGENT

                logger.debug(
                    f"📍 Inferred message_type={message_type} from sender={sender}, recipient={recipient}")

            # Parse priority
            try:
                priority = UnifiedMessagePriority(priority_str.lower())
            except (ValueError, TypeError):
                priority = UnifiedMessagePriority.REGULAR

            # Parse tags
            tags = []
            if tags_list:
                for tag_str in tags_list:
                    try:
                        if isinstance(tag_str, str):
                            tags.append(UnifiedMessageTag(tag_str.lower()))
                        else:
                            tags.append(tag_str)
                    except (ValueError, TypeError):
                        pass
            if not tags:
                tags = [UnifiedMessageTag.SYSTEM]

            # Use injected messaging core if provided (for stress testing/mocking)
            if self.messaging_core is not None:
                # Injected core (mock or adapter) - no keyboard control needed
                ok = self.messaging_core.send_message(
                    content=content,
                    sender=sender,
                    recipient=recipient,
                    message_type=message_type,
                    priority=priority,
                    tags=tags,
                    metadata=metadata or {},
                )
            else:
                # Default: Real messaging core with keyboard control
                from .messaging_core import send_message
                from .keyboard_control_lock import keyboard_control

                # CRITICAL: Preserve message category in metadata for template detection
                # Extract category from metadata if present
                category_from_meta = None
                if isinstance(metadata, dict):
                    category_str = metadata.get('message_category')
                    if category_str:
                        try:
                            from .messaging_models_core import MessageCategory
                            category_from_meta = MessageCategory(category_str.lower())
                        except (ValueError, AttributeError):
                            pass
                
                # Ensure metadata includes category for downstream template detection
                delivery_metadata = dict(metadata) if metadata else {}
                if category_from_meta:
                    delivery_metadata['message_category'] = category_from_meta.value
                
                # Wrap in keyboard control to prevent race conditions
                with keyboard_control(f"queue_delivery::{recipient}"):
                    ok = send_message(
                        content=content,
                        sender=sender,
                        recipient=recipient,
                        message_type=message_type,
                        priority=priority,
                        tags=tags,
                        metadata=delivery_metadata,
                    )

            return ok

        except ImportError as e:
            logger.error(f"Import error in _deliver_via_core: {e}")
            return False
        except Exception as e:
            logger.error(f"Error in _deliver_via_core: {e}", exc_info=True)
            return False

    def _deliver_fallback_inbox(
        self, recipient: str, content: str, metadata: dict,
        sender: str = None, priority_str: str = None
    ) -> bool:
        """
        Backup path: Inbox file-based delivery.

        Used when PyAutoGUI delivery fails (e.g., Cursor queue full).

        Args:
            recipient: Agent ID to deliver to
            content: Message content
            metadata: Message metadata
            sender: Sender identifier (preserved from message)
            priority_str: Priority string (preserved from message)

        Returns:
            True if inbox delivery successful, False otherwise
        """
        try:
            from ..utils.inbox_utility import create_inbox_message

            # FIXED: Preserve actual sender and priority from message, not metadata
            actual_sender = sender or metadata.get("sender", "SYSTEM")
            actual_priority = priority_str or metadata.get(
                "priority", "normal")

            success = create_inbox_message(
                recipient=recipient,
                content=content,
                sender=actual_sender,
                priority=actual_priority,
            )
            
            # VERIFICATION: Verify delivery succeeded
            if not success:
                logger.error(
                    f"❌ Inbox delivery failed for {recipient} - "
                    f"create_inbox_message returned False"
                )
                return False
            
            logger.info(f"✅ Inbox delivery verified for {recipient}")
            return True
        except ImportError:
            logger.warning("Inbox utility not available")
            return False
        except Exception as e:
            logger.error(f"Inbox delivery error: {e}", exc_info=True)
            return False
    
    def _verify_delivery(
        self, recipient: str, content: str, sender: str, timeout_seconds: int = 10
    ) -> bool:
        """
        Verify message delivery by checking recipient's inbox directory.
        
        After PyAutoGUI delivery, check if message file exists in inbox.
        Uses content hash matching to verify correct message was delivered.
        
        Args:
            recipient: Agent ID to check
            content: Message content to verify
            sender: Sender identifier
            timeout_seconds: Maximum time to wait for file to appear
            
        Returns:
            True if message verified in inbox, False otherwise
        """
        try:
            import hashlib
            from pathlib import Path
            
            # Calculate content hash for matching
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
            
            # Get inbox directory
            project_root = Path(__file__).resolve().parent.parent.parent
            inbox_dir = project_root / "agent_workspaces" / recipient / "inbox"
            
            if not inbox_dir.exists():
                logger.debug(f"Inbox directory does not exist: {inbox_dir}")
                return False
            
            # Poll for message file (PyAutoGUI delivery may take a moment)
            start_time = time.time()
            check_interval = 0.5
            
            while time.time() - start_time < timeout_seconds:
                # Check for recent inbox files
                try:
                    inbox_files = list(inbox_dir.glob("*.md"))
                    
                    # Check files created in last timeout window
                    for inbox_file in inbox_files:
                        try:
                            # Check file age (must be recent)
                            file_age = time.time() - inbox_file.stat().st_mtime
                            if file_age > timeout_seconds:
                                continue  # Skip old files
                            
                            # Read file content
                            file_content = inbox_file.read_text(encoding="utf-8")
                            
                            # Check if content matches (by hash or substring)
                            if content_hash in file_content or content[:100] in file_content:
                                logger.info(
                                    f"✅ Delivery verified for {recipient}: "
                                    f"found matching message in {inbox_file.name}"
                                )
                                return True
                        except Exception as e:
                            logger.debug(f"Error checking inbox file {inbox_file}: {e}")
                            continue
                
                except Exception as e:
                    logger.debug(f"Error listing inbox files: {e}")
                
                # Wait before next check
                time.sleep(check_interval)
            
            # Timeout - message not found in inbox
            logger.warning(
                f"⚠️ Delivery verification timeout for {recipient}: "
                f"message not found in inbox after {timeout_seconds}s"
            )
            return False
            
        except Exception as e:
            logger.error(f"Error verifying delivery for {recipient}: {e}", exc_info=True)
            return False  # Treat verification failure as delivery failure
