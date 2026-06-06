class ADWEError(Exception):
    code = "adwe_error"


class RepositoryCloneError(ADWEError):
    code = "repository_clone_failed"


class PatchApplyWorkflowError(ADWEError):
    code = "patch_apply_failed"


class TestExecutionError(ADWEError):
    code = "test_execution_failed"


class PullRequestError(ADWEError):
    code = "pull_request_failed"
