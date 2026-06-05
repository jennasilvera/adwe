from adwe.workflows.state import WorkflowState


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]

    return {
        "code_modification": {
            "status": "planned",
            "summary": "Generated safe code modification proposal.",
            "proposed_changes": [
                "Add tests for workflow creation.",
                "Add structured audit logs for each agent step.",
                "Add CI migration validation.",
            ],
            "based_on_file_count": analysis.get("file_count"),
        }
    }
