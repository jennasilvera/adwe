from fastapi import APIRouter

from adwe.models.patch_apply_schema import PatchApplyRequest
from adwe.models.patch_preview_schema import PatchPreviewResponse

router = APIRouter(prefix="/v1/patch-workflows", tags=["patch-workflows"])


@router.post("/preview", response_model=PatchPreviewResponse)
async def preview_patch(payload: PatchApplyRequest):
    return PatchPreviewResponse(
        repository_url=payload.repository_url,
        branch_name=payload.branch_name,
        dry_run=payload.dry_run,
        diff_lines=len(payload.diff.splitlines()),
        test_command=payload.test_command,
    )
