import json
from pathlib import Path


def load_factors():
    """
    data/emission_factors.json dosyasını okuyup
    emisyon katsayılarını sözlük olarak döndürür.
    """
    data_dir = Path(__file__).resolve().parent.parent / "data"
    factors_path = data_dir / "emission_factors.json"

    with open(factors_path, "r", encoding="utf-8") as f:
        return json.load(f)
