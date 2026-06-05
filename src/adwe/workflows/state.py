from typing import Any, TypedDict


class WorkflowState(TypedDict):
    repository_url: str
    repository_analysis: dict[str, Any]
    implementation_plan: str
