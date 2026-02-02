from fastapi import APIRouter, Query

from app.api.deps import DBSession, CurrentAdmin
from app.schemas.analytics import (
    OverviewStats,
    TimeseriesResponse,
    TopTagsResponse,
    TopCategoriesResponse,
    SentimentTrendsResponse,
    TopicsResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=OverviewStats)
def get_overview(
    db: DBSession,
    admin: CurrentAdmin
):
    """Get overview statistics."""
    service = AnalyticsService(db)
    return service.get_overview()


@router.get("/timeseries", response_model=TimeseriesResponse)
def get_timeseries(
    db: DBSession,
    admin: CurrentAdmin,
    days: int = Query(30, ge=1, le=365)
):
    """Get feedback volume over time."""
    service = AnalyticsService(db)
    return service.get_timeseries(days=days)


@router.get("/top-tags", response_model=TopTagsResponse)
def get_top_tags(
    db: DBSession,
    admin: CurrentAdmin,
    limit: int = Query(10, ge=1, le=50)
):
    """Get top tags by feedback count."""
    service = AnalyticsService(db)
    return service.get_top_tags(limit=limit)


@router.get("/top-categories", response_model=TopCategoriesResponse)
def get_top_categories(
    db: DBSession,
    admin: CurrentAdmin,
    limit: int = Query(10, ge=1, le=50)
):
    """Get top categories by feedback count."""
    service = AnalyticsService(db)
    return service.get_top_categories(limit=limit)


@router.get("/sentiment-trends", response_model=SentimentTrendsResponse)
def get_sentiment_trends(
    db: DBSession,
    admin: CurrentAdmin,
    days: int = Query(30, ge=1, le=365)
):
    """Get sentiment score trends over time."""
    service = AnalyticsService(db)
    return service.get_sentiment_trends(days=days)


@router.get("/topics", response_model=TopicsResponse)
def get_topics(
    db: DBSession,
    admin: CurrentAdmin,
    k: int = Query(5, ge=2, le=20)
):
    """Get topic clusters from feedback content."""
    service = AnalyticsService(db)
    return service.get_topics(k=k)
