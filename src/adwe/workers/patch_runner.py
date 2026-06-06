import logging

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus
from adwe.models.workflow import Workflow
from adwe.services.audit import record_audit_event
from adwe.services.patch_workflow import apply_patch_workflow

logger = logging.getLogger(__name__)


async def apply_patch_job(ctx, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None:
            logger.warning("patch_not_found patch_id=%s", patch_id)
            return

        workflow = await session.get(Workflow, patch.workflow_id)

        if workflow is None:
            logger.warning("workflow_not_found workflow_id=%s", patch.workflow_id)
            return

        patch.status = PatchStatus.APPLYING

        await record_audit_event(
            session=session,
            workflow_id=patch.workflow_id,
            event_type="patch.applying",
            payload={"patch_id": patch.id, "file_path": patch.file_path},
        )

        await session.commit()

        try:
            result = apply_patch_workflow(
                repository_url=workflow.repository_url,
                branch_name=f"adwe/{workflow.id}",
                diff=patch.diff,
                commit_message=f"Apply ADWE patch for workflow {workflow.id}",
                dry_run=True,
            )

            patch.branch_name = result.get("branch_name")
            patch.commit_sha = result.get("commit_sha")
            patch.status = PatchStatus.APPLIED

            await record_audit_event(
                session=session,
                workflow_id=patch.workflow_id,
                event_type="patch.applied",
                payload={
                    "patch_id": patch.id,
                    "file_path": patch.file_path,
                    "branch_name": patch.branch_name,
                    "commit_sha": patch.commit_sha,
                },
            )

        except Exception as exc:
            logger.exception("patch_apply_failed patch_id=%s", patch.id)

            patch.status = PatchStatus.FAILED
            patch.apply_error = str(exc)

            await record_audit_event(
                session=session,
                workflow_id=patch.workflow_id,
                event_type="patch.apply_failed",
                payload={
                    "patch_id": patch.id,
                    "file_path": patch.file_path,
                    "error": str(exc),
                },
            )

        await session.commit()
