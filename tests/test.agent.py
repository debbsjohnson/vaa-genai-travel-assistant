from unittest.mock import AsyncMock, patch
from travel_assistant.llm.agent import generate_advice

@patch("travel_assistant.llm.agent.AsyncOpenAI")
async def test_generate_advice(mock_openai):
    # Setup mock responses
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    
    # Mock OpenAI response
    mock_client.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(
            tool_calls=[AsyncMock(
                function=AsyncMock(
                    name="return_advice",
                    arguments=json.dumps({
                        "destination": "Test City",
                        "reason": "Test reason",
                        "budget": "Moderate",
                        "tips": ["Tip 1", "Tip 2"]
                    })
                )
            )]
        )]
    )
    
    # Call the function
    advice = await generate_advice("test query", settings)
    
    # Validate
    assert advice.destination == "Test City"
    assert len(advice.tips) == 2