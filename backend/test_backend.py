import pytest
from httpx import AsyncClient, ASGITransport
from server.backend import app
from uuid import uuid4

import asyncio

@pytest.mark.asyncio
async def test_list_books():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_book_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "Test Book", "author": "Author"})
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Author"

@pytest.mark.asyncio
async def test_add_book_missing_all_fields():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_missing_title():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"author": "Author"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_missing_author():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "Book Only"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_wrong_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"titel": "Typo", "author": "Author"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_wrong_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": 123, "author": "Author"})
        assert response.status_code == 422
        response = await ac.post("/books", json={"title": "Book", "author": 456})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_book_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "BookToUpdate", "author": "Author"})
        book_id = response.json()["id"]
        response = await ac.put(f"/books/{book_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_update_book_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/books/999999", json={"title": "Nope"})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_book():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "BookToDelete", "author": "Author"})
        book_id = response.json()["id"]
        response = await ac.delete(f"/books/{book_id}")
    assert response.status_code == 200
    # Try deleting again (should fail)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete(f"/books/{book_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_user_success():
    transport = ASGITransport(app=app)
    unique_name = f"TestUser_{uuid4().hex}"
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": unique_name})
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == unique_name

@pytest.mark.asyncio
async def test_add_user_missing_all_fields():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_wrong_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"nam": "Typo"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_wrong_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": 123})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_empty_string():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": "   "})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_borrow_and_return_book():
    transport = ASGITransport(app=app)
    unique_name = f"Borrower_{uuid4().hex}"
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_resp = await ac.post("/users", json={"name": unique_name})
        user_id = user_resp.json()["id"]
        book_resp = await ac.post("/books", json={"title": "Borrowable", "author": "Author"})
        book_id = book_resp.json()["id"]
        response = await ac.post(f"/books/{book_id}/borrow", params={"user_id": user_id})
        assert response.status_code == 200
        response = await ac.post(f"/books/{book_id}/borrow", params={"user_id": user_id})
        assert response.status_code == 400
        response = await ac.post(f"/books/{book_id}/return")
        assert response.status_code == 200
        response = await ac.post(f"/books/{book_id}/return")
        assert response.status_code == 400 