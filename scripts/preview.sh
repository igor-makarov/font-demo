#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

serve site &
server_pid=$!

cleanup() {
  kill "$server_pid" 2>/dev/null || true
  wait "$server_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

chokidar README.md style.css 'fonts/**/*' --command './scripts/build.sh'
