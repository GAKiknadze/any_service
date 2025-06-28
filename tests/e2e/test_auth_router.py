import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from src.interfaces.api.v1.routers.auth import auth_router
from fastapi import FastAPI


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1/auth")
    with TestClient(app) as c:
        yield c


@pytest.mark.skip("on dev")
def test_register_and_login_flow(client):
    # Register new user
    email = f"user_{uuid4()}@example.com"
    password = "testpassword"
    payload = {
        "email": email,
        "password": password,
        "profile": {
            "nick_name": f"nick_{uuid4()}",
            "first_name": "Test",
            "last_name": "User",
        },
    }
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # Login with the same user
    login_payload = {"email": email, "password": password}
    resp = client.post("/api/v1/auth/login", json=login_payload)
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Refresh token
    cookies = {"refresh_token": tokens["refresh_token"]}
    resp = client.post("/api/v1/auth/refresh", cookies=cookies)
    assert resp.status_code == 200
    refreshed = resp.json()
    assert "access_token" in refreshed
    assert "refresh_token" in refreshed

    # Logout
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = client.post("/api/v1/auth/logout", headers=headers)
    assert resp.status_code == 204


@pytest.mark.skip("on dev")
def test_login_invalid_credentials(client):
    payload = {"email": "notfound@example.com", "password": "wrong"}
    resp = client.post("/api/v1/auth/login", json=payload)
    assert resp.status_code == 401 or resp.status_code == 400


@pytest.mark.skip("on dev")
def test_refresh_without_cookie(client):
    resp = client.post("/api/v1/auth/refresh")
    assert resp.status_code == 401 or resp.status_code == 400


@pytest.mark.skip("on dev")
def test_logout_without_token(client):
    resp = client.post("/api/v1/auth/logout")
    assert resp.status_code == 401 or resp.status_code == 400
