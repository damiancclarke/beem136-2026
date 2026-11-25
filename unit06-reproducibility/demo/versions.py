# versions.py: the same five lines of pandas, run under different versions
import pandas as pd
print("pandas", pd.__version__)

df = pd.DataFrame({"country":    ["Wales", "Wales", "England", "England"],
                   "la_code":    ["W06000001", "W06000002", "E06000001", "E06000002"],
                   "collisions": [120, 80, 300, 250]})

# (1) a "fix" to one value, written as chained assignment
df["collisions"][df["la_code"] == "W06000002"] = 0
print("(1) total collisions:", df["collisions"].sum())

# (2) mean by country, with a text column still in the data
try:
    print("(2)", df.groupby("country").mean().to_dict())
except Exception as e:
    print("(2) ERROR:", type(e).__name__)

# (3) what type is the area code?
print("(3) dtype of la_code:", df["la_code"].dtype)
