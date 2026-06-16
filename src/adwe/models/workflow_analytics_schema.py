from pydantic import BaseModel


class TopPatchTarget(BaseModel):
    file: str
    count: int


class WorkflowAnalyticsResponse(BaseModel):
    repositories_analyzed: int
    unique_repositories: int
    workflows_completed_last_24h: int
    workflows_failed_last_24h: int
    top_patch_targets: list[TopPatchTarget]
    most_common_patch_type: str | None = None
    average_patch_priority: float | None = None
