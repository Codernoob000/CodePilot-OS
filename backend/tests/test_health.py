"""Health endpoint tests."""

from fastapi.testclient import TestClient


def test_health_endpoint_returns_process_status(client: TestClient) -> None:
    """The health endpoint exposes stable probe metadata and correlation ID."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    assert response.json() == {
        "status": "ok",
        "service": "CodePilot OS API",
        "version": "0.1.0",
        "environment": "test",
        "request_id": response.headers["X-Request-ID"],
    }
