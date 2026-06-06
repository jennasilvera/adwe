from adwe.services.git_push import push_branch


def test_push_branch_imports():
    assert callable(push_branch)
