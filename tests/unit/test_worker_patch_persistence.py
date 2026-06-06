from adwe.models.patch import Patch
from adwe.models.patch_status import PatchStatus


def test_patch_model_supports_generated_proposals():
    patch = Patch(
        workflow_id="workflow-123",
        file_path="README.md",
        diff="diff --git a/README.md b/README.md\n",
        status=PatchStatus.PROPOSED,
    )

    assert patch.workflow_id == "workflow-123"
    assert patch.file_path == "README.md"
    assert patch.status == PatchStatus.PROPOSED
