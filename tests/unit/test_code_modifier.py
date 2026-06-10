from adwe.agents.code_modifier import modify_code


def test_code_modifier_generates_plan_aware_analysis_patch():
    state = {
        "repository_analysis": {
            "file_count": 10,
            "detected_tools": {"fastapi": True, "docker": False},
        },
        "implementation_plan": {
            "architecture": {
                "api_route_count": 2,
                "database_model_count": 3,
                "migration_count": 1,
                "test_count": 5,
            },
            "strengths": ["FastAPI API layer detected."],
            "risks": ["Docker support missing."],
            "recommended_next_steps": ["Add Docker support for local development."],
        },
    }

    result = modify_code(state)
    patch = result["code_modification"]["patch"]

    assert "ADWE_ANALYSIS.md" in patch
    assert "Repository Summary" in patch
    assert "Detected Tooling" in patch
    assert "Strengths" in patch
    assert "Risks" in patch
    assert "Recommended Next Steps" in patch
    assert "Add Docker support for local development." in patch
