"""Very small helper to extract or choose destination + theme."""

import re, random, json
from pathlib import Path
from travel_assistant.core.config import get_settings


# ── load experiences once ────────────────────────────────────────────
# CAT_PATH = Path(__file__).resolve().parents[2] / "data" / "experiences_catalogue.json"

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # repo root
CAT_PATH = PROJECT_ROOT / "seed_data" / "experiences_catalogue.json"

with CAT_PATH.open(encoding="utf-8") as f:
    EXPERIENCES = json.load(f)

CITIES = {row["city"] for row in EXPERIENCES}


# ── helper functions ────────────────────────────────────────────────
def parse(query: str) -> tuple[str | None, str | None]:
    """Return (city, theme); either may be None."""
    q = query.lower()
    theme = next(
        (t for t in ["foodie", "beach", "adventure", "culture", "luxury"] if t in q),
        None,
    )
    for city in CITIES:
        if re.search(rf"\b{re.escape(city.lower())}\b", q):
            return city, theme
    return None, theme


def pick_city(theme: str | None) -> str:
    """Choose a city; if theme given, prefer cities whose name contains it."""
    themed = [c for c in CITIES if theme and theme in c.lower()]
    pool = themed or sorted(CITIES)
    if not pool:
        raise RuntimeError("Catalogue contains no cities")
    return random.choice(pool)  # or pool[0] for deterministic tests
