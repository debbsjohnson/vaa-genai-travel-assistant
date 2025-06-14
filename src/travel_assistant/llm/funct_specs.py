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

# Export individual function specs
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

# Maintain the existing FUNCTION_SPECS list
FUNCTION_SPECS = [
    hotel_fn_spec,
    flight_fn_spec,
    experience_fn_spec,
    return_advice_fn_spec,
]


# from travel_assistant.models.schemas import TravelAdvice


# def fn(body: dict) -> dict:
#     """helper to wrap the spec in the new envelope"""
#     return {"type": "function", "function": body}


# SEARCH_PARAMS = {
#     "type": "object",
#     "properties": {
#         "query": {"type": "string"},
#         "city": {"type": "string"},
#         "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#     },
#     "required": ["query", "city"],
# }

# FUNCTION_SPECS = [
#     fn(
#         {
#             "name": "search_hotels",
#             "description": "Find up to k hotels that match a free-text query.",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "search_flights",
#             "description": "Find up to k flights that match a free-text query.",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "search_experiences",
#             "description": "Find up to k experiences that match a free-text query.",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "return_advice",
#             "description": "Return the final travel advice in TravelAdvice schema.",
#             "parameters": TravelAdvice.model_json_schema(),
#         }
#     ),
# ]


# from travel_assistant.models.schemas import TravelAdvice


# def fn(body: dict) -> dict:
#     return {"type": "function", "function": body}


# SEARCH_PARAMS = {
#     "type": "object",
#     "properties": {
#         "query": {"type": "string"},
#         "city": {"type": "string"},
#         "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#     },
#     "required": ["query", "city"],  # ← city now mandatory
# }

# FUNCTION_SPECS = [
#     fn(
#         {
#             "name": "search_hotels",
#             "description": "Find hotels …",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "search_flights",
#             "description": "Find flights …",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "search_experiences",
#             "description": "Find experiences …",
#             "parameters": SEARCH_PARAMS,
#         }
#     ),
#     fn(
#         {
#             "name": "return_advice",
#             "description": "Return final advice",
#             "parameters": TravelAdvice.model_json_schema(),
#         }
#     ),
# ]


# from travel_assistant.models.schemas import TravelAdvice


# def fn(body: dict) -> dict:
#     """helper to wrap the spec in the new envelope"""
#     return {"type": "function", "function": body}


# FUNCTION_SPECS = [
#     fn(
#         {
#             "name": "search_hotels",
#             "description": "Find up to k hotels that match a free-text query.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {"type": "string"},
#                     "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#                 },
#                 "required": ["query"],
#             },
#         }
#     ),
#     fn(
#         {
#             "name": "search_flights",
#             "description": "Find up to k flights that match a free-text query.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {"type": "string"},
#                     "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#                 },
#                 "required": ["query"],
#             },
#         }
#     ),
#     fn(
#         {
#             "name": "search_experiences",
#             "description": "Find up to k experiences that match a free-text query.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {"type": "string"},
#                     "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#                 },
#                 "required": ["query"],
#             },
#         }
#     ),
#     fn(
#         {
#             "name": "return_advice",
#             "description": "Return the final travel advice in TravelAdvice schema.",
#             "parameters": TravelAdvice.model_json_schema(),
#         }
#     ),
# ]


# from travel_assistant.models.schemas import TravelAdvice

# FUNCTION_SPECS = [
#     {
#         "name": "search_hotels",
#         "description": "Find up to k hotels that match a free-text query.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {"type": "string"},
#                 "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#             },
#             "required": ["query"],
#         },
#     },
#     {
#         "name": "search_flights",
#         "description": "Find up to k flights that match a free-text query.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {"type": "string"},
#                 "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#             },
#             "required": ["query"],
#         },
#     },
#     {
#         "name": "search_experiences",
#         "description": "Find up to k experiences that match a free-text query.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {"type": "string"},
#                 "k": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
#             },
#             "required": ["query"],
#         },
#     },
#     {
#         "name": "return_advice",
#         "description": "Return the final travel advice exactly matching the TravelAdvice schema.",
#         "parameters": TravelAdvice.model_json_schema(),
#     },
# ]
