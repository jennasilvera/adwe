from adwe.services.workspace import repository_workspace


def test_repository_workspace_imports():
    assert callable(repository_workspace)
