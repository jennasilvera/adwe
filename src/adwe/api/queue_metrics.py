from fastapi import APIRouter

from adwe.services.queue_metrics import get_queue_metrics

router = APIRouter(prefix="/v1/queue-metrics", tags=["queue-metrics"])


@router.get("")
async def queue_metrics():
    return await get_queue_metrics()
