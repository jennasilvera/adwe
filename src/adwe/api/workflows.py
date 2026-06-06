import logging

from arq import create_pool
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead
from adwe.models.workflow_status import WorkflowStatus
from adwe.services.audit import record_audit_event
from adwe.workers.queue import get_redis_settings

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])
logger = logging.getLogger(__name__)


async def enqueue_workflow_run(workflow_id: str) -> str:
    redis = await create_pool(get_redis_settings())

    job = await redis.enqueue_job(
        "run_workflow",
        workflow_id,
    )

    return job.job_id


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate):
    async with AsyncSessionLocal() as session:
        workflow = Workflow(
            repository_url=payload.repository_url,
            status=WorkflowStatus.PENDING,
        )

        session.add(workflow)
        await session.flush()

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="workflow.created",
            payload={"repository_url": payload.repository_url},
        )

        job_id = await enqueue_workflow_run(workflow.id)
        workflow.queue_job_id = job_id

        await session.commit()
        await session.refresh(workflow)

        return workflow


@router.get("", response_model=list[WorkflowRead])
async def list_workflows():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Workflow).order_by(Workflow.created_at.desc())
        )
        return result.scalars().all()


@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(workflow_id: str):
    async with AsyncSessionLocal() as session:
        workflow = await session.get(Workflow, workflow_id)

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        return workflow


@router.post("/{workflow_id}/run", response_model=WorkflowRead)
async def run_workflow_endpoint(workflow_id: str):
    async with AsyncSessionLocal() as session:
        workflow = await session.get(Workflow, workflow_id)

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        workflow.status = WorkflowStatus.PENDING
        job_id = await enqueue_workflow_run(workflow_id)
        workflow.queue_job_id = job_id

        await session.commit()
        await session.refresh(workflow)

        return workflow
