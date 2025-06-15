from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from travel_assistant.core.config import get_settings
from travel_assistant.retrieval.vector_store import VectorStore

settings = get_settings()
DATA_DIR: Path = settings.project_root / "data"


@lru_cache
def load_store(name: str) -> VectorStore:
    store = VectorStore()
    store.load(DATA_DIR / f"{name}.faiss")
    return store


# initialize cached vector stores
_vs_hotel = load_store("hotels")
_vs_flight = load_store("flights")
_vs_exp = load_store("experiences")


def _filter_by_city(rows: list[dict], city: str) -> list[dict]:
    """Filter rows by city (case-insensitive)"""
    if not city:
        return rows
    return [r for r in rows if r.get("city", "").lower() == city.lower()]


def search_hotels(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search hotels matching query within the specified city"""
    # get all hotels in the target city
    city_hotels = _filter_by_city(_vs_hotel.meta, city)

    if city_hotels:
        # perform search within city-specific hotels
        return _vs_hotel.search_subset(query, city_hotels, k)

    # fallback to global search if no city specified or no city matches
    return _vs_hotel.search(query, k)


def search_flights(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search flights matching query within the specified city"""
    # get all flights in the target city
    city_flights = _filter_by_city(_vs_flight.meta, city)

    if city_flights:
        # perform search within city-specific flights
        return _vs_flight.search_subset(query, city_flights, k)

    # fallback to global search
    return _vs_flight.search(query, k)


def search_experiences(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search experiences matching query within the specified city"""
    # get all experiences in the target city
    city_experiences = _filter_by_city(_vs_exp.meta, city)

    if city_experiences:
        # perform search within city-specific experiences
        return _vs_exp.search_subset(query, city_experiences, k)

    # fallback to global search
    return _vs_exp.search(query, k)
