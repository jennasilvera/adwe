from fastapi.testclient import TestClient

from adwe.api.app import app


def test_workflow_routes_are_registered():
    client = TestClient(app)

    schema = client.get("/openapi.json").json()
    paths = schema["paths"]

    assert "/v1/workflows" in paths
    assert "/v1/workflows/{workflow_id}" in paths
    assert "/v1/workflows/{workflow_id}/run" in paths
    assert "/v1/audit-events" in paths
