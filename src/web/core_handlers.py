"""
Core System Handlers
====================

<!-- SSOT Domain: web -->

Handler classes for core system operations.
Wires core services to web layer.

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.base_handler import BaseHandler

try:
    from src.core.agent_lifecycle import AgentLifecycle
    AGENT_LIFECYCLE_AVAILABLE = True
except ImportError:
    AGENT_LIFECYCLE_AVAILABLE = False

try:
    from src.core.utils.message_queue_utils import get_queue_status
    MESSAGE_QUEUE_AVAILABLE = True
except ImportError:
    MESSAGE_QUEUE_AVAILABLE = False


class CoreHandlers(BaseHandler):
    """Handler class for core system operations."""

    def __init__(self):
        """Initialize core handlers."""
        super().__init__("CoreHandlers")

    def handle_get_agent_lifecycle_status(self, request, agent_id: str) -> tuple:
        """
        Handle request to get agent lifecycle status.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        if not AGENT_LIFECYCLE_AVAILABLE:
            return jsonify({"success": False, "error": "AgentLifecycle not available"}), 503

        try:
            lifecycle = AgentLifecycle(agent_id)
            status = lifecycle.get_status()

            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_start_cycle(self, request, agent_id: str) -> tuple:
        """
        Handle request to start agent lifecycle cycle.

        Args:
            request: Flask request object
            agent_id: Agent identifier

        Returns:
            Tuple of (response_data, status_code)
        """
        if not AGENT_LIFECYCLE_AVAILABLE:
            return jsonify({"success": False, "error": "AgentLifecycle not available"}), 503

        try:
            lifecycle = AgentLifecycle(agent_id)
            lifecycle.start_cycle()

            return jsonify({"success": True, "message": f"Cycle started for {agent_id}"}), 200

        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_message_queue_status(self, request) -> tuple:
        """
        Handle request to get message queue status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not MESSAGE_QUEUE_AVAILABLE:
            return jsonify({"success": False, "error": "Message queue utils not available"}), 503

        try:
            status = get_queue_status()
            return jsonify({"success": True, "data": status}), 200

        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_execution_status(self, request) -> tuple:
        """Handle request to get execution manager status."""
        try:
            from src.core.managers.core_execution_manager import CoreExecutionManager
            manager = CoreExecutionManager()
            status = manager.get_status()
            return jsonify({"success": True, "data": status}), 200
        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_service_status(self, request) -> tuple:
        """Handle request to get service manager status."""
        try:
            from src.core.managers.core_service_manager import CoreServiceManager
            manager = CoreServiceManager()
            status = manager.get_status()
            return jsonify({"success": True, "data": status}), 200
        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_resource_status(self, request) -> tuple:
        """Handle request to get resource manager status."""
        try:
            from src.core.managers.core_resource_manager import CoreResourceManager
            manager = CoreResourceManager()
            status = manager.get_status()
            return jsonify({"success": True, "data": status}), 200
        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_recovery_status(self, request) -> tuple:
        """Handle request to get recovery manager status."""
        try:
            from src.core.managers.core_recovery_manager import CoreRecoveryManager
            manager = CoreRecoveryManager()
            status = manager.get_status()
            return jsonify({"success": True, "data": status}), 200
        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_results_status(self, request) -> tuple:
        """Handle request to get results manager status."""
        try:
            from src.core.managers.core_results_manager import CoreResultsManager
            manager = CoreResultsManager()
            status = manager.get_status()
            return jsonify({"success": True, "data": status}), 200
        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_process_message_queue(self, request) -> tuple:
        """Handle request to process message queue entries."""
        if not MESSAGE_QUEUE_AVAILABLE:
            return jsonify({"success": False, "error": "Message queue utils not available"}), 503

        try:
            from src.core.utils.message_queue_utils import MessageQueueUtils
            data = request.get_json() or {}
            max_entries = data.get("max_entries", 10)
            
            entries = MessageQueueUtils.get_entries_ready_for_processing(max_entries)
            processed = len(entries)
            
            result = {
                "processed": processed,
                "entries": [
                    {
                        "id": entry.message_id,
                        "status": entry.status.value if hasattr(entry.status, 'value') else str(entry.status),
                        "recipient": entry.recipient,
                        "attempts": entry.delivery_attempts
                    }
                    for entry in entries
                ]
            }
            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500

    def handle_get_queue_size(self, request) -> tuple:
        """Handle request to get message queue size."""
        if not MESSAGE_QUEUE_AVAILABLE:
            return jsonify({"success": False, "error": "Message queue utils not available"}), 503

        try:
            from src.core.utils.message_queue_utils import get_queue_status
            status = get_queue_status()
            
            # Extract size information from status
            queue_size = status.get("total_entries", 0) if isinstance(status, dict) else 0
            
            result = {
                "queue_size": queue_size,
                "status": status
            }
            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            error_response = self.handle_error(e, context="get_agent_lifecycle_status")
            return jsonify(error_response), 500


