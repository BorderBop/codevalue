# Test Plan for Automation Project

## 1. Introduction
This document describes the test plan for the Automation Project — a demo FastAPI backend with a comprehensive automated testing suite. The goal is to ensure the reliability, correctness, and performance of the API and its business logic through systematic automated testing.

---

## 2. Scope
- All API endpoints of the FastAPI backend (books, users, borrow/return)
- Data validation and business logic
- Database integration
- API contract (OpenAPI compliance)
- Error handling and negative scenarios
- Performance under load

---

## 3. Objectives
- Verify that all API endpoints work as specified
- Ensure correct handling of valid and invalid input
- Validate business rules (e.g., unique user names, borrow/return logic)
- Ensure API contract is not broken
- Confirm system stability under concurrent load
- Provide fast feedback for development and CI/CD

---

## 4. Test Types and Coverage

| Test Type         | Description                                                      | Tools/Location                        |
|-------------------|------------------------------------------------------------------|---------------------------------------|
| Unit              | Test individual functions, models, and business logic            | `automation/tests/unit`               |
| Integration       | Test API endpoints with real DB, FastAPI app, httpx              | `automation/tests/integration`        |
| API/Contract      | Validate OpenAPI schema, endpoint presence, required fields      | `automation/tests/api`                |
| Mock              | Simulate server responses, test error handling                   | `automation/tests/mocks`              |
| End-to-end (e2e)  | Black-box tests via real HTTP requests to running server         | `automation/tests/e2e`                |
| Performance       | Load testing with realistic user scenarios (Locust)              | `performance/`                        |

---

## 5. Test Environment
- **OS:** Linux, MacOS, Windows (cross-platform)
- **Python:** 3.8+
- **Database:** SQLite (file-based, auto-created)
- **Dependencies:** Listed in `automation/requirements.txt`
- **Tools:** pytest, httpx, FastAPI, Locust
- **CI/CD:** (Optional) Can be integrated with GitHub Actions, GitLab CI, Jenkins, etc.

---

## 6. Test Data
- Test data is generated dynamically in tests (unique names, random values)
- No sensitive or production data is used
- Database is reset/cleaned between tests for isolation

---

## 7. Roles and Responsibilities
- **Test Author:** Maintainer of this repository
- **Test Executor:** Any developer, CI/CD pipeline
- **Test Reviewer:** Code reviewers, QA engineers

---

## 8. Entry and Exit Criteria
- **Entry:**
  - All dependencies installed
  - Server and DB available (for integration/e2e/performance)
- **Exit:**
  - All critical and high-priority tests pass
  - No regressions or critical errors found
  - Performance meets basic expectations (no crashes under load)

---

## 9. Test Execution and Reporting
- Tests are run via `run_all_tests.sh` (Linux/Mac) or `run_all_tests.bat` (Windows)
- Results are shown in the console (pytest output)
- Failures and errors are to be investigated and fixed before release/merge
- Performance test results (Locust) are available in the web UI and can be exported

---

## 10. Performance/Load Testing Details

Performance testing is conducted using [Locust](https://locust.io/) and covers several types of load scenarios:

- **Smoke Test:**
  - Quick, low-load run to verify the system is up and basic flows work.
- **Baseline Test:**
  - Establishes normal response times and throughput under typical load (e.g., 1-5 users).
- **Stress Test:**
  - Gradually increases the number of users/requests to determine the system's breaking point and observe failure modes.
- **Spike Test:**
  - Applies a sudden, sharp increase in load to see how the system handles abrupt traffic surges.
- **Endurance (Soak) Test:**
  - Runs a moderate load for an extended period (e.g., hours) to detect memory leaks, resource exhaustion, or performance degradation over time.
- **Scalability Test:**
  - Measures how the system handles increasing load and whether it scales linearly or bottlenecks appear.

**How to apply in this project:**
- Locust scenarios can be configured via the web UI or command-line options to simulate any of the above types.
- Example: To run a stress test, set a high number of users and a fast spawn rate.
- Example: For endurance, run Locust for several hours with a moderate user count.
- The provided Locust script (`performance/test_load_books.py`) can be extended to cover more complex user journeys and business flows.

**Metrics collected:**
- Response time (average, percentiles)
- Requests per second
- Error rate
- System resource usage (external monitoring)

---

## 11. Risks and Mitigations
- **Risk:** Incomplete negative test coverage
  - **Mitigation:** All endpoints and business rules have negative tests
- **Risk:** Environment differences (OS, Python version)
  - **Mitigation:** Use venv, cross-platform scripts, and requirements.txt
- **Risk:** Database state leakage between tests
  - **Mitigation:** Use fixtures to reset DB between tests

---

## 12. Maintenance
- Tests and test data should be updated with any API or business logic changes
- Dependencies should be kept up to date
- Test plan should be reviewed regularly

---

## 13. References
- [Project Readme.md](../Readme.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Locust Documentation](https://docs.locust.io/) 