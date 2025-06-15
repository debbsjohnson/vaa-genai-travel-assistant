from unittest.mock import patch, AsyncMock
import pytest
from travel_assistant.models.schemas import TravelAdvice
from travel_assistant.llm.agent import generate_advice
from travel_assistant.core.config import Settings
import json


@pytest.mark.asyncio
@patch("travel_assistant.llm.agent.AsyncOpenAI")
@patch("travel_assistant.retrieval.get_all_cities")  # << Add this
async def test_generate_advice(mock_get_all_cities, mock_openai):
    # mock valid cities list to include "Test City"
    mock_get_all_cities.return_value = ["Test City", "Los Angeles", "Tokyo"]  # << Add

    mock_client = AsyncMock()
    mock_openai.return_value = mock_client

    settings = Settings(
        openai_api_key="sk_test_key",
        openai_project_id="test_project_id",
        openai_model="gpt-3.5-turbo",
    )

    # Mock the LLM response
    mock_client.chat.completions.create.return_value = AsyncMock(
        choices=[
            AsyncMock(
                message=AsyncMock(
                    tool_calls=[
                        AsyncMock(
                            function=AsyncMock(
                                name="return_advice",
                                arguments=json.dumps(
                                    {
                                        "destination": "Test City",
                                        "reason": "Test reason",
                                        "budget": "Moderate",
                                        "tips": ["Tip 1", "Tip 2"],
                                    }
                                ),
                            )
                        )
                    ]
                )
            )
        ]
    )

    # run the function
    advice = await generate_advice("test query", settings)

    # validate
    assert (
        advice.destination == "Test City"
    ), f"Expected 'Test City', got '{advice.destination}'"
