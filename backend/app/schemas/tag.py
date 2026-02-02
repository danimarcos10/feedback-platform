from pydantic import BaseModel
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None


class TagResponse(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
