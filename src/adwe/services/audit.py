from sqlalchemy.ext.asyncio import AsyncSession

from adwe.models.audit_event import AuditEvent


async def record_audit_event(
    session: AsyncSession,
    event_type: str,
    workflow_id: str | None = None,
    payload: dict | None = None,
) -> AuditEvent:
    event = AuditEvent(
        workflow_id=workflow_id,
        event_type=event_type,
        payload=payload,
    )
    session.add(event)
    return event
