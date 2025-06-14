from fastapi import APIRouter, Depends, Request
from travel_assistant.models.schemas import TravelQuery, TravelAdvice
from travel_assistant.api.deps import settings_dep
from travel_assistant.core.config import Settings
from travel_assistant.llm.agent import generate_advice
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/travel-assistant", response_model=TravelAdvice)
@limiter.limit("10/minute")
async def travel_assistant_endpoint(
    request: Request,  # Required by slowapi
    query_in: TravelQuery,
    settings: Settings = Depends(settings_dep),
):
    advice: TravelAdvice = await generate_advice(query_in.query, settings)
    return advice


# from fastapi import APIRouter, Depends
# from travel_assistant.api.deps import (
#     settings_dep,
#     hotels_store_dep,
#     flights_store_dep,
#     experiences_store_dep,
# )

# from travel_assistant.core.config import Settings
# from travel_assistant.api.deps import settings_dep
# from travel_assistant.services.advisor import advisor
# from travel_assistant.models.schemas import TravelQuery, TravelAdvice

# router = APIRouter()


# @router.post("/travel-assistant", response_model=TravelAdvice)
# async def travel_assistant(
#     query: TravelQuery,
#     settings: Settings = Depends(settings_dep),
#     hotels: VectorStore = Depends(hotels_store_dep),
#     flights: VectorStore = Depends(flights_store_dep),
#     experiences: VectorStore = Depends(experiences_store_dep),
# ):
#     return await advisor(query.query, settings, hotels, flights, experiences)

# src/travel_assistant/api/routes.py
# from fastapi import APIRouter, Depends
# from travel_assistant.models.schemas import TravelQuery, TravelAdvice
# from travel_assistant.api.deps import settings_dep
# from travel_assistant.core.config import Settings

# # from travel_assistant.services.advisor import get_travel_advice
# from travel_assistant.llm.agent import generate_advice
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded


# router = APIRouter()


# limiter = Limiter(key_func=get_remote_address)


# @router.post("/travel-assistant", response_model=TravelAdvice)
# @limiter.limit("5/minute")
# async def travel_assistant_endpoint(
#     query_in: TravelQuery,
#     settings: Settings = Depends(settings_dep),
# ):
#     # 1) Pass the raw query string to your service function
#     advice: TravelAdvice = await generate_advice(query_in.query, settings)
#     return advice
