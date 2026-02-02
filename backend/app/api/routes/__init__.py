from .auth import router as auth_router
from .users import router as users_router
from .feedback import router as feedback_router
from .admin import router as admin_router
from .analytics import router as analytics_router
from .categories import router as categories_router
from .tags import router as tags_router

__all__ = [
    "auth_router",
    "users_router",
    "feedback_router",
    "admin_router",
    "analytics_router",
    "categories_router",
    "tags_router",
]
