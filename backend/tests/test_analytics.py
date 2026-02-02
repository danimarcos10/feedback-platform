"""Tests for analytics endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestAnalytics:
    """Tests for analytics endpoints (admin only)."""

    def test_get_overview_as_admin(self, client: TestClient, admin_headers, user_headers):
        """Test admin can access analytics overview."""
        # Create some feedback first
        client.post(
            "/feedback/",
            json={"title": "Test 1", "content": "Content 1"},
            headers=user_headers
        )
        client.post(
            "/feedback/",
            json={"title": "Test 2", "content": "Content 2"},
            headers=user_headers
        )
        
        response = client.get("/analytics/overview", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_feedback" in data
        assert "open_feedback" in data
        assert "resolved_feedback" in data
        assert data["total_feedback"] >= 2

    def test_get_overview_as_user_forbidden(self, client: TestClient, user_headers):
        """Test regular user cannot access analytics."""
        response = client.get("/analytics/overview", headers=user_headers)
        assert response.status_code == 403

    def test_get_timeseries(self, client: TestClient, admin_headers, user_headers):
        """Test getting feedback volume timeseries."""
        # Create feedback
        client.post(
            "/feedback/",
            json={"title": "Timeseries Test", "content": "Content"},
            headers=user_headers
        )
        
        response = client.get("/analytics/timeseries?days=7", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 8  # 7 days + today

    def test_get_top_tags(self, client: TestClient, admin_headers):
        """Test getting top tags."""
        response = client.get("/analytics/top-tags?limit=5", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    def test_get_top_categories(self, client: TestClient, admin_headers):
        """Test getting top categories."""
        response = client.get("/analytics/top-categories?limit=5", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    def test_get_sentiment_trends(self, client: TestClient, admin_headers, user_headers):
        """Test getting sentiment trends."""
        # Create feedback with different sentiments
        client.post(
            "/feedback/",
            json={"title": "Great feature!", "content": "I love this feature, it's amazing!"},
            headers=user_headers
        )
        client.post(
            "/feedback/",
            json={"title": "Terrible bug", "content": "This is awful and broken."},
            headers=user_headers
        )
        
        response = client.get("/analytics/sentiment-trends?days=7", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    def test_get_topics_insufficient_data(self, client: TestClient, admin_headers):
        """Test topics endpoint with insufficient data returns empty."""
        response = client.get("/analytics/topics?k=3", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "clusters" in data
