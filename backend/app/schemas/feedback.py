from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.feedback import FeedbackStatus
from .category import CategoryResponse
from .tag import TagResponse
from .user import UserResponse


class FeedbackBase(BaseModel):
    title: str
    content: str


class FeedbackCreate(FeedbackBase):
    category_id: int | None = None
    tag_ids: list[int] = []


class FeedbackUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    category_id: int | None
    status: FeedbackStatus
    sentiment_score: float | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
    category: CategoryResponse | None = None
    tags: list[TagResponse] = []

    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    items: list[FeedbackResponse]
    total: int
    page: int
    page_size: int


class StatusUpdateRequest(BaseModel):
    status: FeedbackStatus


class CategoryUpdateRequest(BaseModel):
    category_id: int


class TagsUpdateRequest(BaseModel):
    tag_ids: list[int]


class AdminResponseCreate(BaseModel):
    message: str


class AdminResponseResponse(BaseModel):
    id: int
    feedback_id: int
    admin_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatusEventResponse(BaseModel):
    id: int
    feedback_id: int
    old_status: str | None
    new_status: str
    changed_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackDetailResponse(FeedbackResponse):
    """Feedback with admin responses and status history."""
    admin_responses: list[AdminResponseResponse] = []
    status_events: list[StatusEventResponse] = []
