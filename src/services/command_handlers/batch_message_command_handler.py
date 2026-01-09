#!/usr/bin/env python3
"""
Batch Message Command Handler - V2 Compliance
==============================================

Handler for batch message CLI commands (--batch-start, --batch-add, --batch-send, --batch-status, --batch-cancel).

PHASE 4 CONSOLIDATION: Migrated from handlers/batch_message_handler.py
Consolidated batch messaging operations with unified interface.

V2 Compliance: <400 lines, modular design
Author: Agent-7 (Modularization)
<!-- SSOT Domain: integration -->
"""

import logging
from typing import Any
from src.core.unified_service_base import UnifiedServiceBase

logger = logging.getLogger(__name__)


class BatchMessageCommandHandler(UnifiedServiceBase):
    """Handler for batch message CLI commands (--batch-start, --batch-add, --batch-send, --batch-status, --batch-cancel).

    PHASE 4 CONSOLIDATION: Migrated from handlers/batch_message_handler.py
    Consolidated batch messaging operations with unified interface.
    """

    def __init__(self):
        """Initialize batch message command handler."""
        super().__init__("BatchMessageCommandHandler")
        self.batch_service = None
        self._init_batch_service()

    def _init_batch_service(self):
        """Initialize batch service with fallback."""
        try:
            from ..message_batching_service import MessageBatchingService
            self.batch_service = MessageBatchingService()
        except ImportError:
            logger.warning("MessageBatchingService not available for batch operations")
            self.batch_service = None

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return (hasattr(args, 'batch_start') and args.batch_start) or \
               (hasattr(args, 'batch_add') and args.batch_add) or \
               (hasattr(args, 'batch_send') and args.batch_send) or \
               (hasattr(args, 'batch_status') and args.batch_status) or \
               (hasattr(args, 'batch_cancel') and args.batch_cancel) or \
               (hasattr(args, 'batch') and args.batch)

    def handle(self, args) -> bool:
        """Handle batch message commands."""
        try:
            if hasattr(args, 'batch_start') and args.batch_start:
                return self._handle_batch_start(args)
            elif hasattr(args, 'batch_add') and args.batch_add:
                return self._handle_batch_add(args)
            elif hasattr(args, 'batch_send') and args.batch_send:
                return self._handle_batch_send(args)
            elif hasattr(args, 'batch_status') and args.batch_status:
                return self._handle_batch_status(args)
            elif hasattr(args, 'batch_cancel') and args.batch_cancel:
                return self._handle_batch_cancel(args)
            elif hasattr(args, 'batch') and args.batch:
                return self._handle_batch_list(args)
            return False
        except Exception as e:
            logger.error(f"Batch message command handling error: {e}")
            return False

    def _handle_batch_start(self, args) -> bool:
        """Handle batch start command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = self.batch_service.start_batch()
            print(f"✅ Batch started with ID: {batch_id}")
            print("   Use --batch-add to add messages to this batch")
            return True
        except Exception as e:
            logger.error(f"Batch start error: {e}")
            return False

    def _handle_batch_add(self, args) -> bool:
        """Handle batch add command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            message = getattr(args, 'message', None)
            recipient = getattr(args, 'recipient', None)

            if not all([batch_id, message, recipient]):
                print("❌ Batch ID, message, and recipient required")
                return False

            success = self.batch_service.add_to_batch(batch_id, message, recipient)
            if success:
                print(f"✅ Message added to batch {batch_id}")
                return True
            else:
                print(f"❌ Failed to add message to batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch add error: {e}")
            return False

    def _handle_batch_send(self, args) -> bool:
        """Handle batch send command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if not batch_id:
                print("❌ Batch ID required")
                return False

            success = self.batch_service.send_batch(batch_id)
            if success:
                print(f"✅ Batch {batch_id} sent successfully")
                return True
            else:
                print(f"❌ Failed to send batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch send error: {e}")
            return False

    def _handle_batch_status(self, args) -> bool:
        """Handle batch status command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if batch_id:
                status = self.batch_service.get_batch_status(batch_id)
                if status:
                    print(f"📊 Batch {batch_id} Status:")
                    print(f"   🔄 Status: {status.get('status', 'unknown')}")
                    print(f"   📨 Messages: {status.get('message_count', 0)}")
                    print(f"   ✅ Sent: {status.get('sent_count', 0)}")
                    print(f"   ❌ Failed: {status.get('failed_count', 0)}")
                else:
                    print(f"❌ Batch {batch_id} not found")
                    return False
            else:
                # List all batches
                batches = self.batch_service.list_batches()
                if batches:
                    print(f"📋 Active Batches ({len(batches)}):")
                    for batch in batches:
                        print(f"   • {batch['id']}: {batch['status']} ({batch['message_count']} messages)")
                else:
                    print("ℹ️  No active batches")
            return True
        except Exception as e:
            logger.error(f"Batch status error: {e}")
            return False

    def _handle_batch_cancel(self, args) -> bool:
        """Handle batch cancel command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batch_id = getattr(args, 'batch_id', None)
            if not batch_id:
                print("❌ Batch ID required")
                return False

            success = self.batch_service.cancel_batch(batch_id)
            if success:
                print(f"✅ Batch {batch_id} cancelled")
                return True
            else:
                print(f"❌ Failed to cancel batch {batch_id}")
                return False
        except Exception as e:
            logger.error(f"Batch cancel error: {e}")
            return False

    def _handle_batch_list(self, args) -> bool:
        """Handle batch list command."""
        try:
            if not self.batch_service:
                print("❌ Batch service not available")
                return False

            batches = self.batch_service.list_batches()
            if batches:
                print(f"📋 All Batches ({len(batches)}):")
                for batch in batches:
                    print(f"   • {batch['id']}: {batch['status']} ({batch['message_count']} messages)")
            else:
                print("ℹ️  No batches found")
            return True
        except Exception as e:
            logger.error(f"Batch list error: {e}")
            return False