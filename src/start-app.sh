#!/usr/bin/env bash
set -euo pipefail

echo "Starting App"
exec python3 slack_app.py
