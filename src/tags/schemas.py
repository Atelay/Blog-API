from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str


class TagBase(TagCreate):
    id: int
