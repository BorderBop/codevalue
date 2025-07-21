# Example E2E test placeholder
# To use: run the FastAPI server separately (e.g. uvicorn server.backend:app --reload)
# and set BASE_URL to the running server's address.

import os
import pytest
import httpx

BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:8000")

def test_e2e_books():
    response = httpx.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 