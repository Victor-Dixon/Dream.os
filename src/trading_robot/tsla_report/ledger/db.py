# <!-- SSOT Domain: trading_robot -->
"""SQLite ledger for TSLA recommendations and scores."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class LedgerConfig:
    path: Path = Path("data/tsla_report/ledger.sqlite3")


class Ledger:
    """SQLite-backed ledger."""

    def __init__(self, config: LedgerConfig | None = None) -> None:
        self.config = config or LedgerConfig()
        self.config.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.config.path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_hash TEXT PRIMARY KEY,
                    asof_utc TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    data_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS recommendations (
                    rec_id TEXT PRIMARY KEY,
                    snapshot_hash TEXT NOT NULL,
                    created_utc TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    setup_type TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    trigger_json TEXT NOT NULL,
                    entry_json TEXT NOT NULL,
                    stop_json TEXT NOT NULL,
                    target_json TEXT NOT NULL,
                    timebox_minutes INTEGER NOT NULL,
                    notes TEXT NOT NULL,
                    regime_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS scores (
                    rec_id TEXT PRIMARY KEY,
                    scored_utc TEXT NOT NULL,
                    result TEXT NOT NULL,
                    mfe REAL NOT NULL,
                    mae REAL NOT NULL,
                    r_multiple REAL NOT NULL,
                    hit_target INTEGER NOT NULL,
                    hit_stop INTEGER NOT NULL,
                    triggered INTEGER NOT NULL,
                    assumptions_json TEXT NOT NULL
                );
                """
            )

    def save_snapshot(self, snapshot_hash: str, snapshot: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO snapshots VALUES (?, ?, ?, ?)",
                (snapshot_hash, snapshot["asof_utc"], snapshot["ticker"], json.dumps(snapshot)),
            )

    def save_recommendations(self, recs: Iterable[dict[str, Any]], regime: dict[str, Any], snapshot_hash: str) -> None:
        with self._connect() as conn:
            for rec in recs:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO recommendations
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        rec["rec_id"],
                        snapshot_hash,
                        rec["created_utc"],
                        rec["ticker"],
                        rec["setup_type"],
                        rec["direction"],
                        rec["confidence"],
                        json.dumps(rec["trigger"]),
                        json.dumps(rec["entry_assumption"]),
                        json.dumps(rec["stop"]),
                        json.dumps(rec["target"]),
                        rec["timebox_minutes"],
                        rec["notes"],
                        json.dumps(regime),
                    ),
                )

    def save_score(self, score: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO scores
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    score["rec_id"],
                    score["scored_utc"],
                    score["result"],
                    score["mfe"],
                    score["mae"],
                    score["r_multiple"],
                    int(score["hit_target"]),
                    int(score["hit_stop"]),
                    int(score["triggered"]),
                    json.dumps(score["assumptions"]),
                ),
            )

    def fetch_recommendations_by_date(self, date_prefix: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT rec_id, created_utc, ticker, setup_type, direction, confidence,
                       trigger_json, entry_json, stop_json, target_json, timebox_minutes, notes
                FROM recommendations
                WHERE created_utc LIKE ?
                """,
                (f"{date_prefix}%",),
            ).fetchall()
        recs = []
        for row in rows:
            recs.append(
                {
                    "rec_id": row[0],
                    "created_utc": row[1],
                    "ticker": row[2],
                    "setup_type": row[3],
                    "direction": row[4],
                    "confidence": row[5],
                    "trigger": json.loads(row[6]),
                    "entry_assumption": json.loads(row[7]),
                    "stop": json.loads(row[8]),
                    "target": json.loads(row[9]),
                    "timebox_minutes": row[10],
                    "notes": row[11],
                }
            )
        return recs

    def fetch_weekly_summary(self, since_date: str) -> list[tuple]:
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT r.setup_type, COUNT(*),
                       AVG(s.r_multiple),
                       SUM(CASE WHEN s.result = 'win' THEN 1 ELSE 0 END) as wins
                FROM recommendations r
                JOIN scores s ON r.rec_id = s.rec_id
                WHERE r.created_utc >= ?
                GROUP BY r.setup_type
                """,
                (since_date,),
            ).fetchall()
