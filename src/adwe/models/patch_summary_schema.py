from pydantic import BaseModel


class PatchSummaryRead(BaseModel):
    workflow_id: str
    total: int
    proposed: int
    applied: int
    rejected: int
