
import json
from openai import OpenAI
from travel_assistant.retrieval.search import (
    search_hotels,
    search_flights,
    search_experiences,
)


from travel_assistant.llm.funct_specs import FUNCTION_SPECS
from travel_assistant.models.schemas import TravelAdvice


async def get_travel_advice(query: str, settings) -> TravelAdvice:
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a travel assistant..."},
            {"role": "user", "content": query},
        ],
        tools=FUNCTION_SPECS,
        tool_choice="auto",
    )

    # process tool calls
    message = response.choices[0].message
    if message.tool_calls:
        for call in message.tool_calls:
            if call.function.name == "return_advice":
                args = json.loads(call.function.arguments)
                return TravelAdvice(**args)

    # fallback
    return TravelAdvice(
        destination="Various destinations",
        reason="We couldn't find recommendations",
        budget="Varies",
        tips=["Please try a different query"],
    )
