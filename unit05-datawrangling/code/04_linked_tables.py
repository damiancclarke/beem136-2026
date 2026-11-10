"""
04_linked_tables.py
STATS19 is really three linked tables. For 2024:
    collision  one row per collision                      key: collision_index
    vehicle    one row per vehicle in a collision         key: collision_index + vehicle_reference
    casualty   one row per person hurt in a collision     key: collision_index + casualty_reference
Each casualty is linked to one vehicle (for pedestrians, the vehicle that hit them).
This script shows three things that go wrong when joining them, and how to check.
Input:  data/raw/dft-road-casualty-statistics-{collision,vehicle,casualty}-2024.csv
        output/panel.csv (from 03_build_panel.py)
Output: output/pedestrians_la_2024.csv
Run from the unit05-datawrangling folder with:  python code/04_linked_tables.py
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUTPUT = Path("output")


def stats19(table, **kwargs):
    """Read one STATS19 table for 2024."""
    return pd.read_csv(RAW / f"dft-road-casualty-statistics-{table}-2024.csv", **kwargs)


# ---- 1. Trap 1: identifiers read as numbers ------------------------------------
# Without dtype=, pandas guesses the type of each column, in chunks. In the 2024
# collision file it guesses text for some rows and integers for others.
# (You will see pandas print a DtypeWarning here: that warning is the clue.)
naive = stats19("collision", usecols=["collision_index"])
print("Types pandas guessed:",
      naive["collision_index"].map(type).value_counts().to_dict())

vehicles = stats19("vehicle", dtype={"collision_index": str},
                   usecols=["collision_index", "vehicle_reference", "vehicle_type"])
test = vehicles.merge(naive, on="collision_index", how="left", indicator=True)
print("Naive merge of vehicles to collisions:", test["_merge"].value_counts().to_dict())

# The fix: identifiers are labels, so read them as text
ID = {"collision_index": str, "local_authority_ons_district": str}
collisions = stats19("collision", dtype=ID,
                     usecols=["collision_index", "local_authority_ons_district",
                              "number_of_vehicles", "number_of_casualties"])
casualties = stats19("casualty", dtype=ID)

# ---- 2. Check the keys of each table -------------------------------------------
assert collisions["collision_index"].is_unique
assert not vehicles.duplicated(["collision_index", "vehicle_reference"]).any()
assert not casualties.duplicated(["collision_index", "casualty_reference"]).any()
# The counts stored in the collision table should agree with the other tables
assert collisions["number_of_vehicles"].sum() == len(vehicles)
assert collisions["number_of_casualties"].sum() == len(casualties)
print(f"{len(collisions):,} collisions, {len(vehicles):,} vehicles, "
      f"{len(casualties):,} casualties")

# ---- 3. m:1 merges: vehicles onto collisions, casualties onto vehicles ----------
v = vehicles.merge(collisions, on="collision_index", how="outer",
                   validate="m:1", indicator=True)
print("Vehicles -> collisions:", v["_merge"].value_counts().to_dict())

c = casualties.merge(vehicles[["collision_index", "vehicle_reference", "vehicle_type"]],
                     on=["collision_index", "vehicle_reference"], how="left",
                     validate="m:1", indicator=True)
print("Casualties -> vehicles:", c["_merge"].value_counts().to_dict())

# ---- 4. Trap 2: the many-to-many merge -------------------------------------------
# Joining casualties to vehicles by collision_index ALONE pairs every casualty
# with every vehicle in the same collision. Rows multiply, silently.
wrong = casualties.merge(vehicles, on="collision_index")
print(f"m:m merge: {len(wrong):,} rows from {len(casualties):,} casualties")
try:
    casualties.merge(vehicles, on="collision_index", validate="m:1")
except pd.errors.MergeError as err:
    print("validate= catches it:", str(err).splitlines()[0])

# ---- 5. Trap 3: missing is not always missing -------------------------------------
# Pedestrian casualties (casualty_class 3) per local authority in 2024.
peds = casualties[casualties["casualty_class"] == 3]
peds = peds.merge(collisions[["collision_index", "local_authority_ons_district"]],
                  on="collision_index", how="left", validate="m:1")
peds = (peds.groupby("local_authority_ons_district").size()
            .rename("pedestrian_casualties").reset_index()
            .rename(columns={"local_authority_ons_district": "la_code"}))

panel = pd.read_csv(OUTPUT / "panel.csv")
p24 = panel.loc[panel["year"] == 2024, ["la_code", "la_name", "population"]]
p24 = p24.merge(peds, on="la_code", how="left", validate="1:1", indicator=True)
print("Pedestrians -> 2024 panel:", p24["_merge"].value_counts().to_dict())
print(p24.loc[p24["_merge"] == "left_only", ["la_code", "la_name", "population"]])
# No row means no pedestrian was hurt there: here a missing value is a true zero.
# (2024 uses the same codes as the population file, and Heathrow is dropped.)
p24["pedestrian_casualties"] = p24["pedestrian_casualties"].fillna(0).astype(int)
p24.drop(columns="_merge").to_csv(OUTPUT / "pedestrians_la_2024.csv", index=False)
