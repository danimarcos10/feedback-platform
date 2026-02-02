"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestRegister:
    """Tests for user registration."""

    def test_register_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            json={"email": "newuser@example.com", "password": "newpassword123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["role"] == "user"
        assert "id" in data

    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test registration with existing email fails."""
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email format fails."""
        response = client.post(
            "/auth/register",
            json={"email": "invalid-email", "password": "password123"}
        )
        assert response.status_code == 422


class TestLogin:
    """Tests for user login."""

    def test_login_success(self, client: TestClient, test_user):
        """Test successful login returns token."""
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "testpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user):
        """Test login with wrong password fails."""
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user fails."""
        response = client.post(
            "/auth/login",
            data={"username": "nouser@example.com", "password": "password"}
        )
        assert response.status_code == 401


class TestCurrentUser:
    """Tests for getting current user info."""

    def test_get_me_authenticated(self, client: TestClient, user_headers, test_user):
        """Test getting current user info when authenticated."""
        response = client.get("/auth/me", headers=user_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "user"

    def test_get_me_unauthenticated(self, client: TestClient):
        """Test getting current user info without auth fails."""
        response = client.get("/auth/me")
        assert response.status_code == 401
