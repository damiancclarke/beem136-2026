# Collapse: many rows -> one row per group.
import pandas as pd

both = pd.DataFrame({
    "id":   ["24A", "24B", "25A", "25B", "25C"],
    "year": [2024, 2024, 2025, 2025, 2025],
    "la":   ["Leeds", "Exeter", "Leeds", "Leeds", "Cardiff"],
})

collisions = (both.groupby(["la", "year"], as_index=False)
              .agg(collisions=("id", "count")))
print(collisions)

# Exeter 2025 and Cardiff 2024 have NO ROW, not a row with zero.
