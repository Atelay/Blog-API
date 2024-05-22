from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    email: str


class AuthorBase(AuthorCreate):
    id: int
