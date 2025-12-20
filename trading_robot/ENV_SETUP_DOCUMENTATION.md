# Trading Robot Environment Variable Documentation

**Created**: 2025-12-20  
**Author**: Agent-3 (Infrastructure & DevOps Specialist)

## Overview

This document describes all environment variables used by the Trading Robot system. The `.env` file should be created from `env.example` and configured according to your setup.

## Quick Start

1. Copy the example file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your Alpaca API credentials (required for paper trading)

3. Validate configuration:
   ```bash
   python -c "from config.settings import config; is_valid, errors = config.validate_config(); print('Valid' if is_valid else 'Errors:', errors)"
   ```

## Required Variables (Paper Trading)

### ALPACA_API_KEY
- **Required**: Yes (for paper trading)
- **Description**: Your Alpaca API key for paper trading
- **How to get**: https://app.alpaca.markets/paper/dashboard/overview
- **Example**: `PKXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

### ALPACA_SECRET_KEY
- **Required**: Yes (for paper trading)
- **Description**: Your Alpaca secret key for paper trading
- **How to get**: https://app.alpaca.markets/paper/dashboard/overview
- **Security**: Keep this secret, never commit to git

## Trading Mode Configuration

### TRADING_MODE
- **Required**: Yes
- **Options**: `paper` or `live`
- **Default**: `paper`
- **Description**: Trading mode (use `paper` for testing, `live` for real trading)
- **Recommendation**: Always start with `paper` until validated

### LIVE_TRADING_ENABLED
- **Required**: Yes (if TRADING_MODE=live)
- **Options**: `true` or `false`
- **Default**: `false`
- **Description**: Explicit flag required for live trading (safety safeguard)
- **Warning**: Only set to `true` after extensive paper trading validation

## Broker Configuration

### BROKER
- **Required**: Yes
- **Options**: `alpaca` or `robinhood`
- **Default**: `alpaca`
- **Description**: Trading broker selection

### ALPACA_BASE_URL
- **Required**: Yes (if broker=alpaca)
- **Options**: 
  - Paper: `https://paper-api.alpaca.markets` (default)
  - Live: `https://api.alpaca.markets`
- **Default**: `https://paper-api.alpaca.markets`
- **Description**: Alpaca API endpoint URL

### ALPACA_FEED
- **Required**: No
- **Options**: `iex`, `sip` (live only)
- **Default**: `iex`
- **Description**: Market data feed type

## Risk Management (Conservative Defaults)

### MAX_POSITIONS
- **Default**: `10`
- **Description**: Maximum number of concurrent positions
- **Recommended**: 5-10 for conservative trading

### MAX_POSITION_SIZE_PCT
- **Default**: `0.1` (10%)
- **Description**: Maximum percentage of portfolio per position
- **Recommended**: 0.05-0.1 (5-10%) for conservative trading

### MAX_PORTFOLIO_RISK_PCT
- **Default**: `0.05` (5%)
- **Description**: Maximum portfolio risk percentage
- **Recommended**: 0.03-0.05 (3-5%) for conservative trading

### DAILY_LOSS_LIMIT_PCT
- **Default**: `0.03` (3%)
- **Description**: Stop trading if daily loss exceeds this percentage
- **Recommended**: 0.02-0.03 (2-3%) for conservative trading

### MAX_DAILY_TRADES
- **Default**: `20`
- **Description**: Maximum number of trades per day
- **Recommended**: 10-20 for conservative trading

### DEFAULT_STOP_LOSS_PCT
- **Default**: `0.02` (2%)
- **Description**: Default stop loss percentage per trade

### DEFAULT_TAKE_PROFIT_PCT
- **Default**: `0.04` (4%)
- **Description**: Default take profit percentage per trade

## Database Configuration

### DATABASE_URL (Development - SQLite)
- **Default**: `sqlite:///trading_robot.db`
- **Description**: SQLite database file (auto-created, no setup required)
- **Use Case**: Development, testing, paper trading

### DATABASE_URL (Production - PostgreSQL)
- **Format**: `postgresql://user:password@host:port/database`
- **Example**: `postgresql://trading_user:password@localhost:5432/trading_robot`
- **Use Case**: Production, live trading
- **Note**: Requires PostgreSQL database setup

### REDIS_URL
- **Default**: (empty, optional)
- **Description**: Redis connection URL (for Celery/task queue)
- **Format**: `redis://localhost:6379/0`
- **Use Case**: Advanced features, task queuing

## Logging Configuration

### LOG_LEVEL
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`
- **Description**: Logging verbosity level

### LOG_FILE
- **Default**: `logs/trading_robot.log`
- **Description**: Path to log file (relative to trading_robot directory)
- **Note**: Log directory will be created automatically

## Web Dashboard

### WEB_HOST
- **Default**: `0.0.0.0`
- **Description**: Dashboard host (0.0.0.0 = all interfaces)

### WEB_PORT
- **Default**: `8000`
- **Description**: Dashboard port number

### ENABLE_DASHBOARD
- **Options**: `true` or `false`
- **Default**: `true`
- **Description**: Enable web dashboard

## Emergency Configuration

### EMERGENCY_STOP_ENABLED
- **Options**: `true` or `false`
- **Default**: `true`
- **Description**: Enable emergency stop functionality

### EMERGENCY_STOP_LOSS_PCT
- **Default**: `0.1` (10%)
- **Description**: Emergency stop triggers at this portfolio loss percentage

### EMERGENCY_SHUTDOWN_TIMEOUT
- **Default**: `300` (5 minutes)
- **Description**: Timeout in seconds for emergency shutdown

## Validation

The configuration is automatically validated using `config.validate_config()`. Validation checks:

1. **API Credentials**: ALPACA_API_KEY and ALPACA_SECRET_KEY must be set
2. **Trading Mode**: Must be "paper" or "live"
3. **Live Trading Safeguards**: 
   - LIVE_TRADING_ENABLED=true required for live trading
   - ALPACA_BASE_URL must not point to paper API for live trading
4. **Risk Limits**: 
   - DAILY_LOSS_LIMIT_PCT: 0-10%
   - MAX_POSITION_SIZE_PCT: 0-50%
   - MAX_DAILY_TRADES: > 0

## Next Steps

1. **Fill in Alpaca API credentials** in `.env` file
2. **Review risk limits** (defaults are conservative)
3. **Run validation** to ensure configuration is correct
4. **Start with paper trading** to validate system
5. **Upgrade to live trading** only after extensive validation

## Security Notes

- ⚠️ **Never commit `.env` file to git** (it's in .gitignore)
- ⚠️ **Keep API keys secret** - treat them like passwords
- ⚠️ **Use paper trading first** - validate system before live trading
- ⚠️ **Review risk limits** - defaults are conservative but adjust based on your risk tolerance
