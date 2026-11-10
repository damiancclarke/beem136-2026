"""
get_data.py
Download every raw input file for Unit 5 into data/raw/, exactly as published.
The files are already in the class repository, so you do NOT need to run this.
It is here as a record of where each file came from, and so that anyone can
rebuild data/raw/ from scratch.
Run from the unit05-datawrangling folder with:  python code/get_data.py
"""
from pathlib import Path
from urllib.request import urlretrieve

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

DFT = "https://data.dft.gov.uk/road-accidents-safety-data/"
ONS_POP = ("https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/"
           "populationandmigration/populationestimates/datasets/"
           "populationestimatesforukenglandandwalesscotlandandnorthernireland/"
           "mid2025/mye25tablesuk.xlsx")
ONS_GEO = "https://open-geography-portalx-ons.hub.arcgis.com/api/download/v1/items/"

FILES = {
    # (1) Department for Transport, STATS19 road safety data: one row per collision
    **{f"dft-road-casualty-statistics-collision-{y}.csv":
       f"{DFT}dft-road-casualty-statistics-collision-{y}.csv"
       for y in [2022, 2023, 2024, 2025]},
    # ... one row per vehicle, and one row per casualty (2024 only, for the linked-tables example)
    "dft-road-casualty-statistics-vehicle-2024.csv":
        f"{DFT}dft-road-casualty-statistics-vehicle-2024.csv",
    "dft-road-casualty-statistics-casualty-2024.csv":
        f"{DFT}dft-road-casualty-statistics-casualty-2024.csv",
    # (2) Office for National Statistics, mid-year population estimates (mid-2025 edition)
    "mye25tablesuk.xlsx": ONS_POP,
    # (3) ONS Open Geography Portal, official lookups between local authority codes
    "lad22_to_lad23_lookup.csv": ONS_GEO + "32e1e25b27d7472da86a250c5f0c2d2d/csv?layers=0",
    "lad24_to_lad25_lookup.csv": ONS_GEO + "40d74f80a6cb49f68fdd9fa53efbb1dd/csv?layers=0",
}

for name, url in FILES.items():
    print(f"Downloading {name}")
    urlretrieve(url, RAW / name)

print("Done. Files are in", RAW)
