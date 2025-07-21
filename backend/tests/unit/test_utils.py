import pytest
from backend.server.backend import BookCreate, BookUpdate, UserCreate, Book, User
from pydantic import ValidationError

def test_book_create_valid():
    book = BookCreate(title="Test Title", author="Test Author")
    assert book.title == "Test Title"
    assert book.author == "Test Author"

def test_book_create_missing_title():
    with pytest.raises(ValidationError):
        BookCreate(author="Test Author")

def test_book_create_missing_author():
    with pytest.raises(ValidationError):
        BookCreate(title="Test Title")

def test_book_update_partial():
    upd = BookUpdate(title="New Title")
    assert upd.title == "New Title"
    assert upd.author is None
    upd2 = BookUpdate(author="New Author")
    assert upd2.author == "New Author"
    assert upd2.title is None

def test_user_create_valid():
    user = UserCreate(name="Alice")
    assert user.name == "Alice"

def test_user_create_empty_name():
    with pytest.raises(ValidationError):
        UserCreate(name="   ")

def test_user_create_missing_name():
    with pytest.raises(ValidationError):
        UserCreate()

def test_user_create_min_length():
    with pytest.raises(ValidationError):
        UserCreate(name="")

def test_user_create_strip_whitespace():
    user = UserCreate(name="  Bob  ")
    assert user.name == "Bob"

# Simple business logic tests (not DB)
def test_book_is_borrowed_flag():
    book = Book(id=1, title="T", author="A", is_borrowed=False, borrower_id=None)
    assert not book.is_borrowed
    book.is_borrowed = True
    assert book.is_borrowed

def test_user_book_relationship():
    user = User(id=1, name="U")
    book = Book(id=2, title="T", author="A", is_borrowed=False, borrower_id=1)
    # Simulate relationship
    user.books = [book]
    book.borrower = user
    assert book.borrower.name == "U"
    assert user.books[0].title == "T" 