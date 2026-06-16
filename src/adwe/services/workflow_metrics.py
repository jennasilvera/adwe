from sqlalchemy import func, select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus
from adwe.models.workflow import Workflow


async def get_workflow_metrics() -> dict:
    async with AsyncSessionLocal() as session:
        total = await session.scalar(select(func.count(Workflow.id)))

        completed = await session.scalar(
            select(func.count(Workflow.id)).where(Workflow.status == "completed")
        )

        failed = await session.scalar(
            select(func.count(Workflow.id)).where(Workflow.status == "failed")
        )

        running = await session.scalar(
            select(func.count(Workflow.id)).where(Workflow.status == "running")
        )

        total_patches = await session.scalar(select(func.count(Patch.id)))

        proposed_patches = await session.scalar(
            select(func.count(Patch.id)).where(Patch.status == PatchStatus.PROPOSED)
        )

        applied_patches = await session.scalar(
            select(func.count(Patch.id)).where(Patch.status == PatchStatus.APPLIED)
        )

        failed_patches = await session.scalar(
            select(func.count(Patch.id)).where(Patch.status == PatchStatus.FAILED)
        )

        avg_duration = await session.scalar(
            select(
                func.avg(
                    func.extract("epoch", Workflow.completed_at - Workflow.started_at)
                )
            ).where(
                Workflow.started_at.is_not(None),
                Workflow.completed_at.is_not(None),
            )
        )

        total_count = total or 0
        completed_count = completed or 0
        failed_count = failed or 0
        patch_count = total_patches or 0
        applied_patch_count = applied_patches or 0

        return {
            "workflow": {
                "total": total_count,
                "completed": completed_count,
                "failed": failed_count,
                "running": running or 0,
                "success_rate": completed_count / total_count if total_count else 0,
                "failure_rate": failed_count / total_count if total_count else 0,
                "average_duration_seconds": float(avg_duration) if avg_duration else None,
            },
            "patches": {
                "total": patch_count,
                "proposed": proposed_patches or 0,
                "applied": applied_patch_count,
                "failed": failed_patches or 0,
                "apply_rate": applied_patch_count / patch_count if patch_count else 0,
                "average_patches_per_workflow": (
                    patch_count / total_count if total_count else 0
                ),
            },
        }
