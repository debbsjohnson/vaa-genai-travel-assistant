from __future__ import annotations

import numpy as np

import pickle
from typing import List, Iterable, Dict
import faiss
from pathlib import Path

from openai import OpenAI
from travel_assistant.core.config import get_settings
import math

settings = get_settings()

client = OpenAI(
    api_key=settings.openai_api_key.get_secret_value(),
    project=settings.openai_project_id,
)


def embed_batch(texts: list[str], max_batch: int = 100) -> list[list[float]]:
    """
    Embed a list of texts, chunking so we never exceed the OpenAI limit
    (max 8192 tokens or 2048 inputs per request, but we stay extra safe at 100).
    """
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), max_batch):
        chunk = texts[i : i + max_batch]
        resp = client.embeddings.create(
            model=settings.embed_model,
            input=chunk,
        )
        all_embeddings.extend([d.embedding for d in resp.data])
    return all_embeddings


def flatten(record: Dict) -> str:
    "converts one row from the catalogue into a single string for the embedding"

    return " ".join(str(v) for v in record.values() if v)


class VectorStore:
    def __init__(self) -> None:
        self.index: faiss.IndexFlatL2 | None = None
        self.meta: List[Dict] = []

    # build and load the index from the seed data
    def build(self, records: Iterable[Dict]) -> None:
        # self.meta = []  #
        # for idx, r in enumerate(records):
        #     r = dict(r)  # copy so we can mutate safely
        #     r["__id"] = idx  # ⭐ store index position for fast lookup
        #     self.meta.append(r)
        self.meta = list(records)
        for i, r in enumerate(self.meta):
            r["__id"] = i
        embeddings = embed_batch([flatten(r) for r in self.meta])
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype=np.float32))

    def save(self, path: Path) -> None:
        if not self.index:
            raise RuntimeError("index not built")
        faiss.write_index(self.index, str(path))
        with open(path.with_suffix(".pkl"), "wb") as f:
            pickle.dump(self.meta, f)

    def load(self, path: Path) -> None:
        self.index = faiss.read_index(str(path))
        with open(path.with_suffix(".pkl"), "rb") as f:
            self.meta = pickle.load(f)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        if self.index is None:
            raise RuntimeError("index not initialised")
        emb = embed_batch([query])[0]
        D, I = self.index.search(np.array([emb], dtype="float32"), k)
        return [self.meta[i] for i in I[0]]

    def search_subset(self, query: str, rows: list[Dict], k: int = 3) -> list[Dict]:
        """Similarity search restricted to the supplied metadata rows."""
        if not rows:
            return []

        if self.index is None:  # Added null check
            raise RuntimeError("index not initialised")

        # embeds query once
        q_emb = embed_batch([query])[0]

        # fetches vectors for the subset rows
        ids = [self.meta.index(r) for r in rows]
        vecs = self.index.reconstruct_n(0, self.index.ntotal)
        sub = [vecs[i] for i in ids]

        # computes cosine distance ( because faiss index is L2; cosine is fine for demo)
        q = np.array([q_emb], dtype="float32")
        dot = np.dot(vecs, q_emb)
        nq = np.linalg.norm(q_emb)
        nv = np.linalg.norm(vecs, axis=1)
        cosine = 1 - dot / (nv * nq + 1e-8)

        # ranks & returns top-k rows
        ranked = sorted(zip(rows, cosine), key=lambda t: t[1])
        return [r for r, _ in ranked[:k]]
