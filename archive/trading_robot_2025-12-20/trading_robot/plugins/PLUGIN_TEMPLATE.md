# Plugin Template Guide

This document shows the complete structure of a trading robot plugin using the TSLA Improved Strategy as an example.

---

## 📁 Plugin Directory Structure

```
plugins/robots/{plugin_id}/
├── __init__.py              # Plugin exports
├── {plugin_id}.py          # Main strategy implementation
└── metadata.json           # Plugin metadata
```

**Example:**
```
plugins/robots/tsla_improved_strategy/
├── __init__.py
├── tsla_improved_strategy.py
└── metadata.json
```

---

## 1. `__init__.py` - Plugin Exports

**File:** `plugins/robots/{plugin_id}/__init__.py`

```python
"""
{Plugin Name} Plugin
===================

{Description of what the plugin does}
"""

from .{plugin_id} import {PluginClass}

__all__ = ["{PluginClass}"]
```

**Example:**
```python
"""
TSLA Improved Strategy Plugin
==============================

Risk-based TSLA trading strategy with MA crossover and RSI filtering.
"""

from .tsla_improved_strategy import TslaImprovedStrategy

__all__ = ["TslaImprovedStrategy"]
```

---

## 2. `metadata.json` - Plugin Metadata

**File:** `plugins/robots/{plugin_id}/metadata.json`

```json
{
  "plugin_id": "your_plugin_id",
  "name": "Your Plugin Name",
  "version": "1.0.0",
  "description": "Detailed description of what your strategy does, how it works, and what makes it unique.",
  "author": "Your Name or Company",
  "symbol": "SYMBOL",
  "strategy_type": "Trend Following | Mean Reversion | Breakout | etc.",
  "created_date": "2025-12-15T00:00:00",
  "updated_date": "2025-12-15T00:00:00",
  "is_for_sale": true,
  "price": 99.99,
  "currency": "USD",
  "sales_count": 0,
  "rating": 0.0,
  "review_count": 0,
  "total_pnl": 0.0,
  "total_trades": 0,
  "win_rate": 0.0,
  "sharpe_ratio": 0.0,
  "max_drawdown": 0.0,
  "default_parameters": {
    "param1": 50,
    "param2": 200,
    "param3": 14
  },
  "required_parameters": [],
  "tags": [
    "SYMBOL",
    "Strategy Type",
    "Key Features"
  ],
  "category": "Trend Following",
  "documentation_url": null,
  "support_url": null
}
```

**Example (TSLA Improved Strategy):**
```json
{
  "plugin_id": "tsla_improved_strategy",
  "name": "TSLA Improved Strategy (Risk-True)",
  "version": "1.0.0",
  "description": "Risk-based TSLA trading strategy using 50/200 MA crossover with RSI filtering. True risk-based position sizing with 0.5% equity risk per trade, 1% stop loss, and 15% profit target. Includes optional trailing stop functionality.",
  "author": "TradingRobotPlug",
  "symbol": "TSLA",
  "strategy_type": "Trend Following",
  "created_date": "2025-12-15T00:00:00",
  "updated_date": "2025-12-15T00:00:00",
  "is_for_sale": true,
  "price": 99.99,
  "currency": "USD",
  "sales_count": 0,
  "rating": 0.0,
  "review_count": 0,
  "total_pnl": 0.0,
  "total_trades": 0,
  "win_rate": 0.0,
  "sharpe_ratio": 0.0,
  "max_drawdown": 0.0,
  "default_parameters": {
    "ma_short_length": 50,
    "ma_long_length": 200,
    "rsi_length": 14,
    "rsi_overbought": 60,
    "rsi_oversold": 40,
    "risk_pct_equity": 0.5,
    "stop_pct_price": 1.0,
    "target_pct_price": 15.0,
    "use_trailing_stop": true,
    "trail_offset_pct": 0.5,
    "trail_trigger_pct": 5.0
  },
  "required_parameters": [],
  "tags": [
    "TSLA",
    "Trend Following",
    "MA Crossover",
    "RSI",
    "Risk-Based",
    "Paper Trading"
  ],
  "category": "Trend Following",
  "documentation_url": null,
  "support_url": null
}
```

---

## 3. `{plugin_id}.py` - Strategy Implementation

**File:** `plugins/robots/{plugin_id}/{plugin_id}.py`

