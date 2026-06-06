import pytest

from adwe.services.git_push import GitPushError, push_branch


def test_push_branch_requires_github_token(tmp_path):
    with pytest.raises(GitPushError):
        push_branch(tmp_path, "adwe/test")
