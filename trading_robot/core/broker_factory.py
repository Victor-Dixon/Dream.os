"""
Broker Factory - Creates broker client instances based on configuration
"""
from typing import Optional
from loguru import logger

from config.settings import config
from .broker_interface import BrokerInterface
from .alpaca_client import AlpacaClient
from .robinhood_client import RobinhoodClient


def create_broker_client(broker_name: Optional[str] = None) -> BrokerInterface:
    """
    Factory function to create broker client based on configuration.
    
    Args:
        broker_name: Optional broker name override. If None, uses config.broker
        
    Returns:
        BrokerInterface: Broker client instance
        
    Raises:
        ValueError: If broker name is invalid or not supported
    """
    broker = broker_name or config.broker.lower()
    
    if broker == "alpaca":
        logger.info("📊 Creating Alpaca broker client")
        return AlpacaClient()
    
    elif broker == "robinhood":
        logger.info("📊 Creating Robinhood broker client")
        logger.warning("⚠️ Robinhood integration uses unofficial robin_stocks library")
        logger.warning("⚠️ May violate Robinhood Terms of Service - use at your own risk")
        return RobinhoodClient()
    
    else:
        raise ValueError(
            f"Unsupported broker: {broker}. "
            f"Supported brokers: 'alpaca', 'robinhood'"
        )







