from unittest.mock import patch


@patch("travel_assistant.core.guardrails.OpenAI")  # Updated path
def test_content_moderation(mock_openai, client):
    # mock the moderation response
    mock_client = mock_openai.return_value
    mock_moderation = mock_client.moderations.create.return_value
    mock_moderation.results = [type("obj", (object,), {"flagged": True})]

    resp = client.post(
        "/travel-assistant", json={"query": "inappropriate explicit content"}
    )
    assert resp.status_code == 400
    assert "inappropriate" in resp.json()["detail"]


