"""
Robinhood Option Fill Journal Bot.

<!-- SSOT Domain: trading_robot -->
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

from dotenv import load_dotenv
import robin_stocks.robinhood as rh

from .discord_post import post_to_discord

DB_PATH = Path("data/trading_journal/trades.sqlite3")


def init_db(db_path: Path) -> None:
    """Initialize the SQLite database for option order journaling."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS option_orders (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            state TEXT,
            chain_symbol TEXT,
            direction TEXT,
            quantity REAL,
            average_price REAL,
            premium REAL,
            raw_json TEXT
        )
        """
    )
    con.commit()
    con.close()


def login() -> None:
    """Authenticate to Robinhood using environment variables."""
    username = os.environ["RH_USERNAME"]
    password = os.environ["RH_PASSWORD"]
    rh.login(username, password)


def fetch_filled_option_orders(limit: int = 200) -> Iterable[Dict[str, object]]:
    """Fetch recently filled Robinhood option orders."""
    orders = rh.get_all_option_orders(info=None) or []
    filled = [order for order in orders if order.get("state") == "filled"]
    return filled[-limit:]


def upsert(con: sqlite3.Connection, order: Dict[str, object]) -> Optional[Tuple[str, str, float, float, float]]:
    """Insert a new filled option order, returning summary details if inserted."""
    order_id = order.get("id")
    if not order_id:
        return None

    cur = con.cursor()
    cur.execute("SELECT 1 FROM option_orders WHERE id = ?", (order_id,))
    if cur.fetchone():
        return None

    qty = float(order.get("quantity") or 0)
    avg = float(order.get("average_price") or 0)
    symbol = order.get("chain_symbol") or "TSLA"
    direction = order.get("direction") or ""
    premium = qty * avg * 100.0

    created_at = order.get("created_at") or datetime.now(timezone.utc).isoformat()
    state = order.get("state") or ""
    raw = str(order)

    cur.execute(
        """
        INSERT INTO option_orders (
            id, created_at, state, chain_symbol, direction, quantity, average_price, premium, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (order_id, created_at, state, symbol, direction, qty, avg, premium, raw),
    )
    con.commit()

    return symbol, direction, qty, avg, premium


def main() -> None:
    """Entry point for journaling filled Robinhood option orders."""
    load_dotenv()
    init_db(DB_PATH)
    login()

    con = sqlite3.connect(DB_PATH)
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    for order in fetch_filled_option_orders():
        result = upsert(con, order)
        if result and webhook:
            symbol, direction, qty, avg, premium = result
            post_to_discord(
                webhook,
                f"🧾 **Logged** {symbol} | {direction} | qty={qty} | avg={avg:.2f} | est premium=${premium:.2f}",
            )

    con.close()


if __name__ == "__main__":
    main()
