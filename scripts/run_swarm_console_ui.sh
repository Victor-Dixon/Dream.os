#!/usr/bin/env bash
# SSOT Domain: scripts
set -euo pipefail

cd "$(dirname "$0")/../apps/ui"
python -m http.server 5173
