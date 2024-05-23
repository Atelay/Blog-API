from pydantic import BaseModel, Field
from typing import List, Optional

from src.tags.schemas import TagBase


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: Optional[int] = Field(None)
    category_id: Optional[int] = Field(None)
    tags: List[int] = []


class PostBase(PostCreate):
    id: int
    tags: List[TagBase] = []
