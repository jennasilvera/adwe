import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.patch import Patch
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead
from adwe.models.workflow_status import WorkflowStatus
from adwe.services.audit import record_audit_event
from adwe.workflows.engine import workflow_graph

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])
logger = logging.getLogger(__name__)


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
        result = await session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalar_one_or_none()

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        return workflow


@router.post("/{workflow_id}/run", response_model=WorkflowRead)
async def run_workflow(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalar_one_or_none()

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        workflow.status = WorkflowStatus.RUNNING

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="workflow.started",
            payload={"repository_url": workflow.repository_url},
        )

        try:
            logger.info("workflow_started workflow_id=%s", workflow.id)

            graph_result = workflow_graph.invoke(
                {"repository_url": workflow.repository_url}
            )

            workflow.status = WorkflowStatus.COMPLETED
            workflow.repository_analysis = graph_result.get("repository_analysis")
            workflow.implementation_plan = graph_result.get("implementation_plan")
            workflow.code_modification = graph_result.get("code_modification")

            code_modification = graph_result.get("code_modification") or {}
            if code_modification.get("diff"):
                session.add(
                    Patch(
                        workflow_id=workflow.id,
                        file_path="README.md",
                        diff=code_modification["diff"],
                        status=code_modification.get("status", "proposed"),
                    )
                )

            await record_audit_event(
                session=session,
                workflow_id=workflow.id,
                event_type="workflow.completed",
                payload=graph_result,
            )

            logger.info("workflow_completed workflow_id=%s", workflow.id)

        except Exception as exc:
            workflow.status = WorkflowStatus.FAILED

            await record_audit_event(
                session=session,
                workflow_id=workflow.id,
                event_type="workflow.failed",
                payload={"error": str(exc)},
            )

            logger.exception("workflow_failed workflow_id=%s", workflow.id)

        await session.commit()
        await session.refresh(workflow)

        return workflow
