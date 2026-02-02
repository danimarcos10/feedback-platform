"""
Shared test fixtures and configuration.
Run all tests with: pytest
Run with coverage: pytest --cov=app --cov-report=html
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Import all models to register them with Base
from app.models import feedback, category, tag, feedback_tag, status_event, admin_response


# Test database - in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create test database tables and return session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with fresh database."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin(db):
    """Create a test admin user."""
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def user_token(client, test_user):
    """Get auth token for test user."""
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client, test_admin):
    """Get auth token for test admin."""
    response = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture
def user_headers(user_token):
    """Get auth headers for test user."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token):
    """Get auth headers for test admin."""
    return {"Authorization": f"Bearer {admin_token}"}
