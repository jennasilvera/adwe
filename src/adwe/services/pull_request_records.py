from sqlalchemy.ext.asyncio import AsyncSession

from adwe.models.pull_request import PullRequest


async def record_pull_request(
    session: AsyncSession,
    repository_url: str,
    branch_name: str,
    title: str,
    status: str,
    url: str | None = None,
    workflow_id: str | None = None,
) -> PullRequest:
    record = PullRequest(
        workflow_id=workflow_id,
        repository_url=repository_url,
        branch_name=branch_name,
        title=title,
        url=url,
        status=status,
    )

    session.add(record)
    return record
