"""Tests for categories and tags endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestCategories:
    """Tests for category operations."""

    def test_create_category_as_admin(self, client: TestClient, admin_headers):
        """Test admin can create category."""
        response = client.post(
            "/categories/",
            json={"name": "Bug Report"},
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Bug Report"

    def test_create_category_as_user_forbidden(self, client: TestClient, user_headers):
        """Test regular user cannot create category."""
        response = client.post(
            "/categories/",
            json={"name": "Test Category"},
            headers=user_headers
        )
        assert response.status_code == 403

    def test_list_categories(self, client: TestClient, admin_headers, user_headers):
        """Test listing categories (any authenticated user)."""
        # Create category as admin
        client.post(
            "/categories/",
            json={"name": "Feature Request"},
            headers=admin_headers
        )
        
        # List as user (should work)
        response = client.get("/categories/", headers=user_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_create_duplicate_category_fails(self, client: TestClient, admin_headers):
        """Test creating duplicate category fails."""
        # Create first
        client.post("/categories/", json={"name": "Duplicate"}, headers=admin_headers)
        
        # Try to create again
        response = client.post("/categories/", json={"name": "Duplicate"}, headers=admin_headers)
        assert response.status_code == 400


class TestTags:
    """Tests for tag operations."""

    def test_create_tag_as_admin(self, client: TestClient, admin_headers):
        """Test admin can create tag."""
        response = client.post(
            "/tags/",
            json={"name": "urgent"},
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == "urgent"

    def test_create_tag_as_user_forbidden(self, client: TestClient, user_headers):
        """Test regular user cannot create tag."""
        response = client.post(
            "/tags/",
            json={"name": "test-tag"},
            headers=user_headers
        )
        assert response.status_code == 403

    def test_list_tags(self, client: TestClient, admin_headers, user_headers):
        """Test listing tags (any authenticated user)."""
        # Create tag as admin
        client.post("/tags/", json={"name": "important"}, headers=admin_headers)
        
        # List as user (should work)
        response = client.get("/tags/", headers=user_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1
