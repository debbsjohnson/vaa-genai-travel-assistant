from travel_assistant.models.schemas import TravelAdvice


def create_tool_spec(name: str, description: str, parameters: dict) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }


SEARCH_PARAMS = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "Search keywords"},
        "city": {"type": "string", "description": "Target city for search"},
        "k": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5,
            "default": 3,
            "description": "Number of results to return",
        },
    },
    "required": ["query"],
}

# export individual function specs
hotel_fn_spec = create_tool_spec(
    "search_hotels", "Search hotels in our catalogue", SEARCH_PARAMS
)

flight_fn_spec = create_tool_spec(
    "search_flights", "Search available flights", SEARCH_PARAMS
)

experience_fn_spec = create_tool_spec(
    "search_experiences", "Search travel experiences and activities", SEARCH_PARAMS
)

return_advice_fn_spec = create_tool_spec(
    "return_advice",
    "Return final structured travel advice",
    TravelAdvice.model_json_schema(),
)

# maintain the existing FUNCTION_SPECS list
FUNCTION_SPECS = [
    hotel_fn_spec,
    flight_fn_spec,
    experience_fn_spec,
    return_advice_fn_spec,
]

