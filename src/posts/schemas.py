from pydantic import BaseModel
from typing import List

from src.tags.schemas import TagBase


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    category_id: int
    tags: List[int] = []


class PostBase(PostCreate):
    id: int
    tags: List[TagBase] = []
