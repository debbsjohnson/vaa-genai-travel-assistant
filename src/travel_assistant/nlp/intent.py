"""very small helper to extract or choose destination + theme."""

import re, random, json
from pathlib import Path
from travel_assistant.core.config import get_settings
from travel_assistant.retrieval import get_all_cities

# LOAD EXPERIENCE ONCE

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CAT_PATH = PROJECT_ROOT / "seed_data" / "experiences_catalogue.json"

with CAT_PATH.open(encoding="utf-8") as f:
    EXPERIENCES = json.load(f)

CITIES = {row["city"] for row in EXPERIENCES}


# helper functions


def parse(query: str):
    """Very basic parser to extract a known city from the query, if any."""
    cities = get_all_cities()
    for city in cities:
        if city.lower() in query.lower():
            # found a city name in the query
            theme = query.replace(city, "", 1).strip(
                ",. "
            )  # theme = query without the city
            return city, theme
    return None, query  # no known city found


def pick_city(theme: str):
    """Choose a fallback city from seed data based on theme keywords."""
    all_cities = list(get_all_cities())
    if not all_cities:
        return None
    theme_lower = (theme or "").lower()
    # simple keyword-based picks:
    if "asia" in theme_lower:
        # prefer an Asian city if available
        for preferred in ["Tokyo", "Delhi", "Singapore", "Hong Kong"]:
            if preferred in all_cities:
                return preferred
    if "beach" in theme_lower or "summer" in theme_lower:
        for preferred in ["Bridgetown", "Tampa", "Miami"]:
            if preferred in all_cities:
                return preferred  # bridgetown (Barbados) or any coastal city in seeds
    if "mountain" in theme_lower:
        if "Denver" in all_cities:
            return "Denver"
    # default to the first city in seed list as a fallback
    return all_cities[0]
