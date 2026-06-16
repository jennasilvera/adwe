from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from adwe.db.session import AsyncSessionLocal
from adwe.models.audit_event import AuditEvent
from adwe.models.workflow import Workflow
from adwe.models.workflow_timeline_schema import (
    WorkflowTimelineEvent,
    WorkflowTimelineResponse,
)

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])


@router.get("/{workflow_id}/timeline", response_model=WorkflowTimelineResponse)
async def get_workflow_timeline(workflow_id: str):
    async with AsyncSessionLocal() as session:
        workflow = await session.get(Workflow, workflow_id)

        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found")

        rows = await session.execute(
            select(AuditEvent)
            .where(AuditEvent.workflow_id == workflow_id)
            .order_by(AuditEvent.created_at.asc())
        )

        events = [
            WorkflowTimelineEvent(
                timestamp=event.created_at,
                event=event.event_type,
                payload=event.payload,
            )
            for event in rows.scalars().all()
        ]

        return WorkflowTimelineResponse(
            workflow_id=workflow_id,
            events=events,
        )
