import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, LoginRequest
from app.schemas.user import UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, request: RegisterRequest) -> UserResponse:
        """Register a new user."""
        logger.info(f"Registration attempt for email: {request.email}")
        
        try:
            # Check if user exists
            existing_user = self.db.query(User).filter(User.email == request.email).first()
            if existing_user:
                logger.warning(f"Registration failed - email already exists: {request.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Create user
            user = User(
                email=request.email,
                hashed_password=get_password_hash(request.password),
                role=UserRole.USER
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User registered successfully: {request.email} (ID: {user.id})")
            return UserResponse.model_validate(user)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Registration error for {request.email}: {e}", exc_info=True)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )

    def login(self, request: LoginRequest) -> dict:
        """Authenticate user and return token."""
        user = self.db.query(User).filter(User.email == request.email).first()
        
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def create_admin(self, email: str, password: str) -> User:
        """Create an admin user (for initial setup)."""
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
