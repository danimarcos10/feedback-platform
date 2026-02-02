from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta, date
from typing import Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from app.models.feedback import Feedback, FeedbackStatus
from app.models.tag import Tag
from app.models.category import Category
from app.models.feedback_tag import FeedbackTag
from app.schemas.analytics import (
    OverviewStats,
    TimeseriesResponse,
    TimeseriesPoint,
    TopTagsResponse,
    TagCount,
    TopCategoriesResponse,
    CategoryCount,
    SentimentTrendsResponse,
    SentimentPoint,
    TopicsResponse,
    TopicCluster,
)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self) -> OverviewStats:
        """Get overview statistics."""
        total = self.db.query(func.count(Feedback.id)).scalar() or 0
        
        open_statuses = [FeedbackStatus.NEW, FeedbackStatus.TRIAGED, FeedbackStatus.IN_PROGRESS]
        open_count = (
            self.db.query(func.count(Feedback.id))
            .filter(Feedback.status.in_(open_statuses))
            .scalar() or 0
        )
        
        resolved_count = (
            self.db.query(func.count(Feedback.id))
            .filter(Feedback.status == FeedbackStatus.RESOLVED)
            .scalar() or 0
        )
        
        # Calculate average resolution time
        avg_resolution_time = None
        resolved_feedback = (
            self.db.query(Feedback)
            .filter(
                Feedback.status == FeedbackStatus.RESOLVED,
                Feedback.resolved_at.isnot(None)
            )
            .all()
        )
        
        if resolved_feedback:
            total_hours = sum(
                (f.resolved_at - f.created_at).total_seconds() / 3600
                for f in resolved_feedback
                if f.resolved_at and f.created_at
            )
            avg_resolution_time = total_hours / len(resolved_feedback)
        
        return OverviewStats(
            total_feedback=total,
            open_feedback=open_count,
            resolved_feedback=resolved_count,
            average_resolution_time_hours=avg_resolution_time
        )

    def get_timeseries(self, days: int = 30) -> TimeseriesResponse:
        """Get feedback volume over time."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = (
            self.db.query(
                func.date(Feedback.created_at).label('date'),
                func.count(Feedback.id).label('count')
            )
            .filter(Feedback.created_at >= start_date)
            .group_by(func.date(Feedback.created_at))
            .order_by(func.date(Feedback.created_at))
            .all()
        )
        
        # Fill in missing dates with zero counts
        date_counts = {r.date: r.count for r in results}
        data = []
        current_date = start_date.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            data.append(TimeseriesPoint(
                date=current_date,
                count=date_counts.get(current_date, 0)
            ))
            current_date += timedelta(days=1)
        
        return TimeseriesResponse(data=data)

    def get_top_tags(self, limit: int = 10) -> TopTagsResponse:
        """Get top tags by feedback count."""
        results = (
            self.db.query(
                Tag.id,
                Tag.name,
                func.count(FeedbackTag.feedback_id).label('count')
            )
            .join(FeedbackTag, Tag.id == FeedbackTag.tag_id)
            .group_by(Tag.id, Tag.name)
            .order_by(func.count(FeedbackTag.feedback_id).desc())
            .limit(limit)
            .all()
        )
        
        return TopTagsResponse(
            data=[
                TagCount(tag_id=r.id, tag_name=r.name, count=r.count)
                for r in results
            ]
        )

    def get_top_categories(self, limit: int = 10) -> TopCategoriesResponse:
        """Get top categories by feedback count."""
        results = (
            self.db.query(
                Category.id,
                Category.name,
                func.count(Feedback.id).label('count')
            )
            .join(Feedback, Category.id == Feedback.category_id)
            .group_by(Category.id, Category.name)
            .order_by(func.count(Feedback.id).desc())
            .limit(limit)
            .all()
        )
        
        return TopCategoriesResponse(
            data=[
                CategoryCount(category_id=r.id, category_name=r.name, count=r.count)
                for r in results
            ]
        )

    def get_sentiment_trends(self, days: int = 30) -> SentimentTrendsResponse:
        """Get sentiment score trends over time."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = (
            self.db.query(
                func.date(Feedback.created_at).label('date'),
                func.avg(Feedback.sentiment_score).label('avg_sentiment'),
                func.count(Feedback.id).label('count')
            )
            .filter(
                Feedback.created_at >= start_date,
                Feedback.sentiment_score.isnot(None)
            )
            .group_by(func.date(Feedback.created_at))
            .order_by(func.date(Feedback.created_at))
            .all()
        )
        
        return SentimentTrendsResponse(
            data=[
                SentimentPoint(
                    date=r.date,
                    average_sentiment=round(r.avg_sentiment, 3) if r.avg_sentiment else 0,
                    count=r.count
                )
                for r in results
            ]
        )

    def get_topics(self, k: int = 5) -> TopicsResponse:
        """Cluster feedback into topics using TF-IDF and KMeans."""
        # Get all feedback with content
        feedbacks = (
            self.db.query(Feedback)
            .filter(Feedback.content.isnot(None))
            .all()
        )
        
        if len(feedbacks) < k:
            # Not enough feedback to cluster
            return TopicsResponse(clusters=[])
        
        # Prepare text data
        texts = [f"{f.title} {f.content}" for f in feedbacks]
        feedback_ids = [f.id for f in feedbacks]
        feedback_titles = [f.title for f in feedbacks]
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
        except ValueError:
            # Not enough documents or vocabulary
            return TopicsResponse(clusters=[])
        
        # KMeans clustering
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Get feature names for keywords
        feature_names = vectorizer.get_feature_names_out()
        
        # Build cluster information
        clusters = []
        for cluster_id in range(k):
            # Get indices of feedback in this cluster
            cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
            
            if not cluster_indices:
                continue
            
            # Get top keywords for this cluster
            cluster_center = kmeans.cluster_centers_[cluster_id]
            top_keyword_indices = cluster_center.argsort()[-5:][::-1]
            keywords = [feature_names[i] for i in top_keyword_indices]
            
            # Get example feedback
            example_indices = cluster_indices[:3]  # Top 3 examples
            example_ids = [feedback_ids[i] for i in example_indices]
            example_titles_list = [feedback_titles[i] for i in example_indices]
            
            # Generate label from top keywords
            label = ", ".join(keywords[:3])
            
            clusters.append(TopicCluster(
                cluster_id=cluster_id,
                label=label,
                keywords=keywords,
                example_feedback_ids=example_ids,
                example_titles=example_titles_list,
                count=len(cluster_indices)
            ))
        
        # Sort by count descending
        clusters.sort(key=lambda x: x.count, reverse=True)
        
        return TopicsResponse(clusters=clusters)
