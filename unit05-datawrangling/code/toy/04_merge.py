# Merge: add columns, matching rows on a key.
import pandas as pd

pop = pd.DataFrame({
    "la":         ["Exeter", "Cardiff", "Leeds"],
    "population": [134000, 383000, 829000],
})
crashes = pd.DataFrame({
    "la":         ["Cardiff", "Leeds", "Heathrow"],
    "collisions": [282, 1385, 33],
})

# Exeter is only on the left, Heathrow only on the right.
# how= decides what happens to them. Try "inner", "left", "right".
merged = pop.merge(crashes, on="la", how="outer", indicator=True)
print(merged)

print(merged["_merge"].value_counts())
