# Automation Project

## Overview
This repository is a demonstration project for automated testing in Python. It implements a simple FastAPI backend and showcases a complete testing strategy, including:
- **Unit tests** for business logic and data validation
- **Integration tests** for API and database interaction
- **API/Contract tests** for OpenAPI schema and endpoint compliance
- **Mock tests** for simulating server responses and error handling
- **End-to-end (e2e) tests** for black-box system validation
- **Performance (load) tests** using Locust for load simulation

The project is designed for educational, interview, and demo purposes. It provides clear examples of how to structure, write, and run different types of automated tests for a Python web application using FastAPI, pytest, httpx, and Locust.

---

## 1. Installation

### 1.1. Clone the repository
```
git clone <your-repo-url>
cd codevalue
```

### 1.2. Create and activate a virtual environment
```
python3 -m venv automation/venv
source automation/venv/bin/activate
```

### 1.3. Install dependencies
```
pip install -r automation/requirements.txt
```

### 1.4. (Optional) Install Locust for performance testing
```
pip install locust
```

---

## 2. Project Structure

```
codevalue/
  automation/
    server/           # FastAPI app and models
    tests/
      unit/           # Unit tests (pure Python logic, no DB or HTTP)
      integration/    # Integration tests (real DB, FastAPI app, httpx)
      api/            # API/contract tests (OpenAPI schema, endpoint checks)
      mocks/          # Mock tests (httpx.MockTransport, error handling)
      e2e/            # End-to-end tests (real HTTP, black-box)
  performance/        # Locust load tests
  run_all_tests.sh    # Script to run all tests (with server auto-start)
  requirements.txt    # Python dependencies
  Readme.md           # This documentation
```

---

## 3. How to Run Tests

### 3.1. Run all tests (recommended)
```
./run_all_tests.sh
```
- This script will automatically stop any old server, start a new one, run all tests, and stop the server after completion.

### 3.2. Run manually (by test type)

- **Unit tests:**
  ```
  pytest automation/tests/unit
  ```
- **Integration tests:**
  ```
  pytest automation/tests/integration
  ```
- **API/Contract tests:**
  ```
  pytest automation/tests/api
  ```
- **Mock tests:**
  ```
  pytest automation/tests/mocks
  ```
- **End-to-end (e2e) tests:**
  1. Start the FastAPI server:
     ```
     uvicorn automation.server.backend:app --reload
     ```
  2. In another terminal:
     ```
     pytest automation/tests/e2e
     ```
- **Performance (load) tests:**
  1. Install Locust:
     ```
     pip install locust
     ```
  2. Start the FastAPI server (see above)
  3. From the project root:
     ```
     locust -f performance/test_load_books.py --host=http://127.0.0.1:8000
     ```
  4. Open http://localhost:8089 in your browser

---

## 4. Types of Automated Tests

### Unit tests
- **What they check:** Individual functions, classes, business logic without DB or HTTP calls.
- **Why they are needed:** Quickly catch logic errors, require no complex environment.

### Integration tests
- **What they check:** Interaction between application components, FastAPI working with a real DB via httpx.
- **Why they are needed:** Ensure everything works together as expected.

### API/Contract tests
- **What they check:** API compliance with the specification (OpenAPI), presence and correctness of endpoints.
- **Why they are needed:** Guarantee that the external API contract is not broken.

### Mock tests
- **What they check:** Client logic and error handling using mocked server responses (httpx.MockTransport).
- **Why they are needed:** Allow testing behavior without a real server or DB, convenient for edge cases.

### End-to-end (e2e) tests
- **What they check:** The full request path from client to server and back, as in real production.
- **Why they are needed:** Test the system as a "black box", catch integration bugs.

### Performance (load) tests
- **What they check:** How the application behaves under load (many users, frequent requests).
- **Why they are needed:** Help find bottlenecks, check stability and scalability.

---

## 5. The Importance of Negative Tests

Negative tests (testing invalid input, error conditions, and edge cases) are critical for robust automated testing. They ensure that your application:
- Handles invalid or unexpected data gracefully
- Returns correct error codes and messages
- Prevents security issues and data corruption
- Remains stable and predictable under all circumstances

By including negative tests for every endpoint and business rule, you can be confident that your system not only works when everything is correct, but also fails safely and informatively when something goes wrong.

---

## 6. Notes
- All tests can be run from the project root.
- For integration and e2e tests, make sure the server and DB are available.
- For performance tests, always start the server separately.

---

**If you have any questions about running or structuring the tests, feel free to ask!**
