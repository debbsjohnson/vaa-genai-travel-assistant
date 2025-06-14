from __future__ import annotations
from openai import AsyncOpenAI
from travel_assistant.core.config import get_settings, Settings
from travel_assistant.retrieval import search
from travel_assistant.models.schemas import TravelAdvice
from travel_assistant.llm.funct_specs import FUNCTION_SPECS
from travel_assistant.nlp.intent import parse, pick_city
from pydantic import ValidationError
import orjson, json
import logging

# Set up logging
logger = logging.getLogger(__name__)

SYSTEM = {
    "role": "system",
    "content": [
        {
            "type": "text",
            "text": (
                "You are Virgin Atlantic's AI Travel Assistant. "
                "Use the available tools to ground every recommendation in real catalogue data. "
                "If the user does not specify a city, choose the most relevant one yourself, "
                "then call return_advice()."
            ),
        }
    ],
}

MAX_ATTEMPTS = 3


def parse_free_response(content: str) -> TravelAdvice:
    """Fallback when LLM doesn't use tool calls"""
    return TravelAdvice(
        destination="Various destinations",
        reason="We apologize, but we couldn't find specific information for your request. Please try again with more details.",
        budget="Varies",
        tips=[
            "Consider refining your search criteria",
            "Try a different destination or time frame",
            "Contact our support for more personalized assistance",
        ],
    )


async def generate_advice(user_query: str, settings: Settings) -> TravelAdvice:
    for attempt in range(MAX_ATTEMPTS):
        try:
            client = AsyncOpenAI(
                api_key=settings.openai_api_key.get_secret_value(),
                project=settings.openai_project_id,
            )

            city, theme = parse(user_query)
            if city is None:
                city = pick_city(theme)

            # Use a simpler message structure
            system_message = (
                SYSTEM["content"][0]["text"] + f" (Destination context: {city})"
            )
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_query},
            ]

            iteration = 0
            max_iterations = 5
            while iteration < max_iterations:
                iteration += 1

                resp = await client.chat.completions.create(
                    model=settings.openai_model,
                    messages=messages,
                    tools=FUNCTION_SPECS,
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=600,
                )
                msg = resp.choices[0].message
                messages.append(msg)  # Add assistant response to context

                # Handle tool calls
                if msg.tool_calls:
                    for call in msg.tool_calls:
                        fn_name = call.function.name
                        fn_args = orjson.loads(call.function.arguments)
                        fn_args.setdefault("city", city)

                        if fn_name == "return_advice":
                            try:
                                return TravelAdvice.model_validate(fn_args)
                            except ValidationError as e:
                                logger.error(f"Validation failed: {e}")
                                # Add error to context and retry
                                messages.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": call.id,
                                        "content": f"Validation error: {str(e)}",
                                    }
                                )
                                continue

                        # Handle search functions
                        if fn_name == "search_hotels":
                            results = search.search_hotels(**fn_args)
                            if not results or "error" in results[0]:
                                return TravelAdvice(
                                    destination=city,
                                    reason=f"We couldn't find hotels matching your request for {city}",
                                    budget="Unknown",
                                    tips=[
                                        "Try adjusting your search criteria",
                                        "Contact support for assistance",
                                    ],
                                )
                        elif fn_name == "search_flights":
                            results = search.search_flights(**fn_args)
                        elif fn_name == "search_experiences":
                            results = search.search_experiences(**fn_args)
                        else:
                            logger.warning(f"Unexpected tool: {fn_name}")
                            return parse_free_response(msg.content or "")

                        # Append tool response
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": call.id,
                                "content": json.dumps(results, separators=(",", ":")),
                            }
                        )

                    continue  # Continue processing with new messages

                # Handle direct response (no tool calls)
                return parse_free_response(msg.content or "")

            # Max iterations reached
            return parse_free_response("")

        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < MAX_ATTEMPTS - 1:
                continue
            # Final fallback
            return TravelAdvice(
                destination="Multiple destinations available",
                reason="Please refine your query for more specific recommendations",
                budget="Varies",
                tips=["Try being more specific with your request"],
            )


# from __future__ import annotations
# from openai import AsyncOpenAI
# from travel_assistant.core.config import get_settings
# from travel_assistant.retrieval import search
# from travel_assistant.models.schemas import TravelAdvice
# from travel_assistant.llm.funct_specs import FUNCTION_SPECS
# from travel_assistant.nlp.intent import parse, pick_city
# import orjson, json
# from pydantic import ValidationError
# from travel_assistant.core.config import Settings


# settings = get_settings()

# # client = AsyncOpenAI(
# #     api_key=settings.openai_api_key.get_secret_value(),
# #     project=settings.openai_project_id,
# # )

