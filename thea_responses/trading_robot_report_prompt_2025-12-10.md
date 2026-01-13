
# Thea Request — Trading Robot Readout (≈15k chars target)

## Purpose
We want to stop repeat Robinhood blowups by moving to a guarded, automated flow. This prompt summarizes our current trading-robot assets (code + strategy) and asks you (Thea) to critique, harden, and propose the fastest path to a safe, small-size live trial.

## Stack We Have (Python Trading Robot, Alpaca-first)
- Repo module: `trading_robot/`
- Broker layer: Alpaca client (`core/alpaca_client.py`, REST v2) + broker factory; Robinhood client stub exists.
- Trading engine: `core/trading_engine.py` with preflight validation, account fetch, market clock checks, order placement (market/limit), order cancel, portfolio/positions refresh; async monitors for market status and positions.
- Risk: `core/risk_manager.py` and `RiskMonitor`
  - Limits: daily loss limit (`DAILY_LOSS_LIMIT_PCT`), max daily trades, max position size pct, min/max order value, emergency stop hooks.
  - Position sizing: risk-per-trade 1% of equity default; max position size computed off portfolio pct.
  - Stop/TP calculators; daily counters reset helper; risk report generator.
  - Alerts: exposure >80%, concentration >20%, daily loss < -3%, high trade frequency, outside trading hours.
  - Emergency stop scaffolding (needs wiring to engine to flatten + halt).
- Preflight: `core/preflight_validator.py`
  - Checks config validity, API connectivity, account status/balances, risk limits sanity, emergency-stop setup, live-trading flags/URL correctness.
  - Produces human-readable validation report; blocks on errors.
- Execution: `execution/live_executor.py`
  - Symbol universe default: AAPL/MSFT/GOOGL/AMZN/TSLA.
  - Per-symbol 5m cooldown, 1m data fetch (last 100 bars), multi-strategy consensus with confidence threshold, then risk-validated market order; trade recording.
  - Position monitor checks stop-loss/TP using risk calculators; closes via market sells.
  - Risk monitor loop uses RiskManager alerts.
  - Daily reset helper around market open.
- Strategies: `strategies/base_strategy.py` (V2) + `strategy_implementations.py`
  - TrendFollowingStrategy: fast/slow SMA, BUY when fast>slow else SELL; confidence scaled by MA diff.
  - MeanReversionStrategy: Bollinger Bands, BUY below lower band, SELL above upper; confidence scaled by distance.
  - StrategyManager to aggregate results and consensus.
  - Indicators: SMA/EMA/RSI/MACD/Bollinger in `indicators.py`; risk sizing helper `risk_management.py`.
- Backtesting: `backtesting/backtester.py` (basic runner).
- Web dashboard: FastAPI scaffold (`web/dashboard.py`, `dashboard_routes.py`) for status/portfolio/market data routes + websocket updates.
- Config: `config/settings.py` (`config.validate_config`, live vs paper, trading hours/days, limits, API keys).
- Tests: `tests/test_trading_robot.py` (basic coverage).

