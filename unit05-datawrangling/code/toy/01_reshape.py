# Reshape: the same information, wide or long.
import pandas as pd

wide = pd.DataFrame({
    "la":       ["Exeter", "Cardiff"],
    "Mid-2024": [133000, 380000],
    "Mid-2025": [134000, 383000],
})
print(wide)

# wide -> long: one row per area AND year
long = wide.melt(id_vars="la", var_name="year", value_name="population")
print(long)

# long -> wide: back again
back = long.pivot(index="la", columns="year", values="population")
print(back)
