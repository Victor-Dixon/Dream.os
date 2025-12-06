# Trading Replay Journal Service

**Domain**: Business Intelligence (Agent-5)  
**SSOT Tag**: `<!-- SSOT Domain: business-intelligence -->`  
**Status**: ✅ Active Service

---

## Purpose

Interactive market replay training system with behavioral scoring. Provides candle-by-candle replay simulation, paper trading, journaling, and behavioral analysis.

---

## CLI Commands

### Create Session
```bash
python -m src.services.trader_replay.trader_replay_cli create \
  --symbol AAPL \
  --date 2024-01-15 \
  --timeframe 1m \
  --agent Agent-5
```

### Start Replay
```bash
python -m src.services.trader_replay.trader_replay_cli start \
  --session-id 1
```

### Step Replay
```bash
python -m src.services.trader_replay.trader_replay_cli step \
  --session-id 1 \
  --direction forward
```

### Pause Replay
```bash
python -m src.services.trader_replay.trader_replay_cli pause \
  --session-id 1
```

### Get Status
```bash
python -m src.services.trader_replay.trader_replay_cli status \
  --session-id 1
```

---

## Data Model

### Sessions
- **id**: Primary key
- **symbol_id**: Foreign key to symbols
- **session_date**: Date (YYYY-MM-DD)
- **timeframe**: Candle timeframe (e.g., "1m")
- **candle_count**: Number of candles
- **status**: ready, in_progress, completed, paused
- **UNIQUE(symbol_id, session_date, timeframe)**: Prevents duplicates

### Candles
- **id**: Primary key
- **session_id**: Foreign key to sessions
- **timestamp**: ISO timestamp
- **open, high, low, close**: OHLC prices
- **volume**: Trade volume
- **candle_index**: Order within session
- **UNIQUE(session_id, timestamp)**: Ensures no duplicates

### Paper Trades
- **id**: Primary key
- **session_id**: Foreign key to sessions
- **entry_timestamp, exit_timestamp**: Trade timestamps
- **entry_price, exit_price**: Trade prices
- **quantity**: Position size
- **side**: long or short
- **stop_loss, take_profit**: Risk management
- **pnl, r_multiple**: Performance metrics
- **status**: open, closed, stopped

### Journal Entries
- **id**: Primary key
- **session_id**: Foreign key to sessions
- **timestamp**: Entry timestamp
- **candle_index**: Optional candle reference
- **trade_id**: Optional trade reference
- **entry_type**: note, setup, trigger, risk, result, lesson
- **content**: Entry text
- **emotion_tag**: Optional emotion label

### Scores
- **id**: Primary key
- **session_id**: Foreign key to sessions
- **score_type**: stop_integrity, patience, risk_discipline, rule_adherence
- **score_value**: 0-100 score
- **details**: JSON with score breakdown
- **UNIQUE(session_id, score_type)**: One score per type per session

---

## Scoring Definitions

### Stop Integrity (0-100)
Measures adherence to stop loss rules.

**Components**:
- Stop usage rate: Percentage of trades with stops
- Stop effectiveness: Percentage of stops actually triggered

**High Score (80-100)**: All trades have stops, stops are respected  
**Low Score (0-40)**: No stops used, stops moved or ignored

### Patience (0-100)
Measures quality over quantity.

**Components**:
- Trade frequency: Penalty for overtrading
- Win rate: Bonus for winning trades
- Time spacing: Reward for spacing trades

**High Score (70-100)**: Few high-quality trades, well-spaced  
**Low Score (0-40)**: Overtrading, rapid-fire entries

### Risk Discipline (0-100)
Measures position sizing and risk-reward ratios.

**Components**:
- Position size consistency: Variance from average
- R-multiple average: Risk-reward ratio quality

**High Score (75-100)**: Consistent sizing, good R-multiples  
**Low Score (0-40)**: Inconsistent sizing, poor risk-reward

### Rule Adherence (0-100)
Measures following trading plan.

**Components**:
- Entry type consistency: Consistent use of market/limit
- Risk management usage: Stop/target usage

**High Score (80-100)**: Consistent practices, proper risk management  
**Low Score (0-40)**: Inconsistent practices, poor risk management

---

## Determinism Rules

### Session Immutability
**Rule**: Once a session is created, its candle data is **immutable**.

**Enforcement**:
- Candles are bound to session via `session_id` FK
- `UNIQUE(session_id, timestamp)` prevents duplicates
- No UPDATE operations on candles after creation

### Replay Determinism
**Rule**: Same session data → same replay behavior.

**Guarantees**:
- Candles loaded in order by `candle_index`
- Replay state progression is deterministic
- Scores calculated from frozen session data

### Score Stability
**Rule**: Scores must be pure functions over session + trade data.

**Implications**:
- Same input data → same scores
- Scores can be compared across time
- Historical scores remain valid

---

## Integration Points

### Agent Workspaces
- Session data stored in `agent_workspaces/Agent-5/trader_replay/`
- Agent-specific replay histories
- Behavioral scoring tied to agent performance

### Messaging Infrastructure
- Orchestrator uses `UnifiedMessagingService`
- Session completion alerts
- Behavioral score reports to Agent-5

### Repository Pattern
- `SessionRepository`: Session data access
- `TradeRepository`: Paper trade persistence
- `JournalRepository`: Journal entry management
- `ScoreRepository`: Behavioral score storage

---

## Service Architecture

```
src/services/trader_replay/
├── __init__.py                      # Service exports
├── models.py                        # Data models
├── replay_engine.py                 # Core replay logic
├── repositories.py                  # Repository pattern
├── trader_replay_orchestrator.py   # Service orchestrator
├── trader_replay_cli.py            # CLI interface
├── behavioral_scoring.py           # Scoring algorithms
├── schema.sql                       # Database schema
└── DREAMOS_INTEGRATION.md          # Integration docs
```

---

## Testing

### Test Fixtures
- `tests/fixtures/trader_replay/`: Deterministic test data
- Disciplined session fixture: Good trading behavior
- Chaotic session fixture: Poor trading behavior

### Test Coverage
- Replay engine: Deterministic replay validation
- Repositories: CRUD operations, isolation
- Scoring: Golden test fixtures
- CLI: Smoke tests with temp DB

---

## Version History

- **v1.0.0** (2025-12-05): Initial implementation
  - Replay engine with deterministic behavior
  - Repository pattern for data access
  - Behavioral scoring algorithms
  - CLI interface

---

**Last Updated**: 2025-12-05  
**Maintained By**: Agent-3 (Infrastructure) + Agent-5 (Business Intelligence)



