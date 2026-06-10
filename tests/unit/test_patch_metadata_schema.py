from adwe.models.patch_schema import PatchRead


def test_patch_read_exposes_preview_metadata():
    patch = PatchRead(
        id="patch-123",
        workflow_id="workflow-123",
        file_path="docs/adwe-api-surface.md",
        diff="diff --git a/docs/adwe-api-surface.md b/docs/adwe-api-surface.md\n",
        status="proposed",
        created_at="2026-01-01T00:00:00",
        summary="Generated API surface analysis documentation.",
        files_changed=["docs/adwe-api-surface.md"],
        reasoning="Selected from repository analysis and implementation plan.",
    )

    assert patch.summary == "Generated API surface analysis documentation."
    assert patch.files_changed == ["docs/adwe-api-surface.md"]
    assert patch.reasoning is not None
