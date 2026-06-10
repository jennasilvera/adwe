from adwe.agents.planner import create_plan


def test_planner_uses_rule_based_fallback_by_default():
    state = {
        "repository_analysis": {
            "languages": {"Python": 1},
            "detected_tools": {"fastapi": True},
            "api_routes": [],
            "database_models": [],
            "config_files": [],
            "migration_files": [],
            "test_files": [],
        }
    }

    result = create_plan(state)
    plan = result["implementation_plan"]

    assert plan["planner"] == "rule_based"
    assert "recommended_next_steps" in plan
    assert "architecture" in plan
