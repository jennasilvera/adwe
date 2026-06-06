from pydantic import BaseModel


class PatchApplyRequest(BaseModel):
    repository_url: str
    branch_name: str
    diff: str
    commit_message: str


class PatchApplyResponse(BaseModel):
    branch_name: str
    commit_sha: str
    status: str
