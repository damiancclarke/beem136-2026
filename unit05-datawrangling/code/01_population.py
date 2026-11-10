"""
01_population.py
Build the "skeleton" of our final dataset: one row per GB local authority and year.
Input:  data/raw/mye25tablesuk.xlsx  (ONS mid-year population estimates, sheet MYE4)
Output: output/population.csv        (350 local authorities x 4 years = 1,400 rows)
Run from the unit05-datawrangling folder with:  python code/01_population.py
Needs openpyxl to read Excel files:  pip install openpyxl
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)
YEARS = [2022, 2023, 2024, 2025]

# ---- 1. Read the raw sheet ------------------------------------------------
# The first 7 rows of the sheet are notes for humans, so the header is on row 8.
pop = pd.read_excel(RAW / "mye25tablesuk.xlsx", sheet_name="MYE4", skiprows=7)
print("Raw sheet:", pop.shape)
print(pop.iloc[:3, :6])

# ---- 2. Keep one type of area only ----------------------------------------
# The sheet stacks countries, regions, counties AND local authorities.
# Adding them all up would count every person several times.
print(pop["Geography"].value_counts())
LA_TYPES = ["Unitary Authority", "Non-metropolitan District",
            "Metropolitan District", "London Borough", "Council Area"]
pop = pop[pop["Geography"].isin(LA_TYPES)]
# Northern Ireland is not in the road safety data (it is not in Great Britain)
pop = pop[~pop["Code"].str.startswith("N")]

pop = pop.rename(columns={"Code": "la_code", "Name": "la_name",
                          "Geography": "la_type"})
print("Local authorities by country:",
      pop["la_code"].str[0].value_counts().to_dict())
assert len(pop) == 350, "Expected 296 English + 22 Welsh + 32 Scottish LAs"
assert pop["la_code"].is_unique

# ---- 3. Reshape wide -> long ----------------------------------------------
# One column per year (Mid-2025, Mid-2024, ...) becomes one row per year.
pop = pop.melt(id_vars=["la_code", "la_name", "la_type"],
               var_name="year", value_name="population")
pop["year"] = pop["year"].str.replace("Mid-", "").astype(int)
pop = pop[pop["year"].isin(YEARS)]
pop = pop.sort_values(["la_code", "year"]).reset_index(drop=True)

# ---- 4. Check the structure we expected before we started -----------------
assert len(pop) == 350 * len(YEARS)
assert not pop.duplicated(["la_code", "year"]).any(), "la_code x year must be a key"
assert pop["population"].notna().all()
print(pop.head(4))
print("Rows:", len(pop))

pop.to_csv(OUTPUT / "population.csv", index=False)
