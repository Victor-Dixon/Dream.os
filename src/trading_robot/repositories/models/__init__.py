# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: trading_robot -->
"""

from . import portfolio
from . import position
from . import trade
from . import trading_models

# Export classes for direct imports (prefer dedicated modules over trading_models)
from .portfolio import Portfolio
from .position import Position
from .trade import Trade

__all__ = [
    'portfolio',
    'position',
    'trade',
    'trading_models',
    # Class exports
    'Portfolio',
    'Position',
    'Trade',
]
