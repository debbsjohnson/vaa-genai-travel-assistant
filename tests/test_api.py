# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from travel_assistant.main import app
from travel_assistant.models.schemas import TravelAdvice


@pytest.fixture
def client():
    return TestClient(app)


import pytest
from travel_assistant.retrieval.catalogue_loader import load_json

# load seed data once at the beginning
HOTELS = load_json("hotel")
FLIGHTS = load_json("flight")
EXPERIENCES = load_json("experiences")


def test_travel_assistant_returns_seed_data(client, seed_data):
    # this tests with a query that should match seed data
    resp = client.post("/travel-assistant", json={"query": "beach in July"})
    assert resp.status_code == 200

    # to get response and validate structure
    body = resp.json()
    assert "destination" in body
    assert "reason" in body
    assert "budget" in body
    assert "tips" in body

    # checks whether destination appears in seed data
    all_cities = set()
    for hotel in HOTELS:
        all_cities.add(hotel["city"])
    for experience in EXPERIENCES:
        all_cities.add(experience["city"])

    assert (
        body["destination"] in all_cities
    ), f"Destination {body['destination']} not in seed data"


@pytest.mark.parametrize(
    "query",
    [
        "romantic getaway in Paris",
        "family vacation with kids",
        "adventure trip to mountains",
    ],
)
def test_various_queries(client, query):
    resp = client.post("/travel-assistant", json={"query": query})
    assert resp.status_code == 200
    body = resp.json()
    assert body["destination"]


def test_response_schema(client):
    resp = client.post("/travel-assistant", json={"query": "test"})
    assert resp.status_code == 200
    # will raise exception if invalid
    TravelAdvice.model_validate(resp.json())


def test_unknown_destination(client):
    """Test handling of queries for destinations not in seed data"""
    resp = client.post("/travel-assistant", json={"query": "trip to Mars"})
    assert resp.status_code == 200
    body = resp.json()
    assert "Mars" not in body["destination"]

    # after some hassle, more flexible assertion
    reason = body["reason"].lower()
    assert any(
        keyword in reason
        for keyword in ["sorry", "apologize", "unable", "cannot", "unavailable"]
    ), f"Expected apology in reason, got: {reason}"


# # @pytest.mark.asyncio
# def test_travel_assistant_returns_seed_data(client):
#     resp = client.post("/travel-assistant", json={"query": "beach in July"})
#     assert resp.status_code == 200
#     body = resp.json()
#     # Assert destination is in your hotel_catalogue.json
#     destinations = [h["city"] for h in load_hotels_from_json()]
#     assert body["destination"] in destinations

# async def fake_advisor(query, settings, hotels, flights, experiences):
#     return TravelAdvice(
#         destination="Test City",
#         reason="Test reason",
#         budget="Low",
#         tips=["Tip1", "Tip2"],
#     )

# monkeypatch.setattr("travel_assistant.services.advisor.advisor", fake_advisor)

# response = client.post(
#     "/travel-assistant",
#     json={"query": "Any query"},
# )
# assert response.status_code == 200
# data = response.json()
# assert data["destination"] == "Test City"
# assert data["reason"] == "Test reason"
# assert data["budget"] == "Low"
# assert "tips" in data and isinstance(data["tips"], list)
