from typing import TypedDict


class WorkflowState(TypedDict):
    repository_url: str
    repository_analysis: str
    implementation_plan: str
