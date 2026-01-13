"""Logging utilities for the unified workspace.
<!-- SSOT Domain: logging -->


**CONSOLIDATED**: This module now redirects to unified_logging_system.
Maintained for backward compatibility.
"""

from __future__ import annotations

import logging
from pathlib import Path

# Redirect to unified logging system
try:
    from src.core.unified_logging_system import get_logger, configure_logging
    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False


def setup_logger(name: str = "workspace", level: int = logging.INFO) -> logging.Logger:
    """

    Set up and return a logger with console and file handlers.
    
    **CONSOLIDATED**: Now uses unified_logging_system.
    Maintained for backward compatibility.

    Idempotent: calling multiple times will not duplicate handlers, and will
    ensure a file handler for logs/<name>.log exists.
    """
    if UNIFIED_AVAILABLE:
        # Convert level int to string
        level_str = logging.getLevelName(level)
        if level_str.startswith("Level "):
            level_str = "INFO"  # Default if invalid
        
        # Configure logging with file handler
        log_dir = Path(__file__).resolve().parents[2] / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"
        configure_logging(level=level_str, log_file=log_file)
        
        # Return logger from unified system
        return get_logger(name)
    
    # Fallback to original implementation
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Ensure console handler exists (stderr/stdout)
    if not any(
        type(h).__name__ == "StreamHandler" and not hasattr(h, "baseFilename")
        for h in logger.handlers
    ):
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    # Ensure file handler exists at logs/<name>.log
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / f"{name}.log"
    if not any(
        getattr(h, "baseFilename", None)
        and str(h.baseFilename).lower().endswith(str(file_path).lower())
        for h in logger.handlers
    ):
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
