import faiss
import numpy as np
from unittest.mock import patch
import pytest
from travel_assistant.retrieval.vector_store import VectorStore


@pytest.fixture
def vector_store():
    vs = VectorStore()
    vs.meta = [
        {"text": "beach resort", "city": "Miami", "__id": 0},
        {"text": "mountain cabin", "city": "Denver", "__id": 1},
        {"text": "city hotel", "city": "New York", "__id": 2},
    ]
    dim = 3  # Match the number of documents
    vs.index = faiss.IndexFlatL2(dim)
    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],  # beach
            [0.0, 1.0, 0.0],  # mountain
            [0.0, 0.0, 1.0],  # city
        ],
        dtype="float32",
    )
    vs.index.add(embeddings)
    return vs


def test_vector_store_search(vector_store):
    with patch("travel_assistant.retrieval.vector_store.embed_batch") as mock_embed:
        mock_embed.return_value = [[1.0, 0.0, 0.0]]
        results = vector_store.search("beach", k=1)
        assert results[0]["text"] == "beach resort"


def test_search_subset(vector_store):
    with patch("travel_assistant.retrieval.vector_store.embed_batch") as mock_embed:
        mock_embed.return_value = [[1.0, 0.0, 0.0]]
        subset = [r for r in vector_store.meta if r["city"] == "Miami"]
        results = vector_store.search_subset("beach", subset, k=1)
        assert results[0]["city"] == "Miami"
