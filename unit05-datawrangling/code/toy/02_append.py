# Append: stack datasets on top of each other.
import pandas as pd

y24 = pd.DataFrame({
    "id":   ["24A", "24B"],
    "year": [2024, 2024],
    "la":   ["Leeds", "Exeter"],
})
y25 = pd.DataFrame({
    "id":   ["25A", "25B", "25C"],
    "year": [2025, 2025, 2025],
    "la":   ["Leeds", "Leeds", "Cardiff"],
})

both = pd.concat([y24, y25], ignore_index=True)
print(both)

# check: rows after = sum of rows before
assert len(both) == len(y24) + len(y25)
