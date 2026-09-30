from fastapi.testclient import TestClient
from gcp_python_api.main import app

client = TestClient(app)

def test_get_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_greet():
    name = "John"
    response = client.get(f"/greet/{name}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}