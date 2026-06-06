from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://adwe:adwe@localhost:5432/adwe"
    redis_url: str = "redis://localhost:6379/0"
    github_token: str | None = None


settings = Settings()
