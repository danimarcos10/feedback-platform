from fastapi import APIRouter, Query
from typing import Optional

from app.api.deps import DBSession, CurrentUser
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    FeedbackListResponse,
    FeedbackDetailResponse,
)
from app.services.feedback_service import FeedbackService
from app.models.feedback import FeedbackStatus

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse)
def create_feedback(
    request: FeedbackCreate,
    db: DBSession,
    current_user: CurrentUser
):
    """Create new feedback."""
    service = FeedbackService(db)
    feedback = service.create_feedback(current_user.id, request)
    return FeedbackResponse.model_validate(feedback)


@router.get("/mine", response_model=FeedbackListResponse)
def get_my_feedback(
    db: DBSession,
    current_user: CurrentUser,
    status: Optional[FeedbackStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get current user's feedback list."""
    service = FeedbackService(db)
    return service.get_user_feedback(
        user_id=current_user.id,
        status=status,
        page=page,
        page_size=page_size
    )


@router.get("/{feedback_id}", response_model=FeedbackDetailResponse)
def get_feedback(
    feedback_id: int,
    db: DBSession,
    current_user: CurrentUser
):
    """Get feedback by ID (owner or admin only)."""
    service = FeedbackService(db)
    feedback = service.get_feedback_by_id(feedback_id)
    
    if not feedback:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Check authorization
    from app.models.user import UserRole
    if feedback.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this feedback"
        )
    
    return FeedbackDetailResponse.model_validate(feedback)


@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    feedback_id: int,
    request: FeedbackUpdate,
    db: DBSession,
    current_user: CurrentUser
):
    """Update feedback (owner only, if not resolved)."""
    service = FeedbackService(db)
    feedback = service.update_feedback(feedback_id, current_user.id, request)
    return FeedbackResponse.model_validate(feedback)


@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: DBSession,
    current_user: CurrentUser
):
    """Delete feedback (owner only, if not resolved)."""
    service = FeedbackService(db)
    service.delete_feedback(feedback_id, current_user.id)
    return {"message": "Feedback deleted successfully"}
