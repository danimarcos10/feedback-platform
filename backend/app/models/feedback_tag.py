from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base


class FeedbackTag(Base):
    """Many-to-many relationship between Feedback and Tag."""
    __tablename__ = "feedback_tags"

    feedback_id = Column(Integer, ForeignKey("feedback.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
