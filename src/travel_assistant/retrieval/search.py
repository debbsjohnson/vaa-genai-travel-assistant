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


def _filter(rows: list[dict], city: str) -> list[dict]:
    """Return only rows matching the given city (case-insensitive)."""
    if not city:
        return rows
    return [r for r in rows if r.get("city", "").lower() == city.lower()]


def search_hotels(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search hotels matching query within the specified city; fall back globally."""
    rows = _filter(_vs_hotel.meta, city)
    if rows:
        # city subset exists → restricted search
        if hasattr(_vs_hotel, "search_subset"):
            return _vs_hotel.search_subset(query, rows, k)
        sims = _vs_hotel.search(query, k * 10)
        return [r for r in sims if r.get("city", "").lower() == city.lower()][:k]
    # no rows for this city → global search fallback
    return _vs_hotel.search(query, k)


def search_flights(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search flights matching query within the specified city."""
    rows = _filter(_vs_flight.meta, city)
    if rows:
        if hasattr(_vs_flight, "search_subset"):
            return _vs_flight.search_subset(query, rows, k)
        sims = _vs_flight.search(query, k * 10)
        return [r for r in sims if r.get("city", "").lower() == city.lower()][:k]
    return _vs_flight.search(query, k)


def search_experiences(query: str, k: int = 3, *, city: str = "") -> list[dict]:
    """Search experiences matching query within the specified city."""
    rows = _filter(_vs_exp.meta, city)
    if rows:
        if hasattr(_vs_exp, "search_subset"):
            return _vs_exp.search_subset(query, rows, k)
        sims = _vs_exp.search(query, k * 10)
        return [r for r in sims if r.get("city", "").lower() == city.lower()][:k]
    return _vs_exp.search(query, k)

    if not results:
        return [{"error": "No hotels found matching your criteria"}]


# from __future__ import annotations

# from functools import lru_cache
# from pathlib import Path

# from travel_assistant.core.config import get_settings
# from travel_assistant.retrieval.vector_store import VectorStore

# settings = get_settings()
# DATA_DIR: Path = settings.project_root / "data"


# @lru_cache
# def load_store(name: str) -> VectorStore:
#     "load and cache a Vectorstore (faiss index + metadata)"

#     # idx_path = DATA_DIR / f"{name}.faiss"
#     store = VectorStore()
#     store.load(DATA_DIR / f"{name}.faiss")
#     return store


# vs_hotel = load_store("hotels")
# vs_flight = load_store("flights")
# vs_experience = load_store("experiences")

# PUBLIC HELPERS USED BY LLM TOOLS


# def _filter(rows: list[dict], city: str) -> list[dict]:
#     return [r for r in rows if r["city"].lower() == city.lower()]


# def search_hotels(query: str, k: int = 3, *, city: str) -> list[dict]:
#     rows = _filter(vs_hotel.meta, city)
#     return vs_hotel.search(query, k, rows) if rows else []


# def search_flights(query: str, k: int = 3, *, city: str) -> list[dict]:
#     rows = _filter(vs_flight.meta, city)
#     return vs_flight.search(query, k, rows) if rows else []


# def search_experiences(query: str, k: int = 3, *, city: str) -> list[dict]:
#     rows = _filter(vs_experience.meta, city)
#     return vs_experience.search(query, k, rows) if rows else []


# def _filter(rows, city):
#     return [r for r in rows if r["city"].lower() == city.lower()]


# def search_hotels(query: str, k: int = 3, *, city: str) -> list[dict]:
#     subset = _filter(vs_hotel.meta, city)
#     return vs_hotel.search_subset(query, subset, k)


# def search_flights(query: str, k: int = 3, *, city: str) -> list[dict]:
#     subset = _filter(vs_flight.meta, city)
#     return vs_flight.search_subset(query, subset, k)


# def search_experiences(query: str, k: int = 3, *, city: str) -> list[dict]:
#     subset = _filter(vs_experience.meta, city)
#     return vs_experience.search_subset(query, subset, k)


# def search_hotels(query: str, k: int = 3) -> list[dict]:
#     return load_store("hotels").search(query, k)


# def search_flights(query: str, k: int = 3) -> list[dict]:
#     return load_store("flights").search(query, k)


# def search_experiences(query: str, k: int = 3) -> list[dict]:
#     return load_store("experiences").search(query, k)
