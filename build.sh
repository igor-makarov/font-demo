#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

rm -rf site
mkdir -p site

pandoc README.md \
  --from=markdown \
  --to=html5 \
  --standalone \
  --css=style.css \
  --metadata=pagetitle:"Carlito font rendering demonstration" \
  --output=site/index.html

cp style.css site/style.css
cp -R fonts site/fonts

printf 'Built site/index.html\n'
