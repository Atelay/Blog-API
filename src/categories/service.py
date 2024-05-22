from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .models import Category
from .schemas import CategoryCreate
from src.database import get_async_session


async def get_categories(
    session: AsyncSession = Depends(get_async_session),
) -> List[Category]:
    """Get all categories.

    Parameters:
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        List[Category]: A list of `Category` objects representing all categories in the database.
    """
    result = await session.execute(select(Category))
    categories: List[Category] = result.scalars().all()
    return categories


async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Category:
    """Get an category by their ID.

    Parameters:
        category_id (int): The ID of the category to retrieve.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Category: The `Category` object with the given ID, or a 404 error if not found.
    """
    query = select(Category).where(Category.id == category_id)
    result = await session.execute(query)
    response: Category = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="Category not found")
    return response


async def create_category(
    category_data: CategoryCreate, session: AsyncSession
) -> Category:
    """Create a new category.

    Parameters:
        category_data (CategoryCreate): The category data to be created.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Category: The newly created `Category` object.
    """
    try:
        db_category = Category(**category_data.model_dump())
        session.add(db_category)
        await session.commit()
        await session.refresh(db_category)
        return db_category
    except IntegrityError as exc:
        raise HTTPException(
            status_code=400, detail=f"Category creation failed: {str(exc)}"
        )


async def update_category(
    category: Category, category_data: CategoryCreate, session: AsyncSession
) -> Category:
    """Update an category.

    Parameters:
        category (Category): The `Category` object to be updated.
        category_data (CategoryCreate): The updated category data.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        Category: The updated `Category` object.
    """
    try:
        query = (
            update(Category)
            .where(Category.id == category.id)
            .values(**category_data.model_dump())
            .returning(Category)
        )
        result = await session.execute(query)
        await session.commit()
        response: Category = result.scalars().first()
        return response
    except IntegrityError as exc:
        raise HTTPException(
            status_code=400, detail=f"Category update failed: {str(exc)}"
        )


async def delete_category(category: Category, session: AsyncSession) -> str:
    """Delete an category.

    Parameters:
        category (Category): The `Category` object to be deleted.
        session (AsyncSession): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the category was deleted.
    """
    try:
        query = delete(Category).where(Category.id == category.id)
        await session.execute(query)
        await session.commit()
        return f"Category with id {category.id} was deleted"
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Category deletion failed: {str(exc)}"
        )
