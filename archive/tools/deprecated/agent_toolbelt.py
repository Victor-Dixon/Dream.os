#!/usr/bin/env python3
# ruff: noqa: E501  # Archive file - long lines acceptable for deprecated code
"""
⚠️ DEPRECATED: This tool has been archived.
Use toolbelt.py instead (primary toolbelt implementation).
Archived: 2025-01-27
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import sys
import time

DATA = Path("data/knowledge")

def _append_jsonl(path, entry):
    """Append entry to JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# ---------- brain.* ----------
def brain_share(args):
    entry = dict(
        ts=time.time(),
        topic=args.topic,
        recipients=args.recipients,
        actionable=args.actionable
    )
    _append_jsonl(DATA / "brain.shares.jsonl", entry)
    print("OK: brain.share recorded")

# ---------- oss.* (stubs; URLs tracked for later workers) ----------
def oss_clone(args):
    rec = dict(ts=time.time(), repo=args.repo, owner=args.owner)
    _append_jsonl(DATA / "oss.clone.jsonl", rec)
    print("OK: oss.clone queued")

def oss_issues(args):
    # placeholder query spec; real fetch lives in worker
    rec = dict(ts=time.time(), labels=args.labels, repo=args.repo)
    _append_jsonl(DATA / "oss.issues.query.jsonl", rec)
    print("OK: oss.issues query recorded")

def oss_import(args):
    rec = dict(
        ts=time.time(),
        assign_to=args.assign_to,
        source="oss.issues.result",
        count=args.count
    )
    _append_jsonl(DATA / "oss.import.jsonl", rec)
    print("OK: oss.import staged")

def oss_status(args):
    print(json.dumps({"agent": args.agent, "period": args.period, "status": "TBD"}, indent=2))

# ---------- debate.* ----------
def debate_start(args):
    rec = dict(
        ts=time.time(),
        topic=args.topic,
        participants=args.participants,
        duration_hours=args.duration
    )
    _append_jsonl(DATA / "debate.start.jsonl", rec)
    print("OK: debate.start recorded")

def debate_vote(args):
    rec = dict(ts=time.time(), topic=args.topic, voter=args.voter, choice=args.choice)
    _append_jsonl(DATA / "debate.vote.jsonl", rec)
    print("OK: debate.vote recorded")

def debate_status(args):
    print(json.dumps({"topic": args.topic, "status": "TBD"}, indent=2))

# ---------- msgtask.* ----------
def msgtask_ingest(args):
    rec = dict(ts=time.time(), source=args.source, text=args.text)
    _append_jsonl(DATA / "msgtask.ingest.jsonl", rec)
    print("OK: msgtask.ingest recorded")

def msgtask_parse(args):
    print(json.dumps({"text": args.text, "parsed": "TBD"}, indent=2))

def msgtask_fingerprint(args):
    print(json.dumps({"text": args.text, "fingerprint": "TBD"}, indent=2))

# ---------- Main CLI ----------
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Agent Toolbelt (DEPRECATED)")
    sub = p.add_subparsers(dest="command", help="Commands")

    # brain
    s = sub.add_parser("brain.share")
    s.add_argument("--topic", required=True)
    s.add_argument("--recipients", nargs="*", required=True)
    s.add_argument("--actionable", action="store_true")
    s.set_defaults(func=brain_share)

    # oss
    s = sub.add_parser("oss.clone")
    s.add_argument("--repo", required=True)
    s.add_argument("--owner", default="Agent-7")
    s.set_defaults(func=oss_clone)
    s = sub.add_parser("oss.issues")
    s.add_argument("--repo", required=False, default="*")
    s.add_argument("--labels", nargs="*", default=["good-first-issue"])
    s.set_defaults(func=oss_issues)
    s = sub.add_parser("oss.import")
    s.add_argument("--assign-to", dest="assign_to", default="Agent-7")
    s.add_argument("--count", type=int, default=5)
    s.set_defaults(func=oss_import)
    s = sub.add_parser("oss.status")
    s.add_argument("--agent", default="Agent-7")
    s.add_argument("--period", default="weekly")
    s.set_defaults(func=oss_status)

    # debate
    s = sub.add_parser("debate.start")
    s.add_argument("--topic", required=True)
    s.add_argument("--participants", nargs="*", required=True)
    s.add_argument("--duration", type=int, default=24)
    s.set_defaults(func=debate_start)
    s = sub.add_parser("debate.vote")
    s.add_argument("--topic", required=True)
    s.add_argument("--voter", required=True)
    s.add_argument("--choice", required=True)
    s.set_defaults(func=debate_vote)
    s = sub.add_parser("debate.status")
    s.add_argument("--topic", required=True)
    s.set_defaults(func=debate_status)

    # msgtask
    s = sub.add_parser("msgtask.ingest")
    s.add_argument("--source", required=True)
    s.add_argument("--text", required=True)
    s.set_defaults(func=msgtask_ingest)
    s = sub.add_parser("msgtask.parse")
    s.add_argument("--text", required=True)
    s.set_defaults(func=msgtask_parse)
    s = sub.add_parser("msgtask.fingerprint")
    s.add_argument("--text", required=True)
    s.set_defaults(func=msgtask_fingerprint)

    args = p.parse_args()
    if not args.command:
        p.print_help()
        sys.exit(1)
    args.func(args)
