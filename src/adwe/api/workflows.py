from fastapi import APIRouter
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead
from adwe.workflows.engine import workflow_graph

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate):
    async with AsyncSessionLocal() as session:
        result = workflow_graph.invoke(
            {"repository_url": payload.repository_url}
        )

        workflow = Workflow(
            repository_url=payload.repository_url,
            status="completed",
            repository_analysis=result.get("repository_analysis"),
            implementation_plan=result.get("implementation_plan"),
        )

        session.add(workflow)
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
