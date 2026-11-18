"""
05_figures.py
Figures from the panel built in 01-03: from a first default plot to a figure
you could put in a paper, plus some deliberately bad examples.
Run from the unit05-datawrangling folder:  python code/05_figures.py
Needs output/panel.csv (bash code/run_all.sh) and matplotlib.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # write files, never open a window
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT = Path("output")
FIGS = OUTPUT / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# One colour AND one marker shape per country, fixed for every figure.
# Colours are steps of viridis (readable with colour blindness and in grey);
# the shapes mean countries can be told apart without colour at all.
COLOURS = {"England": "#440154", "Wales": "#25848e", "Scotland": "#5ec962"}
MARKERS = {"England": "o", "Wales": "s", "Scotland": "^"}
# No titles inside the figures: what a figure shows goes in the caption
# (on the slide, or in the paper), where it can be edited with the text.
GREY = "#b9b9b4"
POLICY = 2023 + (260 / 365)                # 17 September 2023, as a year

plt.rcParams.update({"font.size": 13, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 100})

panel = pd.read_csv(OUTPUT / "panel.csv")

# ---- The numbers behind most figures: add up first, divide after ------------
by_country = (panel.groupby(["country", "year"], as_index=False)
              [["collisions", "population"]].sum())
by_country["per_100k"] = by_country["collisions"] / by_country["population"] * 100_000
assert len(by_country) == 3 * 4


def save(fig, name):
    fig.savefig(FIGS / f"{name}.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight")   # vector, for papers
    plt.close(fig)


# ---- 1. A first try: pandas defaults ------------------------------------------
# .plot() draws one line per COLUMN, so it wants wide data: reshape first.
wide = by_country.pivot(index="year", columns="country", values="per_100k")
with plt.style.context("default"):        # matplotlib exactly as it comes
    ax = wide.plot()
    save(ax.get_figure(), "fig1_default")

# ---- 2. The same data, made to answer the question ----------------------------
# Levels differ a lot between countries, so compare CHANGES: index 2022 = 100.
base = by_country[by_country["year"] == 2022].set_index("country")["per_100k"]
by_country["index"] = 100 * by_country["per_100k"] / by_country["country"].map(base)

fig, ax = plt.subplots(figsize=(9, 5))
for country, d in by_country.groupby("country"):
    ax.plot(d["year"], d["index"], color=COLOURS[country], lw=2.5,
            marker=MARKERS[country], ms=9)
    last = d[d["year"] == 2025].iloc[0]
    ax.annotate(country, (2025, last["index"]), xytext=(8, 0),
                textcoords="offset points", va="center",
                color="#333333", fontweight="bold")
ax.axvline(POLICY, color="#555555", ls="--", lw=1)
ax.text(POLICY + 0.04, 101.8, "Wales: 20mph\ndefault starts",
        fontsize=11, color="#555555", va="top")
ax.axhline(100, color=GREY, lw=1, zorder=0)
ax.set_xticks([2022, 2023, 2024, 2025])
ax.set_xlim(2021.8, 2025.6)
ax.set_ylabel("Collisions per person (2022 = 100)")
save(fig, "fig2_indexed")

# ---- 3. A figure for US: the distribution, to find surprises -------------------
y24 = panel[panel["year"] == 2024]
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(y24["collisions_per_100k"], bins=60, color=COLOURS["England"],
        edgecolor="white")
col = y24.loc[y24["la_name"] == "City of London", "collisions_per_100k"].iloc[0]
ax.annotate("City of London\n(15,000 residents,\nhundreds of thousands\nof commuters)",
            (col, 1), xytext=(col - 330, 35), fontsize=11,
            arrowprops=dict(arrowstyle="->", color="#555555"))
ax.set_xlabel("Collisions per 100,000 residents, 2024")
ax.set_ylabel("Local authorities")
save(fig, "fig3_histogram")

# ---- 4. Too many lines: 22 Welsh authorities, default colours -----------------
wales = panel[panel["wales"] == 1]
fig, ax = plt.subplots(figsize=(9, 5))
for name, d in wales.groupby("la_name"):
    ax.plot(d["year"], d["collisions_per_100k"], label=name)
ax.legend(fontsize=7, ncol=2, bbox_to_anchor=(1, 1))
save(fig, "fig4_spaghetti")

# ---- 5. The same lines in grey, with the totals that matter on top -----------
wales = wales.assign(index=100 * wales["collisions_per_100k"]
                     / wales["la_code"].map(wales[wales["year"] == 2022]
                                            .set_index("la_code")["collisions_per_100k"]))
fig, ax = plt.subplots(figsize=(9, 5))
for _, d in wales.groupby("la_code"):
    ax.plot(d["year"], d["index"], color=GREY, lw=1)
for country in ["England", "Wales"]:
    d = by_country[by_country["country"] == country]
    ax.plot(d["year"], d["index"], color=COLOURS[country], lw=3,
            marker=MARKERS[country], ms=9)
    ax.annotate(f"{country} (all)", (2025, d["index"].iloc[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", fontweight="bold")
ax.annotate("each grey line: one\nWelsh local authority", (2022.08, 52),
            fontsize=11, color="#555555")
ax.axvline(POLICY, color="#555555", ls="--", lw=1)
ax.set_xticks([2022, 2023, 2024, 2025])
ax.set_xlim(2021.8, 2025.7)
ax.set_ylabel("Collisions per person (2022 = 100)")
save(fig, "fig5_highlight")

# ---- 6. Two years, one point per authority: a 45-degree line -------------------
sc = panel.pivot(index=["la_code", "la_name", "country"], columns="year",
                 values="collisions_per_100k").reset_index()
fig, ax = plt.subplots(figsize=(6.5, 6.5))
for country in ["England", "Scotland", "Wales"]:
    d = sc[sc["country"] == country]
    ax.scatter(d[2022], d[2024], s=45 if country == "Wales" else 22,
               marker=MARKERS[country],
               color=COLOURS[country], alpha=1 if country == "Wales" else 0.55,
               edgecolor="white", linewidth=0.6, label=country,
               zorder=3 if country == "Wales" else 2)
ax.plot([20, 1600], [20, 1600], color="#555555", lw=1)
ax.text(700, 330, "below the line:\nfewer in 2024", fontsize=11, color="#555555")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(20, 1600)
ax.set_ylim(20, 1600)
ticks = [25, 50, 100, 200, 500, 1000]
ax.set_xticks(ticks, [f"{t:,}" for t in ticks])
ax.set_yticks(ticks, [f"{t:,}" for t in ticks])
ax.minorticks_off()
ax.set_xlabel("Collisions per 100,000, 2022 (log scale)")
ax.set_ylabel("Collisions per 100,000, 2024 (log scale)")
ax.legend(frameon=False, loc="upper left")
save(fig, "fig6_scatter")

# ---- 7. The same two bars, two y-axes ------------------------------------------
w = by_country[by_country["country"] == "Wales"].set_index("year")["per_100k"]
fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
for ax, bottom, title in [(axes[0], 90, "Axis starts at 90"),
                          (axes[1], 0, "Axis starts at 0")]:
    ax.bar(["2022", "2024"], [w[2022], w[2024]], color=COLOURS["Wales"], width=0.6)
    ax.set_ylim(bottom, 110)
    ax.set_title(title, loc="left")
axes[0].set_ylabel("Collisions per 100,000, Wales")
fig.tight_layout()
save(fig, "fig7_truncated")

print("Figures written to", FIGS)
print(by_country.round(1))
