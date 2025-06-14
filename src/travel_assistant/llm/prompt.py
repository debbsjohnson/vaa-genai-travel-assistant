def generate_prompt(user_query: str) -> str:
    return f"""
You are a travel assistant.

A user has asked: "{user_query}"

Respond with:
- A recommended destination
- A reason for the recommendation
- A rough budget category
- 3 tips or suggestions
"""
