from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.patch import Patch
from adwe.models.patch_schema import PatchRead
from adwe.models.patch_status import PatchStatus
from adwe.services.audit import record_audit_event

router = APIRouter(prefix="/v1/workflows", tags=["patches"])


@router.get("/{workflow_id}/patches", response_model=list[PatchRead])
async def list_workflow_patches(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Patch).where(Patch.workflow_id == workflow_id)
        )
        return result.scalars().all()


@router.get("/{workflow_id}/patches/{patch_id}", response_model=PatchRead)
async def get_workflow_patch(workflow_id: str, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None or patch.workflow_id != workflow_id:
            raise HTTPException(status_code=404, detail="Patch not found")

        return patch


@router.post("/{workflow_id}/patches/{patch_id}/approve", response_model=PatchRead)
async def approve_patch(workflow_id: str, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None or patch.workflow_id != workflow_id:
            raise HTTPException(status_code=404, detail="Patch not found")

        patch.status = PatchStatus.APPLIED

        await record_audit_event(
            session=session,
            workflow_id=workflow_id,
            event_type="patch.approved",
            payload={"patch_id": patch_id, "file_path": patch.file_path},
        )

        await session.commit()
        await session.refresh(patch)

        return patch


@router.post("/{workflow_id}/patches/{patch_id}/reject", response_model=PatchRead)
async def reject_patch(workflow_id: str, patch_id: str):
    async with AsyncSessionLocal() as session:
        patch = await session.get(Patch, patch_id)

        if patch is None or patch.workflow_id != workflow_id:
            raise HTTPException(status_code=404, detail="Patch not found")

        patch.status = PatchStatus.REJECTED

        await record_audit_event(
            session=session,
            workflow_id=workflow_id,
            event_type="patch.rejected",
            payload={"patch_id": patch_id, "file_path": patch.file_path},
        )

        await session.commit()
        await session.refresh(patch)

        return patch
