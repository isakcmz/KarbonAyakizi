# logic/scenario_store.py

import json
from pathlib import Path
from datetime import datetime


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE = DATA_DIR / "saved_scenarios.json"


def load_scenarios():
    """saved_scenarios.json içindeki tüm senaryoları döndürür."""
    if not FILE.exists():
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_scenarios(scenarios):
    """Tüm senaryoları JSON dosyasına yazar."""
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=4, ensure_ascii=False)


def add_scenario(base_total, new_total, base_data, new_data):
    """Yeni bir senaryoyu JSON listesine ekler."""
    scenarios = load_scenarios()

    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "base_total_kg": base_total,
        "scenario_total_kg": new_total,
        "reduction_kg": base_total - new_total,
        "base_data": base_data,
        "scenario_data": new_data
    }

    scenarios.append(new_entry)
    save_scenarios(scenarios)
