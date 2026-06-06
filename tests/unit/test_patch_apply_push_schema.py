from adwe.models.patch_apply_schema import PatchApplyRequest


def test_patch_apply_request_push_defaults_false():
    payload = PatchApplyRequest(
        repository_url="https://github.com/pallets/flask",
        branch_name="adwe/test",
        diff="diff --git a/README.md b/README.md\n",
        commit_message="test commit",
    )

    assert payload.push is False


def test_patch_apply_request_accepts_push_true():
    payload = PatchApplyRequest(
        repository_url="https://github.com/pallets/flask",
        branch_name="adwe/test",
        diff="diff --git a/README.md b/README.md\n",
        commit_message="test commit",
        push=True,
    )

    assert payload.push is True
