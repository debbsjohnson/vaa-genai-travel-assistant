from fastapi import APIRouter, Depends, Request, HTTPException
from travel_assistant.models.schemas import TravelQuery, TravelAdvice
from travel_assistant.api.deps import settings_dep
from travel_assistant.core.config import Settings
from travel_assistant.llm.agent import generate_advice
from travel_assistant.core.guardrails import moderate_content
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/travel-assistant", response_model=TravelAdvice)
@limiter.limit("10/minute")
async def travel_assistant_endpoint(
    request: Request,
    query_in: TravelQuery,
    settings: Settings = Depends(settings_dep),
):
    """
    generate travel advice based on a natural language query.

    args:
        request: fastAPI request object
        query_in: pydantic model with user query
        settings: application settings with OpenAI credentials

    returns:
        TravelAdvice: structured travel recommendation

    raises:
        HTTPException: if content is inappropriate or processing fails
    """
    try:
        if moderate_content(query_in.query, settings):
            logger.warning(f"Inappropriate content detected: {query_in.query}")
            raise HTTPException(
                status_code=400,
                detail="Your query contains inappropriate content. Please modify your request.",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content moderation failed: {e}")
        raise HTTPException(status_code=500, detail="Content moderation error")

    try:
        advice: TravelAdvice = await generate_advice(query_in.query, settings)
        logger.info(f"Generated advice for query: {query_in.query}")
        return advice
    except Exception as e:
        logger.exception(f"Error processing query: {query_in.query}")
        raise HTTPException(
            status_code=500,
            detail="We encountered an error processing your request. Please try again later.",
        )
