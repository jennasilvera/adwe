from fastapi import APIRouter

from adwe.models.patch_apply_schema import PatchApplyRequest
from adwe.models.patch_preview_schema import PatchPreviewResponse

router = APIRouter(prefix="/v1/patch-workflows", tags=["patch-workflows"])


def _extract_changed_files(diff: str) -> list[str]:
    files: list[str] = []

    for line in diff.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                path = parts[3]
                if path.startswith("b/"):
                    path = path[2:]
                files.append(path)

    return files


@router.post("/preview", response_model=PatchPreviewResponse)
async def preview_patch(payload: PatchApplyRequest):
    files_changed = _extract_changed_files(payload.diff)

    summary = (
        f"Patch changes {len(files_changed)} file(s) "
        f"across {len(payload.diff.splitlines())} diff line(s)."
    )

    return PatchPreviewResponse(
        repository_url=payload.repository_url,
        branch_name=payload.branch_name,
        dry_run=payload.dry_run,
        diff_lines=len(payload.diff.splitlines()),
        test_command=payload.test_command,
        files_changed=files_changed,
        summary=summary,
    )
