# Data flow for /travel-assistant:
# 1. User POST → routes.py:travel_assistant_endpoint
# 2. settings_dep loads config
# 3. generate_advice(query, settings) is called
#    • parse intent (intent.py)
#    • embed & vector_search → hotels, flights, experiences (retrieval/)
#    • build prompt + function specs (prompt.py, func_specs.py)
#    • call OpenAI (agent.py)
#    • unpack function_call.arguments → TravelAdvice (schemas.py)
#    • return TravelAdvice

import json
from openai import OpenAI
from travel_assistant.retrieval.search import (
    search_hotels,
    search_flights,
    search_experiences,
)

# from travel_assistant.llm.funct_specs import (
#     hotel_fn_spec,
#     flight_fn_spec,
#     experience_fn_spec,
#     return_advice_fn_spec,
# )
from travel_assistant.llm.funct_specs import FUNCTION_SPECS
from travel_assistant.models.schemas import TravelAdvice


async def get_travel_advice(query: str, settings) -> TravelAdvice:
    # 1) Use your search functions to ground the query in real data
    hotels = search_hotels(query)  # returns a list of dicts from hotel_catalogue.json
    flights = search_flights(query)
    experiences = search_experiences(query)

    # 2) Call OpenAI with function-calling
    client = OpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[...],
        tools=FUNCTION_SPECS,  # Use the tools parameter
        tool_choice="auto",  # Instead of function_call
    )
    # response = await client.chat.completions.create(
    #     model="gpt-4-0613",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a travel assistant. Use only the provided functions.",
    #         },
    #         {"role": "user", "content": query},
    #     ],
    #     functions=[
    #         hotel_fn_spec,
    #         flight_fn_spec,
    #         experience_fn_spec,
    #         return_advice_fn_spec,
    #     ],
    #     function_call="auto",
    #     # pass grounding data as “tool inputs” via function results if needed:
    #     tools_results={
    #         "search_hotels": hotels,
    #         "search_flights": flights,
    #         "search_experiences": experiences,
    #     },
    # )

    # 3) Extract the function_call arguments
    message = response.choices[0].message
    if message.function_call and message.function_call.name == "return_advice":
        args = json.loads(message.function_call.arguments)
        # 4) Map into your Pydantic model
        advice = TravelAdvice(**args)
        return advice

    # fallback if model didn’t call the right function
    raise RuntimeError("Unexpected OpenAI response format")
