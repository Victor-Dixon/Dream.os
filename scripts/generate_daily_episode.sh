#!/bin/bash
# Generate Digital Dreamscape Daily Episode
# Wrapper script for easy execution

cd "$(dirname "$0")/.." || exit 1

python tools/generate_daily_episode.py "$@"

