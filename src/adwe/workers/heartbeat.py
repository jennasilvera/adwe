from datetime import datetime, timezone

from arq import create_pool

from adwe.workers.queue import get_redis_settings

HEARTBEAT_KEY = "adwe:worker:last_heartbeat"


async def record_heartbeat() -> None:
    redis = await create_pool(get_redis_settings())
    await redis.set(
        HEARTBEAT_KEY,
        datetime.now(timezone.utc).isoformat(),
    )


async def get_heartbeat() -> dict:
    redis = await create_pool(get_redis_settings())
    value = await redis.get(HEARTBEAT_KEY)

    return {
        "last_heartbeat": value.decode() if value else None,
    }
