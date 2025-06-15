from pathlib import Path
import json

ROOT_DIR = (
    Path(__file__).resolve().parents[3]
)  # (for catalogue_loader.py, src, retriever, travel_assistant)
SEED_DIR = ROOT_DIR / "seed_data"


def load_json(name: str) -> list[dict]:
    with open(SEED_DIR / f"{name}_catalogue.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_data():
    return {
        "hotels": load_json("hotel"),
        "flights": load_json("flight"),
        "experiences": load_json("experiences"),
    }


def load_cities() -> set[str]:
    cities = set()
    for name in ["hotel", "flight", "experiences"]:
        data = load_json(name)
        cities.update({item["city"].lower() for item in data if "city" in item})
    return cities
