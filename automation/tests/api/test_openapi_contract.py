import pytest
from httpx import AsyncClient, ASGITransport
from automation.server.backend import app

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