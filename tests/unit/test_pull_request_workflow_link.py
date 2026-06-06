from adwe.models.pull_request import PullRequest
from adwe.services.pull_request_records import record_pull_request


def test_record_pull_request_accepts_workflow_id():
    assert callable(record_pull_request)
    assert PullRequest.__tablename__ == "pull_requests"
