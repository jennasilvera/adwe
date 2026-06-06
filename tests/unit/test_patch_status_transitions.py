from adwe.models.patch_status import PatchStatus


def test_patch_status_transition_values():
    assert PatchStatus.PROPOSED == "proposed"
    assert PatchStatus.APPLIED == "applied"
    assert PatchStatus.APPLYING == "applying"
    assert PatchStatus.REJECTED == "rejected"
