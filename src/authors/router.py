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
    """
    Get all authors.

    Parameters:
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        List[AuthorBase]: A list of `AuthorBase` objects representing all authors in the database.
    """
    return await get_authors(session)


@router.get("/{author_id}", response_model=AuthorBase)
async def get_author_by_id(author: Mapped = Depends(get_author)):
    """
    Get an author by their ID.

    Parameters:
        author_id (int): The ID of the author to retrieve.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        AuthorBase: The `AuthorBase` object with the given ID, or a 404 error if not found.
    """
    return author


@router.post("/", response_model=AuthorBase)
async def create_new_author(
    author: AuthorCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new author.

    Parameters:
        author (AuthorCreate): The author data to be created.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        AuthorBase: The newly created `AuthorBase` object.
    """
    return await create_author(author, session)


@router.put("/{author_id}", response_model=AuthorBase)
async def update_author_by_id(
    author_data: AuthorCreate,
    author: Mapped = Depends(get_author),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an author.

    Parameters:
        author_data (AuthorCreate): The updated author data.
        author (Author, optional): The `Author` object to be updated.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        AuthorBase: The updated `AuthorBase` object.
    """
    return await update_author(author, author_data, session)


@router.delete("/{author_id}")
async def delete_author_by_id(
    author: Mapped = Depends(get_author),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete an author.

    Parameters:
        author (Author, optional): The `Author` object to be deleted.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the author was deleted.
    """
    return await delete_author(author, session)
