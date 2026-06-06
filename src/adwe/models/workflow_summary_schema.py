from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkflowSummaryRead(BaseModel):
    id: str
    repository_url: str
    status: str
    queue_job_id: str | None = None
    pull_request_id: str | None = None
    retry_count: int = 0
    last_error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: float | None = None
    file_count: int | None = None
    detected_languages: dict[str, Any] | None = None
    recommended_next_steps: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)
