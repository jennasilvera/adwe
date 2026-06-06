from datetime import datetime
import logging

from sqlalchemy import select

from adwe.core.constants import MAX_WORKFLOW_RETRIES
from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_status import WorkflowStatus
from adwe.workflows.engine import workflow_graph
from adwe.workers.heartbeat import record_heartbeat

logger = logging.getLogger(__name__)


async def run_workflow(ctx, workflow_id: str):
    await record_heartbeat()

    async with AsyncSessionLocal() as session:
        workflow = await session.scalar(
            select(Workflow).where(Workflow.id == workflow_id)
        )

        if workflow is None:
            return

        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        await session.commit()

        try:
            result = workflow_graph.invoke(
                {"repository_url": workflow.repository_url}
            )

            workflow.repository_analysis = result.get("repository_analysis")
            workflow.implementation_plan = result.get("implementation_plan")
            workflow.code_modification = result.get("code_modification")

            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()

        except Exception as exc:
            logger.exception("workflow_failed workflow_id=%s", workflow_id)

            workflow.retry_count += 1
            workflow.last_error = str(exc)
            workflow.completed_at = datetime.utcnow()

            if workflow.retry_count < MAX_WORKFLOW_RETRIES:
                workflow.status = WorkflowStatus.PENDING
                await session.commit()

                await ctx["redis"].enqueue_job(
                    "run_workflow",
                    workflow.id,
                    _defer_by=workflow.retry_count * 30,
                )

                return

            workflow.status = WorkflowStatus.FAILED

        await session.commit()
