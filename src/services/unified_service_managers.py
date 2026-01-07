#!/usr/bin/env python3
"""
Unified Service Managers V2 - Phase 4 Consolidation
===================================================

PHASE 4 CONSOLIDATION: Consolidated service manager modules
Merged from: contract_system/manager.py, protocol/route_manager.py, swarm_intelligence_manager.py

Reduced from 3 separate manager files (~800+ lines) to 1 consolidated module

Consolidated service managers for:
- ContractManager: Contract operations and task assignments
- RouteManager: Message routing and route optimization
- SwarmIntelligenceManager: Swarm intelligence operations

Features:
- Unified manager interface across different service domains
- Consolidated initialization and error handling
- Single responsibility principle maintained
- V2 compliance and SSOT integration

V2 Compliance: <600 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: integration -->
"""

import logging
from datetime import datetime
from typing import Any, Optional

from ..core.base.base_service import BaseService

logger = logging.getLogger(__name__)


class UnifiedContractManager(BaseService):
    """Unified contract manager for contract operations and task assignments.

    PHASE 4 CONSOLIDATION: Migrated from contract_system/manager.py
    Handles contract lifecycle, task assignments, and system status tracking.
    """

    def __init__(self):
        """Initialize unified contract manager."""
        super().__init__("UnifiedContractManager")
        self._init_storage()

    def _init_storage(self):
        """Initialize contract storage with fallback."""
        try:
            from .contract_system.storage import ContractStorage
            from .contract_system.cycle_planner_integration import CyclePlannerIntegration
            self.storage = ContractStorage()
            self.cycle_planner = CyclePlannerIntegration()
        except ImportError:
            # Fallback initialization
            self.storage = None
            self.cycle_planner = None
            logger.warning("Contract storage not available - using fallback mode")

    def get_system_status(self) -> dict[str, Any]:
        """Get overall system contract status."""
        try:
            if not self.storage:
                return {"error": "Contract storage not available"}

            contracts = self.storage.get_all_contracts()

            # Convert Contract objects to dicts for status checking
            contracts_data = [
                c.to_dict() if hasattr(c, 'to_dict')
                else c.__dict__ if hasattr(c, '__dict__')
                else {}
                for c in contracts
            ]

            status = {
                "total_contracts": len(contracts),
                "active_contracts": len([c for c in contracts_data if c.get("status") == "active"]),
                "completed_contracts": len([
                    c for c in contracts_data if c.get("status") == "completed"
                ]),
                "pending_contracts": len([c for c in contracts_data if c.get("status") == "pending"]),
                "failed_contracts": len([c for c in contracts_data if c.get("status") == "failed"]),
                "contracts": contracts_data
            }

            return status

        except Exception as e:
            logger.error(f"Error getting contract system status: {e}")
            return {"error": str(e)}

    def assign_contract(self, agent_id: str, contract_data: dict[str, Any]) -> dict[str, Any]:
        """Assign a contract to an agent."""
        try:
            if not self.storage:
                return {"success": False, "error": "Contract storage not available"}

            # Create contract object
            contract = self.storage.create_contract(
                agent_id=agent_id,
                title=contract_data.get("title", ""),
                description=contract_data.get("description", ""),
                priority=contract_data.get("priority", "normal"),
                deadline=contract_data.get("deadline"),
                requirements=contract_data.get("requirements", [])
            )

            # Save contract
            self.storage.save_contract(contract)

            # Integrate with cycle planner if available
            if self.cycle_planner:
                try:
                    self.cycle_planner.notify_contract_assigned(agent_id, contract)
                except Exception as e:
                    logger.warning(f"Cycle planner integration failed: {e}")

            return {
                "success": True,
                "contract_id": contract.contract_id,
                "message": f"Contract assigned to {agent_id}"
            }

        except Exception as e:
            logger.error(f"Error assigning contract: {e}")
            return {"success": False, "error": str(e)}

    def get_agent_contracts(self, agent_id: str) -> dict[str, Any]:
        """Get contracts for a specific agent."""
        try:
            if not self.storage:
                return {"success": False, "error": "Contract storage not available"}

            contracts = self.storage.get_agent_contracts(agent_id)
            contracts_data = [
                c.to_dict() if hasattr(c, 'to_dict')
                else c.__dict__ if hasattr(c, '__dict__')
                else {}
                for c in contracts
            ]

            return {
                "success": True,
                "agent_id": agent_id,
                "contracts": contracts_data,
                "total": len(contracts_data)
            }

        except Exception as e:
            logger.error(f"Error getting agent contracts: {e}")
            return {"success": False, "error": str(e)}


