from fastapi.testclient import TestClient

from gcp_python_api.config import Settings
from gcp_python_api.main import app, get_settings

client = TestClient(app)


def get_settings_override() -> Settings:
    return Settings(app_env="test", demo_api_key="some_api_key")


app.dependency_overrides[get_settings] = get_settings_override


def test_get_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_greet():
    name = "John"
    response = client.get(f"/greet/{name}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}


def test_get_environment():
    response = client.get("/environment")

    assert response.status_code == 200
    assert response.json() == {"result": "test"}


def test_get_api_key():
    response = client.get("/api-key")

    assert response.status_code == 200
    assert response.json() == {"is_configured": True}
