from fastapi.testclient import TestClient

from adwe.api.app import app


def test_patch_summary_route_exists():
    client = TestClient(app)

    response = client.get("/openapi.json")
    paths = response.json()["paths"]

    assert "/v1/workflows/{workflow_id}/patches-summary" in paths
