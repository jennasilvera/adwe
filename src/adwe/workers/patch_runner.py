import logging

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus
from adwe.services.audit import record_audit_event

logger = logging.getLogger(__name__)


async def apply_patch_job(ctx, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None:
            logger.warning("patch_not_found patch_id=%s", patch_id)
            return

        patch.status = PatchStatus.APPLYING

        await record_audit_event(
            session=session,
            workflow_id=patch.workflow_id,
            event_type="patch.applying",
            payload={"patch_id": patch.id, "file_path": patch.file_path},
        )

        await session.commit()

        # Real repository patch application will be wired here.
        patch.status = PatchStatus.APPLIED

        await record_audit_event(
            session=session,
            workflow_id=patch.workflow_id,
            event_type="patch.applied",
            payload={"patch_id": patch.id, "file_path": patch.file_path},
        )

        await session.commit()
