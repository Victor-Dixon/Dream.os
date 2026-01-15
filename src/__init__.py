"""
Agent Cellphone V2 - Swarm AI Coordination Framework

A revolutionary multi-agent coordination system that enables AI agents to work
together seamlessly, creating superhuman productivity through intelligent
parallel processing and task coordination.
"""

__version__ = "2.0.0"
__author__ = "Agent Cellphone Development Team"
__email__ = "team@agent-cellphone-v2.com"
__license__ = "MIT"
__description__ = "Swarm AI Coordination Framework for Multi-Agent Collaboration"
__url__ = "https://github.com/your-org/agent-cellphone-v2"

# Import main components for easy access
try:
    from .core.messaging_core import MessagingCore
    from .services.messaging_cli import MessagingCLI
    from .services.unified_service_managers import UnifiedContractManager
except ImportError:
    # Handle import errors gracefully during installation
    MessagingCore = None
    MessagingCLI = None
    UnifiedContractManager = None

__all__ = [
    "MessagingCore",
    "MessagingCLI",
    "UnifiedContractManager",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    "__url__",
]
