from adwe.workflows.state import WorkflowState


def create_plan(state: WorkflowState):
    analysis = state["repository_analysis"]

    languages = analysis.get("languages", {})
    tools = analysis.get("detected_tools", {})

    plan = {
        "summary": "Generated implementation plan from repository architecture.",
        "recommended_next_steps": [
            "Add automated tests for workflow creation and repository analysis.",
            "Add structured logging with request and workflow IDs.",
            "Add CI checks for linting, formatting, tests, and migrations.",
            "Add audit events for each workflow stage.",
        ],
        "detected_languages": languages,
        "detected_tools": tools,
    }

    return {"implementation_plan": plan}