### Expanded component inventory (for your reasoning)
- `core/broker_interface.py`: abstraction for broker adapters (Alpaca implemented; Robinhood scaffold).
- `core/broker_factory.py`: selects broker client from config (Alpaca default).
- `core/trading_engine.py`: async engine; monitors market clock every 60s, positions every 30s; converts historical bars to list-of-dicts for strategies; switches market->limit if market closed; stores orders dict.
- `core/preflight_validator.py`: runs configuration validation, API ping (clock), account status (active/approved, cash/buying power warnings), risk limits validation, emergency-stop validation, live-mode URL check, produces status PASS/FAIL + report text; `can_proceed_with_trading`.
- `core/risk_manager.py`: daily PnL tracking vs daily_start_value; max_daily_loss = pct * initial_balance; validates trades against min/max order value and position size cap; position size via risk-per-trade 1% default; calculates stop/TP prices; concentration/exposure metrics; daily counters reset; generates human-readable risk report; emergency stop currently logs only.
- `core/risk_monitor`: alert list (exposure >80%, concentration >20%, daily loss < -3%, high trade frequency, outside trading hours).
- `execution/live_executor.py`: orchestrates symbol scan → strategy consensus → risk validation → order submit → record trade; per-symbol min_trade_interval 300s; market hours gate uses risk manager; monitors positions for stop/TP triggers (market exit); cancels open orders on stop; daily reset near market open.
- `strategies/base_strategy.py`: abstract; data validation (needs O/H/L/C/V, len >= 50); indicator wrapper (SMA, EMA, RSI, MACD, BB upper/lower); risk mgmt helper for position sizing; StrategyManager with consensus (via RiskManagement.get_consensus_signal).
- `strategies/strategy_implementations.py`: TrendFollowing (fast/slow SMA) and MeanReversion (Bollinger) with confidence scaling; hold if invalid data.
- `strategies/signal_processing.py` (implied): Signal enum (BUY/SELL/HOLD), StrategyResult container.
- `strategies/risk_management.py`: simple consensus logic (already V2).
- `execution/live_executor.py`: symbol universe configurable (list ops provided).
- `web/dashboard.py` / `dashboard_routes.py`: FastAPI app, websocket endpoint (`/ws/updates`), routes for status/portfolio/market data/trade; includes emergency stop route stub.
- `backtesting/backtester.py`: runs strategy on historical data and aggregates metrics (win rate, profit factor, drawdown, Sharpe, total return).
- `config/settings.py`: env-driven: ALPACA_API_KEY/SECRET/BASE_URL, broker type, market hours/days, MAX_POSITION_SIZE_PCT, DAILY_LOSS_LIMIT_PCT, MIN/MAX_ORDER_VALUE, MAX_DAILY_TRADES, EMERGENCY_STOP flags/thresholds, initial balance, live_trading_enabled toggle, default stops/TPs.
- `main.py`: entrypoint wiring engine/executor/web.
- `requirements.txt`: includes alpaca_trade_api, loguru, FastAPI, etc. (not listed here but present).
- `tests/test_trading_robot.py`: covers risk validation and engine basics (light).

## TSLA Strategy (Pine v6 provided by user)
- Long when price > 50/200 SMA and RSI < 60; Short when price < 50/200 SMA and RSI > 40.
- Risk sizing: riskPctEquity% per trade, stop = 1% of price (min tick guard), qty = risk $ / stop distance.
- Targets: 15% profit; trailing stop optional with trigger (5%) and offset (0.5%).
- No explicit daily loss limit, time window, spread/slippage guard, or chop cooldown; assumes canShort; uses TradingView strategy sizing math, not broker-aware.

## Gaps / Risks to close before live trial
- Broker safety wiring: emergency stop is logged but not yet flattening/halting; market-order heavy; no slippage/spread guard; no borrow check for shorts.
- Risk completeness: daily loss cap exists but not enforced in executor halt; max one-position-at-a-time not enforced; no per-symbol notional cap override; no session kill switch flag.
- Execution quality: no limit/MP/IOC routing, no bracket OCO, no trailing via broker-native orders; no partial take-profit staging.
- Data quality: assumes Alpaca bars OK; no mid/spread checks; no stale-data guard.
- Monitoring/alerts: logs only; no Discord/SMS; no persistent state store for crashes.
- Compliance: no explicit paper/live toggle at runtime; needs explicit tiny-size live pilot plan.

### Proposed guardrail defaults (you can refine)
- Mode: paper first; live only after 3–5 green sessions with <1% drawdown and fills within 20bps slippage vs. signal price.
- Daily loss limit: 1–2% of equity; halt + flatten when breached; lockout until next session.
- Per-trade notional cap: 5–10% of equity; independent of riskPct sizing; enforce min qty >=1.
- Time window: 10:00–15:30 ET; optional no-trade last 15m to avoid close risk.
- Cooldown: 10–15 minutes after any stop-out; per-symbol 5–10 minute spacing (already 5m).
- Order template: limit or market-with-protection; attach stop + optional TP; if trailing, trigger 2–3%, offset 0.5–1%.
- Position policy: one position per symbol; optionally long-only to avoid borrow issues on Robinhood; if shorting, check borrow availability.
- Spread/slippage guard: skip entry if (ask-bid)/mid > 0.3–0.5% or if price deviates >0.3% during order ack.
- Data freshness: reject bars older than 2 minutes; abort if API lagging.
- Emergency stop: on any of (daily loss hit, API failure >N retries, stale data, missing quote, abnormal slippage) → cancel open orders, flatten, halt, alert.

