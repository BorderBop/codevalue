# Library Backend API

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy

## Install dependencies
```
pip install -r requirements.txt
```

## Run the server
```
uvicorn backend.backend:app --reload
```

## Main endpoints
- `GET /books` — get all books
- `POST /books` — add a new book
- `PUT /books/{book_id}` — update a book
- `DELETE /books/{book_id}` — delete a book
- `GET /users` — get all users
- `POST /users` — add a new user
- `POST /books/{book_id}/borrow?user_id=...` — borrow a book for a user
- `POST /books/{book_id}/return` — return a book

The database is created automatically (SQLite, file `library.db`). 
