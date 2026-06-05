from datetime import datetime

from typing import Any

from pydantic import BaseModel


class WorkflowCreate(BaseModel):
    repository_url: str


class WorkflowRead(BaseModel):
    id: str
    repository_url: str
    status: str
    created_at: datetime
    repository_analysis: dict[str, Any] | None = None

    model_config = {"from_attributes": True}
