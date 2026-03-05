#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: run_formatter.sh '<formatter command>'" >&2
  exit 2
fi

eval "$1"
