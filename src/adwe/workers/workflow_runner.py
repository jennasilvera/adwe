import asyncio
import logging

from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.models.workflow_status import WorkflowStatus
from adwe.workflows.engine import workflow_graph

logger = logging.getLogger(__name__)


async def run_workflow(ctx, workflow_id: str):
    async with AsyncSessionLocal() as session:

        workflow = await session.scalar(
            select(Workflow).where(Workflow.id == workflow_id)
        )

        if workflow is None:
            return

        workflow.status = WorkflowStatus.RUNNING
        await session.commit()

        try:
            result = workflow_graph.invoke(
                {"repository_url": workflow.repository_url}
            )

            workflow.repository_analysis = result.get(
                "repository_analysis"
            )

            workflow.implementation_plan = result.get(
                "implementation_plan"
            )

            workflow.code_modification = result.get(
                "code_modification"
            )

            workflow.status = WorkflowStatus.COMPLETED

        except Exception as e:

            logger.exception(
                "workflow_failed workflow_id=%s",
                workflow_id,
            )

            workflow.status = WorkflowStatus.FAILED

        await session.commit()
