from fastapi import APIRouter, HTTPException

from adwe.models.patch_apply_schema import PatchApplyRequest, PatchApplyResponse
from adwe.services.patch_workflow import apply_patch_workflow

router = APIRouter(prefix="/v1/patch-workflows", tags=["patch-workflows"])


@router.post("/apply", response_model=PatchApplyResponse)
async def apply_patch(payload: PatchApplyRequest):
    try:
        return apply_patch_workflow(
            repository_url=payload.repository_url,
            branch_name=payload.branch_name,
            diff=payload.diff,
            commit_message=payload.commit_message,
            test_command=payload.test_command,
            dry_run=payload.dry_run,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Patch workflow failed: {exc}",
        ) from exc
