# Performance Testing with Locust

This folder contains load tests for your FastAPI backend using [Locust](https://locust.io/).

## How to Run the Load Test

### 1. Install Locust

Make sure your virtual environment is activated, then run:

```
pip install locust
```

### 2. Start the FastAPI Server

Before running the load test, you **must** start your FastAPI server. For example, from the project root:

```
cd automation
source venv/bin/activate
uvicorn server.backend:app --reload
```

Or from the project root:

```
uvicorn automation.server.backend:app --reload
```

### 3. Run the Locust Load Test

From the project root (`codevalue/`):

```
locust -f performance/test_load_books.py --host=http://127.0.0.1:8000
```

Then open your browser at [http://localhost:8089](http://localhost:8089) to start the test and set the number of users and spawn rate.

---

- The scenario will add a book, create a user, borrow and return the book, and then delete the book in a loop.
- You can add more scenarios or endpoints by editing `test_load_books.py`. 