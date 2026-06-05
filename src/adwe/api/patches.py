from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_schema import PatchRead

router = APIRouter(prefix="/v1/patches", tags=["patches"])


@router.get("/workflows/{workflow_id}", response_model=list[PatchRead])
async def list_workflow_patches(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Patch)
            .where(Patch.workflow_id == workflow_id)
            .order_by(Patch.created_at.asc())
        )
        return result.scalars().all()


@router.get("/{patch_id}", response_model=PatchRead)
async def get_patch(patch_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Patch).where(Patch.id == patch_id)
        )
        patch = result.scalar_one_or_none()

        if patch is None:
            raise HTTPException(status_code=404, detail="Patch not found")

        return patch
