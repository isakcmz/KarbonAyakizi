import json
from pathlib import Path

# Veri klasörünün yolu
DATA_DIR = Path(__file__).parent.parent / "data"
FACTORS_PATH = DATA_DIR / "emission_factors.json"

with open(FACTORS_PATH, "r", encoding="utf-8") as f:
    FACTORS = json.load(f)
