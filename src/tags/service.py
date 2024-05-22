from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database import get_async_session
from .models import Tag
from .schemas import TagCreate


async def get_tags(session: AsyncSession = Depends(get_async_session)) -> List[Tag]:
    """Get all tags.

    Parameters:
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        List[Tag]: A list of `Tag` objects representing all tags in the database.
    """
    result = await session.execute(select(Tag))
    tags: List[Tag] = result.scalars().all()
    return tags


async def get_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Tag:
    """Get an tag by their ID.

    Parameters:
        tag_id (int): The ID of the tag to retrieve.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Tag: The `Tag` object with the given ID, or a 404 error if not found.
    """
    query = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(query)
    response: Tag = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="Tag not found")
    return response


async def create_tag(tag_data: TagCreate, session: AsyncSession) -> Tag:
    """Create a new tag.

    Parameters:
        tag_data (TagCreate): The tag data to be created.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Tag: The newly created `Tag` object.
    """
    try:
        db_tag = Tag(**tag_data.model_dump())
        session.add(db_tag)
        await session.commit()
        await session.refresh(db_tag)
        return db_tag
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Tag creation failed: {str(exc)}")


async def update_tag(tag: Tag, tag_data: TagCreate, session: AsyncSession) -> Tag:
    """Update an tag.

    Parameters:
        tag (Tag): The `Tag` object to be updated.
        tag_data (TagCreate): The updated tag data.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Tag: The updated `Tag` object.
    """
    try:
        query = (
            update(Tag)
            .where(Tag.id == tag.id)
            .values(**tag_data.model_dump())
            .returning(Tag)
        )
        result = await session.execute(query)
        await session.commit()
        response: Tag = result.scalars().first()
        return response
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Tag update failed: {str(exc)}")


async def delete_tag(tag: Tag, session: AsyncSession) -> str:
    """Delete an tag.

    Parameters:
        tag (Tag): The `Tag` object to be deleted.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the tag was deleted.
    """
    try:
        query = delete(Tag).where(Tag.id == tag.id)
        await session.execute(query)
        await session.commit()
        return f"Tag with id {tag.id} was deleted"
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Tag deletion failed: {str(exc)}")
