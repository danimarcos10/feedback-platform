"""Tests for feedback endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestUserFeedback:
    """Tests for user feedback operations."""

    def test_create_feedback_success(self, client: TestClient, user_headers):
        """Test creating feedback as authenticated user."""
        response = client.post(
            "/feedback/",
            json={
                "title": "Test Feedback",
                "content": "This is a test feedback content."
            },
            headers=user_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Feedback"
        assert data["status"] == "new"
        assert "sentiment_score" in data

    def test_create_feedback_unauthenticated(self, client: TestClient):
        """Test creating feedback without auth fails."""
        response = client.post(
            "/feedback/",
            json={"title": "Test", "content": "Content"}
        )
        assert response.status_code == 401

    def test_get_my_feedback(self, client: TestClient, user_headers):
        """Test getting user's own feedback list."""
        # Create feedback first
        client.post(
            "/feedback/",
            json={"title": "My Feedback", "content": "My content"},
            headers=user_headers
        )
        
        response = client.get("/feedback/mine", headers=user_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) >= 1

    def test_get_feedback_by_id(self, client: TestClient, user_headers):
        """Test getting specific feedback by ID."""
        # Create feedback
        create_response = client.post(
            "/feedback/",
            json={"title": "Specific Feedback", "content": "Content"},
            headers=user_headers
        )
        feedback_id = create_response.json()["id"]
        
        response = client.get(f"/feedback/{feedback_id}", headers=user_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Specific Feedback"

    def test_update_feedback(self, client: TestClient, user_headers):
        """Test updating own feedback."""
        # Create feedback
        create_response = client.post(
            "/feedback/",
            json={"title": "Original Title", "content": "Original content"},
            headers=user_headers
        )
        feedback_id = create_response.json()["id"]
        
        # Update
        response = client.put(
            f"/feedback/{feedback_id}",
            json={"title": "Updated Title"},
            headers=user_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    def test_delete_feedback(self, client: TestClient, user_headers):
        """Test deleting own feedback."""
        # Create feedback
        create_response = client.post(
            "/feedback/",
            json={"title": "To Delete", "content": "Content"},
            headers=user_headers
        )
        feedback_id = create_response.json()["id"]
        
        # Delete
        response = client.delete(f"/feedback/{feedback_id}", headers=user_headers)
        assert response.status_code == 200
        
        # Verify deleted
        get_response = client.get(f"/feedback/{feedback_id}", headers=user_headers)
        assert get_response.status_code == 404


class TestAdminFeedback:
    """Tests for admin feedback operations."""

    def test_get_all_feedback_as_admin(self, client: TestClient, admin_headers, user_headers):
        """Test admin can get all feedback."""
        # Create feedback as user
        client.post(
            "/feedback/",
            json={"title": "User Feedback", "content": "Content"},
            headers=user_headers
        )
        
        # Get all as admin
        response = client.get("/admin/feedback", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1

    def test_get_all_feedback_as_user_forbidden(self, client: TestClient, user_headers):
        """Test regular user cannot access admin endpoint."""
        response = client.get("/admin/feedback", headers=user_headers)
        assert response.status_code == 403

    def test_update_status(self, client: TestClient, admin_headers, user_headers):
        """Test admin can update feedback status."""
        # Create feedback as user
        create_response = client.post(
            "/feedback/",
            json={"title": "Status Test", "content": "Content"},
            headers=user_headers
        )
        feedback_id = create_response.json()["id"]
        
        # Update status as admin
        response = client.put(
            f"/admin/feedback/{feedback_id}/status",
            json={"status": "in_progress"},
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_respond_to_feedback(self, client: TestClient, admin_headers, user_headers):
        """Test admin can respond to feedback."""
        # Create feedback as user
        create_response = client.post(
            "/feedback/",
            json={"title": "Response Test", "content": "Content"},
            headers=user_headers
        )
        feedback_id = create_response.json()["id"]
        
        # Respond as admin
        response = client.post(
            f"/admin/feedback/{feedback_id}/respond",
            json={"message": "Thank you for your feedback!"},
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Thank you for your feedback!"
