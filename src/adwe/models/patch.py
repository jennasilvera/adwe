from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from adwe.db.base import Base
from adwe.models.patch_status import PatchStatus


class Patch(Base):
    __tablename__ = "patches"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    workflow_id: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    diff: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default=PatchStatus.PROPOSED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    branch_name: Mapped[str | None] = mapped_column(String, nullable=True)
    commit_sha: Mapped[str | None] = mapped_column(String, nullable=True)
    apply_error: Mapped[str | None] = mapped_column(String, nullable=True)
    push_requested: Mapped[bool] = mapped_column(default=False)