# # TOOLS = {
# #     "search_hotels": lambda query, k=3: search.search_hotels(query, k),
# #     "search_flights": lambda query, k=3: search.search_flights(query, k),
# #     "search_experiences": lambda query, k=3: search.search_experiences(query, k),
# # }

# # TOOLS = {
# #     "search_hotels": lambda query, k=3, city=None, **_: search.search_hotels(
# #         query, k, city=city
# #     ),
# #     "search_flights": lambda query, k=3, city=None, **_: search.search_flights(
# #         query, k, city=city
# #     ),
# #     "search_experiences": lambda query, k=3, city=None, **_: search.search_experiences(
# #         query, k, city=city
# #     ),
# # }

# TOOLS = {
#     "search_hotels": lambda query, k=3, city=None, **_: search.search_hotels(
#         query, k, city=city
#     ),
#     "search_flights": lambda query, k=3, city=None, **_: search.search_flights(
#         query, k, city=city
#     ),
#     "search_experiences": lambda query, k=3, city=None, **_: search.search_experiences(
#         query, k, city=city
#     ),
# }


# SYSTEM = {
#     "role": "system",
#     "content": [
#         {
#             "type": "text",
#             "text": (
#                 "You are Virgin Atlantic's AI Travel Assistant. "
#                 "Use the available tools to ground every recommendation in real catalogue data. "
#                 "If the user does not specify a city, choose the most relevant one yourself, "
#                 "then call return_advice()."
#             ),
#         }
#     ],
# }

# MAX_ATTEMPTS = 3


# async def generate_advice(user_query: str, settings: Settings) -> TravelAdvice:
#     for attempt in range(MAX_ATTEMPTS):
#         try:
#             client = AsyncOpenAI(
#                 api_key=settings.openai_api_key.get_secret_value(),
#                 project=settings.openai_project_id,
#             )

#             city, theme = parse(user_query)
#             if city is None:
#                 city = pick_city(theme)

#             system_with_city = SYSTEM.copy()
#             system_with_city["content"][0]["text"] += f" (Destination context: {city})"
#             messages = [
#                 system_with_city,
#                 {"role": "user", "content": [{"type": "text", "text": user_query}]},
#             ]

#             # messages = [
#             #     SYSTEM,
#             #     {"role": "user", "content": [{"type": "text", "text": user_query}]},
#             # ]

#             while True:
#                 resp = await client.chat.completions.create(
#                     model=settings.openai_model,
#                     messages=messages,
#                     tools=FUNCTION_SPECS,
#                     tool_choice="auto",
#                     temperature=0.3,
#                     max_tokens=600,
#                 )
#                 msg = resp.choices[0].message

#                 if msg.tool_calls:
#                     messages.append(msg)  # always append the assistant message

#                     for call in msg.tool_calls:
#                         fn_name = call.function.name
#                         fn_args = orjson.loads(call.function.arguments)
#                         fn_args.setdefault("city", city)  # ensure `city` is present

#                         if fn_name == "return_advice":
#                             return TravelAdvice.model_validate(fn_args)

#                         # Explicit extraction for search functions
#                         if fn_name == "search_hotels":
#                             results = search.search_hotels(
#                                 query=fn_args["query"],
#                                 city=fn_args["city"],
#                                 k=fn_args.get("k", 3),
#                             )
#                         elif fn_name == "search_flights":
#                             results = search.search_flights(
#                                 query=fn_args["query"],
#                                 city=fn_args["city"],
#                                 k=fn_args.get("k", 3),
#                             )
#                         elif fn_name == "search_experiences":
#                             results = search.search_experiences(
#                                 query=fn_args["query"],
#                                 city=fn_args["city"],
#                                 k=fn_args.get("k", 3),
#                             )
#                         else:
#                             # raise RuntimeError(f"Unexpected tool: {fn_name}")
#                             return parse_free_response(msg.content)

#                         # Append the tool's response
#                         messages.append(
#                             {
#                                 "role": "tool",
#                                 "tool_call_id": call.id,
#                                 "content": json.dumps(results, separators=(",", ":")),
#                             }
#                         )

#                     continue  # go back and let the assistant refine based on tool output

#                 try:
#                     advice = TravelAdvice.model_validate(args)
#                     # Ensure tips is a list of strings
#                     if not isinstance(advice.tips, list) or not all(
#                         isinstance(tip, str) for tip in advice.tips
#                     ):
#                         advice.tips = [
#                             "Plan ahead",
#                             "Pack appropriately",
#                             "Check local customs",
#                         ]
#                     return advice
#                 except ValidationError as e:
#                     logger.error(f"Validation failed: {e}")
#                     # Fallback advice
#                     return TravelAdvice(
#                         destination="Multiple destinations available",
#                         reason="Please refine your query for more specific recommendations",
#                         budget="Varies",
#                         tips=["Try being more specific with your request"],
#                     )

