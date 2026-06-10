from adwe.agents.code_modifier import _select_patch_target


def test_code_modifier_selects_migration_validation_target():
    target, summary = _select_patch_target(
        {"detected_tools": {"alembic": True}},
        {"recommended_next_steps": ["Add migration validation to CI."]},
    )

    assert target == "docs/adwe-migration-validation.md"
    assert "migration" in summary.lower()


def test_code_modifier_selects_docker_healthcheck_target():
    target, summary = _select_patch_target(
        {"detected_tools": {"docker": True}},
        {"recommended_next_steps": ["Add Docker Compose health checks."]},
    )

    assert target == "docs/adwe-docker-healthchecks.md"
    assert "docker" in summary.lower()


def test_code_modifier_selects_api_surface_target():
    target, summary = _select_patch_target(
        {"detected_tools": {"fastapi": True}, "api_routes": ["src/adwe/api/app.py"]},
        {"recommended_next_steps": []},
    )

    assert target == "docs/adwe-api-surface.md"
    assert "api" in summary.lower()
