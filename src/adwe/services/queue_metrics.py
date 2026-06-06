from arq import create_pool

from adwe.workers.queue import get_redis_settings


async def get_queue_metrics() -> dict:
    redis = await create_pool(get_redis_settings())
    queued_jobs = await redis.queued_jobs()

    return {
        "queued_jobs": len(queued_jobs),
    }
