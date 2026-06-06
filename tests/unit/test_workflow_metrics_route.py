from fastapi.testclient import TestClient

from adwe.api.app import app


def test_workflow_metrics_route_exists():
    client = TestClient(app)

    response = client.get("/openapi.json")
    paths = response.json()["paths"]

    assert "/v1/workflow-metrics" in paths
