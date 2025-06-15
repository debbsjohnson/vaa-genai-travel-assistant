from .search import search_hotels, search_flights, search_experiences  # noqa: F401

from .catalogue_loader import load_cities


def get_all_cities() -> set[str]:
    return load_cities()
