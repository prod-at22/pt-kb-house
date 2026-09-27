#!/usr/bin/env bash
# Salin index.html + calc-config.json dari setiap repo KB asal ke folder destinasi dalam house.
set -euo pipefail
OWNER="${OWNER:-prod-at22}"
for slug in $(jq -r 'keys[]' destinations.json); do
  repo=$(jq -r --arg s "$slug" '.[$s]' destinations.json)
  mkdir -p "$slug"
  for f in index.html calc-config.json; do
    if curl -fsSL "https://raw.githubusercontent.com/$OWNER/$repo/HEAD/$f" -o "$slug/$f.tmp"; then
      mv "$slug/$f.tmp" "$slug/$f"
    else
      rm -f "$slug/$f.tmp"; echo "skip $repo/$f"
    fi
  done
done
