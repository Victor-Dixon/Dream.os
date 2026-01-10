#!/usr/bin/env bash
# SSOT Domain: scripts
set -euo pipefail

cd "$(dirname "$0")/.."
python -m uvicorn apps.api.main:app --reload --port 8080
