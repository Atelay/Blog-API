from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.database import get_async_session
from .service import get_posts, get_post, create_post, update_post, delete_post
from .schemas import PostCreate, PostBase


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[PostBase])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    """
    Get all posts.

    Parameters:
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        List[PostBase]: A list of `PostBase` objects representing all posts in the database.
    """
    return await get_posts(session)


@router.get("/{post_id}", response_model=PostBase)
async def get_post_by_id(post: Mapped = Depends(get_post)):
    """
    Get an post by their ID.

    Parameters:
        post_id (int): The ID of the post to retrieve.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        PostBase: The `PostBase` object with the given ID, or a 404 error if not found.
    """
    return post


@router.post("/", response_model=PostBase)
async def create_new_post(
    post: PostCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new post.

    Parameters:
        post (PostCreate): The post data to be created.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        PostBase: The newly created `PostBase` object.
    """
    return await create_post(post, session)


@router.put("/{post_id}", response_model=PostBase)
async def update_post_by_id(
    post_data: PostCreate,
    post: Mapped = Depends(get_post),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an post.

    Parameters:
        post_data (PostCreate): The updated post data.
        post (Post, optional): The `Post` object to be updated.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        PostBase: The updated `PostBase` object.
    """
    return await update_post(post, post_data, session)


@router.delete("/{post_id}")
async def delete_post_by_id(
    post: Mapped = Depends(get_post),
    session: AsyncSession = Depends(get_async_session),
) -> str:
    """
    Delete an post.

    Parameters:
        post (Post, optional): The `Post` object to be deleted.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the post was deleted.
    """
    return await delete_post(post, session)
