#!/usr/bin/env bash
# run_all.sh
# Rebuild every output of this unit from the raw data, in order.
# Run from the unit05-datawrangling folder with:  bash code/run_all.sh
set -euo pipefail
mkdir -p output

echo "1. Population: the skeleton (350 local authorities x 4 years)"
python code/01_population.py > output/01_population.log

echo "2. Collisions: append four years, collapse to local authority x year"
python code/02_collisions.py > output/02_collisions.log

echo "3. Merge population, collisions and policy into the panel"
python code/03_build_panel.py > output/03_build_panel.log

echo "4. Linked tables: collisions, vehicles and casualties (2024)"
python code/04_linked_tables.py > output/04_linked_tables.log

echo "Done. Logs and data are in output/:"
ls output
