import sys
from pathlib import Path

# this ensures 'src' directory is on sys.path so imports like 'travel_assistant' work
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest
from travel_assistant.retrieval.catalogue_loader import load_json
from fastapi.testclient import TestClient
from travel_assistant.main import app


@pytest.fixture(scope="session")
def seed_data():
    return {
        "hotels": load_json("hotel"),
        "flights": load_json("flight"),
        "experiences": load_json("experiences"),
    }


# import pytest


@pytest.fixture
def client():
    return TestClient(app)
