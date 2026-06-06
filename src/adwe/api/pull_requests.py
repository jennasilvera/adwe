from fastapi import APIRouter

from adwe.models.pull_request_schema import PullRequestCreate, PullRequestRead
from adwe.services.github_pr import create_pull_request

router = APIRouter(prefix="/v1/pull-requests", tags=["pull-requests"])


@router.post("", response_model=PullRequestRead)
async def open_pull_request(payload: PullRequestCreate):
    return create_pull_request(
        repository_url=payload.repository_url,
        branch_name=payload.branch_name,
        title=payload.title,
        body=payload.body,
    )
