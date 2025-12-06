"""
Pipeline Handlers
=================

Handler classes for pipeline operations.
Wires pipeline systems to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import with availability flag
try:
    from src.core.auto_gas_pipeline_system import AutoGasPipelineSystem
    GAS_PIPELINE_AVAILABLE = True
except ImportError:
    GAS_PIPELINE_AVAILABLE = False


class PipelineHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for pipeline operations."""
    
    def __init__(self):
        """Initialize pipeline handlers."""
        super().__init__("PipelineHandlers")
    
    def _get_pipeline_system(self):
        """Get pipeline system instance (lazy import pattern)."""
        if GAS_PIPELINE_AVAILABLE:
            return AutoGasPipelineSystem()
        return None
    
    def handle_get_gas_pipeline_status(self, request) -> Tuple[Any, int]:
        """
        Handle request to get gas pipeline system status.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability
        availability_error = self.check_availability(
            GAS_PIPELINE_AVAILABLE,
            "GasPipelineSystem"
        )
        if availability_error:
            return availability_error
        
        try:
            pipeline = self._get_pipeline_system()
            status = pipeline.get_system_status()
            
            response = self.format_response(status, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_gas_pipeline_status")
            return jsonify(error_response), 500
    
    def handle_monitor_gas_pipeline(self, request) -> Tuple[Any, int]:
        """
        Handle request to monitor and send gas to agents.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            GAS_PIPELINE_AVAILABLE,
            "GasPipelineSystem"
        )
        if availability_error:
            return availability_error
        
        try:
            pipeline = self._get_pipeline_system()
            result = pipeline.monitor_and_send_gas()
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_monitor_gas_pipeline")
            return jsonify(error_response), 500
    
    def handle_get_agent_gas_status(self, request, agent_id: str) -> Tuple[Any, int]:
        """
        Handle request to get gas status for specific agent.
        
        Args:
            request: Flask request object
            agent_id: Agent identifier
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            GAS_PIPELINE_AVAILABLE,
            "GasPipelineSystem"
        )
        if availability_error:
            return availability_error
        
        try:
            pipeline = self._get_pipeline_system()
            status = pipeline.get_agent_status(agent_id)
            
            response = self.format_response(status, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"handle_get_agent_gas_status_{agent_id}")
            return jsonify(error_response), 500


