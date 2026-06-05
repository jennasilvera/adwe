from fastapi import APIRouter
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_schema import WorkflowCreate, WorkflowRead

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate):
    async with AsyncSessionLocal() as session:
        workflow = Workflow(repository_url=payload.repository_url)
        session.add(workflow)
        await session.commit()
        await session.refresh(workflow)
        return workflow


@router.get("", response_model=list[WorkflowRead])
async def list_workflows():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Workflow).order_by(Workflow.created_at.desc()))
        return result.scalars().all()
