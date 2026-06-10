from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://adwe:adwe@localhost:5432/adwe"
    redis_url: str = "redis://localhost:6379/0"
    github_token: str | None = None

    llm_api_key: str | None = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_enabled: bool = False


settings = Settings()
