"""
02_collisions.py
From one row per collision (microdata) to one row per local authority and year.
Input:  data/raw/dft-road-casualty-statistics-collision-YYYY.csv, YYYY = 2022-2025
Output: output/collisions_la_year.csv
Run from the unit05-datawrangling folder with:  python code/02_collisions.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)
YEARS = [2022, 2023, 2024, 2025]

# Only read the columns we need: each file has 44 columns and about 100,000 rows
COLS = ["collision_index", "collision_year", "local_authority_ons_district",
        "collision_severity", "number_of_casualties", "speed_limit"]

# ---- 1. Read each year and append ------------------------------------------
pieces = []
for year in YEARS:
    # Identifiers are labels, not numbers: always read them as text (str).
    # Without dtype=, pandas reads the 2024 collision_index as text in some
    # rows and as integers in others, and later merges silently fail.
    df = pd.read_csv(RAW / f"dft-road-casualty-statistics-collision-{year}.csv",
                     usecols=COLS,
                     dtype={"collision_index": str,
                            "local_authority_ons_district": str})
    assert (df["collision_year"] == year).all(), f"{year} file has other years in it"
    print(year, df.shape)
    pieces.append(df)

collisions = pd.concat(pieces, ignore_index=True)
print("Appended:", collisions.shape)

# ---- 2. Check the unit of observation ---------------------------------------
# One row should be one collision, so collision_index must be unique
assert collisions["collision_index"].is_unique
assert len(collisions) == sum(len(p) for p in pieces)

# ---- 3. Clean -----------------------------------------------------------------
collisions = collisions.rename(columns={"local_authority_ons_district": "la_code",
                                        "collision_year": "year"})
# STATS19 writes "missing" as -1. Left alone, -1 would count as a speed limit.
print("Speed limit values:", collisions["speed_limit"].value_counts().sort_index().to_dict())
collisions["speed_limit"] = collisions["speed_limit"].replace(-1, np.nan)

# severity is coded 1 = fatal, 2 = serious, 3 = slight
collisions["fatal"] = (collisions["collision_severity"] == 1).astype(int)
collisions["ksi"] = (collisions["collision_severity"] <= 2).astype(int)   # killed or seriously injured
collisions["on_20mph"] = (collisions["speed_limit"] == 20).astype(int)

# ---- 4. Collapse: one row per local authority x year --------------------------
la_year = (collisions
           .groupby(["la_code", "year"], as_index=False)
           .agg(collisions=("collision_index", "count"),
                casualties=("number_of_casualties", "sum"),
                fatal=("fatal", "sum"),
                ksi=("ksi", "sum"),
                on_20mph=("on_20mph", "sum")))

# Nothing lost along the way?
assert la_year["collisions"].sum() == len(collisions)
print(la_year.head(4))
print("Rows after collapse:", len(la_year),
      f" (we expected 350 x {len(YEARS)} = {350 * len(YEARS):,}. Why not?)")
print("Distinct codes by year:", la_year.groupby("year")["la_code"].nunique().to_dict())

# ---- 5. A trap: filter first, then count -------------------------------------
# Counting the rows of fatal collisions only gives no row at all for an
# area-year with zero fatal collisions. The zeros disappear, they are not 0.
fatal_only = collisions[collisions["fatal"] == 1].groupby(["la_code", "year"]).size()
print("Area-years with a fatal collision:", len(fatal_only),
      " | area-years with fatal == 0 above:", (la_year["fatal"] == 0).sum())

la_year.to_csv(OUTPUT / "collisions_la_year.csv", index=False)
