"""Shared backend test fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import create_application


@pytest.fixture
def client() -> TestClient:
    """Return an isolated API client with deterministic test settings."""
    get_settings.cache_clear()
    app = create_application(
        Settings(environment="test", docs_enabled=False, cors_origins=("http://testserver",))
    )
    with TestClient(app) as test_client:
        yield test_client
    get_settings.cache_clear()
