# Automation (Backend & API)

This directory contains a sample FastAPI backend for a library system, along with a full suite of automated tests. The backend exposes a simple REST API for managing books and users, and demonstrates best practices for structuring, testing, and documenting Python web applications.

---

## Project Structure

```
automation/
  server/           # FastAPI app and models (main backend code)
    backend.py      # Main FastAPI application
  tests/            # All automated tests (see root Readme for details)
    ...
requirements.txt    # Python dependencies for backend and tests
```

- **server/**: Contains the FastAPI application and all business logic.
- **tests/**: Contains unit, integration, API/contract, mock, and e2e tests for the backend.
- **requirements.txt**: All dependencies needed to run the backend and tests.

---

## Purpose of the Server

This backend simulates a simple library system, allowing you to:
- Add, update, list, and delete books
- Add and list users
- Borrow and return books

It is designed for demonstration, learning, and as a foundation for automated testing.

---

## API Endpoints

All endpoints are available under the root URL (default: `http://127.0.0.1:8000`).

### 1. List all books
**GET /books**

- **Response:** JSON array of books
- **Example curl:**
  ```bash
  curl http://127.0.0.1:8000/books
  ```

### 2. Add a new book
**POST /books**

- **Body:**
  ```json
  {
    "title": "Book Title",
    "author": "Author Name"
  }
  ```
- **Response:** JSON object of the created book
- **Example curl:**
  ```bash
  curl -X POST http://127.0.0.1:8000/books \
    -H "Content-Type: application/json" \
    -d '{"title": "Book Title", "author": "Author Name"}'
  ```

### 3. Update a book
**PUT /books/{book_id}**

- **Path parameter:** `book_id` (integer)
- **Body:** (any of the fields)
  ```json
  {
    "title": "New Title",
    "author": "New Author"
  }
  ```
- **Response:** JSON object of the updated book
- **Example curl:**
  ```bash
  curl -X PUT http://127.0.0.1:8000/books/1 \
    -H "Content-Type: application/json" \
    -d '{"title": "New Title"}'
  ```

### 4. Delete a book
**DELETE /books/{book_id}**

- **Path parameter:** `book_id` (integer)
- **Response:** `{ "detail": "Book deleted" }`
- **Example curl:**
  ```bash
  curl -X DELETE http://127.0.0.1:8000/books/1
  ```

### 5. List all users
**GET /users**

- **Response:** JSON array of users
- **Example curl:**
  ```bash
  curl http://127.0.0.1:8000/users
  ```

### 6. Add a new user
**POST /users**

- **Body:**
  ```json
  {
    "name": "User Name"
  }
  ```
- **Response:** JSON object of the created user
- **Example curl:**
  ```bash
  curl -X POST http://127.0.0.1:8000/users \
    -H "Content-Type: application/json" \
    -d '{"name": "User Name"}'
  ```

### 7. Borrow a book
**POST /books/{book_id}/borrow?user_id=...**

- **Path parameter:** `book_id` (integer)
- **Query parameter:** `user_id` (integer)
- **Response:** `{ "detail": "Book borrowed" }` or error
- **Example curl:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/books/1/borrow?user_id=2"
  ```

### 8. Return a book
**POST /books/{book_id}/return**

- **Path parameter:** `book_id` (integer)
- **Response:** `{ "detail": "Book returned" }` or error
- **Example curl:**
  ```bash
  curl -X POST http://127.0.0.1:8000/books/1/return
  ```

---

## Data Models

### Book
- `id`: integer
- `title`: string
- `author`: string
- `is_borrowed`: boolean
- `borrower_id`: integer or null

### User
- `id`: integer
- `name`: string

---

## Types of Tests

- **Unit tests:** Test business logic and data validation in isolation.
- **Integration tests:** Test API and DB interaction using the real FastAPI app.
- **API/Contract tests:** Ensure endpoints and OpenAPI schema are correct.
- **Mock tests:** Simulate server responses and error handling.
- **End-to-end (e2e) tests:** Validate the system as a black box.
- **Performance (load) tests:** Use Locust to simulate real user load.

See the root `Readme.md` for details on running and structuring tests. 
