from fastapi.testclient import TestClient

from adwe.api.app import app


def test_patch_routes_are_registered():
    client = TestClient(app)

    response = client.get("/openapi.json")
    routes = response.json()["paths"]

    assert "/v1/workflows/{workflow_id}/patches" in routes
    assert "/v1/workflows/{workflow_id}/patches/{patch_id}/approve" in routes
    assert "/v1/workflows/{workflow_id}/patches/{patch_id}/reject" in routes
