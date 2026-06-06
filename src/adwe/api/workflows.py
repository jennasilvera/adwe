import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead
from adwe.models.workflow_status import WorkflowStatus
from adwe.services.audit import record_audit_event
from adwe.workers.workflow_runner import run_workflow as run_workflow_task

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])
logger = logging.getLogger(__name__)


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate, background_tasks: BackgroundTasks):
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

        await session.commit()
        await session.refresh(workflow)

        background_tasks.add_task(run_workflow_task, workflow.id)

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
        result = await session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalar_one_or_none()

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        return workflow


@router.post("/{workflow_id}/run", response_model=WorkflowRead)
async def run_workflow_endpoint(workflow_id: str, background_tasks: BackgroundTasks):
    async with AsyncSessionLocal() as session:
        workflow = await session.get(Workflow, workflow_id)

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        workflow.status = WorkflowStatus.PENDING
        await session.commit()
        await session.refresh(workflow)

        background_tasks.add_task(run_workflow_task, workflow.id)

        return workflow
