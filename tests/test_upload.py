from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app


client = TestClient(app)

def test_upload_schema():
    with open("sample_openapi.yaml", "rb") as file:
        response = client.post(
            "/upload",
            files={"file": ("sample_openapi.yaml", file, "application/x-yaml")},
            data={"application": "test-app", "service": "test-service"},
        )
    assert response.status_code == 200
    json_data = response.json()
    assert "Schema v" in json_data["message"]
    assert json_data["filepath"].endswith(".yaml")
