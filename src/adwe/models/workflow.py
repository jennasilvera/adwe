from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from adwe.db.base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    repository_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    queue_job_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="pending",
    )

    repository_analysis: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    implementation_plan: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    code_modification: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    @property
    def duration_seconds(self) -> float | None:
        if self.started_at is None or self.completed_at is None:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()
