#!/usr/bin/env bash
# install.sh — Install twat-speech locally
# Speech processing plugin for twat
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing twat-speech..."
uv pip install -e . 2>/dev/null || pip install -e .
echo "Done."
