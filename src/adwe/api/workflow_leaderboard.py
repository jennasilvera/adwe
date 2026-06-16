from fastapi import APIRouter
from sqlalchemy import func, select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus
from adwe.models.workflow import Workflow
from adwe.models.workflow_leaderboard_schema import (
    WorkflowLeaderboardEntry,
    WorkflowLeaderboardResponse,
)

router = APIRouter(prefix="/v1/workflow-leaderboard", tags=["workflow-leaderboard"])


@router.get("", response_model=WorkflowLeaderboardResponse)
async def workflow_leaderboard():
    async with AsyncSessionLocal() as session:
        rows = await session.execute(
            select(
                Workflow.id,
                Workflow.repository_url,
                func.count(Patch.id),
            )
            .outerjoin(Patch, Patch.workflow_id == Workflow.id)
            .group_by(
                Workflow.id,
                Workflow.repository_url,
            )
            .order_by(func.count(Patch.id).desc())
            .limit(20)
        )

        entries = []

        for workflow_id, repository_url, patch_count in rows:
            proposed_count = await session.scalar(
                select(func.count(Patch.id)).where(
                    Patch.workflow_id == workflow_id,
                    Patch.status == PatchStatus.PROPOSED,
                )
            )

            applied_count = await session.scalar(
                select(func.count(Patch.id)).where(
                    Patch.workflow_id == workflow_id,
                    Patch.status == PatchStatus.APPLIED,
                )
            )

            entries.append(
                WorkflowLeaderboardEntry(
                    workflow_id=workflow_id,
                    repository_url=repository_url,
                    patch_count=patch_count,
                    approved_patch_count=proposed_count or 0,
                    applied_patch_count=applied_count or 0,
                )
            )

        return WorkflowLeaderboardResponse(entries=entries)