class UnifiedRouteManager(BaseService):
    """Unified route manager for message routing and optimization.

    PHASE 4 CONSOLIDATION: Migrated from protocol/route_manager.py
    Manages message routes, optimization, and routing configuration.
    """

    def __init__(self):
        """Initialize unified route manager."""
        super().__init__("UnifiedRouteManager")
        self.routes: dict[str, Any] = {}
        self.route_configs: dict[str, dict[str, Any]] = {}
        self._init_route_types()

    def _init_route_types(self):
        """Initialize route types with fallback."""
        try:
            from .protocol.messaging_protocol_models import MessageRoute, RouteOptimization
            self.MessageRoute = MessageRoute
            self.RouteOptimization = RouteOptimization
        except ImportError:
            # Fallback route types
            self.MessageRoute = type('MessageRoute', (), {'DIRECT': 'direct', 'BROADCAST': 'broadcast'})
            self.RouteOptimization = type('RouteOptimization', (), {})

    def add_route(
        self,
        route_name: str,
        route_type: Any,
        optimization: Optional[Any] = None,
        config: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Add a new route."""
        try:
            if optimization is None:
                optimization = self.RouteOptimization()

            self.routes[route_name] = {
                "type": route_type,
                "optimization": optimization,
                "created_at": datetime.now(),
                "active": True
            }

            if config:
                self.route_configs[route_name] = config

            logger.info(f"Added route: {route_name}")
            return True

        except Exception as e:
            logger.error(f"Error adding route {route_name}: {e}")
            return False

    def remove_route(self, route_name: str) -> bool:
        """Remove a route."""
        try:
            if route_name in self.routes:
                del self.routes[route_name]
                if route_name in self.route_configs:
                    del self.route_configs[route_name]
                logger.info(f"Removed route: {route_name}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error removing route {route_name}: {e}")
            return False

    def get_route(self, route_name: str) -> Optional[dict[str, Any]]:
        """Get a specific route."""
        return self.routes.get(route_name)

    def list_routes(self) -> dict[str, Any]:
        """List all routes."""
        return {
            "routes": self.routes,
            "total": len(self.routes),
            "active": len([r for r in self.routes.values() if r.get("active", False)])
        }


class UnifiedSwarmIntelligenceManager(BaseService):
    """Unified swarm intelligence manager for swarm operations.

    PHASE 4 CONSOLIDATION: Migrated from swarm_intelligence_manager.py
    Handles swarm intelligence operations and agent coordination.
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        """Initialize unified swarm intelligence manager."""
        super().__init__("UnifiedSwarmIntelligenceManager")
        self.agent_id = agent_id
        self.config_path = config_path
        self.vector_db_available = False
        self._init_vector_db()

    def _init_vector_db(self):
        """Initialize vector database with fallback."""
        try:
            from .vector_database import (
                get_vector_database_service,
                VECTOR_DB_AVAILABLE,
            )
            self.vector_db_available = VECTOR_DB_AVAILABLE
            if self.vector_db_available:
                self.vector_service = get_vector_database_service()
        except ImportError:
            self.vector_db_available = False
            self.vector_service = None
            logger.warning("Vector database not available - swarm intelligence limited")

    def get_swarm_status(self) -> dict[str, Any]:
        """Get swarm intelligence status."""
        return {
            "agent_id": self.agent_id,
            "vector_db_available": self.vector_db_available,
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "swarm_coordination" if self.vector_db_available else "basic_coordination",
                "agent_discovery",
                "intelligence_sharing"
            ]
        }

    def search_swarm_knowledge(self, query: str) -> dict[str, Any]:
        """Search swarm knowledge base."""
        try:
            if not self.vector_db_available or not self.vector_service:
                return {
                    "success": False,
                    "error": "Vector database not available",
                    "fallback": "basic_search"
                }

            # Use vector database for advanced search
            from .vector_database import SearchQuery
            search_query = SearchQuery(
                query=query,
                limit=10,
                include_metadata=True
            )

            results = self.vector_service.search(search_query)
            return {
                "success": True,
                "query": query,
                "results": results,
                "total": len(results) if results else 0
            }

        except Exception as e:
            logger.error(f"Error searching swarm knowledge: {e}")
            return {"success": False, "error": str(e)}

    def coordinate_with_swarm(self, message: str, target_agents: Optional[list[str]] = None) -> dict[str, Any]:
        """Coordinate with swarm agents."""
        try:
            coordination_data = {
                "from_agent": self.agent_id,
                "message": message,
                "target_agents": target_agents or ["all"],
                "timestamp": datetime.now().isoformat(),
                "coordination_type": "intelligence_sharing"
            }

            # In a full implementation, this would send to other agents
            # For now, return coordination data
            return {
                "success": True,
                "coordination_id": f"coord_{int(datetime.now().timestamp())}",
                "data": coordination_data
            }

        except Exception as e:
            logger.error(f"Error coordinating with swarm: {e}")
            return {"success": False, "error": str(e)}


# Backward compatibility aliases
ContractManager = UnifiedContractManager
RouteManager = UnifiedRouteManager
SwarmIntelligenceManager = UnifiedSwarmIntelligenceManager

# Export all unified managers
__all__ = [
    "UnifiedContractManager",
    "UnifiedRouteManager",
    "UnifiedSwarmIntelligenceManager",
    "ContractManager",  # Backward compatibility
    "RouteManager",     # Backward compatibility
    "SwarmIntelligenceManager",  # Backward compatibility
]