from adwe.services.patch_workflow import apply_patch_workflow


def test_apply_patch_workflow_imports():
    assert callable(apply_patch_workflow)
