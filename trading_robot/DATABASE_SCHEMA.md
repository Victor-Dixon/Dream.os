# Trading Robot Database Schema Documentation

**Created**: 2025-12-20  
**Author**: Agent-3 (Infrastructure & DevOps Specialist)

## Overview

The trading robot uses SQLAlchemy ORM for database abstraction, supporting both SQLite (development) and PostgreSQL (production). All database models are defined in `database/models.py`.

## Database Configuration

- **Development**: SQLite (`sqlite:///trading_robot.db`)
- **Production**: PostgreSQL (configured via `DATABASE_URL` environment variable)

See `ENV_SETUP_DOCUMENTATION.md` for database configuration details.

## Tables

### 1. `trades`

Trade execution records storing completed trades.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Primary key |
| `broker_order_id` | String(100) | Broker's order ID (unique, indexed) |
| `symbol` | String(10) | Stock symbol (indexed) |
| `side` | Enum | Order side: `buy`, `sell` |
| `quantity` | Numeric(12,4) | Number of shares |
| `price` | Numeric(12,4) | Execution price per share |
| `commission` | Numeric(10,4) | Commission/fees |
| `total_value` | Numeric(12,2) | Total trade value (quantity × price) |
| `executed_at` | DateTime | Trade execution timestamp (indexed) |
| `created_at` | DateTime | Record creation timestamp |
| `order_id` | Integer (FK) | Foreign key to `orders.id` |
| `strategy_name` | String(100) | Strategy that generated trade |
| `notes` | Text | Additional notes |

**Indexes**:
- `idx_trades_symbol_executed`: (`symbol`, `executed_at`)
- `idx_trades_strategy_executed`: (`strategy_name`, `executed_at`)

### 2. `positions`

Current portfolio positions and their status.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Primary key |
| `symbol` | String(10) | Stock symbol (unique, indexed) |
| `quantity` | Numeric(12,4) | Number of shares held |
| `avg_cost` | Numeric(12,4) | Average cost per share |
| `current_price` | Numeric(12,4) | Current market price |
| `cost_basis` | Numeric(12,2) | Total cost basis (quantity × avg_cost) |
| `market_value` | Numeric(12,2) | Current market value (quantity × current_price) |
| `unrealized_pnl` | Numeric(12,2) | Unrealized profit/loss |
| `unrealized_pnl_pct` | Numeric(8,4) | Unrealized P&L percentage |
| `opened_at` | DateTime | Position opening timestamp |
| `last_updated` | DateTime | Last update timestamp |
| `is_open` | Boolean | Position status (indexed) |
| `closed_at` | DateTime | Position closing timestamp (if closed) |
| `strategy_name` | String(100) | Strategy that opened position |
| `notes` | Text | Additional notes |

### 3. `orders`

Order requests and their status tracking.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Primary key |
| `broker_order_id` | String(100) | Broker's order ID (unique, indexed) |
| `symbol` | String(10) | Stock symbol (indexed) |
| `side` | Enum | Order side: `buy`, `sell` |
| `order_type` | Enum | Order type: `market`, `limit`, `stop`, `stop_limit`, `trailing_stop` |
| `quantity` | Numeric(12,4) | Number of shares |
| `limit_price` | Numeric(12,4) | Limit price (for limit orders) |
| `stop_price` | Numeric(12,4) | Stop price (for stop orders) |
| `time_in_force` | String(20) | Time in force (e.g., "day", "gtc") |
| `status` | Enum | Order status (indexed): `pending`, `submitted`, `partially_filled`, `filled`, `canceled`, `rejected`, `expired` |
| `filled_quantity` | Numeric(12,4) | Quantity filled so far |
| `avg_fill_price` | Numeric(12,4) | Average fill price |
| `submitted_at` | DateTime | Order submission timestamp |
| `filled_at` | DateTime | Order fill completion timestamp |
| `canceled_at` | DateTime | Order cancellation timestamp |
| `created_at` | DateTime | Record creation timestamp (indexed) |
| `updated_at` | DateTime | Last update timestamp |
| `strategy_name` | String(100) | Strategy that generated order |
| `notes` | Text | Additional notes |
| `error_message` | Text | Error message (if order failed) |

**Relationships**:
- One-to-many with `trades` (one order can have multiple trade executions)

