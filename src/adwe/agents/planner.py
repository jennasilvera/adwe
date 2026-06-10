from adwe.workflows.state import WorkflowState


def create_plan(state: WorkflowState):
    analysis = state["repository_analysis"]

    tools = analysis.get("detected_tools", {})
    languages = analysis.get("languages", {})
    api_routes = analysis.get("api_routes", [])
    database_models = analysis.get("database_models", [])
    config_files = analysis.get("config_files", [])
    migration_files = analysis.get("migration_files", [])
    test_files = analysis.get("test_files", [])

    recommended_steps: list[str] = []
    risks: list[str] = []
    strengths: list[str] = []

    if tools.get("fastapi"):
        strengths.append("FastAPI API layer detected.")

    if tools.get("sqlalchemy"):
        strengths.append("SQLAlchemy persistence layer detected.")

    if tools.get("alembic"):
        strengths.append("Alembic migration system detected.")

    if tools.get("docker"):
        strengths.append("Docker-based local development detected.")

    if tools.get("github_actions"):
        strengths.append("GitHub Actions CI detected.")

    if not tools.get("github_actions"):
        recommended_steps.append("Add GitHub Actions CI for tests and linting.")

    if not tools.get("docker"):
        recommended_steps.append("Add Docker support for local development.")

    if tools.get("alembic") and migration_files:
        recommended_steps.append("Add migration validation to CI.")

    if len(test_files) < 10:
        risks.append("Test coverage appears light for a workflow automation platform.")
        recommended_steps.append("Increase automated test coverage for API, workers, and services.")
    else:
        strengths.append("Substantial test suite detected.")

    if api_routes:
        recommended_steps.append("Add endpoint-level smoke tests for all public API routes.")

    if database_models:
        recommended_steps.append("Add database model relationship tests and migration regression tests.")

    if "docker-compose.yml" in config_files:
        recommended_steps.append("Add Docker Compose health checks for Postgres, Redis, API, and worker.")

    recommended_steps.append("Add structured audit events for every agent transition.")
    recommended_steps.append("Add workflow-level artifact summaries for recruiter-friendly demos.")

    return {
        "implementation_plan": {
            "summary": "Generated structured implementation plan from repository architecture analysis.",
            "detected_languages": languages,
            "detected_tools": tools,
            "architecture": {
                "api_route_count": len(api_routes),
                "database_model_count": len(database_models),
                "migration_count": len(migration_files),
                "test_count": len(test_files),
                "config_files": config_files,
            },
            "strengths": strengths,
            "risks": risks,
            "recommended_next_steps": recommended_steps,
        }
    }
