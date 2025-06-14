# api/deps.py
from functools import lru_cache
from travel_assistant.core.config import get_settings, Settings
from travel_assistant.retrieval.vector_store import VectorStore
from pathlib import Path


@lru_cache
def settings_dep() -> Settings:
    return get_settings()


def _load_vs(name: str) -> VectorStore:
    vs = VectorStore()
    vs.load(Path(get_settings().project_root, "data", f"{name}.faiss"))
    return vs


hotels_store_dep = lru_cache()(_load_vs)("hotels")  # no Settings arg
flights_store_dep = lru_cache()(_load_vs)("flights")
experiences_store_dep = lru_cache()(_load_vs)("experiences")
