"""
Minimal unified logging system stub for trading_robot tests.
"""

import logging


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


__all__ = ["get_logger"]








