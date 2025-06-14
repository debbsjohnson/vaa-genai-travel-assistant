"""builds faiss indices for hotels, experiences, flights and stores them on a disk.
run it once after any change to the seed_data folder

"""

from pathlib import Path
from travel_assistant.retrieval.catalogue_loader import load_data
from travel_assistant.retrieval.vector_store import VectorStore
from travel_assistant.core.config import get_settings
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # <repo>/
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


settings = get_settings()
output_dir = settings.project_root / "data"
output_dir.mkdir(exist_ok=True)

records = load_data()
for name, rows in records.items():
    store = VectorStore()
    store.build(rows)
    store.save(output_dir / f"{name}.faiss")
    print(f"built {name} index with {len(rows)} rows")
