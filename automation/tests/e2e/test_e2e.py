# Example E2E tests
# To use: run the FastAPI server separately (e.g. uvicorn automation.server.backend:app --reload)
# and set BASE_URL to the running server's address.

import os
import httpx
import pytest

BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:8000")


def test_e2e_list_books():
    response = httpx.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_e2e_add_book():
    data = {"title": "E2E Book", "author": "E2E Author"}
    response = httpx.post(f"{BASE_URL}/books", json=data)
    assert response.status_code in (200, 201)
    book = response.json()
    assert book["title"] == data["title"]
    assert book["author"] == data["author"]
    # Clean up
    httpx.delete(f"{BASE_URL}/books/{book['id']}")


def test_e2e_add_user():
    data = {"name": "E2E User"}
    response = httpx.post(f"{BASE_URL}/users", json=data)
    assert response.status_code in (200, 201)
    user = response.json()
    assert user["name"] == data["name"]


def test_e2e_borrow_and_return_book():
    # Add user
    user_resp = httpx.post(f"{BASE_URL}/users", json={"name": "E2E Borrower"})
    assert user_resp.status_code in (200, 201)
    user_id = user_resp.json()["id"]
    # Add book
    book_resp = httpx.post(f"{BASE_URL}/books", json={"title": "E2E Borrowable", "author": "E2E Author"})
    assert book_resp.status_code in (200, 201)
    book_id = book_resp.json()["id"]
    # Borrow
    borrow_resp = httpx.post(f"{BASE_URL}/books/{book_id}/borrow", params={"user_id": user_id})
    assert borrow_resp.status_code == 200
    # Return
    return_resp = httpx.post(f"{BASE_URL}/books/{book_id}/return")
    assert return_resp.status_code == 200
    # Clean up
    httpx.delete(f"{BASE_URL}/books/{book_id}")


def test_e2e_delete_book():
    # Add book
    book_resp = httpx.post(f"{BASE_URL}/books", json={"title": "E2E ToDelete", "author": "E2E Author"})
    assert book_resp.status_code in (200, 201)
    book_id = book_resp.json()["id"]
    # Delete
    del_resp = httpx.delete(f"{BASE_URL}/books/{book_id}")
    assert del_resp.status_code == 200
    # Check deleted
    get_resp = httpx.get(f"{BASE_URL}/books")
    assert all(b["id"] != book_id for b in get_resp.json()) 