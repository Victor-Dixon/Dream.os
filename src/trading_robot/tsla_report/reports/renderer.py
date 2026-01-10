# <!-- SSOT Domain: trading_robot -->
"""Render TSLA morning report."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RenderedReport:
    markdown: str
    payload: dict[str, Any]


def render_report(snapshot: dict[str, Any]) -> RenderedReport:
    levels = snapshot["levels"]
    intraday = snapshot["intraday"]
    session = snapshot["session_context"]
    options = snapshot["options"]
    recs = snapshot["recommendations"]
    lines = [
        f"**TSLA Morning Report** ({snapshot['asof_utc']})",
        f"Bias: **{snapshot['regime']['trend']}** | Volatility: **{snapshot['regime']['volatility']}** | Confidence: **{snapshot['confidence']:.2f}**",
        "",
        "**Key Levels**",
        f"PMH {levels['PMH']:.2f} | PML {levels['PML']:.2f}",
        f"PDH {levels['PDH']:.2f} | PDL {levels['PDL']:.2f}",
        f"VWAP {levels['VWAP']:.2f} | ATR+ {levels['ATR_UP']:.2f} | ATR- {levels['ATR_DN']:.2f}",
        "",
        "**Session Context**",
        f"Premarket High/Low: {session['premarket']['high']:.2f}/{session['premarket']['low']:.2f}",
        f"Gap %: {session['gap_pct']:.2f}",
        "",
        "**Intraday**",
        f"Price {intraday['price']:.2f} | EMA9 {intraday['ema9']:.2f} | EMA21 {intraday['ema21']:.2f}",
        f"VWAP {intraday['vwap']:.2f} | ATR14 {intraday['atr14']:.2f} | Range % {intraday['range_pct']:.2f}",
        "",
        "**Scenarios & Setups**",
    ]
    for rec in recs:
        lines.append(
            f"- **{rec['setup_type']}** ({rec['direction']}) | Trigger: {rec['trigger']['type']} {rec['trigger']['level']} | "
            f"Stop: {rec['stop']['price']} | Target: {rec['target']['price']} | Timebox: {rec['timebox_minutes']}m"
        )
        lines.append(f"  - Notes: {rec['notes']}")
    wait_clause = "WAIT if price chops around VWAP or fails to trigger in timebox."
    lines.append("")
    lines.append(f"**WAIT Clause**: {wait_clause}")
    lines.append("")
    lines.append("**Data Provenance**")
    lines.append(f"Market Provider: {snapshot['providers']['market']} | Options: {options['available']} | As-Of: {snapshot['asof_utc']}")
    markdown = "\n".join(lines)
    payload = {
        "content": markdown,
        "username": "TradingRobotPlug",
    }
    return RenderedReport(markdown=markdown, payload=payload)
