#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: run_lint.sh '<lint command>'" >&2
  exit 2
fi

eval "$1"
