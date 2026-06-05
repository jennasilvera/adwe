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
