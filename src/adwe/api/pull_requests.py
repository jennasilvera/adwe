from fastapi import APIRouter

from adwe.db.session import AsyncSessionLocal
from adwe.models.pull_request_schema import PullRequestCreate, PullRequestRead
from adwe.services.github_pr import create_pull_request
from adwe.services.pull_request_records import record_pull_request

router = APIRouter(prefix="/v1/pull-requests", tags=["pull-requests"])


@router.post("", response_model=PullRequestRead)
async def open_pull_request(payload: PullRequestCreate):
    result = create_pull_request(
        repository_url=payload.repository_url,
        branch_name=payload.branch_name,
        title=payload.title,
        body=payload.body,
    )

    async with AsyncSessionLocal() as session:
        await record_pull_request(
            session=session,
            repository_url=result["repository_url"],
            branch_name=result["branch_name"],
            title=result["title"],
            url=result.get("url"),
            status=result["status"],
        )

        await session.commit()

    return result
