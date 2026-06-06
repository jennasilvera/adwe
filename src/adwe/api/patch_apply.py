from fastapi import APIRouter

from adwe.models.patch_apply_schema import PatchApplyRequest, PatchApplyResponse
from adwe.services.patch_workflow import apply_patch_workflow

router = APIRouter(prefix="/v1/patch-workflows", tags=["patch-workflows"])


@router.post("/apply", response_model=PatchApplyResponse)
async def apply_patch(payload: PatchApplyRequest):
    return apply_patch_workflow(
        repository_url=payload.repository_url,
        branch_name=payload.branch_name,
        diff=payload.diff,
        commit_message=payload.commit_message,
    )
