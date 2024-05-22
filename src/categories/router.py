from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.database import get_async_session
from .service import (
    get_category,
    get_categories,
    create_category,
    update_category,
    delete_category,
)
from .schemas import CategoryBase, CategoryCreate


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CategoryBase])
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    """
    Get all categories.

    Parameters:
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        List[CategoryBase]: A list of `CategoryBase` objects representing all categories in the database.
    """
    return await get_categories(session)


@router.get("/{category_id}", response_model=CategoryBase)
async def get_category_by_id(category: Mapped = Depends(get_category)):
    """
    Get an category by their ID.

    Parameters:
        category_id (int): The ID of the category to retrieve.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        CategoryBase: The `CategoryBase` object with the given ID, or a 404 error if not found.
    """
    return category


@router.post("/", response_model=CategoryBase)
async def create_new_category(
    category: CategoryCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new category.

    Parameters:
        category (CategoryCreate): The category data to be created.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        CategoryBase: The newly created `CategoryBase` object.
    """
    return await create_category(category, session)


@router.put("/{category_id}", response_model=CategoryBase)
async def update_category_by_id(
    category_data: CategoryCreate,
    category: Mapped = Depends(get_category),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an category.

    Parameters:
        category_data (CategoryCreate): The updated category data.
        category (Category, optional): The `Category` object to be updated.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        CategoryBase: The updated `CategoryBase` object.
    """
    return await update_category(category, category_data, session)


@router.delete("/{category_id}")
async def delete_category_by_id(
    category: Mapped = Depends(get_category),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete an category.

    Parameters:
        category (Category, optional): The `Category` object to be deleted.
        session (AsyncSession, optional): The `AsyncSession` object used to interact with the database.

    Returns:
        str: A message indicating that the category was deleted.
    """
    return await delete_category(category, session)
