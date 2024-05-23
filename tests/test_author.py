import pytest
from httpx import AsyncClient
from fastapi import status

from src.authors.models import Author
from .conftest import async_session_maker


FAKE_AUTHOR = {"name": "John Doe", "email": "Lw2Bc@example.com"}


@pytest.mark.asyncio
async def test_get_authors(ac: AsyncClient):
    response = await ac.get("api/v1/authors/")
    assert response.text == "[]"
    assert response.status_code == status.HTTP_200_OK

    async with async_session_maker() as session:
        session.add(Author(**FAKE_AUTHOR))
        await session.commit()

    response = await ac.get("api/v1/authors/")
    data: dict = response.json()[0]
    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == FAKE_AUTHOR["email"]
    assert data["name"] == FAKE_AUTHOR["name"]
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_create_author(ac: AsyncClient):
    response = await ac.post("api/v1/authors/", json=FAKE_AUTHOR)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == FAKE_AUTHOR["email"]
    assert response.json()["name"] == FAKE_AUTHOR["name"]


@pytest.mark.asyncio
async def test_update_author(ac: AsyncClient):
    async with async_session_maker() as session:
        session.add(Author(**FAKE_AUTHOR))
        await session.commit()

    response = await ac.put(
        "api/v1/authors/1", json={"name": "Jane Doe", "email": "Jane@example.com"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "Jane@example.com"
    assert response.json()["name"] == "Jane Doe"


@pytest.mark.asyncio
async def test_delete_author(ac: AsyncClient):
    async with async_session_maker() as session:
        session.add(Author(**FAKE_AUTHOR))
        await session.commit()

    response = await ac.delete("api/v1/authors/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Author with id 1 was deleted"

    response = await ac.get("api/v1/authors/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
