# Table 4 replication and robustness extension

**Bauer, Lakdawala and Mueller (2022), “Market-Based Monetary Policy Uncertainty,” *The Economic Journal*.**  
Paper: https://doi.org/10.1093/ej/ueab086  
Original replication package: https://doi.org/10.5281/zenodo.5566246

This folder reproduces the authors' **Table 4**, then implements one sensitivity check for the **10-year nominal US Treasury yield**, specification 2. It is a focused subset of the published replication package, not an attempt to recreate every figure and table in the article.

## Question and specification

Do changes in monetary-policy uncertainty (MPU) remain positively associated with changes in the 10-year Treasury yield when the announcement with the largest absolute change in MPU is omitted?

The estimation uses the authors' original specification: an intercept, a monetary-policy surprise (MPS), and MPU. The model is estimated using OLS with **HC0 heteroskedasticity-robust standard errors**. The only change in the extension is removing **9 August 2011**, the observation with the largest absolute MPU change in the supplied Table 4 sample. The authors' exclusion of the July 2007–June 2009 financial-crisis period is maintained.

## Requirements

- MATLAB with the **Econometrics Toolbox** and **Statistics and Machine Learning Toolbox**. The authors used MATLAB R2021a; the provided compatibility changes support the newer MATLAB Online interface used for this reproduction.
- No separate R or Python environment is required for this focused exercise.
- All data needed for Table 4 and the extension are in `data/tab4data.csv` (processed data provided by the paper's authors).

## Run instructions

1. Download and extract this folder. In MATLAB, make **this `tutorial-mpu` directory** the current folder.
2. Run `tab4` to reproduce Table 4. The script creates matrices `tab4a` and `tab4b` in the Workspace. The 10-year-yield specification-2 MPU coefficient is `tab4a(6,5)` and its robust t-statistic is `tab4a(7,5)`.
3. Run `extension_one_event`. It estimates the full-sample regression and the same model after excluding the specified event. Results are displayed in MATLAB and saved to `results/extension_results.csv`.
4. Compare the displayed estimates with `results/reference_results.csv`.

## Results

| 10-year nominal Treasury yield | Observations | MPU coefficient | HC0 robust t-statistic |
|---|---:|---:|---:|
| Original Table 4 specification 2 | 197 | 0.6849 | 2.82 |
| Exclude 9 August 2011 | 196 | 0.5379 | 2.35 |

Omitting the event reduces the estimated MPU coefficient by approximately **21.5%**. The association remains positive and statistically significant at 5% in both regressions. This sensitivity check does not establish that the omitted observation is invalid or that the association is causal.

The original Table 4 MATLAB script was run successfully in MATLAB Online, and the one-event regression was separately run in MATLAB using the same fitted-model function and HC0 inference. These results were additionally checked independently against the supplied data. The standalone `extension_one_event.m` file is provided so the extension can be re-run from a clean working directory.

## Files and code changes

| File | Purpose |
|---|---|
| `tab4.m` | Authors' Table 4 script, with paths updated to work from this folder |
| `extension_one_event.m` | Sensitivity check: omit the largest absolute MPU-change event |
| `aux_files/olsrob_nodisp.m` | Authors' OLS/robust-inference helper; updated MATLAB `hac()` calling convention, preserving HC0 |
| `aux_files/outreg2.m` | Authors' table-formatting helper, unchanged |
| `data/tab4data.csv` | Authors' processed data for Table 4 |
| `results/reference_results.csv` | Reference coefficients, HC0 standard errors, t-statistics and R-squared values |
| `AUTHORS_README.pdf` | Authors' documentation for their complete original package |

The initial Table 4 run required two technical changes: (1) portable file paths for MATLAB Online, and (2) using a fitted regression model with the current `hac()` function's two-output interface. Both changes affect software compatibility, **not the regression specification or the HC0 standard-error method**.

## Reproducibility assessment and scope

The authors' README supplies software versions, dependencies and a script-to-result mapping. Table 4 can be generated independently using `tab4.m`, but there is no single master script for the full published package; the results of this MATLAB table script are held in Workspace matrices rather than exported as a formatted file. The version-specific `hac()` error also required a documented fix.

Because the original CME futures and options transactions are proprietary, the published package contains **derived MPU series and processed analysis data** rather than the underlying transactions. Accordingly, this is a replication of the Table 4 regression **conditional on the authors' processed data**, not an independent reconstruction of the uncertainty measure.

The original paper, data, scripts and auxiliary functions are credited to **Bauer, Lakdawala and Mueller**. Full documentation and remaining files are available at the authors' replication archive linked above.
