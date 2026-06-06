from sqlalchemy import func, select

from adwe.db.session import AsyncSessionLocal
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

        return {
            "total": total_count,
            "completed": completed_count,
            "failed": failed_count,
            "running": running or 0,
            "success_rate": completed_count / total_count if total_count else 0,
            "failure_rate": failed_count / total_count if total_count else 0,
            "average_duration_seconds": float(avg_duration) if avg_duration else None,
        }
