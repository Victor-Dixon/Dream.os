#!/usr/bin/env python3
"""
Error Handler - Handle Pipeline Errors
======================================

Handles errors during pipeline execution.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def handle_pipeline_error(
    agent_id: str,
    error: Exception,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Handle pipeline error and log appropriately.

    Args:
        agent_id: Agent ID where error occurred
        error: Exception that occurred
        context: Optional context dictionary
    """
    logger.error(f"Pipeline error for {agent_id}: {error}", exc_info=True)

    if context:
        logger.debug(f"Error context: {context}")

    # Could add error reporting to Swarm Brain here
    # For now, just log the error
