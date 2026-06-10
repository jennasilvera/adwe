from adwe.agents.planner import _candidate_targets


def test_candidate_targets_include_migration_docs():
    targets = _candidate_targets(
        {"detected_tools": {"alembic": True}},
        ["Add migration validation to CI."],
    )

    assert "docs/adwe-migration-validation.md" in targets


def test_candidate_targets_include_api_surface_docs():
    targets = _candidate_targets(
        {
            "detected_tools": {"fastapi": True},
            "api_routes": ["src/adwe/api/app.py"],
        },
        [],
    )

    assert "docs/adwe-api-surface.md" in targets
