from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.models.feedback import Feedback, FeedbackStatus
from app.models.tag import Tag
from app.models.category import Category
from app.models.status_event import StatusEvent
from app.models.admin_response import AdminResponse
from app.models.user import User, UserRole
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    FeedbackListResponse,
    StatusUpdateRequest,
    AdminResponseCreate,
)

# Custom lexicon for product feedback sentiment analysis
CUSTOM_LEXICON = {
    # Strong negative words
    "terrible": -3.5,
    "awful": -3.5,
    "unusable": -3.8,
    "broken": -3.0,
    "buggy": -2.5,
    "confusing": -2.7,
    "clunky": -2.3,
    "frustrating": -2.5,
    "horrible": -3.5,
    "worst": -3.5,
    "hate": -3.0,
    "painful": -2.5,
    "unreliable": -2.5,
    # Positive words
    "intuitive": 2.4,
    "smooth": 2.2,
    "clean": 1.8,
    "amazing": 3.2,
    "great": 2.5,
    "excellent": 3.0,
    "fantastic": 3.2,
    "perfect": 3.5,
    "love": 3.0,
    "best": 2.8,
    "beautiful": 2.5,
    "helpful": 2.0,
    "responsive": 2.0,
    "fast": 1.8,
}

# Keywords for forced sentiment override
STRONG_NEGATIVE_KEYWORDS = {"terrible", "awful", "unusable", "hate", "broken", "worst", "horrible"}
STRONG_POSITIVE_KEYWORDS = {"amazing", "love", "perfect", "excellent", "fantastic", "great", "best"}


