import logging

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus

logger = logging.getLogger(__name__)


async def apply_patch_job(ctx, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None:
            logger.warning("patch_not_found patch_id=%s", patch_id)
            return

        patch.status = PatchStatus.APPLYING
        await session.commit()

        # Real repository patch application will be wired here.
        # For now, mark the queued job path as successful.
        patch.status = PatchStatus.APPLIED

        await session.commit()
