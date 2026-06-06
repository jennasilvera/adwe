from typing import Any

from pydantic import BaseModel


class WorkflowArtifactsRead(BaseModel):
    workflow_id: str
    repository_analysis: dict[str, Any] | None = None
    implementation_plan: dict[str, Any] | None = None
    code_modification: dict[str, Any] | None = None
    pull_request_id: str | None = None
    queue_job_id: str | None = None
