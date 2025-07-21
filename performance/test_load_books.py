from locust import HttpUser, task, between
import random
import string

class BooksUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def full_book_lifecycle(self):
        # Add a book
        book_title = "PerfTestBook_" + ''.join(random.choices(string.ascii_letters, k=8))
        book_author = "Author_" + ''.join(random.choices(string.ascii_letters, k=5))
        resp = self.client.post("/books", json={"title": book_title, "author": book_author})
        if resp.status_code != 200 and resp.status_code != 201:
            print(f"Failed to add book: {resp.text}")
            return
        book_id = resp.json()["id"]

        # Add a user
        user_name = "PerfUser_" + ''.join(random.choices(string.ascii_letters, k=8))
        resp = self.client.post("/users", json={"name": user_name})
        if resp.status_code != 200 and resp.status_code != 201:
            print(f"Failed to add user: {resp.text}")
            # Clean up book
            self.client.delete(f"/books/{book_id}")
            return
        user_id = resp.json()["id"]

        # Borrow the book
        resp = self.client.post(f"/books/{book_id}/borrow", params={"user_id": user_id})
        if resp.status_code != 200:
            print(f"Failed to borrow book: {resp.text}")

        # Return the book
        resp = self.client.post(f"/books/{book_id}/return")
        if resp.status_code != 200:
            print(f"Failed to return book: {resp.text}")

        # Delete the book
        resp = self.client.delete(f"/books/{book_id}")
        if resp.status_code != 200:
            print(f"Failed to delete book: {resp.text}") 