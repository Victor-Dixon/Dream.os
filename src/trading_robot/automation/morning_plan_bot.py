"""
Config-Driven Discord Morning Plan Bot.

<!-- SSOT Domain: trading_robot -->
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import pytz
import yfinance as yf
from dotenv import load_dotenv

from .discord_post import post_to_discord
from .indicators import detect_macd_cross, detect_macd_curl, macd as macd_calc

DEFAULT_CONFIG_PATH = Path("config/trading_robot_morning_plan.json")


def load_config(path: Path) -> Dict[str, object]:
    """Load JSON configuration for the morning plan bot."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def fetch_intraday(symbol: str, interval: str, period: str = "5d") -> pd.DataFrame:
    """Fetch intraday data for a symbol using yfinance."""
    df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=False)
    df = df.dropna()
    return df


def fmt_level(value: Optional[float]) -> str:
    """Format a price level for display."""
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def build_plan(
    symbol: str,
    r_dollars: int,
    daily_max_r: int,
    macd_params: Dict[str, int],
    df_15: pd.DataFrame,
    df_5: pd.DataFrame,
) -> str:
    """Build the Discord plan message based on current market data."""
    if df_15.empty or df_5.empty:
        return (
            f"**{symbol} MORNING PLAN — Momentum + MACD**\n"
            "No intraday data available yet. Check again closer to market open."
        )

    last15 = df_15.iloc[-1]
    prev_day_high = None
    prev_day_low = None
    if len(df_15) > 2:
        daily = df_15.resample("1D").agg({"High": "max", "Low": "min"}).dropna()
        if len(daily) > 1:
            prev_day_high = float(daily.iloc[-2]["High"])
            prev_day_low = float(daily.iloc[-2]["Low"])

    last_price = float(last15["Close"])

    df_5m = macd_calc(df_5, **macd_params)
    hist_tail = df_5m["HIST"].tail(5).tolist()
    curl = detect_macd_curl(hist_tail)
    cross = detect_macd_cross(df_5m["MACD"], df_5m["SIGNAL"])

    plan_lines: List[str] = []
    plan_lines.append(
        f"**{symbol} MORNING PLAN — Momentum + MACD (1R=${r_dollars}, Daily Max={daily_max_r}R=${r_dollars * daily_max_r})**"
    )
    plan_lines.append(f"Last price (15m): **{fmt_level(last_price)}**")
    if prev_day_high is not None and prev_day_low is not None:
        plan_lines.append(f"Yesterday H/L: **{fmt_level(prev_day_high)} / {fmt_level(prev_day_low)}**")
    plan_lines.append("")
    plan_lines.append("**HARD RULES (AUTOPILOT)**")
    plan_lines.append(f"- Max loss per idea/trade: **-${r_dollars} (1R)**")
    plan_lines.append(f"- Daily max loss: **-${r_dollars * daily_max_r} ({daily_max_r}R)** → STOP")
    plan_lines.append("- No stop widening. No adding to losers.")
    plan_lines.append("- If stopped once: 10-min cooldown.")
    plan_lines.append("")
    plan_lines.append("**SETUPS (ONLY THESE)**")
    plan_lines.append("1) **Momentum Break + MACD Confirm**")
    plan_lines.append("   - Long: break & hold above key level (YHigh/ORH) AND 5m HIST rising; prefer MACD>Signal")
    plan_lines.append("   - Short: break & hold below key level (YLow/ORL) AND 5m HIST falling; prefer MACD<Signal")
    plan_lines.append("2) **MACD Curl (early move)**")
    plan_lines.append("   - Trigger: 5m HIST still < 0 but rising with higher lows (curl)")
    plan_lines.append("   - Entry: confirmation candle + reclaim of micro level; exit hard at -$100 if wrong")
    plan_lines.append("3) **MACD Crossover (confirmation)**")
    plan_lines.append("   - Trigger: MACD crosses above Signal on 5m + momentum candle")
    plan_lines.append("   - Entry: first retest hold; avoid chasing first candle")
    plan_lines.append("")
    plan_lines.append("**TODAY’S SIGNAL SNAPSHOT (5m)**")
    hist_preview = ", ".join([f"{val:.4f}" for val in hist_tail])
    plan_lines.append(f"- HIST last 5: `{hist_preview}`")
    plan_lines.append(f"- Curl detected: **{curl}**")
    plan_lines.append(f"- Cross detected: **{cross}**")
    plan_lines.append("")
    plan_lines.append("**EXECUTION TEMPLATE (so you don’t cut winners / hold losers)**")
    plan_lines.append("- Enter only at a level + confirmation (no mid-range gambling).")
    plan_lines.append("- On entry place bracket rules:")
    plan_lines.append(f"  - Stop: **- ${r_dollars}** (hard)")
    plan_lines.append(f"  - TP1: **+ ${r_dollars}** (sell 50%)")
    plan_lines.append("  - Runner: after TP1, stop → breakeven; trail structure or aim +2R")
    plan_lines.append("")
    plan_lines.append("**NO-TRADE CONDITIONS**")
    plan_lines.append("- 5m MACD flat + chop (alternating candles) → stand down.")
    plan_lines.append("- Already hit -2R on day → you’re done.")

    return "\n".join(plan_lines)


def main() -> None:
    """Entry point for posting the morning plan to Discord."""
    load_dotenv()
    config_path = Path(os.getenv("TRADING_ROBOT_MORNING_PLAN_CONFIG", DEFAULT_CONFIG_PATH))
    cfg = load_config(config_path)

    tz = pytz.timezone(os.getenv("TZ", cfg.get("tz", "America/Chicago")))
    now = datetime.now(tz).strftime("%Y-%m-%d %I:%M %p %Z")

    symbol = cfg.get("symbol", "TSLA")
    r_dollars = int(cfg.get("r_dollars", 100))
    daily_max_r = int(cfg.get("daily_max_r", 2))
    macd_params = cfg.get("macd", {"fast": 12, "slow": 26, "signal": 9})

    df_15 = fetch_intraday(symbol, "15m", "5d")
    df_5 = fetch_intraday(symbol, "5m", "5d")

    plan = f"_{now}_\n" + build_plan(symbol, r_dollars, daily_max_r, macd_params, df_15, df_5)

    webhook = os.getenv("DISCORD_WEBHOOK_URL") or cfg["discord"]["webhook_url"]
    post_to_discord(webhook, plan)


if __name__ == "__main__":
    main()
