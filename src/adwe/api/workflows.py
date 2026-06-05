from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead
from adwe.workflows.engine import workflow_graph
from adwe.services.audit import record_audit_event

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate):
    async with AsyncSessionLocal() as session:
        await record_audit_event(
            session=session,
            event_type="workflow.started",
            payload={"repository_url": payload.repository_url},
        )

        result = workflow_graph.invoke(
            {"repository_url": payload.repository_url}
        )

        workflow = Workflow(
            repository_url=payload.repository_url,
            status="completed",
            repository_analysis=result.get("repository_analysis"),
            implementation_plan=result.get("implementation_plan"),
            code_modification=result.get("code_modification"),
        )

        session.add(workflow)
        await session.flush()

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="repository.analyzed",
            payload=result.get("repository_analysis"),
        )

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="plan.generated",
            payload=result.get("implementation_plan"),
        )

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="code_modification.proposed",
            payload=result.get("code_modification"),
        )

        await record_audit_event(
            session=session,
            workflow_id=workflow.id,
            event_type="workflow.completed",
            payload=result,
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
