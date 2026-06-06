from typing import Any

from pydantic import BaseModel, ConfigDict


class PatchApplyRequest(BaseModel):
    repository_url: str
    branch_name: str
    diff: str
    commit_message: str
    test_command: list[str] | None = None
    dry_run: bool = False
    push: bool = False
    open_pr: bool = False
    pr_title: str | None = None
    pr_body: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "repository_url": "https://github.com/pallets/flask",
                "branch_name": "adwe/update-readme",
                "diff": "diff --git a/README.md b/README.md\n--- a/README.md\n+++ b/README.md\n@@ -1 +1,2 @@\n hello\n+world\n",
                "commit_message": "Update README with ADWE patch",
                "test_command": ["python", "-m", "pytest"],
                "dry_run": True,
                "push": False,
                "open_pr": False
            }
        }
    )


class PatchApplyResponse(BaseModel):
    branch_name: str
    commit_sha: str | None = None
    status: str
    test_result: dict[str, Any] | None = None
    pushed: bool = False
    pull_request: dict[str, Any] | None = None
