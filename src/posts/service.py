from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.authors.service import get_author
from src.categories.service import get_category
from src.tags.models import Tag
from src.tags.service import get_tag

from .models import Post
from .schemas import PostCreate
from src.database import get_async_session


async def get_posts(
    session: AsyncSession = Depends(get_async_session),
) -> List[Post]:
    """Get all posts.

    Parameters:
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        List[Post]: A list of `Post` objects representing all posts in the database.
    """
    result = await session.execute(select(Post))
    posts: List[Post] = result.scalars().all()
    return posts


async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    """Get an post by their ID.

    Parameters:
        post_id (int): The ID of the post to retrieve.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Post: The `Post` object with the given ID, or a 404 error if not found.
    """
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    response: Post = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="Post not found")
    return response


async def create_post(post_data: PostCreate, session: AsyncSession) -> Post:
    """Create a new Post.

    Parameters:
        post_data (PostCreate): The post data to be created.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Post: The newly created `Post` object.
    """
    try:
        await get_author(post_data.author_id, session)
        await get_category(post_data.category_id, session)
        tags = [await get_tag(tag_id, session) for tag_id in post_data.tags]

        db_post = Post(**post_data.model_dump(exclude={"tags"}))
        db_post.tags = tags
        session.add(db_post)
        await session.commit()
        await session.refresh(db_post)
        return db_post
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Post creation failed: {str(exc)}")


async def update_post(post: Post, post_data: PostCreate, session: AsyncSession) -> Post:
    """Update an post.

    Parameters:
        post (Post): The `Post` object to be updated.
        post_data (PostCreate): The updated post data.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Post: The updated `Post` object.
    """
    try:
        await get_author(post_data.author_id, session)
        await get_category(post_data.category_id, session)
        tags: List[Tag] = [await get_tag(tag_id, session) for tag_id in post_data.tags]
        post.tags = tags
        for key, value in post_data.model_dump(exclude={"tags"}).items():
            setattr(post, key, value)
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Post update failed: {str(exc)}")


async def delete_post(post: Post, session: AsyncSession) -> str:
    """Delete an post.

    Parameters:
        post (Post): The `Post` object to be deleted.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the post was deleted.
    """
    try:
        query = delete(Post).where(Post.id == post.id)
        await session.execute(query)
        await session.commit()
        return f"Post with id {post.id} was deleted"
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Post deletion failed: {str(exc)}")
