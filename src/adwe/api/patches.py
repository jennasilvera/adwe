from fastapi import APIRouter
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_schema import PatchRead

router = APIRouter(prefix="/v1/workflows", tags=["patches"])


@router.get("/{workflow_id}/patches", response_model=list[PatchRead])
async def list_workflow_patches(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Patch).where(Patch.workflow_id == workflow_id)
        )
        return result.scalars().all()
