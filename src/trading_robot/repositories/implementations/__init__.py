# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
<!-- SSOT Domain: trading_robot -->
"""

from . import in_memory_query_operations
from . import in_memory_trading_repository
from . import in_memory_write_operations
from . import trading_query_operations
from . import trading_repository_impl
from . import trading_write_operations

# Export TradingRepositoryImpl if available
try:
    from .trading_repository_impl import TradingRepositoryImpl
except ImportError:
    TradingRepositoryImpl = None

# Stub classes for missing implementations (to be implemented)
PortfolioRepositoryImpl = None
PositionRepositoryImpl = None

__all__ = [
    'in_memory_query_operations',
    'in_memory_trading_repository',
    'in_memory_write_operations',
    'trading_query_operations',
    'trading_repository_impl',
    'trading_write_operations',
    'TradingRepositoryImpl',
    'PortfolioRepositoryImpl',
    'PositionRepositoryImpl',
]
