import pytest
from httpx import AsyncClient, ASGITransport
from automation.server.backend import app

def resolve_schema(schema, components):
    # If schema is a $ref, resolve it
    if "$ref" in schema:
        ref = schema["$ref"]
        # ref format: "#/components/schemas/BookCreate"
        _, _, path = ref.partition("#/")
        parts = path.split("/")
        resolved = components
        for part in parts[1:]:
            resolved = resolved[part]
        return resolved
    return schema

@pytest.mark.asyncio
async def test_openapi_schema_contains_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    paths = data["paths"].keys()
    assert "/books" in paths
    assert "/users" in paths
    assert any(p.startswith("/books/") for p in paths)

@pytest.mark.asyncio
async def test_books_post_schema():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    schema = data["paths"]["/books"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    schema = resolve_schema(schema, data["components"])
    assert "title" in schema["properties"]
    assert "author" in schema["properties"]
    assert set(schema["required"]) == {"title", "author"}

@pytest.mark.asyncio
async def test_users_post_schema():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    schema = data["paths"]["/users"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    schema = resolve_schema(schema, data["components"])
    assert "name" in schema["properties"]
    assert schema["required"] == ["name"]

@pytest.mark.asyncio
async def test_endpoint_methods():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    paths = data["paths"]
    # /books supports GET, POST
    assert set(paths["/books"].keys()) == {"get", "post"}
    # /books/{book_id} supports PUT, DELETE
    assert set(paths["/books/{book_id}"].keys()) == {"put", "delete"}
    # /users supports GET, POST
    assert set(paths["/users"].keys()) == {"get", "post"}
    # /books/{book_id}/borrow supports POST
    assert set(paths["/books/{book_id}/borrow"].keys()) == {"post"}
    # /books/{book_id}/return supports POST
    assert set(paths["/books/{book_id}/return"].keys()) == {"post"} 