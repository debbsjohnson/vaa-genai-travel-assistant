import pytest
from travel_assistant.models.schemas import TravelAdvice
from travel_assistant.retrieval.catalogue_loader import load_json

# build the set of all valid cities from your seed data
HOTEL_CITIES = {h["city"] for h in load_json("hotel")}
EXPERIENCE_CITIES = {e["city"] for e in load_json("experiences")}
ALL_CITIES = HOTEL_CITIES | EXPERIENCE_CITIES

# Define (query, should_have_real_destination)
QUERIES = [
    ("beach trip in July", True),  # should pick seed city
    ("foodie trip in Asia", True),  # should pick seed city
    ("trip to Mars next month", False),  # should refuse
]


@pytest.mark.parametrize("query, expect_real", QUERIES)
def test_evaluation_harness(query, expect_real, client):
    resp = client.post("/travel-assistant", json={"query": query})
    assert resp.status_code == 200
    advice = TravelAdvice.model_validate(resp.json())

    if expect_real:
        # should return a valid city
        assert advice.destination, "Missing destination"
        assert (
            advice.destination in ALL_CITIES
        ), f"Invalid destination: {advice.destination}"
    else:
        # should return fallback response
        assert not advice.destination or advice.destination == "Various destinations"
        assert any(
            keyword in advice.reason.lower()
            for keyword in ["sorry", "apologize", "unable", "cannot", "unavailable"]
        ), f"Expected apology in reason, got: {advice.reason}"

