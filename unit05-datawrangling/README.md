# Unit 5: Data wrangling

Run everything from this folder (`cd unit05-datawrangling`). You need `pandas` and `openpyxl` (`pip install pandas openpyxl`).

**The question:** did Wales's default 20mph speed limit (17 September 2023) reduce road collisions, compared with England? We build a panel with one row per Great Britain local authority and year, 2022 to 2025: 350 × 4 = 1,400 rows.

| File | What it is |
|---|---|
| `data/raw/dft-road-casualty-statistics-collision-YYYY.csv` | Department for Transport road safety data (STATS19): one row per collision reported to the police, 2022 to 2025 |
| `data/raw/dft-road-casualty-statistics-vehicle-2024.csv` | The same data for 2024, one row per vehicle |
| `data/raw/dft-road-casualty-statistics-casualty-2024.csv` | The same data for 2024, one row per casualty |
| `data/raw/mye25tablesuk.xlsx` | ONS mid-year population estimates (mid-2025 edition). Sheet `MYE4` has one row per area and one column per year |
| `data/raw/lad22_to_lad23_lookup.csv`, `lad24_to_lad25_lookup.csv` | Official ONS lookups between old and new local authority codes |
| `data/policy/wales_20mph.csv` | **Built by us**: the 22 Welsh local authorities, with the date the 20mph default started |
| `code/get_data.py` | Where every raw file came from. You do not need to run it: the files are already here |
| `code/01_population.py` | Population: filter to local authorities, reshape wide to long |
| `code/02_collisions.py` | Collisions: append four years, collapse to local authority × year |
| `code/03_build_panel.py` | Merge everything, fixing local authority codes that changed |
| `code/04_linked_tables.py` | Collisions, vehicles and casualties: three traps when joining tables |
| `code/run_all.sh` | Master script: runs 01 to 04 in order |
| `code/exercise.py` | The class exercise |

To build everything (about 15 seconds):

```bash
bash code/run_all.sh
```

This creates `output/panel.csv` (1,400 rows), plus a log of what each script printed in `output/`. The files in `data/raw/` are exactly as published. **Never edit these**. Change to data only happens in code.
