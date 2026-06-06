from arq import create_pool
from fastapi import APIRouter

from adwe.workers.queue import get_redis_settings

router = APIRouter(prefix="/v1/queue", tags=["queue"])


@router.get("/health")
async def queue_health():
    redis = await create_pool(get_redis_settings())
    await redis.ping()

    return {"status": "ok", "redis": "ok"}
