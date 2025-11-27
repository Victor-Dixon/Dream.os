#!/usr/bin/env python3
"""
Disk & CI health monitor for consolidation PRs.

Outputs:
    * Disk usage (C:/ and D:/) to ensure merge tooling has room
    * GitHub PR + combined status (success/pending/failure) for active merge PRs

Usage:
    python tools/monitor_disk_and_ci.py
    python tools/monitor_disk_and_ci.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import requests


PR_TARGETS = [
    {
        "label": "DigitalDreamscape → DreamVault",
        "repo": "Dadudekc/DreamVault",
        "number": 4,
    },
    {
        "label": "Thea → DreamVault",
        "repo": "Dadudekc/DreamVault",
        "number": 3,
    },
    {
        "label": "UltimateOptionsTradingRobot → trading-leads-bot",
        "repo": "Dadudekc/trading-leads-bot",
        "number": 3,
    },
    {
        "label": "TheTradingRobotPlug → trading-leads-bot",
        "repo": "Dadudekc/trading-leads-bot",
        "number": 4,
    },
    {
        "label": "MeTuber → Streamertools",
        "repo": "Dadudekc/Streamertools",
        "number": 13,
    },
    {
        "label": "DaDudekC → DaDudeKC-Website",
        "repo": "Dadudekc/DaDudeKC-Website",
        "number": 1,
    },
    {
        "label": "LSTMmodel_trainer → MachineLearningModelMaker",
        "repo": "Dadudekc/MachineLearningModelMaker",
        "number": 2,
    },
]


def human_readable(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{value:.2f} TB"


def disk_usage(path: str) -> Dict[str, str]:
    usage = shutil.disk_usage(path)
    return {
        "path": path,
        "total": human_readable(usage.total),
        "used": human_readable(usage.used),
        "free": human_readable(usage.free),
        "percent_used": f"{(usage.used / usage.total) * 100:.1f}%",
    }


def github_request(url: str, token: Optional[str]) -> requests.Response:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response


def fetch_pr_status(pr: Dict[str, str], token: Optional[str]) -> Dict[str, str]:
    repo = pr["repo"]
    number = pr["number"]
    pr_url = f"https://api.github.com/repos/{repo}/pulls/{number}"
    pr_data = github_request(pr_url, token).json()
    sha = pr_data["head"]["sha"]

    status_url = f"https://api.github.com/repos/{repo}/commits/{sha}/status"
    status_data = github_request(status_url, token).json()

    return {
        "label": pr["label"],
        "repo": repo,
        "number": number,
        "state": status_data.get("state", "unknown"),
        "updated_at": status_data.get("updated_at"),
        "sha": sha,
        "statuses": [
            {
                "context": item.get("context"),
                "state": item.get("state"),
                "description": item.get("description"),
                "target_url": item.get("target_url"),
                "updated_at": item.get("updated_at"),
            }
            for item in status_data.get("statuses", [])
        ],
    }


def collect_ci_status(token: Optional[str], targets: List[Dict[str, str]]) -> List[Dict[str, str]]:
    statuses = []
    for target in targets:
        try:
            statuses.append(fetch_pr_status(target, token))
        except requests.HTTPError as exc:
            statuses.append(
                {
                    "label": target["label"],
                    "repo": target["repo"],
                    "number": target["number"],
                    "state": "error",
                    "error": f"{exc}",
                }
            )
        except requests.RequestException as exc:
            statuses.append(
                {
                    "label": target["label"],
                    "repo": target["repo"],
                    "number": target["number"],
                    "state": "error",
                    "error": f"{exc}",
                }
            )
    return statuses


def print_human_report(disks: List[Dict[str, str]], ci_status: List[Dict[str, str]]) -> None:
    print("=== Disk Usage ===")
    for disk in disks:
        print(
            f"{disk['path']}: used {disk['used']} / {disk['total']} "
            f"({disk['percent_used']}), free {disk['free']}"
        )
    print("\n=== CI Status ===")
    for status in ci_status:
        line = (
            f"{status['label']}: repo {status['repo']} PR #{status['number']} "
            f"→ state={status['state']}"
        )
        if status["state"] == "error" and status.get("error"):
            line += f" ({status['error']})"
        print(line)
        for ctx in status.get("statuses", []):
            ctx_line = f"    - {ctx['context']}: {ctx['state']}"
            if ctx.get("description"):
                ctx_line += f" ({ctx['description']})"
            print(ctx_line)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report disk usage and CI status for active consolidation PRs."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human-readable text",
    )
    parser.add_argument(
        "--token",
        help="GitHub token (defaults to GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any PR reports failure/error (default: warn only)",
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    disks = []
    for drive in ("C:/", "D:/"):
        try:
            disks.append(disk_usage(drive))
        except FileNotFoundError:
            disks.append(
                {
                    "path": drive,
                    "error": "drive not found",
                }
            )

    ci_status = collect_ci_status(token, PR_TARGETS)

    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "disks": disks,
        "ci_status": ci_status,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_human_report(disks, ci_status)

    if args.strict:
        for status in ci_status:
            if status["state"] in {"failure", "error"}:
                return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

