# Backend

## Project Structure

- `server/backend.py` — main FastAPI app and models
- `requirements.txt` — dependencies
- `library.db` — SQLite database
- `tests/` — all test code (unit, integration, API/contract, mocks, e2e)

## How to Run Tests

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Run all tests:**
   ```
   pytest tests/
   ```
3. **Run only a specific type of tests:**
   ```
   pytest tests/unit
   pytest tests/integration
   pytest tests/api
   pytest tests/mocks
   pytest tests/e2e
   ```

## Test Types

- **Unit tests:** Test individual functions/classes in isolation (no DB, no FastAPI app).
- **Integration tests:** Test FastAPI app with real DB, using httpx.AsyncClient + ASGITransport.
- **API/Contract tests:** Check OpenAPI schema and endpoint compliance.
- **Mock tests:** Use httpx.MockTransport to test client logic and error handling.
- **E2E tests:** (Optional) Test the app as a black box, possibly with real HTTP server and DB.

---

See the `tests/` directory for examples and details. 
