from pydantic import BaseModel


class PatchPreviewResponse(BaseModel):
    repository_url: str
    branch_name: str
    dry_run: bool
    diff_lines: int
    test_command: list[str] | None