```python
"""
{Plugin Name} ({Strategy Type})
================================

{Description of strategy and what it does}

{Optional: Original source if converted from another language}
"""

from typing import Any, Dict
import pandas as pd
import numpy as np
from loguru import logger

from strategies.signal_processing import Signal, StrategyResult
from plugins.plugin_base import PluginBase
from plugins.plugin_metadata import PluginMetadata


class {PluginClass}(PluginBase):
    """{Plugin Name} with {key feature}."""

    def __init__(self, metadata: PluginMetadata, parameters: Dict[str, Any] = None):
        """Initialize strategy."""
        super().__init__(metadata, parameters)

        # Load parameters from metadata or use defaults
        self.param1 = self.parameters.get("param1", 50)
        self.param2 = self.parameters.get("param2", 200)
        # ... more parameters

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal."""
        # Validate data
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Invalid data"})

        # Check minimum data requirements
        if len(data) < self.param2:  # Use longest period needed
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Insufficient data"})

        try:
            # Calculate indicators
            indicator1 = self.indicators.sma(data["close"], self.param1)
            indicator2 = self.indicators.rsi(data["close"], 14)
            # ... more indicators

            # Get latest values
            current_price = data["close"].iloc[-1]
            indicator1_val = indicator1.iloc[-1] if isinstance(indicator1, pd.Series) else indicator1
            indicator2_val = indicator2.iloc[-1] if isinstance(indicator2, pd.Series) else indicator2

            # Entry conditions
            long_condition = (current_price > indicator1_val) and (indicator2_val < 70)
            short_condition = (current_price < indicator1_val) and (indicator2_val > 30)

            # Determine signal
            if long_condition:
                signal = Signal.BUY
                confidence = 0.8  # Calculate based on your logic
            elif short_condition:
                signal = Signal.SELL
                confidence = 0.8
            else:
                signal = Signal.HOLD
                confidence = 0.0

            # Metadata with indicator values
            metadata = {
                "indicator1": round(indicator1_val, 2),
                "indicator2": round(indicator2_val, 2),
                "current_price": round(current_price, 2),
                "long_condition": long_condition,
                "short_condition": short_condition,
            }

            return StrategyResult(symbol, signal, confidence, indicators=metadata)

        except Exception as e:
            logger.error(f"Error in {self.name} analysis: {e}")
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": str(e)})

    def calculate_entry_quantity(
        self, account_balance: float, price: float, stop_loss_price: float
    ) -> int:
        """Calculate position size based on risk model."""
        # Risk amount = equity * risk percentage
        risk_pct = self.parameters.get("risk_pct_equity", 0.5)
        risk_amount = account_balance * (risk_pct / 100.0)

        # Stop distance in price
        stop_dist = abs(price - stop_loss_price)

        # Avoid divide-by-zero
        min_tick = 0.01
        safe_stop_dist = max(stop_dist, min_tick * 10)

        # Quantity = risk amount / stop distance
        raw_qty = risk_amount / safe_stop_dist
        qty = int(np.floor(raw_qty))

        if qty < 1:
            logger.warning(f"Calculated quantity {qty} is too small, skipping trade")
            return 0

        logger.info(f"📊 Position sizing: Risk ${risk_amount:.2f}, Stop ${safe_stop_dist:.2f}, Qty: {qty}")
        return qty

    def calculate_stop_loss(self, entry_price: float, is_long: bool) -> float:
        """Calculate stop loss price."""
        stop_pct = self.parameters.get("stop_pct_price", 1.0) / 100.0
        if is_long:
            return entry_price * (1 - stop_pct)
        else:  # Short
            return entry_price * (1 + stop_pct)

    def calculate_profit_target(self, entry_price: float, is_long: bool) -> float:
        """Calculate profit target price."""
        target_pct = self.parameters.get("target_pct_price", 15.0) / 100.0
        if is_long:
            return entry_price * (1 + target_pct)
        else:  # Short
            return entry_price * (1 - target_pct)
```

**Example (TSLA Improved Strategy - Key Parts):**

