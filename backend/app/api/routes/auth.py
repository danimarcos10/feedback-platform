from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.api.deps import DBSession, CurrentUser
from app.schemas.auth import Token, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    db: DBSession
):
    """Register a new user."""
    auth_service = AuthService(db)
    return auth_service.register(request)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession
):
    """Login and get access token."""
    from app.schemas.auth import LoginRequest
    auth_service = AuthService(db)
    request = LoginRequest(email=form_data.username, password=form_data.password)
    return auth_service.login(request)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser):
    """Get current user information."""
    return UserResponse.model_validate(current_user)
