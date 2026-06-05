from adwe.workflows.state import WorkflowState


def create_plan(state: WorkflowState):
    analysis = state["repository_analysis"]

    tools = analysis.get("detected_tools", {})
    languages = analysis.get("languages", {})

    recommended_steps = []

    if not tools.get("github_actions"):
        recommended_steps.append("Add GitHub Actions CI for tests and linting.")

    if not tools.get("docker"):
        recommended_steps.append("Add Docker support for local development.")

    if analysis.get("test_count", 0) < 5:
        recommended_steps.append("Increase automated test coverage for API and agents.")

    if analysis.get("migration_count", 0) > 0:
        recommended_steps.append("Add migration validation to CI.")

    recommended_steps.append("Add structured audit events for each agent transition.")

    return {
        "implementation_plan": {
            "summary": "Generated plan from repository architecture analysis.",
            "detected_languages": languages,
            "detected_tools": tools,
            "recommended_next_steps": recommended_steps,
        }
    }
