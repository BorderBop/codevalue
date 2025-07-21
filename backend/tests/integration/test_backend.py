import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.server.backend import app
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.server.backend import Base
import asyncio

DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def clear_db():
    # Clear all tables before each test for isolation
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def unique_name():
    return f"TestUser_{uuid4().hex}"

@pytest.mark.asyncio
async def test_list_books(client):
    response = await client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_book_success(client):
    response = await client.post("/books", json={"title": "Test Book", "author": "Author"})
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Author"

@pytest.mark.asyncio
async def test_add_book_missing_all_fields(client):
    response = await client.post("/books", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_missing_title(client):
    response = await client.post("/books", json={"author": "Author"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_missing_author(client):
    response = await client.post("/books", json={"title": "Book Only"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_wrong_field(client):
    response = await client.post("/books", json={"titel": "Typo", "author": "Author"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_book_wrong_type(client):
    response = await client.post("/books", json={"title": 123, "author": "Author"})
    assert response.status_code == 422
    response = await client.post("/books", json={"title": "Book", "author": 456})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_book_success(client):
    response = await client.post("/books", json={"title": "BookToUpdate", "author": "Author"})
    book_id = response.json()["id"]
    response = await client.put(f"/books/{book_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_update_book_not_found(client):
    response = await client.put("/books/999999", json={"title": "Nope"})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_book(client):
    response = await client.post("/books", json={"title": "BookToDelete", "author": "Author"})
    book_id = response.json()["id"]
    response = await client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    response = await client.delete(f"/books/{book_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_user_success(client, unique_name):
    response = await client.post("/users", json={"name": unique_name})
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == unique_name

@pytest.mark.asyncio
async def test_add_user_missing_all_fields(client):
    response = await client.post("/users", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_wrong_field(client):
    response = await client.post("/users", json={"nam": "Typo"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_wrong_type(client):
    response = await client.post("/users", json={"name": 123})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_user_empty_string(client):
    response = await client.post("/users", json={"name": "   "})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_borrow_and_return_book(client, unique_name):
    user_resp = await client.post("/users", json={"name": unique_name})
    user_id = user_resp.json()["id"]
    book_resp = await client.post("/books", json={"title": "Borrowable", "author": "Author"})
    book_id = book_resp.json()["id"]
    response = await client.post(f"/books/{book_id}/borrow", params={"user_id": user_id})
    assert response.status_code == 200
    response = await client.post(f"/books/{book_id}/borrow", params={"user_id": user_id})
    assert response.status_code == 400
    response = await client.post(f"/books/{book_id}/return")
    assert response.status_code == 200
    response = await client.post(f"/books/{book_id}/return")
    assert response.status_code == 400 