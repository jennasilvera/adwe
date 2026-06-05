from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditEventRead(BaseModel):
    id: str
    workflow_id: str | None
    event_type: str
    payload: dict[str, Any] | None
    created_at: datetime

    model_config = {"from_attributes": True}
