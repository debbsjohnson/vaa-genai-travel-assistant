from openai import OpenAI, APIError
from travel_assistant.core.config import Settings
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def moderate_content(text: str, settings: Settings) -> bool:
    try:
        client = OpenAI(
            api_key=settings.openai_api_key.get_secret_value(),
            timeout=10.0,  # 10 second timeout
        )
        response = client.moderations.create(input=text)
        return response.results[0].flagged
    except APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return False  # fail open
    except Exception as e:
        logger.error(f"Moderation error: {str(e)}")
        return False  # fail open
