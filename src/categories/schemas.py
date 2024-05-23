from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryBase(CategoryCreate):
    id: int