#         except Exception as e:
#             if attempt < MAX_ATTEMPTS - 1:
#                 continue
#             raise

#     def parse_free_response(content: str) -> TravelAdvice:
#         """Parse LLM response when it doesn't use tool calls"""
#         # Simple parsing logic - in production you'd use more robust parsing
#         return TravelAdvice(
#             destination="Various destinations",
#             reason="Based on your preferences",
#             budget="Varies",
#             tips=[
#                 "Consider family-friendly resorts",
#                 "Look for kid-friendly activities",
#                 "Check for family discounts",
#             ],
#         )

#         # if msg.tool_calls:
#         #     for call in msg.tool_calls:
#         #         fn_name = call.function.name
#         #         fn_args = orjson.loads(call.function.arguments)
#         #         fn_args.setdefault("city", city)

#         #         if fn_name == "return_advice":
#         #             return TravelAdvice.model_validate(fn_args)

#         #         result = TOOLS[fn_name](**fn_args)

#         #     messages.append(msg)

#         #     # for each call, append its own tool-response
#         #     for call in msg.tool_calls:
#         #         fn_name = call.function.name
#         #         result = TOOLS[fn_name](**orjson.loads(call.function.arguments))
#         #         messages.append(
#         #             {
#         #                 "role": "tool",
#         #                 "tool_call_id": call.id,
#         #                 "content": json.dumps(result, separators=(",", ":")),
#         #             }
#         #         )
#         #     continue

#         # messages.append(msg)


# # from __future__ import annotations

# # from openai import OpenAI
# # from openai import AsyncOpenAI
# # from travel_assistant.core.config import get_settings
# # from travel_assistant.retrieval import search
# # from travel_assistant.models.schemas import TravelAdvice
# # from travel_assistant.llm.funct_specs import FUNCTION_SPECS
# # import orjson
# # import json


# # settings = get_settings()
# # # client = OpenAI()

# # client = AsyncOpenAI(
# #     api_key=settings.openai_api_key.get_secret_value(),
# #     project=settings.openai_project_id,  # ⭐ new line
# # )


# # TOOLS = {
# #     "search_hotels": lambda query, k=3: search.search_hotels(query, k),
# #     "search_flights": lambda query, k=3: search.search_flights(query, k),
# #     "search_experiences": lambda query, k=3: search.search_experiences(query, k),
# # }

# # SYSTEM = {
# #     "role": "system",
# #     "content": [
# #         {
# #             "type": "text",
# #             "text": (
# #                 "You are Virgin Atlantic's AI Travel Assistant."
# #                 "Use available tools to ground every recommendation in real catalogue data."
# #                 "If the user does not specify a destination, select the best-fit city yourself based on the catalogues before calling return_advice()."
# #                 "When ready, call return_advice()"
# #             ),
# #         }
# #     ],
# # }


# # async def generate_advice(user_query: str) -> TravelAdvice:
# #     messages = [
# #         SYSTEM,
# #         {"role": "user", "content": [{"type": "text", "text": user_query}]},
# #     ]

# #     while True:
# #         resp = await client.chat.completions.create(
# #             model=settings.openai_model,
# #             messages=messages,
# #             tools=FUNCTION_SPECS,
# #             tool_choice="auto",
# #             temperature=0.3,
# #             max_tokens=600,
# #         )
# #         msg = resp.choices[0].message

# #         if msg.tool_calls:
# #             call = msg.tool_calls[0]

# #             fn_name = call.function.name
# #             fn_args = orjson.loads(call.function.arguments)

# #             if fn_name == "return_advice":
# #                 return TravelAdvice.model_validate(fn_args)

# #             result = TOOLS[fn_name](**fn_args)

# #             # if call.function.name == "return_advice":
# #             #     return TravelAdvice.model_validate_json(call.function.arguments)

# #             # handles retrieval tool
# #             # result = TOOLS[call.name](**(call.arguments or {}))
# #             messages.append(msg)
# #             messages.append(
# #                 {
# #                     "role": "tool",
# #                     # "name": call.name,
# #                     # "name": fn_name,
# #                     "tool_call_id": call.id,
# #                     # "content": str(result)}
# #                     # "content": [{"type": "text", "text": json.dumps(result)}],
# #                     # "content": [
# #                     #     {"type": "text", "text": orjson.dumps(result).decode()}
# #                     # ],
# #                     "content": json.dumps(result, separators=(",", ":")),
# #                 }
# #             )
# #             continue

# #         # return TravelAdvice.model_validate_json(msg.content)
# #         try:
# #             return TravelAdvice.model_validate_json(msg.content)
# #         except ValueError:
# #             # model didn’t give JSON, treat as assistant reply; break to avoid infinite loop
# #             messages.append(msg)
# #             continue
