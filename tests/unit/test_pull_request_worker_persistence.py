from adwe.services.pull_request_records import record_pull_request


def test_record_pull_request_service_exists():
    assert callable(record_pull_request)
