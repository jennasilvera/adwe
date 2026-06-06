from fastapi import APIRouter

from adwe.services.workflow_metrics import get_workflow_metrics

router = APIRouter(prefix="/v1/workflow-metrics", tags=["workflow-metrics"])


@router.get("")
async def workflow_metrics():
    return await get_workflow_metrics()
