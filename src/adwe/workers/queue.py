from arq.connections import RedisSettings

from adwe.core.config import settings


def get_redis_settings() -> RedisSettings:
    return RedisSettings.from_dsn(settings.redis_url)
