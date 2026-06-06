from fastapi.testclient import TestClient

from adwe.api.app import app


def test_patch_workflow_route_is_registered():
    client = TestClient(app)

    response = client.get("/openapi.json")
    routes = response.json()["paths"]

    assert "/v1/patch-workflows/apply" in routes
