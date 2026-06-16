from datetime import datetime
from typing import Any

from pydantic import BaseModel


class WorkflowTimelineEvent(BaseModel):
    timestamp: datetime
    event: str
    payload: dict[str, Any] | None = None


class WorkflowTimelineResponse(BaseModel):
    workflow_id: str
    events: list[WorkflowTimelineEvent]
