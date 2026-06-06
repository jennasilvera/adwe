from adwe.models.patch_apply_schema import PatchApplyRequest


def test_patch_apply_request_defaults():
    payload = PatchApplyRequest(
        repository_url="https://github.com/pallets/flask",
        branch_name="adwe/test",
        diff="diff --git a/README.md b/README.md\n",
        commit_message="test commit",
    )

    assert payload.dry_run is False
    assert payload.open_pr is False
    assert payload.pr_title is None
    assert payload.pr_body is None
