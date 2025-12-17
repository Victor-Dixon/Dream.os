# Trading Robot Plugin System

## Overview

The plugin system allows you to create, test, and sell trading robot strategies. Each plugin is a self-contained trading strategy that can be:

- **Paper Traded**: Test strategies without risking real money
- **Performance Tracked**: Monitor P&L, win rate, and other metrics
- **Sold**: Offer successful strategies for sale in the marketplace

## Plugin Structure

Each plugin is located in `plugins/robots/{plugin_id}/` and contains:

```
plugins/robots/{plugin_id}/
├── __init__.py              # Plugin exports
├── {plugin_id}.py          # Main strategy implementation
└── metadata.json           # Plugin metadata (name, price, performance, etc.)
```

## Creating a Plugin

### 1. Create Plugin Directory

```bash
mkdir -p plugins/robots/my_strategy
```

### 2. Create Plugin Class

Create `plugins/robots/my_strategy/my_strategy.py`:

```python
from plugins.plugin_base import PluginBase
from plugins.plugin_metadata import PluginMetadata
from strategies.signal_processing import Signal, StrategyResult
import pandas as pd

class MyStrategy(PluginBase):
    def __init__(self, metadata, parameters=None):
        super().__init__(metadata, parameters)
        # Initialize your strategy parameters
        
    def analyze(self, data, symbol):
        # Your strategy logic here
        return StrategyResult(symbol, Signal.BUY, 0.8)
        
    def calculate_entry_quantity(self, account_balance, price, stop_loss):
        # Risk-based position sizing
        return 100
        
    def calculate_stop_loss(self, entry_price, is_long):
        # Calculate stop loss
        return entry_price * 0.98 if is_long else entry_price * 1.02
        
    def calculate_profit_target(self, entry_price, is_long):
        # Calculate profit target
        return entry_price * 1.05 if is_long else entry_price * 0.95
```

### 3. Create Metadata

Create `plugins/robots/my_strategy/metadata.json`:

```json
{
  "plugin_id": "my_strategy",
  "name": "My Trading Strategy",
  "version": "1.0.0",
  "description": "Description of your strategy",
  "author": "Your Name",
  "symbol": "TSLA",
  "strategy_type": "Trend Following",
  "is_for_sale": true,
  "price": 99.99,
  "default_parameters": {},
  "tags": ["TSLA", "Trend Following"]
}
```

## Running Daily Automation

### Manual Execution

```bash
python run_daily_automation.py
```

### Scheduled Execution (Cron/Windows Task Scheduler)

Set up to run daily at market open (e.g., 9:30 AM ET):

**Windows Task Scheduler:**
- Create task to run `python run_daily_automation.py` daily at 9:30 AM

**Linux/Mac Cron:**
```bash
30 9 * * 1-5 cd /path/to/trading_robot && python run_daily_automation.py
```

## Performance Tracking

Each plugin automatically tracks:
- Total P&L
- Win rate
- Profit factor
- Average win/loss
- Total trades

Access performance:

```python
from plugins.plugin_manager import PluginManager

manager = PluginManager()
plugin = manager.load_plugin("tsla_improved_strategy")
performance = plugin.get_performance_summary()
print(performance)
```

## Marketplace

### List Plugins for Sale

```python
from plugins.marketplace import Marketplace
from plugins.plugin_manager import PluginManager

manager = PluginManager()
marketplace = Marketplace(manager)

plugins_for_sale = marketplace.list_plugins_for_sale()
for plugin in plugins_for_sale:
    print(f"{plugin.name}: ${plugin.price}")
```

### Purchase a Plugin

```python
buyer_info = {
    "email": "buyer@example.com",
    "name": "John Doe"
}

success = marketplace.purchase_plugin("tsla_improved_strategy", buyer_info)
```

## TSLA Improved Strategy

The first plugin (`tsla_improved_strategy`) implements:

- **50/200 MA Crossover**: Trend following with moving averages
- **RSI Filtering**: Avoids overbought/oversold conditions
- **Risk-Based Sizing**: 0.5% equity risk per trade
- **Stop Loss**: 1% of entry price
- **Profit Target**: 15% of entry price
- **Trailing Stop**: Optional trailing stop functionality

### Parameters

- `ma_short_length`: 50 (default)
- `ma_long_length`: 200 (default)
- `rsi_length`: 14 (default)
- `rsi_overbought`: 60 (default)
- `rsi_oversold`: 40 (default)
- `risk_pct_equity`: 0.5 (default)
- `stop_pct_price`: 1.0 (default)
- `target_pct_price`: 15.0 (default)
- `use_trailing_stop`: true (default)

## Data Storage

Plugin data is stored in `data/plugins/{plugin_id}/`:

- `trades.jsonl`: All paper trades (one per line)
- `daily_plans.jsonl`: Daily plan execution results

## Next Steps

1. **Run Daily Automation**: Set up scheduled execution
2. **Monitor Performance**: Track P&L and win rate
3. **Optimize Strategy**: Adjust parameters based on results
4. **List for Sale**: Once profitable, enable marketplace listing
5. **Create More Robots**: Build your army of trading robots!

---

**🐝 WE. ARE. SWARM. ⚡🔥**

