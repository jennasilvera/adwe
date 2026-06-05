from fastapi import APIRouter
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.audit_event import AuditEvent
from adwe.models.audit_schema import AuditEventRead

router = APIRouter(prefix="/v1/audit-events", tags=["audit"])


@router.get("", response_model=list[AuditEventRead])
async def list_audit_events():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AuditEvent).order_by(AuditEvent.created_at.desc())
        )
        return result.scalars().all()


@router.get("/workflows/{workflow_id}", response_model=list[AuditEventRead])
async def list_workflow_audit_events(workflow_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AuditEvent)
            .where(AuditEvent.workflow_id == workflow_id)
            .order_by(AuditEvent.created_at.asc())
        )
        return result.scalars().all()
