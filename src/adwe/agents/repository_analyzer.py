from adwe.workflows.state import WorkflowState


def analyze_repository(state: WorkflowState):
    repo = state["repository_url"]

    return {
        "repository_analysis":
            f"Repository discovered: {repo}"
    }
