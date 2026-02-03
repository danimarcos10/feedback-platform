"""
High-signal integration tests that validate real-world behavior.
These tests prove the features claimed in the README actually work.
"""
import pytest
from fastapi.testclient import TestClient

from app.models.status_event import StatusEvent
from app.models.user import User, UserRole
from app.core.security import get_password_hash


class TestPermissions:
    """Test that users cannot access other users' feedback."""

    def test_user_cannot_access_other_users_feedback(self, client: TestClient, db, user_headers):
        """
        User A creates feedback, User B tries to GET it → 403
        
        This validates the ownership/permission system works correctly.
        """
        # User A (test_user via user_headers) creates feedback
        create_response = client.post(
            "/feedback/",
            json={"title": "User A's Private Feedback", "content": "This belongs to User A"},
            headers=user_headers
        )
        assert create_response.status_code == 200
        feedback_id = create_response.json()["id"]
        
        # Create User B
        user_b = User(
            email="userb@example.com",
            hashed_password=get_password_hash("userb_password"),
            role=UserRole.USER
        )
        db.add(user_b)
        db.commit()
        
        # Login as User B
        login_response = client.post(
            "/auth/login",
            data={"username": "userb@example.com", "password": "userb_password"}
        )
        assert login_response.status_code == 200
        user_b_token = login_response.json()["access_token"]
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}
        
        # User B tries to access User A's feedback → should be 403 Forbidden
        get_response = client.get(f"/feedback/{feedback_id}", headers=user_b_headers)
        assert get_response.status_code == 403, (
            f"Expected 403 Forbidden when User B accesses User A's feedback, "
            f"got {get_response.status_code}: {get_response.json()}"
        )


class TestAdminAuditTrail:
    """Test that admin actions create proper audit trails."""

    def test_status_change_creates_audit_event(self, client: TestClient, db, admin_headers, user_headers):
        """
        Admin updates status → status_events table has entry with correct old/new status.
        
        This validates the audit trail system for compliance/tracking.
        """
        # User creates feedback (starts with status "new")
        create_response = client.post(
            "/feedback/",
            json={"title": "Audit Trail Test", "content": "Testing audit functionality"},
            headers=user_headers
        )
        assert create_response.status_code == 200
        feedback_id = create_response.json()["id"]
        initial_status = create_response.json()["status"]
        assert initial_status == "new"
        
        # Admin updates status to "in_progress"
        update_response = client.put(
            f"/admin/feedback/{feedback_id}/status",
            json={"status": "in_progress"},
            headers=admin_headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "in_progress"
        
        # Query status_events table directly - should have exactly 1 entry
        status_events = db.query(StatusEvent).filter(
            StatusEvent.feedback_id == feedback_id
        ).all()
        
        assert len(status_events) == 1, (
            f"Expected exactly 1 status event, found {len(status_events)}"
        )
        
        event = status_events[0]
        assert event.old_status == "new", f"Expected old_status='new', got '{event.old_status}'"
        assert event.new_status == "in_progress", f"Expected new_status='in_progress', got '{event.new_status}'"
        assert event.changed_by is not None, "changed_by should be set to admin user ID"


class TestSentimentAnalysis:
    """Test that sentiment analysis correctly identifies negative/positive feedback."""

    def test_negative_feedback_detected(self, client: TestClient, user_headers):
        """
        Create feedback with "UI is terrible" → sentiment_label == "negative"
        
        This validates the sentiment analysis feature claimed in README.
        """
        # Create feedback with clearly negative content
        response = client.post(
            "/feedback/",
            json={
                "title": "UI is terrible",
                "content": "The user interface is absolutely terrible and frustrating to use."
            },
            headers=user_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify sentiment is detected as negative
        assert "sentiment_label" in data, "Response should include sentiment_label"
        assert data["sentiment_label"] == "negative", (
            f"Expected sentiment_label='negative' for 'UI is terrible', "
            f"got '{data['sentiment_label']}' (score: {data.get('sentiment_score')})"
        )
        
        # Also verify sentiment_score is negative
        assert "sentiment_score" in data, "Response should include sentiment_score"
        assert data["sentiment_score"] < 0, (
            f"Expected negative sentiment_score, got {data['sentiment_score']}"
        )

    def test_positive_feedback_detected(self, client: TestClient, user_headers):
        """
        Create feedback with positive content → sentiment_label == "positive"
        
        Additional validation that sentiment works both ways.
        """
        response = client.post(
            "/feedback/",
            json={
                "title": "Amazing feature",
                "content": "This feature is excellent and works beautifully. Love it!"
            },
            headers=user_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data["sentiment_label"] == "positive", (
            f"Expected sentiment_label='positive' for positive feedback, "
            f"got '{data['sentiment_label']}' (score: {data.get('sentiment_score')})"
        )
        assert data["sentiment_score"] > 0, (
            f"Expected positive sentiment_score, got {data['sentiment_score']}"
        )
