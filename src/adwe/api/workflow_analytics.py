from datetime import datetime, timedelta

from fastapi import APIRouter
from sqlalchemy import func, select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.workflow import Workflow
from adwe.models.workflow_analytics_schema import (
    TopPatchTarget,
    WorkflowAnalyticsResponse,
)

router = APIRouter(prefix="/v1/workflow-analytics", tags=["workflow-analytics"])


def _patch_type(file_path: str) -> str:
    if file_path.startswith(".github/workflows/"):
        return "ci"
    if "migration" in file_path:
        return "migration"
    if "docker" in file_path or "healthcheck" in file_path:
        return "docker"
    if file_path.startswith("docs/"):
        return "documentation"
    return "general"


@router.get("", response_model=WorkflowAnalyticsResponse)
async def workflow_analytics():
    since = datetime.utcnow() - timedelta(hours=24)

    async with AsyncSessionLocal() as session:
        repositories_analyzed = await session.scalar(
            select(func.count(Workflow.id)).where(
                Workflow.repository_analysis.is_not(None),
            )
        )

        unique_repositories = await session.scalar(
            select(func.count(func.distinct(Workflow.repository_url)))
        )

        completed_last_24h = await session.scalar(
            select(func.count(Workflow.id)).where(
                Workflow.status == "completed",
                Workflow.completed_at >= since,
            )
        )

        failed_last_24h = await session.scalar(
            select(func.count(Workflow.id)).where(
                Workflow.status == "failed",
                Workflow.completed_at >= since,
            )
        )

        top_rows = await session.execute(
            select(
                Patch.file_path,
                func.count(Patch.id),
            )
            .group_by(Patch.file_path)
            .order_by(func.count(Patch.id).desc())
            .limit(5)
        )

        top_patch_targets = [
            TopPatchTarget(file=file_path, count=count)
            for file_path, count in top_rows
        ]

        average_priority = await session.scalar(
            select(func.avg(Patch.priority_score)).where(
                Patch.priority_score.is_not(None)
            )
        )

        patch_types = [_patch_type(item.file) for item in top_patch_targets]
        most_common_patch_type = (
            max(set(patch_types), key=patch_types.count)
            if patch_types
            else None
        )

        return WorkflowAnalyticsResponse(
            repositories_analyzed=repositories_analyzed or 0,
            unique_repositories=unique_repositories or 0,
            workflows_completed_last_24h=completed_last_24h or 0,
            workflows_failed_last_24h=failed_last_24h or 0,
            top_patch_targets=top_patch_targets,
            most_common_patch_type=most_common_patch_type,
            average_patch_priority=(
                float(average_priority) if average_priority is not None else None
            ),
        )
