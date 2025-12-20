"""
Trading Robot Configuration Settings
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List
import os


class TradingConfig(BaseSettings):
    """Trading Robot Configuration"""

    # Trading Mode Configuration (CRITICAL SAFEGUARD)
    trading_mode: str = "paper"  # "paper" or "live"
    live_trading_enabled: bool = False  # Explicit flag - must be True for live trading

    # Broker Selection
    broker: str = "alpaca"  # "alpaca" or "robinhood"

    # Alpaca API Configuration
    alpaca_api_key: str = ""
    alpaca_secret_key: str = ""
    alpaca_base_url: str = "https://paper-api.alpaca.markets"  # Paper trading by default
    alpaca_feed: str = "iex"  # Market data feed

    # Robinhood Configuration (uses robin_stocks library)
    robinhood_username: str = ""
    robinhood_password: str = ""

    # Trading Configuration
    max_positions: int = 10
    max_position_size_pct: float = 0.1  # Max 10% of portfolio per position
    max_portfolio_risk_pct: float = 0.05  # Max 5% portfolio risk
    default_stop_loss_pct: float = 0.02  # 2% stop loss
    default_take_profit_pct: float = 0.04  # 4% take profit

    # Risk Management
    daily_loss_limit_pct: float = 0.03  # Stop trading if daily loss exceeds 3%
    max_daily_trades: int = 20
    min_order_value: float = 100.0
    max_order_value: float = 10000.0

    # Trading Hours (EST)
    market_open_hour: int = 9
    market_close_hour: int = 16
    trading_days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Database Configuration
    database_url: str = "sqlite:///trading_robot.db"
    redis_url: Optional[str] = None

    # Web Dashboard
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    enable_dashboard: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/trading_robot.log"

    # Backtesting
    backtest_initial_balance: float = 100000.0
    backtest_commission_pct: float = 0.001  # 0.1% commission
    backtest_slippage_pct: float = 0.0005  # 0.05% slippage

    # Alert Configuration
    enable_email_alerts: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    alert_email_recipients: List[str] = []

    # Emergency Configuration
    emergency_stop_enabled: bool = True
    emergency_stop_loss_pct: float = 0.1  # Emergency stop at 10% loss
    emergency_shutdown_timeout: int = 300  # 5 minutes timeout

    # Initial Balance (for risk calculations)
    initial_balance: float = 100000.0

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env file (Discord bot config, etc.)
    )

    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate configuration for trading readiness."""
        errors = []

        # Validate API credentials
        if not self.alpaca_api_key or self.alpaca_api_key == "":
            errors.append("ALPACA_API_KEY is required")
        if not self.alpaca_secret_key or self.alpaca_secret_key == "":
            errors.append("ALPACA_SECRET_KEY is required")

        # Validate trading mode
        if self.trading_mode not in ["paper", "live"]:
            errors.append(f"Invalid TRADING_MODE: {self.trading_mode}. Must be 'paper' or 'live'")

        # Validate live trading safeguards
        if self.trading_mode == "live":
            if not self.live_trading_enabled:
                errors.append(
                    "Live trading mode requires LIVE_TRADING_ENABLED=true. "
                    "This is a safety safeguard."
                )
            if "paper-api" in self.alpaca_base_url:
                errors.append(
                    "Live trading mode detected but ALPACA_BASE_URL points to paper trading API. "
                    "Use https://api.alpaca.markets for live trading."
                )

        # Validate risk limits
        if self.daily_loss_limit_pct <= 0 or self.daily_loss_limit_pct > 0.1:
            errors.append("DAILY_LOSS_LIMIT_PCT should be between 0 and 0.1 (0-10%)")
        if self.max_position_size_pct <= 0 or self.max_position_size_pct > 0.5:
            errors.append("MAX_POSITION_SIZE_PCT should be between 0 and 0.5 (0-50%)")
        if self.max_daily_trades <= 0:
            errors.append("MAX_DAILY_TRADES must be greater than 0")

        return len(errors) == 0, errors

    def is_live_trading(self) -> bool:
        """Check if configuration is set for live trading."""
        return self.trading_mode == "live" and self.live_trading_enabled

    def is_paper_trading(self) -> bool:
        """Check if configuration is set for paper trading."""
        return self.trading_mode == "paper" or not self.live_trading_enabled


# Global configuration instance
config = TradingConfig()
