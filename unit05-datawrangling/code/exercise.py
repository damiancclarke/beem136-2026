"""
exercise.py
Class exercise for Unit 5. Fill in each TODO, run the file, and check your
answers against the questions on the slides.
Run from the unit05-datawrangling folder with:  python code/exercise.py
Run bash code/run_all.sh first, so that output/panel.csv exists.
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUTPUT = Path("output")

panel = pd.read_csv(OUTPUT / "panel.csv")

# ---- Task 1: long -> wide ---------------------------------------------------
# Keep the Welsh local authorities, and make a table with ONE row per authority
# and one column per year holding collisions_per_100k.
# Hint: df.pivot(index=..., columns=..., values=...)
# Then compute the % change from 2022 to 2024. Which authority fell the most?
wales = panel[panel["wales"] == 1]
# TODO

# ---- Task 2: killed or seriously injured ------------------------------------
# Make a table of KSI collisions (column ksi) per 100,000 people,
# by country (rows) and year (columns). Remember: add up first, divide after.
# TODO

# ---- Task 3: cyclists (collapse, m:1 merge, and zeros) ----------------------
# Using the 2024 vehicle file, count the collisions in each local authority that
# involved at least one pedal cycle (vehicle_type == 1).
# Steps: (a) one row per collision with a flag "involves a cycle"
#        (b) merge on the local authority from the collision file (which kind of merge?)
#        (c) collapse to local authority, and merge onto the 2024 rows of the panel
# How many local authorities have no cycle collisions? Are those missing or zero?
# Remember to read collision_index as text!
# TODO

# ---- Task 4: wide -> long, with messy column names ----------------------------
# Sheet "MYE2 - Persons" of data/raw/mye25tablesuk.xlsx has one column per single
# year of age for mid-2025 ("0", "1", ..., "89", "90 and over").
# Compute the population aged 17 and over (old enough to drive) for each of our
# 350 local authorities, merge it onto the 2025 panel (1:1), and compute
# collisions per 100,000 people aged 17+.
# Hint: melt, then turn the age column into a number.
# TODO
