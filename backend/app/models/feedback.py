from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base


class FeedbackStatus(str, enum.Enum):
    NEW = "new"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    # Use values_callable to ensure PostgreSQL gets lowercase values
    status = Column(
        Enum(FeedbackStatus, values_callable=lambda x: [e.value for e in x]),
        default=FeedbackStatus.NEW,
        nullable=False,
        index=True
    )
    sentiment_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="feedbacks")
    category = relationship("Category", back_populates="feedbacks")
    tags = relationship("Tag", secondary="feedback_tags", back_populates="feedbacks")
    status_events = relationship("StatusEvent", back_populates="feedback", cascade="all, delete-orphan")
    admin_responses = relationship("AdminResponse", back_populates="feedback", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Feedback(id={self.id}, title={self.title}, status={self.status})>"
