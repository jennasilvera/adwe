import pytest
from pydantic import ValidationError

from adwe.models.workflow_schema import WorkflowCreate


def test_workflow_create_accepts_github_https_url():
    payload = WorkflowCreate(repository_url="https://github.com/jennasilvera/adwe")

    assert payload.repository_url == "https://github.com/jennasilvera/adwe"


def test_workflow_create_rejects_non_github_url():
    with pytest.raises(ValidationError):
        WorkflowCreate(repository_url="https://example.com/repo")
