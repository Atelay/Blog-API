from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.database import get_async_session
from .service import (
    delete_author,
    get_author,
    create_author,
    update_author,
    get_authors,
)
from .schemas import AuthorBase, AuthorCreate


router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[AuthorBase])
async def get_all_authors(session: AsyncSession = Depends(get_async_session)):
    return await get_authors(session)


@router.get("/{author_id}", response_model=AuthorBase)
async def get_author_by_id(author: Mapped = Depends(get_author)):
    return author


@router.post("/", response_model=AuthorBase)
async def create_new_author(
    author: AuthorCreate, session: AsyncSession = Depends(get_async_session)
):
    return await create_author(author, session)


@router.put("/{author_id}", response_model=AuthorBase)
async def update_author_by_id(
    author_data: AuthorCreate,
    author: Mapped = Depends(get_author),
    session: AsyncSession = Depends(get_async_session),
):
    return await update_author(author, author_data, session)


@router.delete("/{author_id}")
async def delete_author_by_id(
    author: Mapped = Depends(get_author),
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_author(author, session)
