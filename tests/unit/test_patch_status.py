from adwe.models.patch_status import PatchStatus


def test_patch_status_values():
    assert PatchStatus.PROPOSED == "proposed"
    assert PatchStatus.APPLIED == "applied"
    assert PatchStatus.FAILED == "failed"
