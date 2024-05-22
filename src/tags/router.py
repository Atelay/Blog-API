from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.database import get_async_session
from .schemas import TagBase, TagCreate
from .service import get_tag, get_tags, create_tag, update_tag, delete_tag


router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[TagBase])
async def get_all_tags(session: AsyncSession = Depends(get_async_session)):
    """
    Get all tags.

    Parameters:
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        List[TagBase]: A list of `TagBase` objects representing all tags in the database.
    """
    return await get_tags(session)


@router.get("/{tag_id}", response_model=TagBase)
async def get_tag_by_id(tag: Mapped = Depends(get_tag)):
    """
    Get an tag by their ID.

    Parameters:
        tag_id (int): The ID of the tag to retrieve.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        TagBase: The `TagBase` object with the given ID, or a 404 error if not found.
    """
    return tag


@router.post("/", response_model=TagBase)
async def create_new_tag(
    tag: TagCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new tag.

    Parameters:
        tag (TagCreate): The tag data to be created.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        TagBase: The newly created `TagBase` object.
    """
    return await create_tag(tag, session)


@router.put("/{tag_id}", response_model=TagBase)
async def update_tag_by_id(
    tag_data: TagCreate,
    tag: Mapped = Depends(get_tag),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an tag.

    Parameters:
        tag_data (TagCreate): The updated tag data.
        tag (Tag, optional): The `Tag` object to be updated.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        TagBase: The updated `TagBase` object.
    """
    return await update_tag(tag, tag_data, session)


@router.delete("/{tag_id}")
async def delete_tag_by_id(
    tag: Mapped = Depends(get_tag),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete an tag.

    Parameters:
        tag (Tag, optional): The `Tag` object to be deleted.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the tag was deleted.
    """
    return await delete_tag(tag, session)
