from adwe.services.errors import (
    ADWEError,
    PatchApplyWorkflowError,
    PullRequestError,
    RepositoryCloneError,
    TestExecutionError,
)


def test_structured_error_codes():
    assert ADWEError.code == "adwe_error"
    assert RepositoryCloneError.code == "repository_clone_failed"
    assert PatchApplyWorkflowError.code == "patch_apply_failed"
    assert TestExecutionError.code == "test_execution_failed"
    assert PullRequestError.code == "pull_request_failed"
