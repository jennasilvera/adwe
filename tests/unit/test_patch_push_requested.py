from adwe.models.patch import Patch


def test_patch_push_requested_defaults_false():
    patch = Patch(
        workflow_id="workflow-123",
        file_path="ADWE_ANALYSIS.md",
        diff="diff --git a/ADWE_ANALYSIS.md b/ADWE_ANALYSIS.md\n",
        status="proposed",
    )

    assert patch.push_requested is None or patch.push_requested is False
