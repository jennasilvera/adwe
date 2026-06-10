from adwe.agents.planner import create_plan


def test_planner_generates_structured_plan():
    state = {
        "repository_analysis": {
            "languages": {"Python": 10},
            "detected_tools": {
                "fastapi": True,
                "sqlalchemy": True,
                "alembic": True,
                "docker": True,
                "github_actions": True,
                "pytest": True,
            },
            "api_routes": ["src/adwe/api/app.py"],
            "database_models": ["src/adwe/models/workflow.py"],
            "migration_files": ["migrations/env.py"],
            "test_files": ["tests/unit/test_health.py"],
            "config_files": ["docker-compose.yml"],
        }
    }

    result = create_plan(state)
    plan = result["implementation_plan"]

    assert "architecture" in plan
    assert "strengths" in plan
    assert "risks" in plan
    assert "recommended_next_steps" in plan
    assert plan["architecture"]["api_route_count"] == 1
