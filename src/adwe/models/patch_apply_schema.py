from typing import Any

from pydantic import BaseModel


class PatchApplyRequest(BaseModel):
    repository_url: str
    branch_name: str
    diff: str
    commit_message: str
    test_command: list[str] | None = None


class PatchApplyResponse(BaseModel):
    branch_name: str
    commit_sha: str
    status: str
    test_result: dict[str, Any] | None = None
