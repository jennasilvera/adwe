from pydantic import BaseModel


class WorkflowLeaderboardEntry(BaseModel):
    workflow_id: str
    repository_url: str
    patch_count: int
    approved_patch_count: int
    applied_patch_count: int


class WorkflowLeaderboardResponse(BaseModel):
    entries: list[WorkflowLeaderboardEntry]
