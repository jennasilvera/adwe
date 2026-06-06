from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class WorkflowCreate(BaseModel):
    repository_url: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "repository_url": "https://github.com/pallets/flask"
            }
        }
    )

    @field_validator("repository_url")
    @classmethod
    def validate_repository_url(cls, value: str) -> str:
        if not value.startswith(("https://github.com/", "git@github.com:")):
            raise ValueError("repository_url must be a GitHub repository URL")
        return value


class WorkflowRead(BaseModel):
    id: str
    repository_url: str
    status: str
    queue_job_id: str | None = None
    created_at: datetime
    repository_analysis: dict[str, Any] | None = None
    implementation_plan: dict[str, Any] | None = None
    code_modification: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)
