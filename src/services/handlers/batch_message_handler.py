<<<<<<< HEAD
"""
<!-- SSOT Domain: integration -->

Batch Message Handler - V2 Compliant Module
==========================================

Handles message batching commands for messaging CLI.
Integrates with message_batching_service.

V2 Compliance: < 300 lines, single responsibility
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging

from ...core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class BatchMessageHandler(BaseService):
    """Handles message batching commands for messaging CLI."""

    def __init__(self):
        """Initialize batch message handler."""
        super().__init__("BatchMessageHandler")
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "batch_start")
            and args.batch_start
            or hasattr(args, "batch_add")
            and args.batch_add
            or hasattr(args, "batch_send")
            and args.batch_send
            or hasattr(args, "batch_status")
            and args.batch_status
            or hasattr(args, "batch_cancel")
            and args.batch_cancel
            or hasattr(args, "batch")
            and args.batch
        )

    def handle(self, args) -> dict:
        """Handle batch message commands."""
        try:
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            from ..message_batching_service import get_batching_service

            service = get_batching_service()

            # Determine sender (agent or captain)
            sender = args.agent if hasattr(args, "agent") and args.agent else "CAPTAIN"
            recipient = "Agent-4"  # Default to Captain

            # Handle simplified batch (--batch)
            if args.batch:
                success = self._handle_simplified_batch(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch',
                    'sender': sender,
                    'recipient': recipient
                }

            # Handle batch-start
            if args.batch_start:
                success = self._handle_batch_start(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch_start',
                    'sender': sender,
                    'recipient': recipient
                }

            # Handle batch-add
            if args.batch_add:
                success = self._handle_batch_add(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch_add',
                    'sender': sender,
                    'recipient': recipient
                }

            # Handle batch-send
            if args.batch_send:
                success = self._handle_batch_send(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch_send',
                    'sender': sender,
                    'recipient': recipient
                }

            # Handle batch-status
            if args.batch_status:
                success = self._handle_batch_status(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch_status',
                    'sender': sender,
                    'recipient': recipient
                }

            # Handle batch-cancel
            if args.batch_cancel:
                success = self._handle_batch_cancel(args, service, sender, recipient)
                return {
                    'success': success,
                    'command': 'batch_cancel',
                    'sender': sender,
                    'recipient': recipient
                }

            return {
                'success': False,
                'error': 'No valid batch command specified',
                'command': 'unknown'
            }

        except ImportError as e:
            logger.error(f"❌ Message batching service not available: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': f'Message batching service not available: {e}',
                'command': getattr(args, 'command', 'batch')
            }
        except Exception as e:
            logger.error(f"❌ Batch handling error: {e}")
            self.exit_code = 1
            return {
                'success': False,
                'error': str(e),
                'command': getattr(args, 'command', 'batch')
            }

    def _handle_simplified_batch(self, args, service, sender, recipient) -> bool:
        """Handle simplified batch (all in one command)."""
        if not args.batch:
            logger.error("❌ No messages provided for batch")
            self.exit_code = 1
            return True

        logger.info(f"📦 Simplified batch: {len(args.batch)} messages")

        # Start batch
        service.start_batch(sender, recipient)

        # Add all messages
        for i, message in enumerate(args.batch, 1):
            logger.info(f"📥 Adding message {i}/{len(args.batch)}")
            service.add_to_batch(sender, recipient, message)

        # Send batch
        # Normalize "normal" to "regular" for consistency
        raw_priority = args.priority if hasattr(args, "priority") else "regular"
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority
        
        success, consolidated_message = service.send_batch(
            sender,
            recipient,
            priority=normalized_priority, 
        )

        if success:
            # Send consolidated message via messaging system
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            priority = (
                UnifiedMessagePriority.URGENT
                if normalized_priority == "urgent"      
                else UnifiedMessagePriority.REGULAR
            )

            send_success = send_message(
                content=consolidated_message,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_CAPTAIN,
                priority=priority,
                tags=[UnifiedMessageTag.BATCHED, UnifiedMessageTag.COORDINATION],
            )

            if send_success:
                logger.info(f"✅ Batch sent successfully! {len(args.batch)} messages consolidated")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to send batch message")
                self.exit_code = 1
        else:
            logger.error("❌ Failed to create batch")
            self.exit_code = 1

        return True

    def _handle_batch_start(self, args, service, sender, recipient) -> bool:
        """Handle batch-start command."""
        logger.info(f"🆕 Starting new batch: {sender}→{recipient}")

        success = service.start_batch(sender, recipient)

        if success:
            logger.info(f"✅ Batch started for {sender}→{recipient}")
            logger.info("💡 Use --batch-add to add messages")
            logger.info("💡 Use --batch-send to send consolidated batch")
            self.exit_code = 0
        else:
            logger.error("❌ Failed to start batch")
            self.exit_code = 1

        return True

    def _handle_batch_add(self, args, service, sender, recipient) -> bool:
        """Handle batch-add command."""
        if not args.batch_add:
            logger.error("❌ No message provided")
            self.exit_code = 1
            return True

        logger.info(f"📥 Adding message to batch: {sender}→{recipient}")

        success = service.add_to_batch(sender, recipient, args.batch_add)

        if success:
            status = service.get_batch_status(sender, recipient)
            logger.info(f"✅ Message added! Batch now has {status['message_count']} messages")
            self.exit_code = 0
        else:
            logger.error("❌ Failed to add message to batch")
            logger.info("💡 Use --batch-start first")
            self.exit_code = 1

        return True

    def _handle_batch_send(self, args, service, sender, recipient) -> bool:
        """Handle batch-send command."""
        logger.info(f"📤 Sending batch: {sender}→{recipient}")

        # Normalize "normal" to "regular" for consistency
        raw_priority = args.priority if hasattr(args, "priority") else "regular"
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority
        
        success, consolidated_message = service.send_batch(
            sender,
            recipient,
            priority=normalized_priority, 
        )

        if success:
            # Send consolidated message via messaging system
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            priority = (
                UnifiedMessagePriority.URGENT
                if normalized_priority == "urgent"      
                else UnifiedMessagePriority.REGULAR
            )

            send_success = send_message(
                content=consolidated_message,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_CAPTAIN,
                priority=priority,
                tags=[UnifiedMessageTag.BATCHED, UnifiedMessageTag.COORDINATION],
            )

            if send_success:
                logger.info("✅ Batch sent successfully!")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to send batch message")
                self.exit_code = 1
        else:
            logger.error("❌ Failed to send batch (batch may be empty)")
            self.exit_code = 1

        return True

    def _handle_batch_status(self, args, service, sender, recipient) -> bool:
        """Handle batch-status command."""
        logger.info(f"📊 Checking batch status: {sender}→{recipient}")

        status = service.get_batch_status(sender, recipient)

        if status["exists"]:
            logger.info("✅ Active batch found:")
            logger.info(f"   Agent: {status['agent_id']}")
            logger.info(f"   Recipient: {status['recipient']}")
            logger.info(f"   Messages: {status['message_count']}")
            logger.info(f"   Created: {status['created_at']}")
            self.exit_code = 0
        else:
            logger.info(f"ℹ️ {status['message']}")
            self.exit_code = 0

        return True

    def _handle_batch_cancel(self, args, service, sender, recipient) -> bool:
        """Handle batch-cancel command."""
        logger.info(f"🚫 Cancelling batch: {sender}→{recipient}")

        success = service.cancel_batch(sender, recipient)

        if success:
            logger.info("✅ Batch cancelled successfully")
            self.exit_code = 0
        else:
            logger.warning("⚠️ No active batch to cancel")
            self.exit_code = 0

        return True
=======
"""
<!-- SSOT Domain: integration -->

