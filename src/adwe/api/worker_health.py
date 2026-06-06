from fastapi import APIRouter

from adwe.workers.heartbeat import get_heartbeat

router = APIRouter(prefix="/v1/workers", tags=["workers"])


@router.get("/health")
async def worker_health():
    return await get_heartbeat()
