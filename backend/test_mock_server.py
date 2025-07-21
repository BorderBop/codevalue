import pytest
from httpx import AsyncClient, MockTransport, Request, Response
import json

# Mock handler function for httpx.MockTransport
async def mock_handler(request: Request) -> Response:
    # Simulate different endpoints and methods
    if request.url.path == "/books" and request.method == "GET":
        return Response(200, json=[{"id": 1, "title": "Book", "author": "Author", "is_borrowed": False, "borrower_id": None}])
    if request.url.path == "/books" and request.method == "POST":
        data = json.loads(request.content)
        # Negative: wrong field name (check before missing title)
        if "titel" in data:
            return Response(422, json={"detail": "Unknown field 'titel'"})
        # Negative: missing both fields
        if not data:
            return Response(422, json={"detail": "Missing fields"})
        # Negative: missing title
        if "author" in data and "title" not in data:
            return Response(422, json={"detail": "Missing title"})
        # Negative: missing author
        if "title" in data and "author" not in data:
            return Response(422, json={"detail": "Missing author"})
        # Negative: wrong type
        if isinstance(data.get("title", None), int):
            return Response(422, json={"detail": "Title must be a string"})
        if isinstance(data.get("author", None), int):
            return Response(422, json={"detail": "Author must be a string"})
        # Success
        if "title" in data and "author" in data:
            return Response(201, json={"id": 2, "title": data["title"], "author": data["author"], "is_borrowed": False, "borrower_id": None})
    if request.url.path == "/books/999" and request.method == "PUT":
        return Response(404, json={"detail": "Book not found"})
    if request.url.path == "/books/1" and request.method == "PUT":
        return Response(200, json={"id": 1, "title": "Updated", "author": "Author", "is_borrowed": False, "borrower_id": None})
    if request.url.path == "/users" and request.method == "POST":
        data = json.loads(request.content)
        # Negative: missing all fields
        if not data:
            return Response(422, json={"detail": "Missing name"})
        # Negative: wrong field name
        if "nam" in data:
            return Response(422, json={"detail": "Unknown field 'nam'"})
        # Negative: wrong type
        if isinstance(data.get("name", None), int):
            return Response(422, json={"detail": "Name must be a string"})
        # Negative: empty string
        if data.get("name", "").strip() == "":
            return Response(422, json={"detail": "Name cannot be empty"})
        # Success
        if "name" in data:
            return Response(201, json={"id": 1, "name": data["name"]})
    return Response(400, json={"detail": "Bad request"})

@pytest.mark.asyncio
async def test_mock_list_books():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_mock_add_book_success():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "New Book", "author": "Author"})
    assert response.status_code == 201
    assert response.json()["title"] == "New Book"

@pytest.mark.asyncio
async def test_mock_add_book_missing_all_fields():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={})
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing fields"

@pytest.mark.asyncio
async def test_mock_add_book_missing_title():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"author": "Author"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing title"

@pytest.mark.asyncio
async def test_mock_add_book_missing_author():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "Book Only"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing author"

@pytest.mark.asyncio
async def test_mock_add_book_wrong_field():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"titel": "Typo", "author": "Author"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Unknown field 'titel'"

@pytest.mark.asyncio
async def test_mock_add_book_wrong_type():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": 123, "author": "Author"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Title must be a string"
        response = await ac.post("/books", json={"title": "Book", "author": 456})
        assert response.status_code == 422
        assert response.json()["detail"] == "Author must be a string"

@pytest.mark.asyncio
async def test_mock_update_book_success():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/books/1", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

@pytest.mark.asyncio
async def test_mock_update_book_not_found():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/books/999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

@pytest.mark.asyncio
async def test_mock_add_user_success():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": "MockUser"})
    assert response.status_code == 201
    assert response.json()["name"] == "MockUser"

@pytest.mark.asyncio
async def test_mock_add_user_missing_all_fields():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={})
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing name"

@pytest.mark.asyncio
async def test_mock_add_user_wrong_field():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"nam": "Typo"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Unknown field 'nam'"

@pytest.mark.asyncio
async def test_mock_add_user_wrong_type():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": 123})
    assert response.status_code == 422
    assert response.json()["detail"] == "Name must be a string"

@pytest.mark.asyncio
async def test_mock_add_user_empty_string():
    transport = MockTransport(mock_handler)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={"name": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] == "Name cannot be empty" 