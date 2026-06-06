from fastapi import APIRouter
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.pull_request import PullRequest
from adwe.models.pull_request_record_schema import PullRequestRecordRead

router = APIRouter(prefix="/v1/pull-request-records", tags=["pull-request-records"])


@router.get("", response_model=list[PullRequestRecordRead])
async def list_pull_request_records():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PullRequest).order_by(PullRequest.created_at.desc())
        )
        return result.scalars().all()


@router.get("/workflows/{workflow_id}", response_model=list[PullRequestRecordRead])
async def list_workflow_pull_request_records(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PullRequest)
            .where(PullRequest.workflow_id == workflow_id)
            .order_by(PullRequest.created_at.desc())
        )
        return result.scalars().all()
