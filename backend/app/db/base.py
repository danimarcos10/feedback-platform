# Import Base from separate file to avoid circular imports
from app.db.base_class import Base

# Import all models here for Alembic to detect them
from app.models.user import User
from app.models.feedback import Feedback
from app.models.category import Category
from app.models.tag import Tag
from app.models.feedback_tag import FeedbackTag
from app.models.status_event import StatusEvent
from app.models.admin_response import AdminResponse

__all__ = [
    "Base",
    "User",
    "Feedback",
    "Category",
    "Tag",
    "FeedbackTag",
    "StatusEvent",
    "AdminResponse",
]
