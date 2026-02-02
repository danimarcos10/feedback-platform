from fastapi import APIRouter, Query
from typing import Optional

from app.api.deps import DBSession, CurrentAdmin
from app.schemas.feedback import (
    FeedbackListResponse,
    FeedbackResponse,
    FeedbackDetailResponse,
    StatusUpdateRequest,
    CategoryUpdateRequest,
    TagsUpdateRequest,
    AdminResponseCreate,
    AdminResponseResponse,
)
from app.services.feedback_service import FeedbackService
from app.models.feedback import FeedbackStatus

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/feedback", response_model=FeedbackListResponse)
def get_all_feedback(
    db: DBSession,
    admin: CurrentAdmin,
    status: Optional[FeedbackStatus] = Query(None),
    category_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get all feedback (admin only)."""
    service = FeedbackService(db)
    return service.get_all_feedback(
        status=status,
        category_id=category_id,
        page=page,
        page_size=page_size
    )


@router.put("/feedback/{feedback_id}/status", response_model=FeedbackResponse)
def update_feedback_status(
    feedback_id: int,
    request: StatusUpdateRequest,
    db: DBSession,
    admin: CurrentAdmin
):
    """Update feedback status (admin only)."""
    service = FeedbackService(db)
    feedback = service.update_status(feedback_id, admin.id, request.status)
    return FeedbackResponse.model_validate(feedback)


@router.put("/feedback/{feedback_id}/category", response_model=FeedbackResponse)
def update_feedback_category(
    feedback_id: int,
    request: CategoryUpdateRequest,
    db: DBSession,
    admin: CurrentAdmin
):
    """Update feedback category (admin only)."""
    service = FeedbackService(db)
    feedback = service.update_category(feedback_id, request.category_id)
    return FeedbackResponse.model_validate(feedback)


@router.put("/feedback/{feedback_id}/tags", response_model=FeedbackResponse)
def update_feedback_tags(
    feedback_id: int,
    request: TagsUpdateRequest,
    db: DBSession,
    admin: CurrentAdmin
):
    """Update feedback tags (admin only)."""
    service = FeedbackService(db)
    feedback = service.update_tags(feedback_id, request.tag_ids)
    return FeedbackResponse.model_validate(feedback)


@router.post("/feedback/{feedback_id}/respond", response_model=AdminResponseResponse)
def respond_to_feedback(
    feedback_id: int,
    request: AdminResponseCreate,
    db: DBSession,
    admin: CurrentAdmin
):
    """Add admin response to feedback."""
    service = FeedbackService(db)
    response = service.add_admin_response(feedback_id, admin.id, request)
    return AdminResponseResponse.model_validate(response)
