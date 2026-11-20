"""
Unit and integration tests for System Status and Health endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from app.core.model_manager import model_manager
from app.core.config import get_settings


@pytest.fixture
def client():
    return TestClient(app)


def test_system_status_endpoint(client):
    """GET /api/v1/system/status returns 200 with structured health and model info."""
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["api"] == "online"
    assert "version" in data
    assert "timestamp" in data
    assert "models" in data
    assert "status" in data["models"]
    assert "components" in data["models"]
    assert "embedding" in data["models"]["components"]
    assert data["models"]["components"]["embedding"]["type"] == "local"
    assert "services" in data
    assert data["services"]["api"] == "running"


def test_health_endpoint(client):
    """GET /health returns 200 and matches the dynamic status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["api"] == "online"
    assert "models" in data
    assert "services" in data
    assert data["services"]["api"] == "running"


def test_model_states_reporting(client):
    """Test that model_manager accurately reports various model states without re-loading."""
    # 1. Simulate loading state
    model_manager.reset_for_testing(status="loading")
    data = client.get("/api/v1/system/status").json()
    assert data["models"]["status"] == "loading"
    assert data["models"]["components"]["embedding"]["status"] == "loading"

    # 2. Simulate error state
    model_manager.reset_for_testing(status="error", error="Failed to download model weights")
    data = client.get("/api/v1/system/status").json()
    assert data["models"]["status"] == "error"
    assert data["models"]["components"]["embedding"]["status"] == "error"
    assert "Failed to download" in (data["models"]["components"]["embedding"]["details"] or "")

    # 3. Simulate not_loaded state
    model_manager.reset_for_testing(status="not_loaded")
    data = client.get("/api/v1/system/status").json()
    assert data["models"]["status"] == "not_loaded"
    assert data["models"]["components"]["embedding"]["status"] == "not_loaded"

    # 4. Simulate loaded state
    model_manager.reset_for_testing(status="loaded", model=object())
    data = client.get("/api/v1/system/status").json()
    # If LLM is available, overall is 'loaded', if not configured, overall is 'partial'
    assert data["models"]["status"] in ("loaded", "partial")
    assert data["models"]["components"]["embedding"]["status"] == "loaded"

    # Reset back to not_loaded or neutral
    model_manager.reset_for_testing(status="not_loaded")


def test_no_secrets_exposed(client):
    """Ensure sensitive API keys and secrets are never leaked in status responses."""
    settings = get_settings()
    response = client.get("/api/v1/system/status")
    text = response.text

    if settings.GOOGLE_GENAI_API_KEY:
        assert settings.GOOGLE_GENAI_API_KEY not in text
    if settings.PUBMED_API_KEY:
        assert settings.PUBMED_API_KEY not in text
    if settings.OPENALEX_API_KEY:
        assert settings.OPENALEX_API_KEY not in text
