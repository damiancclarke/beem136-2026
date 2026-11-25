import os
os.chdir("C:/Users/rsmith/Dropbox/PhD/20mph/data")

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("panel.csv")

# Isles of Scilly is tiny and noisy, referee 2 asked us to drop its collisions
df["collisions"][df["la_code"] == "E06000053"] = np.nan
df = df.dropna(subset=["collisions"])

df["rate"] = df["collisions"] / df["population"] * 100000
df["lrate"] = np.log(df["rate"])

# means by authority (for the appendix)
la_means = df.groupby("la_code").mean()
la_means.to_csv("la_means.csv")

# 2x2 table
for c in set(df["country"]):
    sub = df[df["country"] == c]
    print(c, sub[sub.post == 0].rate.mean(), sub[sub.post == 1].rate.mean())

# main regression
m = smf.ols("lrate ~ wales:post + C(la_code) + C(year)", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["la_code"]})
print(m.params["wales:post"], m.bse["wales:post"])

# bootstrap by authority
las = df["la_code"].unique()
b = []
for r in range(199):
    draw = np.random.choice(las, len(las))
    bs = pd.concat([df[df.la_code == l] for l in draw])
    bs["la_b"] = np.repeat(np.arange(len(draw)), [sum(df.la_code == l) for l in draw])
    mb = smf.ols("lrate ~ wales:post + C(la_b) + C(year)", data=bs).fit()
    b.append(mb.params["wales:post"])
print("bootstrap se", np.std(b))

f = open("C:/Users/rsmith/Dropbox/PhD/20mph/paper/table2.tex", "w")
f.write("%.3f & (%.3f) \\\\" % (m.params["wales:post"], np.std(b)))
f.close()
