from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.authors.models import Author
from src.authors.schemas import AuthorCreate
from src.database import get_async_session


async def get_authors(session: AsyncSession):
    result = await session.execute(select(Author))
    authors = result.scalars().all()
    return authors


async def get_author(
    author_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(Author).where(Author.id == author_id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="Author not found")
    return response


async def create_author(author: AuthorCreate, session: AsyncSession):
    db_author = Author(**author.model_dump())
    session.add(db_author)
    await session.commit()
    await session.refresh(db_author)
    return db_author


async def update_author(
    author: Author, author_data: AuthorCreate, session: AsyncSession
):
    query = (
        update(Author)
        .where(Author.id == author.id)
        .values(**author_data.model_dump())
        .returning(Author)
    )
    result = await session.execute(query)
    await session.commit()
    response = result.scalars().first()
    return response


async def delete_author(author: Author, session: AsyncSession):
    query = delete(Author).where(Author.id == author.id)
    await session.execute(query)
    await session.commit()
    return f"Author with id {author.id} was deleted"
