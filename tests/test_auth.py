from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock

from fastapi.testclient import TestClient

from app.db.dependencies import get_current_user, get_user_service
from app.main import app


def test_register():
    user = Mock()
    user.id = 1
    user.email = "test@example.com"
    user.is_active = True
    user.created_at = datetime.now(UTC)

    service = Mock()
    service.create_user = AsyncMock(return_value=user)
    app.dependency_overrides[get_user_service] = lambda: service
    client = TestClient(app)

    response = client.post(
        "auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True

    service.create_user.assert_awaited_once()
    app.dependency_overrides.clear()


def test_login():
    service = Mock()
    service.authenticate = AsyncMock(return_value="test_access_token")

    app.dependency_overrides[get_user_service] = lambda: service

    client = TestClient(app)

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"] == "test_access_token"
    assert data["token_type"] == "bearer"

    service.authenticate.assert_awaited_once()

    app.dependency_overrides.clear()


def test_me():
    user = Mock()
    user.id = 1
    user.email = "test@example.com"
    user.is_active = True
    user.created_at = datetime.now(UTC)

    app.dependency_overrides[get_current_user] = lambda: user

    client = TestClient(app)

    response = client.get("/auth/me")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True

    app.dependency_overrides.clear()
