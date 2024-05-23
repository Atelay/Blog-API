import pytest
from httpx import AsyncClient
from fastapi import status

from src.authors.models import Author
from src.authors.schemas import AuthorBase
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
