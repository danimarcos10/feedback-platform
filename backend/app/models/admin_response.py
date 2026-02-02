from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class AdminResponse(Base):
    """Admin responses/notes on feedback."""
    __tablename__ = "admin_responses"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    feedback = relationship("Feedback", back_populates="admin_responses")
    admin = relationship("User", back_populates="admin_responses")

    def __repr__(self):
        return f"<AdminResponse(id={self.id}, feedback_id={self.feedback_id})>"
