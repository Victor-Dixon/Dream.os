"""
<!-- SSOT Domain: integration -->

Handler module loader.

Wrap imports to avoid hard failures when optional handler dependencies are
missing (e.g., onboarding_handler depends on src.utils.confirm). This keeps
critical handlers like task_handler available for CLI operations.
"""

import importlib
import logging

logger = logging.getLogger(__name__)

__all__ = []
_HANDLERS = [
    "batch_message_handler",
    "command_handler",
    "contract_handler",
    "coordinate_handler",
    "hard_onboarding_handler",
    "onboarding_handler",
    "soft_onboarding_handler",
    "task_handler",
    "utility_handler",
]


def _safe_import(handler_name: str):
    """Attempt to import a handler without breaking the package."""
    try:
        importlib.import_module(f"{__name__}.{handler_name}")
        __all__.append(handler_name)
    except ImportError as exc:
        logger.warning("Skipping handler import %s: %s", handler_name, exc)


for _handler in _HANDLERS:
    _safe_import(_handler)
