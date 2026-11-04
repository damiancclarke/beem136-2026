#!/usr/bin/env bash
# run_all.sh
# Rebuild every output of this unit from the raw data, in order.
# Run from the unit04-linux folder with:  bash code/run_all.sh
set -euo pipefail

echo "1. Stacking the data files"
bash code/stack_waves.sh

echo "2. Checking the stacked file matches the original"
if cmp -s data/mroz.csv output/mroz_stacked.csv; then
    echo "   OK: identical to data/mroz.csv"
else
    echo "   PROBLEM: files differ" >&2
    exit 1
fi

echo "3. Tabulating children under 6"
cut -d, -f3 output/mroz_stacked.csv | tail -n +2 | sort -n | uniq -c > output/kidslt6_tab.txt
cat output/kidslt6_tab.txt

echo "Done."
