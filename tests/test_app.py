"""
Automated Pytest Suite for AutoDeploy Application.
Tests homepage, health check, and application info endpoints using Flask test client.
"""

import pytest
from app import app, APP_NAME


@pytest.fixture
def client():
    """
    Flask test client fixture.
    Configures app for testing and provides a test client instance.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage_status_code(client):
    """Test 1: Homepage returns HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_homepage_contains_app_name(client):
    """Test 2: Homepage HTML contains the application name."""
    response = client.get("/")
    assert response.status_code == 200
    assert APP_NAME.encode("utf-8") in response.data


def test_homepage_contains_running_status(client):
    """Test 3: Homepage HTML displays 'Running' application status."""
    response = client.get("/")
    assert b"Running" in response.data


def test_health_endpoint_status_code(client):
    """Test 4: Health endpoint returns HTTP 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_expected_json(client):
    """Test 5: Health endpoint returns expected JSON payload."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == {
        "status": "healthy",
        "application": "AutoDeploy"
    }


def test_api_info_endpoint_valid_json(client):
    """Test 6: Application info endpoint returns HTTP 200 and valid JSON with metadata."""
    response = client.get("/api/info")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["application"] == "AutoDeploy"
    assert data["status"] == "Running"
    assert "version" in data
    assert "description" in data
    assert "endpoints" in data
    assert data["endpoints"]["health"] == "/health"


def test_404_not_found(client):
    """Test 7: Accessing an undefined endpoint returns HTTP 404."""
    response = client.get("/nonexistent-endpoint-route")
    assert response.status_code == 404
