"""
03_build_panel.py
Merge population, collisions and the policy into the final panel:
one row per GB local authority and year, 2022-2025.
Input:  output/population.csv, output/collisions_la_year.csv  (from scripts 01 and 02)
        data/raw/lad22_to_lad23_lookup.csv, data/raw/lad24_to_lad25_lookup.csv  (ONS)
        data/policy/wales_20mph.csv
Output: output/panel.csv  (1,400 rows), output/rates_by_country.csv
Run from the unit05-datawrangling folder with:  python code/03_build_panel.py
"""
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
POLICY = Path("data/policy")
OUTPUT = Path("output")

pop = pd.read_csv(OUTPUT / "population.csv")
la_year = pd.read_csv(OUTPUT / "collisions_la_year.csv")

# ---- 1. First attempt: merge collisions onto the population skeleton --------
# indicator=True adds a column _merge saying where each row came from
# (like Stata's _merge: left_only = 1, right_only = 2, both = 3).
first = pop.merge(la_year, on=["la_code", "year"], how="outer", indicator=True)
print("First attempt:", first["_merge"].value_counts().to_dict())

# Who did not match? Always look at the non-matches before doing anything else.
problems = first[first["_merge"] != "both"]
print(problems.groupby(["_merge", "year"], observed=True).size())
print(problems.loc[problems["_merge"] == "right_only", "la_code"].value_counts().sort_index())

# ---- 2. Build a crosswalk from the official ONS lookups ---------------------
# (a) April 2023: 17 districts in Cumbria, North Yorkshire and Somerset were
#     abolished and replaced by 4 new unitary authorities. The 2022 collisions
#     use the old codes, the population file uses the new ones.
# (b) April 2025: a small boundary change gave Barnsley and Sheffield new codes.
#     The 2025 collisions use the new codes, the population file the old ones.
# The files start with an invisible "byte order mark", hence utf-8-sig.
lu23 = pd.read_csv(RAW / "lad22_to_lad23_lookup.csv", encoding="utf-8-sig")
lu25 = pd.read_csv(RAW / "lad24_to_lad25_lookup.csv", encoding="utf-8-sig")

# We map every code to the geography used by the population file
xwalk_a = (lu23.loc[lu23["LAD22CD"] != lu23["LAD23CD"], ["LAD22CD", "LAD23CD"]]
               .rename(columns={"LAD22CD": "code_in_data", "LAD23CD": "la_code_pop"}))
xwalk_b = (lu25.loc[lu25["LAD24CD"] != lu25["LAD25CD"], ["LAD25CD", "LAD24CD"]]
               .rename(columns={"LAD25CD": "code_in_data", "LAD24CD": "la_code_pop"}))
xwalk = pd.concat([xwalk_a, xwalk_b], ignore_index=True)   # an append!
print(f"Crosswalk: {len(xwalk_a)} + {len(xwalk_b)} = {len(xwalk)} changed codes")
print(xwalk)

assert xwalk["code_in_data"].is_unique, "each old code must point to ONE new code"
assert xwalk["la_code_pop"].isin(pop["la_code"]).all(), "targets must exist in pop"

# ---- 3. Recode the collisions, then collapse AGAIN ----------------------------
# m:1 merge: many collision rows can share a code, each code is once in xwalk
la_year = la_year.merge(xwalk, left_on="la_code", right_on="code_in_data",
                        how="left", validate="m:1")
la_year["la_code"] = la_year["la_code_pop"].fillna(la_year["la_code"])
la_year = la_year.drop(columns=["code_in_data", "la_code_pop"])
# Allerdale, Carlisle and Copeland are now three rows each called Cumberland in
# 2022, so we add them up into one row.
la_year = la_year.groupby(["la_code", "year"], as_index=False).sum()

# ---- 4. Heathrow --------------------------------------------------------------
# STATS19 gives Heathrow Airport its own code, EHEATHROW. It is not a local
# authority (it is inside Hillingdon) and has no population, so we drop it.
heathrow = la_year["la_code"] == "EHEATHROW"
print("Dropping Heathrow:", la_year.loc[heathrow, "collisions"].sum(), "collisions")
la_year = la_year[~heathrow]

# ---- 5. Second attempt: this time we can demand a perfect 1:1 merge -----------
panel = pop.merge(la_year, on=["la_code", "year"], how="outer",
                  indicator=True, validate="1:1")
print("Second attempt:", panel["_merge"].value_counts().to_dict())
assert (panel["_merge"] == "both").all()
panel = panel.drop(columns="_merge")

# ---- 6. Merge in the policy: m:1 -----------------------------------------------
# Four rows per local authority in the panel, one row per authority in the policy
# file. Only Welsh authorities are in it, so "left_only" is expected here, and
# means "not treated".
policy = pd.read_csv(POLICY / "wales_20mph.csv")
panel = panel.merge(policy[["la_code", "default_20mph_from"]], on="la_code",
                    how="left", validate="m:1", indicator=True)
print("Policy merge:", panel["_merge"].value_counts().to_dict())
panel["wales"] = (panel["_merge"] == "both").astype(int)
panel = panel.drop(columns="_merge")

# ---- 7. Final variables ----------------------------------------------------------
panel["country"] = panel["la_code"].str[0].map({"E": "England", "W": "Wales",
                                                 "S": "Scotland"})
# The limit started on 17 Sept 2023, so 2023 is partly treated
panel["post"] = (panel["year"] >= 2024).astype(int)
panel["collisions_per_100k"] = panel["collisions"] / panel["population"] * 100_000

# ---- 8. Final checks: the structure we wrote down before we started -----------
assert len(panel) == 350 * 4
assert not panel.duplicated(["la_code", "year"]).any()
assert panel["country"].notna().all()
assert panel.groupby("la_code")["wales"].nunique().eq(1).all()
assert panel["wales"].sum() == 22 * 4
print(panel.head(4))

panel.to_csv(OUTPUT / "panel.csv", index=False)

# ---- 9. A first look --------------------------------------------------------------
by_country = panel.groupby(["country", "year"])[["collisions", "on_20mph", "population"]].sum()
by_country["per_100k"] = (by_country["collisions"] / by_country["population"] * 100_000).round(1)
by_country["share_20mph"] = (by_country["on_20mph"] / by_country["collisions"]).round(3)
table = by_country[["per_100k", "share_20mph"]].unstack("country")
print(table)
table.to_csv(OUTPUT / "rates_by_country.csv")