Batch Message Handler - V2 Compliant Module
==========================================

Handles message batching commands for messaging CLI.
Integrates with message_batching_service.

V2 Compliance: < 300 lines, single responsibility
Migrated to BaseService for consolidated initialization and error handling.
"""

import logging

from ...core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class BatchMessageHandler(BaseService):
    """Handles message batching commands for messaging CLI."""

    def __init__(self):
        """Initialize batch message handler."""
        super().__init__("BatchMessageHandler")
        self.exit_code = 0

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (
            hasattr(args, "batch_start")
            and args.batch_start
            or hasattr(args, "batch_add")
            and args.batch_add
            or hasattr(args, "batch_send")
            and args.batch_send
            or hasattr(args, "batch_status")
            and args.batch_status
            or hasattr(args, "batch_cancel")
            and args.batch_cancel
            or hasattr(args, "batch")
            and args.batch
        )

    def handle(self, args) -> bool:
        """Handle batch message commands."""
        try:
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            from ..message_batching_service import get_batching_service

            service = get_batching_service()

            # Determine sender (agent or captain)
            sender = args.agent if hasattr(args, "agent") and args.agent else "CAPTAIN"
            recipient = "Agent-4"  # Default to Captain

            # Handle simplified batch (--batch)
            if args.batch:
                return self._handle_simplified_batch(args, service, sender, recipient)

            # Handle batch-start
            if args.batch_start:
                return self._handle_batch_start(args, service, sender, recipient)

            # Handle batch-add
            if args.batch_add:
                return self._handle_batch_add(args, service, sender, recipient)

            # Handle batch-send
            if args.batch_send:
                return self._handle_batch_send(args, service, sender, recipient)

            # Handle batch-status
            if args.batch_status:
                return self._handle_batch_status(args, service, sender, recipient)

            # Handle batch-cancel
            if args.batch_cancel:
                return self._handle_batch_cancel(args, service, sender, recipient)

            return True

        except ImportError as e:
            logger.error(f"❌ Message batching service not available: {e}")
            self.exit_code = 1
            return True
        except Exception as e:
            logger.error(f"❌ Batch handling error: {e}")
            self.exit_code = 1
            return True

    def _handle_simplified_batch(self, args, service, sender, recipient) -> bool:
        """Handle simplified batch (all in one command)."""
        if not args.batch:
            logger.error("❌ No messages provided for batch")
            self.exit_code = 1
            return True

        logger.info(f"📦 Simplified batch: {len(args.batch)} messages")

        # Start batch
        service.start_batch(sender, recipient)

        # Add all messages
        for i, message in enumerate(args.batch, 1):
            logger.info(f"📥 Adding message {i}/{len(args.batch)}")
            service.add_to_batch(sender, recipient, message)

        # Send batch
        # Normalize "normal" to "regular" for consistency
        raw_priority = args.priority if hasattr(args, "priority") else "regular"
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority
        
        success, consolidated_message = service.send_batch(
            sender,
            recipient,
            priority=normalized_priority, 
        )

        if success:
            # Send consolidated message via messaging system
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            priority = (
                UnifiedMessagePriority.URGENT
                if normalized_priority == "urgent"      
                else UnifiedMessagePriority.REGULAR
            )

            send_success = send_message(
                content=consolidated_message,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_CAPTAIN,
                priority=priority,
                tags=[UnifiedMessageTag.BATCHED, UnifiedMessageTag.COORDINATION],
            )

            if send_success:
                logger.info(f"✅ Batch sent successfully! {len(args.batch)} messages consolidated")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to send batch message")
                self.exit_code = 1
        else:
            logger.error("❌ Failed to create batch")
            self.exit_code = 1

        return True

    def _handle_batch_start(self, args, service, sender, recipient) -> bool:
        """Handle batch-start command."""
        logger.info(f"🆕 Starting new batch: {sender}→{recipient}")

        success = service.start_batch(sender, recipient)

        if success:
            logger.info(f"✅ Batch started for {sender}→{recipient}")
            logger.info("💡 Use --batch-add to add messages")
            logger.info("💡 Use --batch-send to send consolidated batch")
            self.exit_code = 0
        else:
            logger.error("❌ Failed to start batch")
            self.exit_code = 1

        return True

    def _handle_batch_add(self, args, service, sender, recipient) -> bool:
        """Handle batch-add command."""
        if not args.batch_add:
            logger.error("❌ No message provided")
            self.exit_code = 1
            return True

        logger.info(f"📥 Adding message to batch: {sender}→{recipient}")

        success = service.add_to_batch(sender, recipient, args.batch_add)

        if success:
            status = service.get_batch_status(sender, recipient)
            logger.info(f"✅ Message added! Batch now has {status['message_count']} messages")
            self.exit_code = 0
        else:
            logger.error("❌ Failed to add message to batch")
            logger.info("💡 Use --batch-start first")
            self.exit_code = 1

        return True

    def _handle_batch_send(self, args, service, sender, recipient) -> bool:
        """Handle batch-send command."""
        logger.info(f"📤 Sending batch: {sender}→{recipient}")

        # Normalize "normal" to "regular" for consistency
        raw_priority = args.priority if hasattr(args, "priority") else "regular"
        normalized_priority = "regular" if raw_priority == "normal" else raw_priority
        
        success, consolidated_message = service.send_batch(
            sender,
            recipient,
            priority=normalized_priority, 
        )

        if success:
            # Send consolidated message via messaging system
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
                send_message,
            )

            priority = (
                UnifiedMessagePriority.URGENT
                if normalized_priority == "urgent"      
                else UnifiedMessagePriority.REGULAR
            )

            send_success = send_message(
                content=consolidated_message,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.AGENT_TO_CAPTAIN,
                priority=priority,
                tags=[UnifiedMessageTag.BATCHED, UnifiedMessageTag.COORDINATION],
            )

            if send_success:
                logger.info("✅ Batch sent successfully!")
                self.exit_code = 0
            else:
                logger.error("❌ Failed to send batch message")
                self.exit_code = 1
        else:
            logger.error("❌ Failed to send batch (batch may be empty)")
            self.exit_code = 1

        return True

    def _handle_batch_status(self, args, service, sender, recipient) -> bool:
        """Handle batch-status command."""
        logger.info(f"📊 Checking batch status: {sender}→{recipient}")

        status = service.get_batch_status(sender, recipient)

        if status["exists"]:
            logger.info("✅ Active batch found:")
            logger.info(f"   Agent: {status['agent_id']}")
            logger.info(f"   Recipient: {status['recipient']}")
            logger.info(f"   Messages: {status['message_count']}")
            logger.info(f"   Created: {status['created_at']}")
            self.exit_code = 0
        else:
            logger.info(f"ℹ️ {status['message']}")
            self.exit_code = 0

        return True

    def _handle_batch_cancel(self, args, service, sender, recipient) -> bool:
        """Handle batch-cancel command."""
        logger.info(f"🚫 Cancelling batch: {sender}→{recipient}")

        success = service.cancel_batch(sender, recipient)

        if success:
            logger.info("✅ Batch cancelled successfully")
            self.exit_code = 0
        else:
            logger.warning("⚠️ No active batch to cancel")
            self.exit_code = 0

        return True
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
