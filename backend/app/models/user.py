from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # Use values_callable to ensure PostgreSQL gets lowercase values
    role = Column(
        Enum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.USER,
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    feedbacks = relationship("Feedback", back_populates="user")
    status_events = relationship("StatusEvent", back_populates="changed_by_user")
    admin_responses = relationship("AdminResponse", back_populates="admin")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
