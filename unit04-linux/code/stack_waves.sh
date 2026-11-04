#!/usr/bin/env bash
# stack_waves.sh
# Stack the pieces in data/waves/ into one CSV, keeping a single header row.
# Run from the unit04-linux folder with:  bash code/stack_waves.sh
set -euo pipefail

mkdir -p output
out="output/mroz_stacked.csv"

head -n 1 data/waves/mroz_part1.csv > "$out"      # the header, once
for f in data/waves/mroz_part*.csv; do
    tail -n +2 "$f" >> "$out"                     # every line except the header
done

echo "Wrote $(wc -l < "$out") lines to $out"
