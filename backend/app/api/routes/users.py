from fastapi import APIRouter
from app.api.deps import DBSession, CurrentUser, CurrentAdmin
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: DBSession,
    admin: CurrentAdmin,
    skip: int = 0,
    limit: int = 100
):
    """List all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.model_validate(u) for u in users]