**Indexes**:
- `idx_orders_symbol_status`: (`symbol`, `status`)
- `idx_orders_status_created`: (`status`, `created_at`)

### 4. `trading_sessions`

Trading session metadata and statistics.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Primary key |
| `session_name` | String(100) | Session name/identifier |
| `started_at` | DateTime | Session start timestamp (indexed) |
| `ended_at` | DateTime | Session end timestamp |
| `total_trades` | Integer | Total number of trades |
| `winning_trades` | Integer | Number of winning trades |
| `losing_trades` | Integer | Number of losing trades |
| `total_pnl` | Numeric(12,2) | Total profit/loss |
| `total_commission` | Numeric(10,2) | Total commission paid |
| `win_rate` | Numeric(5,2) | Win rate percentage |
| `starting_balance` | Numeric(12,2) | Starting portfolio balance |
| `ending_balance` | Numeric(12,2) | Ending portfolio balance |
| `max_drawdown` | Numeric(8,4) | Maximum drawdown percentage |
| `is_active` | Boolean | Session active status (indexed) |
| `broker` | String(50) | Broker name (e.g., "alpaca") |
| `trading_mode` | String(20) | Trading mode: `paper`, `live` |
| `notes` | Text | Additional notes |

## Relationships

- **Order → Trades**: One-to-many (one order can have multiple trade executions)
- **Trades → Order**: Many-to-one (each trade belongs to one order, nullable)

## Enumerations

### OrderSide
- `buy`
- `sell`

### OrderType
- `market`
- `limit`
- `stop`
- `stop_limit`
- `trailing_stop`

### OrderStatus
- `pending`
- `submitted`
- `partially_filled`
- `filled`
- `canceled`
- `rejected`
- `expired`

### MetricType
- `daily`
- `weekly`
- `monthly`
- `all_time`

## Database Initialization

### Development (SQLite)

1. Database file is automatically created: `trading_robot.db`
2. Initialize tables:
   ```bash
   python scripts/init_database.py
   ```

### Production (PostgreSQL)

1. Create database:
   ```sql
   CREATE DATABASE trading_robot;
   ```

2. Configure `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/trading_robot
   ```

3. Initialize tables:
   ```bash
   python scripts/init_database.py
   ```

## Backup and Restore

### Backup

```bash
# Create backup
python scripts/backup_database.py

# Specify backup directory
python scripts/backup_database.py /path/to/backups
```

**SQLite**: Creates copy of `.db` file  
**PostgreSQL**: Uses `pg_dump` to create custom format backup

### Restore

```python
from database.backup import restore_database
from pathlib import Path

# Restore from backup
restore_database(Path("backups/trading_robot_20251220_120000.db"), confirm=True)
```

**SQLite**: Copies backup file over current database  
**PostgreSQL**: Uses `pg_restore` to restore from backup

## Usage Examples

### Initialize Database

```python
from database.connection import init_database

# Create all tables
init_database(create_tables=True)
```

### Create Session

```python
from database.connection import get_db_session
from database.models import Order, OrderSide, OrderType, OrderStatus

with get_db_session() as session:
    # Create new order
    order = Order(
        symbol="AAPL",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=10.0,
        status=OrderStatus.PENDING,
    )
    session.add(order)
    # session.commit() is called automatically when context exits
```

### Query Data

```python
from database.connection import get_db_session
from database.models import Trade

with get_db_session() as session:
    # Get recent trades
    recent_trades = session.query(Trade).order_by(
        Trade.executed_at.desc()
    ).limit(10).all()
    
    for trade in recent_trades:
        print(f"{trade.symbol} {trade.side} {trade.quantity} @ {trade.price}")
```

## Migration Strategy

For future schema changes:

1. Create migration scripts in `database/migrations/`
2. Use Alembic (recommended) for production migrations
3. For development (SQLite), recreate database or use manual migration scripts

## Next Steps

- Add Alembic for production migrations
- Implement database versioning
- Add performance tracking tables (user_performance_metrics, etc.)
- Add user account system tables (users, user_plugin_access, user_trading_accounts)

## See Also

- `ENV_SETUP_DOCUMENTATION.md`: Environment variable configuration
- `database/connection.py`: Database connection utilities
- `database/models.py`: SQLAlchemy model definitions
- `database/backup.py`: Backup and restore utilities
- `scripts/init_database.py`: Database initialization script
