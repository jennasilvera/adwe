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

        return {
            "total": total or 0,
            "completed": completed or 0,
            "failed": failed or 0,
            "running": running or 0,
        }
