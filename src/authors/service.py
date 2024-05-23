from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.authors.models import Author
from src.authors.schemas import AuthorCreate
from src.database import get_async_session


async def get_authors(
    session: AsyncSession = Depends(get_async_session),
) -> List[Author]:
    """Get all authors.

    Parameters:
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        List[Author]: A list of `Author` objects representing all authors in the database.
    """
    result = await session.execute(select(Author))
    authors: List[Author] = result.scalars().all()
    return authors


async def get_author(
    author_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Author:
    """Get an author by their ID.

    Parameters:
        author_id (int): The ID of the author to retrieve.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Author: The `Author` object with the given ID, or a 404 error if not found.
    """
    query = select(Author).where(Author.id == author_id)
    result = await session.execute(query)
    response: Author = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="Author not found")
    return response


async def create_author(author_data: AuthorCreate, session: AsyncSession) -> Author:
    """Create a new author.

    Parameters:
        author_data (AuthorCreate): The author data to be created.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Author: The newly created `Author` object.
    """
    try:
        db_author = Author(**author_data.model_dump())
        session.add(db_author)
        await session.commit()
        await session.refresh(db_author)
        return db_author
    except IntegrityError as exc:
        raise HTTPException(
            status_code=400, detail=f"Author creation failed: {str(exc)}"
        )


async def update_author(
    author: Author, author_data: AuthorCreate, session: AsyncSession
) -> Author:
    """Update an author.

    Parameters:
        author (Author): The `Author` object to be updated.
        author_data (AuthorCreate): The updated author data.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Author: The updated `Author` object.
    """
    try:
        query = (
            update(Author)
            .where(Author.id == author.id)
            .values(**author_data.model_dump())
            .returning(Author)
        )
        result = await session.execute(query)
        await session.commit()
        response: Author = result.scalars().first()
        return response
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Author update failed: {str(exc)}")


async def delete_author(author: Author, session: AsyncSession) -> str:
    """Delete an author.

    Parameters:
        author (Author): The `Author` object to be deleted.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the author was deleted.
    """
    try:
        query = delete(Author).where(Author.id == author.id)
        await session.execute(query)
        await session.commit()
        return f"Author with id {author.id} was deleted"
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Author deletion failed: {str(exc)}"
        )
