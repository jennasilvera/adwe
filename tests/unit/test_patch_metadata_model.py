from adwe.models.patch import Patch


def test_patch_preview_metadata_fields():
    patch = Patch(
        workflow_id="workflow-123",
        file_path="docs/adwe-api-surface.md",
        diff="diff --git a/docs/adwe-api-surface.md b/docs/adwe-api-surface.md\n",
        summary="Generated API surface analysis documentation.",
        files_changed=["docs/adwe-api-surface.md"],
        reasoning="Selected from repository analysis and implementation plan.",
    )

    assert patch.summary == "Generated API surface analysis documentation."
    assert patch.files_changed == ["docs/adwe-api-surface.md"]
    assert "repository analysis" in patch.reasoning
