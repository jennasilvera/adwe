import logging

from adwe.db.session import AsyncSessionLocal
from adwe.models.workflow import Workflow
from adwe.workflows.engine import workflow_graph

logger = logging.getLogger(__name__)


async def run_workflow(workflow_id: str):
    logger.info("starting workflow %s", workflow_id)

    async with AsyncSessionLocal() as session:

        workflow = await session.get(
            Workflow,
            workflow_id,
        )

        if workflow is None:
            return

        workflow.status = "running"
        await session.commit()

        result = workflow_graph.invoke(
            {
                "repository_url": workflow.repository_url,
            }
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

        workflow.status = "completed"

        await session.commit()

        logger.info(
            "completed workflow %s",
            workflow_id,
        )
