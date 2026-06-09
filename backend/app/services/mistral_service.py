import requests
from app.config import settings


def generate_website(
    document_text: str,
    prompt: str,
    template: str
):

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Create a complete HTML website.

Template:
{template}

Instructions:
{prompt}

Document:
{document_text}

Return ONLY HTML.
"""
                }
            ]
        },
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]