class FeedbackService:
    def __init__(self, db: Session):
        self.db = db
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        # Add custom lexicon to VADER
        self.sentiment_analyzer.lexicon.update(CUSTOM_LEXICON)

    def _calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score using VADER with custom lexicon."""
        scores = self.sentiment_analyzer.polarity_scores(text)
        return scores['compound']  # Returns -1 to 1

    def _get_sentiment_label(self, score: float, text: str) -> str:
        """
        Get sentiment label from score with keyword override.
        Uses improved thresholds for product feedback.
        """
        text_lower = text.lower()
        
        # Strong keyword overrides - if text contains these, force the label
        if any(word in text_lower for word in STRONG_NEGATIVE_KEYWORDS):
            return "negative"
        if any(word in text_lower for word in STRONG_POSITIVE_KEYWORDS):
            return "positive"
        
        # Use improved thresholds (wider neutral band than default VADER)
        if score <= -0.20:
            return "negative"
        elif score >= 0.20:
            return "positive"
        else:
            return "neutral"

    def _analyze_sentiment(self, text: str) -> tuple[float, str]:
        """Analyze sentiment and return both score and label."""
        score = self._calculate_sentiment(text)
        label = self._get_sentiment_label(score, text)
        return score, label

    def create_feedback(self, user_id: int, request: FeedbackCreate) -> Feedback:
        """Create new feedback."""
        # Calculate sentiment with both score and label
        combined_text = f"{request.title} {request.content}"
        sentiment_score, sentiment_label = self._analyze_sentiment(combined_text)
        
        feedback = Feedback(
            user_id=user_id,
            title=request.title,
            content=request.content,
            category_id=request.category_id,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            status=FeedbackStatus.NEW
        )
        
        # Add tags if provided
        if request.tag_ids:
            tags = self.db.query(Tag).filter(Tag.id.in_(request.tag_ids)).all()
            feedback.tags = tags
        
        self.db.add(feedback)
        
        # Create initial status event
        status_event = StatusEvent(
            feedback=feedback,
            old_status=None,
            new_status=FeedbackStatus.NEW.value,
            changed_by=user_id
        )
        self.db.add(status_event)
        
        self.db.commit()
        self.db.refresh(feedback)
        
        return feedback

    def get_feedback_by_id(self, feedback_id: int) -> Feedback | None:
        """Get feedback by ID with relationships loaded."""
        return (
            self.db.query(Feedback)
            .options(
                joinedload(Feedback.category),
                joinedload(Feedback.tags),
                joinedload(Feedback.admin_responses),
                joinedload(Feedback.status_events)
            )
            .filter(Feedback.id == feedback_id)
            .first()
        )

    def get_user_feedback(
        self,
        user_id: int,
        status: FeedbackStatus | None = None,
        page: int = 1,
        page_size: int = 20
    ) -> FeedbackListResponse:
        """Get feedback for a specific user."""
        query = self.db.query(Feedback).filter(Feedback.user_id == user_id)
        
        if status:
            query = query.filter(Feedback.status == status)
        
        total = query.count()
        
        items = (
            query
            .options(joinedload(Feedback.category), joinedload(Feedback.tags))
            .order_by(Feedback.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        
        return FeedbackListResponse(
            items=[FeedbackResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size
        )

    def get_all_feedback(
        self,
        status: FeedbackStatus | None = None,
        category_id: int | None = None,
        page: int = 1,
        page_size: int = 20
    ) -> FeedbackListResponse:
        """Get all feedback (admin only)."""
        query = self.db.query(Feedback)
        
        if status:
            query = query.filter(Feedback.status == status)
        if category_id:
            query = query.filter(Feedback.category_id == category_id)
        
        total = query.count()
        
        items = (
            query
            .options(joinedload(Feedback.category), joinedload(Feedback.tags))
            .order_by(Feedback.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        
        return FeedbackListResponse(
            items=[FeedbackResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size
        )

    def update_feedback(
        self,
        feedback_id: int,
        user_id: int,
        request: FeedbackUpdate
    ) -> Feedback:
        """Update feedback (owner only, if not resolved)."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        if feedback.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this feedback"
            )
        
        if feedback.status == FeedbackStatus.RESOLVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot edit resolved feedback"
            )
        
        if request.title:
            feedback.title = request.title
        if request.content:
            feedback.content = request.content
        
        # Recalculate sentiment (both score and label) when text changes
        combined_text = f"{feedback.title} {feedback.content}"
        feedback.sentiment_score, feedback.sentiment_label = self._analyze_sentiment(combined_text)
        
        self.db.commit()
        self.db.refresh(feedback)
        
        return feedback

    def delete_feedback(self, feedback_id: int, user_id: int) -> None:
        """Delete feedback (owner only, if not resolved)."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        if feedback.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this feedback"
            )
        
        if feedback.status == FeedbackStatus.RESOLVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete resolved feedback"
            )
        
        self.db.delete(feedback)
        self.db.commit()

    def update_status(
        self,
        feedback_id: int,
        admin_id: int,
        new_status: FeedbackStatus
    ) -> Feedback:
        """Update feedback status (admin only)."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        old_status = feedback.status
        feedback.status = new_status
        
        if new_status == FeedbackStatus.RESOLVED:
            feedback.resolved_at = datetime.utcnow()
        
        # Create status event
        status_event = StatusEvent(
            feedback_id=feedback_id,
            old_status=old_status.value,
            new_status=new_status.value,
            changed_by=admin_id
        )
        self.db.add(status_event)
        
        self.db.commit()
        self.db.refresh(feedback)
        
        return feedback

    def update_category(
        self,
        feedback_id: int,
        category_id: int
    ) -> Feedback:
        """Update feedback category (admin only)."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        feedback.category_id = category_id
        self.db.commit()
        self.db.refresh(feedback)
        
        return feedback

    def update_tags(
        self,
        feedback_id: int,
        tag_ids: list[int]
    ) -> Feedback:
        """Update feedback tags (admin only)."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        tags = self.db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        feedback.tags = tags
        
        self.db.commit()
        self.db.refresh(feedback)
        
        return feedback

    def add_admin_response(
        self,
        feedback_id: int,
        admin_id: int,
        request: AdminResponseCreate
    ) -> AdminResponse:
        """Add admin response to feedback."""
        feedback = self.get_feedback_by_id(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        admin_response = AdminResponse(
            feedback_id=feedback_id,
            admin_id=admin_id,
            message=request.message
        )
        
        self.db.add(admin_response)
        self.db.commit()
        self.db.refresh(admin_response)
        
        return admin_response
