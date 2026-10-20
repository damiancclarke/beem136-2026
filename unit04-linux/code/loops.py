import pandas as pd
import statsmodels.formula.api as smf

mroz = pd.read_csv("data/mroz.csv")
workers = mroz[mroz["inlf"] == 1]

specs = {
    "(1) baseline": "lwage ~ educ",
    "(2) + experience": "lwage ~ educ + exper + expersq",
    "(3) + family": "lwage ~ educ + exper + expersq + kidslt6 + kidsge6",
}

for name, formula in specs.items():
    res = smf.ols(formula, data=workers).fit(cov_type="HC1")
    print(f"{name:20s} educ = {res.params['educ']:.3f} ({res.bse['educ']:.3f})")
