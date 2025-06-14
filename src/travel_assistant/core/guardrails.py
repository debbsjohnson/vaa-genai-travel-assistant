from openai import OpenAI


def moderate_content(text: str, settings: Settings) -> bool:
    client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    response = client.moderations.create(input=text)
    return response.results[0].flagged
