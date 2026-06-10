import httpx

from adwe.core.config import settings


class LLMError(Exception):
    pass


def llm_available() -> bool:
    return bool(settings.llm_enabled and settings.llm_api_key)


def generate_text(prompt: str) -> str:
    if not llm_available():
        raise LLMError("LLM is not enabled")

    response = httpx.post(
        f"{settings.llm_base_url.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.llm_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=60,
    )

    if response.status_code >= 400:
        raise LLMError(response.text)

    data = response.json()
    return data["choices"][0]["message"]["content"]
