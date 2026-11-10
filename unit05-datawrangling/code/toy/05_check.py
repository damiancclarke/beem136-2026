# Check: tell pandas what you expect, and it stops you when you are wrong.
import pandas as pd

casualties = pd.DataFrame({
    "id":  ["A", "A", "B"],
    "veh": [1, 2, 1],
    "cas": [1, 2, 1],
})
vehicles = pd.DataFrame({
    "id":   ["A", "A", "B"],
    "veh":  [1, 2, 1],
    "type": ["car", "bus", "car"],
})

# WRONG key: every A-casualty pairs with every A-vehicle (m:m)
wrong = casualties.merge(vehicles, on="id")
print(len(wrong), "rows from", len(casualties), "casualties!")

# validate= turns the silent mistake into an error
try:
    casualties.merge(vehicles, on="id", validate="m:1")
except pd.errors.MergeError as e:
    print("MergeError:", e)

# RIGHT key: one vehicle per casualty
right = casualties.merge(vehicles, on=["id", "veh"], validate="m:1")
print(right)
