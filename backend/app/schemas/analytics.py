from pydantic import BaseModel
from datetime import date


class OverviewStats(BaseModel):
    total_feedback: int
    open_feedback: int
    resolved_feedback: int
    average_resolution_time_hours: float | None


class TimeseriesPoint(BaseModel):
    date: date
    count: int


class TimeseriesResponse(BaseModel):
    data: list[TimeseriesPoint]


class TagCount(BaseModel):
    tag_id: int
    tag_name: str
    count: int


class TopTagsResponse(BaseModel):
    data: list[TagCount]


class CategoryCount(BaseModel):
    category_id: int
    category_name: str
    count: int


class TopCategoriesResponse(BaseModel):
    data: list[CategoryCount]


class SentimentPoint(BaseModel):
    date: date
    average_sentiment: float
    count: int


class SentimentTrendsResponse(BaseModel):
    data: list[SentimentPoint]


class TopicCluster(BaseModel):
    cluster_id: int
    label: str
    keywords: list[str]
    example_feedback_ids: list[int]
    example_titles: list[str]
    count: int


class TopicsResponse(BaseModel):
    clusters: list[TopicCluster]
