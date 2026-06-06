from datetime import datetime

from pydantic import BaseModel


class PatchRead(BaseModel):
    id: str
    workflow_id: str
    file_path: str
    diff: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
    branch_name: str | None = None
    commit_sha: str | None = None
    apply_error: str | None = None
    push_requested: bool = False
    open_pr_requested: bool = False
    pr_title: str | None = None
    pr_body: str | None = None
