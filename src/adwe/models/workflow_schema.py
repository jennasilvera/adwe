from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator


class WorkflowCreate(BaseModel):
    repository_url: str

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
    created_at: datetime
    repository_analysis: dict[str, Any] | None = None
    implementation_plan: dict[str, Any] | None = None
    code_modification: dict[str, Any] | None = None

    model_config = {"from_attributes": True}
