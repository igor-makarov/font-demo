#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

rm -rf site
mkdir -p .build/uv-cache site/fonts
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.build/uv-cache}"

cp fonts/* site/fonts/
uv run --locked python scripts/adjust_line_height.py \
  fonts/Carlito-Regular.ttf \
  site/fonts/Carlito-LineHeight-150.ttf

pandoc README.md \
  --from=markdown \
  --to=html5 \
  --standalone \
  --css=style.css \
  --metadata=pagetitle:"Carlito font rendering demonstration" \
  --output=site/index.html

cp style.css site/style.css

printf 'Built site/index.html\n'