```python
"""
TSLA Improved Strategy (Risk-True)
===================================

Risk-based TSLA trading strategy converted from TradingView Pine Script.
Uses 50/200 MA crossover with RSI filtering and true risk-based position sizing.

Original Pine Script: Improved TSLA Strategy (Risk-True)
"""

from typing import Any, Dict
import pandas as pd
import numpy as np
from loguru import logger

from strategies.signal_processing import Signal, StrategyResult
from plugins.plugin_base import PluginBase
from plugins.plugin_metadata import PluginMetadata


class TslaImprovedStrategy(PluginBase):
    """TSLA Improved Strategy with risk-based position sizing."""

    def __init__(self, metadata: PluginMetadata, parameters: Dict[str, Any] = None):
        """Initialize TSLA strategy."""
        super().__init__(metadata, parameters)

        # Trend parameters
        self.ma_short_length = self.parameters.get("ma_short_length", 50)
        self.ma_long_length = self.parameters.get("ma_long_length", 200)

        # RSI parameters
        self.rsi_length = self.parameters.get("rsi_length", 14)
        self.rsi_overbought = self.parameters.get("rsi_overbought", 60)
        self.rsi_oversold = self.parameters.get("rsi_oversold", 40)

        # Risk model
        self.risk_pct_equity = self.parameters.get("risk_pct_equity", 0.5)
        self.stop_pct_price = self.parameters.get("stop_pct_price", 1.0)

        # Reward parameters
        self.target_pct_price = self.parameters.get("target_pct_price", 15.0)
        self.use_trailing_stop = self.parameters.get("use_trailing_stop", True)
        self.trail_offset_pct = self.parameters.get("trail_offset_pct", 0.5)
        self.trail_trigger_pct = self.parameters.get("trail_trigger_pct", 5.0)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal."""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Invalid data"})

        if len(data) < self.ma_long_length:
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Insufficient data"})

        try:
            # Calculate indicators
            ma_short = self.indicators.sma(data["close"], self.ma_short_length)
            ma_long = self.indicators.sma(data["close"], self.ma_long_length)
            rsi = self.indicators.rsi(data["close"], self.rsi_length)

            # Get latest values
            current_price = data["close"].iloc[-1]
            ma_short_val = ma_short.iloc[-1] if isinstance(ma_short, pd.Series) else ma_short
            ma_long_val = ma_long.iloc[-1] if isinstance(ma_long, pd.Series) else ma_long
            rsi_val = rsi.iloc[-1] if isinstance(rsi, pd.Series) else rsi

            # Entry conditions
            long_condition = (current_price > ma_short_val and current_price > ma_long_val) and (rsi_val < self.rsi_overbought)
            short_condition = (current_price < ma_short_val and current_price < ma_long_val) and (rsi_val > self.rsi_oversold)

            # Determine signal
            if long_condition:
                signal = Signal.BUY
                confidence = min((current_price - ma_long_val) / ma_long_val * 10, 1.0)
            elif short_condition:
                signal = Signal.SELL
                confidence = min((ma_long_val - current_price) / ma_long_val * 10, 1.0)
            else:
                signal = Signal.HOLD
                confidence = 0.0

            # Metadata
            metadata = {
                "ma_short": round(ma_short_val, 2),
                "ma_long": round(ma_long_val, 2),
                "rsi": round(rsi_val, 2),
                "current_price": round(current_price, 2),
                "long_condition": long_condition,
                "short_condition": short_condition,
            }

            return StrategyResult(symbol, signal, confidence, indicators=metadata)

        except Exception as e:
            logger.error(f"Error in TSLA strategy analysis: {e}")
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": str(e)})

    def calculate_entry_quantity(
        self, account_balance: float, price: float, stop_loss_price: float
    ) -> int:
        """Calculate position size based on risk model."""
        risk_amount = account_balance * (self.risk_pct_equity / 100.0)
        stop_dist = abs(price - stop_loss_price)
        safe_stop_dist = max(stop_dist, 0.01 * 10)
        raw_qty = risk_amount / safe_stop_dist
        qty = int(np.floor(raw_qty))
        
        if qty < 1:
            return 0
        return qty

    def calculate_stop_loss(self, entry_price: float, is_long: bool) -> float:
        """Calculate stop loss price."""
        stop_pct = self.stop_pct_price / 100.0
        return entry_price * (1 - stop_pct) if is_long else entry_price * (1 + stop_pct)

    def calculate_profit_target(self, entry_price: float, is_long: bool) -> float:
        """Calculate profit target price."""
        target_pct = self.target_pct_price / 100.0
        return entry_price * (1 + target_pct) if is_long else entry_price * (1 - target_pct)
```

---

## 📋 Required Methods

Every plugin **MUST** implement these 4 methods:

1. **`analyze(data, symbol)`** - Generate trading signals
2. **`calculate_entry_quantity(account_balance, price, stop_loss_price)`** - Position sizing
3. **`calculate_stop_loss(entry_price, is_long)`** - Stop loss calculation
4. **`calculate_profit_target(entry_price, is_long)`** - Profit target calculation

---

## 🎯 Key Points

### Plugin ID Naming
- Use lowercase with underscores: `my_strategy`, `tsla_improved_strategy`
- Must match directory name: `plugins/robots/{plugin_id}/`

### Class Naming
- Convert plugin_id to PascalCase: `my_strategy` → `MyStrategy`
- Class name must match in `__init__.py` export

### Parameters
- All parameters should be in `metadata.json` → `default_parameters`
- Access via `self.parameters.get("param_name", default_value)`

### Signals
- Return `Signal.BUY`, `Signal.SELL`, or `Signal.HOLD`
- Include confidence (0.0 to 1.0)
- Include metadata/indicators for debugging

### Risk Management
- Always use risk-based position sizing
- Calculate stop loss and profit target
- Log important decisions

---

## ✅ Checklist

Before your plugin is ready:

- [ ] All 4 required methods implemented
- [ ] `metadata.json` complete and valid JSON
- [ ] `__init__.py` exports the class correctly
- [ ] Class name matches plugin_id (PascalCase)
- [ ] Parameters defined in `default_parameters`
- [ ] Error handling in `analyze()` method
- [ ] Data validation before analysis
- [ ] Logging for important events
- [ ] Tested with `run_daily_automation.py`

---

## 🚀 Quick Start

1. **Create directory:**
   ```bash
   mkdir -p plugins/robots/my_strategy
   ```

2. **Copy template files:**
   - Copy `metadata.json` and update values
   - Copy `{plugin_id}.py` and implement your strategy
   - Copy `__init__.py` and update class name

3. **Test:**
   ```bash
   python run_daily_automation.py
   ```

---

**🐝 WE. ARE. SWARM. ⚡🔥**

