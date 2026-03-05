#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: run_tests.sh '<test command>'" >&2
  exit 2
fi

eval "$1"
