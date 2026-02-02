from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class StatusEvent(Base):
    """Audit trail for feedback status changes."""
    __tablename__ = "status_events"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id", ondelete="CASCADE"), nullable=False, index=True)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    feedback = relationship("Feedback", back_populates="status_events")
    changed_by_user = relationship("User", back_populates="status_events")

    def __repr__(self):
        return f"<StatusEvent(id={self.id}, feedback_id={self.feedback_id}, {self.old_status} -> {self.new_status})>"
