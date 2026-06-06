from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PullRequestRecordRead(BaseModel):
    id: str
    workflow_id: str | None
    repository_url: str
    branch_name: str
    title: str
    url: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
