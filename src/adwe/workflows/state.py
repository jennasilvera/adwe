from typing import Any, TypedDict


class WorkflowState(TypedDict):
    repository_url: str
    repository_analysis: dict[str, Any]
    implementation_plan: dict[str, Any]
    code_modification: dict[str, Any]
    code_modifications: list[dict[str, Any]]