### Bridging TSLA Pine to the Python bot (suggested path)
- Signal port: replicate SMA(50/200) and RSI(14) on 1m or 5m bars in Python; mirror thresholds: RSI OB=60, OS=40; long when price > both MAs and RSI<60; short when price < both and RSI>40.
- Risk sizing: use RiskManager.calculate_position_size with explicit stop distance = max(1.0–1.5% of price, min tick buffer). Override to risk 0.25–0.5% of equity per trade, then cap by per-trade notional.
- Stops/targets: set stop at entry*(1-1.25%) long / (1+1.25%) short; TP either staged (50% at +4–5%) then trail remainder with trigger 2.5–3%, offset 0.75–1.0%, or single TP at +8–10% if we keep it simpler.
- Order placement: prefer limit with small tolerance around mid; fall back to market-with-protection during high liquidity only; always place stop (and TP if not trailing) as OCO/bracket.
- Cooldown: enforce per-symbol cooldown 10m after stop-out; keep 5m base interval.
- Shorting: if broker lacks borrow, force long-only mode.
- Universe: TSLA only initially; optionally add a single liquid ETF (e.g., QQQ) later.

### Execution + validation plan (paper → tiny live)
1) Paper wiring
   - Configure Alpaca paper keys; set `live_trading_enabled=False`.
   - Run preflight validator; must PASS with emergency stop enabled.
   - Run live executor with TSLA-only universe; log orders to JSONL.
2) Bar-level alignment
   - Compare Python signals vs. TradingView strategy on same 1m/5m bars for a day; diff <1 bar mismatch allowed.
   - Verify size calculation matches Pine risk math within rounding to whole shares.
3) Fill quality
   - Require slippage <20bps median, <50bps p95 vs. signal price in paper (simulate limit cross).
   - Verify stops/TPs land at broker and remain active.
4) Risk drills
   - Force emergency stop by simulating daily loss breach; confirm flatten + halt + alert.
   - Simulate API failure to confirm halt-on-error.
5) Promotion gate
   - 3–5 green paper sessions; max intraday drawdown <1–2%; no unhandled errors.
6) Live pilot (tiny size)
   - Turn on live_trading_enabled + live API URL + smallest allowable qty; keep same limits; daily loss 0.5–1% max during pilot.
   - Monitor live fills vs. expected; abort on any unexpected behavior.

### Data quality & monitoring asks
- Add stale-data guard (bars older than 2m → halt trading).
- Add spread/slippage check pre-trade.
- Add persistence (sqlite/JSON) of last positions/orders to recover after restart.
- Add alerts (Discord/webhook) on entries/exits/halts/emergency.
- Add kill switch flag in config; ensure RiskManager emergency stop triggers engine.stop + flatten.

### What success looks like
- Thea returns a concise plan with explicit parameter defaults, order template recommendations, and a step-by-step runbook that we can execute without further prompting.
- The plan should be actionable within one work session to run paper trading safely, then a very small live pilot if approved.

## What we want from you (Thea)
1) Safety review: identify the fastest, safest path to stop account blowups using the assets above. Call out missing controls and propose concrete parameter defaults (daily loss %, max per-trade notional, time window, cooldowns, position limits, stop/TP schema).
2) Bridging plan: recommend how to run the TSLA SMA/RSI strategy through our Python stack (not TV simulation): bar aggregation, signal port, order template (limit/bracket), and risk hooks.
3) Execution plan: step-by-step paper-trade runbook (using Alpaca paper) and minimal checks to flip to tiny live size after X green sessions.
4) Output format: return a concise plan with three sections: (A) Required safeties to enable, (B) How to run the TSLA strategy on our bot (parameters + order template), (C) Minimal validation before live (data checks, fills vs. signals, PnL tolerances). Keep it under ~1,200 words.

## Context for this prompt size test
- We want to exercise your ability to handle a ~15k-character prompt and return a structured, actionable response we can archive. Please respond in markdown with headings and bullets, concise and specific, no filler.

## If you need more detail
- Ask for: broker choice (Alpaca paper vs live), target timeframes (1m/5m), max trade frequency, borrowing/shorting availability, and whether to force long-only.

## Reminder
- Focus on prevention of catastrophic loss: daily kill, per-trade notional cap, enforce stops at broker, and halt-on-error defaults.

