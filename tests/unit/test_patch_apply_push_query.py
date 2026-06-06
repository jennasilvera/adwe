from fastapi.testclient import TestClient

from adwe.api.app import app


def test_patch_apply_accepts_push_query_parameter():
    client = TestClient(app)

    response = client.get("/openapi.json")
    operation = response.json()["paths"][
        "/v1/workflows/{workflow_id}/patches/{patch_id}/apply"
    ]["post"]

    parameter_names = {param["name"] for param in operation["parameters"]}

    assert "push" in parameter_names
