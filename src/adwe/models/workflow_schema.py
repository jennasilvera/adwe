from datetime import datetime

from pydantic import BaseModel


class WorkflowCreate(BaseModel):
    repository_url: str


class WorkflowRead(BaseModel):
    id: str
    repository_url: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
